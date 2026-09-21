#!/usr/bin/env python3
"""Append one event to tasks/events.jsonl — the only write path into the log.

Usage:
    ./append_event.py --type task.created --actor-kind human --actor-id nmc-costa \
        --task-id dotfiles-workspace-standards-schema --payload '{"project":"dotfiles","title":"..."}'

    echo '{"type": "task.created", "actor": {"kind": "agent", "id": "claude"}, ...}' | ./append_event.py --stdin

English is the default vocabulary for new events (task.created,
task.status_changed, actor.kind human/agent/swarm, status/title/project/...
payload keys) since 2026-09-16 — see language in workspace-standards.yaml.
Events written before that date used the Portuguese vocabulary
(tarefa.criada, humano/agente, estado/titulo/projeto/...); the log is
append-only so those lines are never rewritten, and this script still
accepts the old spellings on write for continuity — see tasks/README.md.

See tasks/README.md for the event schema and the provenance/quota rule (D13).
"""
import argparse
import datetime
import fcntl
import hashlib
import json
import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lifecycle import (  # noqa: E402
    AGENT_ACTOR_KINDS,
    CREATED_TYPES,
    LEGAL_TRANSITIONS,
    PHASE_CHANGED_TYPES,
    STATUS_CHANGED_TYPES,
    IllegalTransitionError,
    current_phase,
    tasks_root,
)

TASKS_DIR = tasks_root()
EVENTS_FILE = TASKS_DIR / "events.jsonl"
LOCK_FILE = TASKS_DIR / ".events.lock"
assert LOCK_FILE.parent == EVENTS_FILE.parent, (
    "EVENTS_FILE and LOCK_FILE must share a parent directory — otherwise two "
    "processes can share the events log while flocking different lock files, "
    "and Layer-A CAS silently stops being atomic while still appearing to work"
)
REQUIRED_FIELDS = ("type", "actor")
AGENT_PROPOSAL_QUOTA = 3
AGENT_PROPOSAL_EXPIRY_DAYS = 14


class ConcurrentModificationError(Exception):
    """--expect-last-event-id didn't match the task's actual last event at
    write time (Layer A CAS, tasks/plans/human-in-the-loop-notifications.md
    §2) — a concurrent writer got there first. Callers exit(3)."""


def load_events():
    if not EVENTS_FILE.exists():
        return []
    events = []
    for line in EVENTS_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            events.append(json.loads(line))
    return events


def fingerprint(payload):
    canonical = json.dumps(payload or {}, sort_keys=True)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:16]


def open_agent_proposals(events, now):
    """Agent-created tasks in state 'new' that haven't expired, keyed by fingerprint."""
    tasks = {}
    for ev in events:
        if ev.get("type") not in CREATED_TYPES or ev.get("actor", {}).get("kind") not in AGENT_ACTOR_KINDS:
            continue
        task_id = ev.get("task_id")
        if not task_id:
            continue
        tasks[task_id] = ev

    open_ids = set()
    fingerprints = set()
    for task_id, ev in tasks.items():
        created = datetime.datetime.fromisoformat(ev["ts"])
        age_days = (now - created).total_seconds() / 86400
        if age_days > AGENT_PROPOSAL_EXPIRY_DAYS:
            continue
        # "resolved" = a later tarefa.estado_mudou event exists for this task_id
        # (moved into todo = approved, or outcome marks it rejected/failed)
        later = [e for e in events if e.get("task_id") == task_id and e["ts"] > ev["ts"]]
        if any(e.get("type") in STATUS_CHANGED_TYPES for e in later):
            continue
        open_ids.add(task_id)
        fingerprints.add(fingerprint(ev.get("payload")))
    return open_ids, fingerprints


def validate_and_enrich(event, events):
    for field in REQUIRED_FIELDS:
        if field not in event:
            raise ValueError(f"missing required field: {field}")
    if "kind" not in event.get("actor", {}):
        raise ValueError("actor.kind is required")

    event.setdefault("event_id", str(uuid.uuid4()))
    event.setdefault("ts", datetime.datetime.now(datetime.timezone.utc).isoformat())
    event.setdefault("session_id", None)
    event.setdefault("task_id", None)
    event.setdefault("parent_event_id", None)
    event.setdefault("payload", {})
    event.setdefault("outcome", None)
    event.setdefault("failure_category", None)

    is_agent_proposal = (
        event["type"] in CREATED_TYPES and event["actor"]["kind"] in AGENT_ACTOR_KINDS
    )
    if is_agent_proposal:
        now = datetime.datetime.fromisoformat(event["ts"])
        open_ids, fingerprints = open_agent_proposals(events, now)
        fp = fingerprint(event.get("payload"))
        if fp in fingerprints:
            raise ValueError(f"duplicate agent proposal (fingerprint {fp} already open)")
        if len(open_ids) >= AGENT_PROPOSAL_QUOTA:
            raise ValueError(
                f"agent proposal quota reached ({AGENT_PROPOSAL_QUOTA} open, "
                f"expiry {AGENT_PROPOSAL_EXPIRY_DAYS}d) — resolve existing 'new' "
                "proposals before adding more"
            )
        event.setdefault("status", "new")
    else:
        event.setdefault("status", "todo" if event["type"] in CREATED_TYPES else None)

    if event["type"] in PHASE_CHANGED_TYPES:
        task_id = event.get("task_id")
        to_phase = (event.get("payload") or {}).get("phase")
        if task_id and to_phase:
            from_phase = current_phase(events, task_id)
            # No task.created event yet is a different problem (move_task.py
            # already refuses this before building the event) — not this
            # function's job to diagnose, so it doesn't block here.
            if from_phase is not None and to_phase not in LEGAL_TRANSITIONS.get(from_phase, set()):
                legal = sorted(LEGAL_TRANSITIONS.get(from_phase, set())) or ["(none — terminal phase)"]
                raise IllegalTransitionError(
                    f"{task_id}: {from_phase!r} -> {to_phase!r} is not a legal transition "
                    f"(legal from {from_phase!r}: {legal})"
                )

    return event


def last_event_id_for_task(events, task_id):
    for ev in reversed(events):
        if ev.get("task_id") == task_id:
            return ev.get("event_id")
    return None


def _write_line(event):
    with EVENTS_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


def append(event, expect_last_event_id=None):
    """The single physical writer to events.jsonl (tasks/plans/
    human-in-the-loop-notifications.md §0). `move_task.py` calls this
    instead of writing `open("a")` itself — it's the phase-transition CLI,
    not a second writer.

    Plain appends (expect_last_event_id=None) take no lock: each line is
    one `write()` syscall under PIPE_BUF, already confirmed safe at 20-way
    concurrency, and there's nothing to re-resolve for an event that isn't
    racing a specific prior state. A CAS-guarded append (§2, Layer A) takes
    `flock(LOCK_EX)` on the sidecar `tasks/.events.lock` — never on
    `events.jsonl` itself — re-reads the tail for this task_id *inside*
    the lock, and raises ConcurrentModificationError if it no longer
    matches: someone else moved this task first.
    """
    if expect_last_event_id is None:
        events = load_events()
        event = validate_and_enrich(event, events)
        _write_line(event)
        return event

    LOCK_FILE.touch(exist_ok=True)
    with LOCK_FILE.open("r+", encoding="utf-8") as lock_fh:
        fcntl.flock(lock_fh, fcntl.LOCK_EX)
        try:
            events = load_events()
            actual = last_event_id_for_task(events, event.get("task_id"))
            if actual != expect_last_event_id:
                raise ConcurrentModificationError(
                    f"{event.get('task_id')}: expected last event {expect_last_event_id!r}, "
                    f"found {actual!r} — someone else moved this task first"
                )
            event = validate_and_enrich(event, events)
            _write_line(event)
            return event
        finally:
            fcntl.flock(lock_fh, fcntl.LOCK_UN)


def build_event_from_args(args):
    payload = json.loads(args.payload) if args.payload else {}
    return {
        "type": args.type,
        "actor": {"kind": args.actor_kind, "id": args.actor_id},
        "session_id": args.session_id,
        "task_id": args.task_id,
        "parent_event_id": args.parent_event_id,
        "payload": payload,
        "outcome": args.outcome,
        "failure_category": args.failure_category,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--stdin", action="store_true", help="read a single JSON event object from stdin")
    parser.add_argument("--type", help="event type, e.g. task.created")
    parser.add_argument("--actor-kind", choices=["human", "agent", "swarm"])
    parser.add_argument("--actor-id", help="e.g. nmc-costa, claude, session id")
    parser.add_argument("--task-id")
    parser.add_argument("--session-id")
    parser.add_argument("--parent-event-id")
    parser.add_argument("--payload", help="JSON object string")
    parser.add_argument("--outcome", choices=["success", "failure", "partial"])
    parser.add_argument("--failure-category")
    parser.add_argument(
        "--expect-last-event-id",
        help="Layer-A CAS guard: abort (exit 3) unless this task_id's last event still has this id",
    )
    args = parser.parse_args()

    if args.stdin:
        event = json.loads(sys.stdin.read())
    else:
        if not args.type or not args.actor_kind or not args.actor_id:
            parser.error("--type, --actor-kind and --actor-id are required unless using --stdin")
        event = build_event_from_args(args)

    try:
        event = append(event, expect_last_event_id=args.expect_last_event_id)
    except IllegalTransitionError as exc:
        print(f"rejected: {exc}", file=sys.stderr)
        sys.exit(2)
    except ConcurrentModificationError as exc:
        print(f"aborted: {exc}", file=sys.stderr)
        sys.exit(3)
    except ValueError as exc:
        print(f"rejected: {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"appended {event['event_id']} ({event['type']}, task_id={event['task_id']})")


if __name__ == "__main__":
    main()
