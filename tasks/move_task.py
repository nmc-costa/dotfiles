#!/usr/bin/env python3
"""Move a task to a new phase — the only tool that should ever change
tasks/kanban.md's contents. Appends a `task.phase_changed` event to
events.jsonl (the source of truth, same as append_event.py writes to) and
regenerates kanban.md in one step, so the human viewing tuiboard never has
to run two commands or touch a file by hand.

Usage:
    ./move_task.py --task-id dotfiles-my-task --to-phase in_progress
    ./move_task.py --task-id dotfiles-my-task --to-phase review --actor-id claude

This is the first real slice of the `tsk` CLI described in tasks/README.md's
"Orchestration architecture" section — just the move, none of the
claiming/locking/daemon machinery yet. Intended caller: the agent session
itself, not the human directly (see that section's "the owner is the
director" note — a human tells the agent what to do, the agent moves the
card).
"""
import argparse
import datetime
import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from append_event import EVENTS_FILE, load_events, validate_and_enrich  # noqa: E402
from rebuild_kanban import PHASES, project as project_kanban, main as rebuild_kanban_main  # noqa: E402


def current_phase(events, task_id):
    tasks = project_kanban(events)
    if task_id not in tasks:
        return None
    return tasks[task_id]["phase"]


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--to-phase", required=True, choices=PHASES)
    parser.add_argument("--actor-kind", default="agent", choices=["human", "agent", "swarm"])
    parser.add_argument("--actor-id", default="claude")
    parser.add_argument("--reason", help="short free-text note on why this moved (optional)")
    args = parser.parse_args()

    events = load_events()
    from_phase = current_phase(events, args.task_id)
    if from_phase is None:
        print(
            f"error: {args.task_id!r} has no task.created event yet — "
            "create it first with append_event.py --type task.created",
            file=sys.stderr,
        )
        sys.exit(1)

    if from_phase == args.to_phase:
        print(f"{args.task_id} is already in {args.to_phase!r} — nothing to do")
        return

    event = {
        "type": "task.phase_changed",
        "actor": {"kind": args.actor_kind, "id": args.actor_id},
        "session_id": None,
        "task_id": args.task_id,
        "parent_event_id": None,
        "payload": {"phase": args.to_phase, "from_phase": from_phase, "reason": args.reason},
        "outcome": None,
        "failure_category": None,
        "event_id": str(uuid.uuid4()),
        "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }
    try:
        event = validate_and_enrich(event, events)
    except ValueError as exc:
        print(f"rejected: {exc}", file=sys.stderr)
        sys.exit(1)

    with EVENTS_FILE.open("a", encoding="utf-8") as f:
        import json

        f.write(json.dumps(event, ensure_ascii=False) + "\n")

    rebuild_kanban_main()
    print(f"moved {args.task_id}: {from_phase} -> {args.to_phase}")


if __name__ == "__main__":
    main()
