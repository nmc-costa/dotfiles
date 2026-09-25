#!/usr/bin/env python3
"""Periodic sweep over tasks/events.jsonl: detects time-based facts that
need a human's attention and raises `notification.raised` events for
tasks/notify.py to deliver. This file only decides WHAT needs attention;
notify.py decides HOW to tell the human. Full design:
tasks/plans/human-in-the-loop-notifications.md §1 (event->action table)
and §4 (watchdogs/heartbeat).

Usage (run periodically — no systemd unit yet, see dotfiles-tsk-systemd-units):
    python3 tasks/sweep.py

Facts detected (tasks/lifecycle.py's FACT_TYPES — see that file's
docstring for why loop_cap_exceeded/agent_session_stalled aren't here
yet):
- sla_expired: the most recent phase_changed for a task is an
  agent-authored move into `validation`, and it's been there at least
  SLA_SECONDS (4h) with nothing since.
- blocked_too_long: the most recent phase_changed for a task is a move
  into `blocked`, and it's been there at least BLOCKED_SECONDS (24h)
  with nothing since. This is a P0 fact (tasks/lifecycle.py's
  P0_FACT_TYPES).

Deliberately NOT in this slice: actually auto-validating an expired SLA
task. §1 calls that action "auto-validação por CAS" — but doing it safely
requires CAS Layer B (§2), the rule that stops this exact auto-action
from overwriting a human's concurrent decision. The plan doc calls Layer
B "a peça mais crítica do plano" and adversarially corrected it three
times. Building it under the same change as the sweep that would be its
first real caller risks getting the one safety-critical piece of this
design wrong under time pressure. This sweep only RAISES the fact; taking
the auto-validation action is follow-up work once Layer B exists.

Writes tasks/.sweep-heartbeat (mtime only, no content) at the end of a
successful round — tasks/brief.py's future contract for "is the sweep
alive" (§4).
"""
import datetime
import json
import sys
from pathlib import Path

TASKS_DIR = Path(__file__).parent  # sibling .py modules only — never data paths

sys.path.insert(0, str(TASKS_DIR))
from append_event import append  # noqa: E402
from lifecycle import AGENT_ACTOR_KINDS, PHASE_CHANGED_TYPES, dedup_key, tasks_root  # noqa: E402

# Data via tasks_root() (tasks/paths.py), like brief.py: a copy of this script
# running inside a worktree must still read/write the one shared log.
EVENTS_FILE = tasks_root() / "events.jsonl"
HEARTBEAT_FILE = tasks_root() / ".sweep-heartbeat"

SLA_SECONDS = 4 * 3600
BLOCKED_SECONDS = 24 * 3600

RAISED_TYPE = "notification.raised"
DELIVERED_TYPE = "notification.delivered"


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


def latest_phase_change_per_task(events):
    """dict[task_id] -> its most recent task.phase_changed event."""
    latest = {}
    for ev in events:
        if ev.get("type") in PHASE_CHANGED_TYPES and ev.get("task_id"):
            latest[ev["task_id"]] = ev
    return latest


def already_raised_and_delivered(events, key):
    """§1's suppression rule: a new `raised` only suppresses if a
    `raised` AND a `delivered` already exist for this dedup_key — a
    `raised` with no `delivered` self-heals on the next sweep instead."""
    raised_ids = {
        e["event_id"] for e in events
        if e["type"] == RAISED_TYPE and e.get("payload", {}).get("dedup_key") == key
    }
    if not raised_ids:
        return False
    delivered_for = {e.get("payload", {}).get("raised_event_id") for e in events if e["type"] == DELIVERED_TYPE}
    return bool(raised_ids & delivered_for)


def detect_facts(events, now):
    facts = []
    for task_id, ev in latest_phase_change_per_task(events).items():
        phase = ev["payload"].get("phase")
        actor_kind = (ev.get("actor") or {}).get("kind")
        ts = datetime.datetime.fromisoformat(ev["ts"])
        age = (now - ts).total_seconds()

        if phase == "validation" and actor_kind in AGENT_ACTOR_KINDS and age >= SLA_SECONDS:
            facts.append(("sla_expired", task_id, ev, age))
        elif phase == "blocked" and age >= BLOCKED_SECONDS:
            facts.append(("blocked_too_long", task_id, ev, age))
    return facts


def main():
    events = load_events()
    now = datetime.datetime.now(datetime.timezone.utc)

    raised_count = 0
    for fact_type, task_id, anchor_event, age in detect_facts(events, now):
        key = dedup_key(task_id, fact_type, int(age))
        if already_raised_and_delivered(events, key):
            continue
        event = {
            "type": RAISED_TYPE,
            "actor": {"kind": "agent", "id": "sweep"},
            "session_id": None,
            "task_id": task_id,
            "parent_event_id": anchor_event["event_id"],
            "payload": {"fact_type": fact_type, "dedup_key": key, "age_seconds": int(age)},
            "outcome": None,
            "failure_category": None,
        }
        appended = append(event)
        events.append(appended)
        raised_count += 1
        print(f"raised {fact_type} for {task_id} (age {int(age)}s, dedup_key={key})")

    HEARTBEAT_FILE.touch()
    print(f"sweep complete: {raised_count} new fact(s) raised, heartbeat updated")


if __name__ == "__main__":
    main()
