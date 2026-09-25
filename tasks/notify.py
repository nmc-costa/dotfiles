#!/usr/bin/env python3
"""Single delivery point for tsk notifications — tasks/plans/
human-in-the-loop-notifications.md §3 ("digest, não rajada"). Reads the
`notification.raised` events tasks/sweep.py produced that have no
matching `notification.delivered` yet, and delivers them:

- P0 facts (tasks/lifecycle.P0_FACT_TYPES — today just `blocked_too_long`)
  get an individual toast plus an UNCONDITIONAL `notify-send` (never
  skipped, regardless of whether herdr's toast was shown).
- Everything else is coalesced into at most one digest toast per run:
  "tsk: N facto(s) precisam de ti" + up to 3 examples + "…e mais K".

Success is always read from herdr's `.result.shown == true`, never its
exit code — herdr's exit codes aren't documented (tasks/plans/
human-in-the-loop-notifications.md, evidence #3). If herdr isn't
installed or doesn't report `shown`, non-P0 facts fall back to
`notify-send` too.

Usage:
    python3 tasks/notify.py                           # deliver pending
    python3 tasks/notify.py --ack --dedup-key "<key>"  # human resolved it
"""
import argparse
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

TASKS_DIR = Path(__file__).parent  # sibling .py modules only — never data paths

sys.path.insert(0, str(TASKS_DIR))
from append_event import append  # noqa: E402
from lifecycle import P0_FACT_TYPES, tasks_root  # noqa: E402

# Data via tasks_root() (tasks/paths.py), like brief.py: a copy of this script
# running inside a worktree must still read/write the one shared log.
EVENTS_FILE = tasks_root() / "events.jsonl"

RAISED_TYPE = "notification.raised"
DELIVERED_TYPE = "notification.delivered"
ACKED_TYPE = "notification.acked"

NOTIFIER_ACTOR = {"kind": "agent", "id": "notify"}


def load_events():
    if not EVENTS_FILE.exists():
        return []
    events = []
    for line in EVENTS_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            events.append(json.loads(line))
    events.sort(key=lambda e: e["ts"])
    return events


def pending_raises(events):
    delivered_for = {e.get("payload", {}).get("raised_event_id") for e in events if e["type"] == DELIVERED_TYPE}
    return [e for e in events if e["type"] == RAISED_TYPE and e["event_id"] not in delivered_for]


def herdr_show(title, body):
    """True only if herdr's own JSON says the toast was actually shown."""
    if not shutil.which("herdr"):
        return False
    try:
        result = subprocess.run(
            ["herdr", "notification", "show", title, "--body", body],
            capture_output=True, text=True, timeout=5,
        )
        payload = json.loads(result.stdout)
        return bool(payload.get("result", {}).get("shown"))
    except (subprocess.TimeoutExpired, json.JSONDecodeError, OSError):
        return False


def notify_send(title, body, urgency=None):
    if not shutil.which("notify-send"):
        return False
    cmd = ["notify-send"]
    if urgency:
        cmd += ["-u", urgency]
    cmd += [title, body]
    try:
        subprocess.run(cmd, timeout=5, check=False)
        return True
    except OSError:
        return False


def _mark_delivered(raised_event, shown):
    event = {
        "type": DELIVERED_TYPE,
        "actor": dict(NOTIFIER_ACTOR),
        "session_id": None,
        "task_id": raised_event["task_id"],
        "parent_event_id": raised_event["event_id"],
        "payload": {"raised_event_id": raised_event["event_id"], "shown": shown},
        "outcome": None,
        "failure_category": None,
    }
    return append(event)


def _group_by_dedup_key(raises):
    """A `raised` with no `delivered` self-heals by re-raising on the next
    sweep (§1) — so several pending raised events can share one
    dedup_key. Group them so a single fact isn't announced N times; every
    underlying event still gets its own `notification.delivered`."""
    groups = {}
    for e in raises:
        key = e["payload"].get("dedup_key")
        groups.setdefault(key, []).append(e)
    return groups

def deliver(raises):
    if not raises:
        print("nothing pending")
        return

    p0_groups = _group_by_dedup_key([e for e in raises if e["payload"].get("fact_type") in P0_FACT_TYPES])
    rest_groups = _group_by_dedup_key([e for e in raises if e["payload"].get("fact_type") not in P0_FACT_TYPES])

    for key, group in p0_groups.items():
        e = group[0]
        title = f"tsk: {e['task_id']} precisa de ti AGORA"
        body = e["payload"].get("fact_type", "")
        # herdr's rate-limit window recovers in <1s (measured); 2s has margin.
        time.sleep(2)
        shown = herdr_show(title, body)
        notify_send(title, body, urgency="critical")  # unconditional for P0
        for ev in group:
            _mark_delivered(ev, shown)
        print(f"delivered P0 {e['task_id']} (herdr shown={shown})")

    if rest_groups:
        n = len(rest_groups)
        top = list(rest_groups.values())[:3]
        summary = "; ".join(f"{group[0]['task_id']}: {group[0]['payload'].get('fact_type')}" for group in top)
        if n > 3:
            summary += f"; …e mais {n - 3}"
        title = f"tsk: {n} facto{'s' if n != 1 else ''} precisam de ti"

        shown = herdr_show(title, summary)
        if not shown:
            notify_send(title, summary)
        for group in rest_groups.values():
            for ev in group:
                _mark_delivered(ev, shown)
        print(f"delivered digest for {n} fact(s) (herdr shown={shown})")


def ack(dedup_key_value):
    events = load_events()
    matches = [e for e in events if e["type"] == RAISED_TYPE and e["payload"].get("dedup_key") == dedup_key_value]
    if not matches:
        print(f"no notification.raised found for dedup_key={dedup_key_value!r}", file=sys.stderr)
        sys.exit(1)
    for e in matches:
        event = {
            "type": ACKED_TYPE,
            "actor": dict(NOTIFIER_ACTOR),
            "session_id": None,
            "task_id": e["task_id"],
            "parent_event_id": e["event_id"],
            "payload": {"dedup_key": dedup_key_value},
            "outcome": None,
            "failure_category": None,
        }
        append(event)
    print(f"acked {len(matches)} raise(s) for dedup_key={dedup_key_value!r}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--ack", action="store_true", help="acknowledge a resolved fact instead of delivering")
    parser.add_argument("--dedup-key", help="required with --ack")
    args = parser.parse_args()

    if args.ack:
        if not args.dedup_key:
            parser.error("--ack requires --dedup-key")
        ack(args.dedup_key)
        return

    deliver(pending_raises(load_events()))


if __name__ == "__main__":
    main()
