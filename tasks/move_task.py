#!/usr/bin/env python3
"""Move a task to a new phase — the only tool that should ever change
tasks/kanban.md's contents. Appends a `task.phase_changed` event to
events.jsonl (the source of truth, same as append_event.py writes to) and
regenerates kanban.md in one step, so the human viewing tuiboard never has
to run two commands or touch a file by hand.

Usage:
    ./move_task.py --task-id dotfiles-my-task --to-phase in_progress
    ./move_task.py --task-id dotfiles-my-task --to-phase review --actor-id claude \
        --team team-alpha --tokens 12000 --cost-usd 0.18 --duration-seconds 900 --cycles 1
    ./move_task.py --task-id dotfiles-my-task --to-phase validation \
        --expect-last-event-id <event_id from the previous move>

Only transitions in tasks/lifecycle.py's LEGAL_TRANSITIONS are accepted
(illegal ones exit 2) — e.g. backlog can only go to planning or deferred,
never straight to in_progress. Moving into validation or done requires
--expect-last-event-id (Layer A CAS, tasks/plans/
human-in-the-loop-notifications.md §2): read the event_id this command
printed on the previous move, or the last line of `events.jsonl` for this
task_id, and pass it back — a mismatch means someone else moved the task
first, and the command aborts (exit 3) instead of overwriting them.

This is the first real slice of the `tsk` CLI described in tasks/README.md's
"Orchestration architecture" section — the move plus Layer-A CAS, none of
the claiming/daemon machinery yet. Intended caller: the agent session
itself, not the human directly (see that section's "the owner is the
director" note — a human tells the agent what to do, the agent moves the
card).

The optional --team/--tokens/--cost-usd/--duration-seconds/--cycles flags
record what a team spent completing the phase it's now LEAVING (i.e. call
them on the move that closes the phase, not the one that opens it) into
the event's payload — events.jsonl is already the source of truth, so this
gives a free audit trail per task/phase/team with no second store to keep
in sync. See rebuild_metrics.py for the aggregated view, and
tasks/demo/ for a worked example. None of the fields are required — a
plain move with no metrics is still valid.

The optional --handoff flag records what whoever picks up this task next
(a different team, a different phase, a fresh session days later) needs to
know to resume without re-deriving it: what's done, what's left, where the
work lives (branch/PR/file), and the concrete next step. Same event,
different purpose than --reason (--reason is a one-line "why did this
move happen", --handoff is "here's the state, continue from here").
Retrieve the latest handoff for a task with:
    ./move_task.py --show-handoff dotfiles-my-task
"""
import argparse
import datetime
import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from append_event import (  # noqa: E402
    ConcurrentModificationError,
    append,
    load_events,
)
from lifecycle import PHASES, IllegalTransitionError, current_phase  # noqa: E402
from rebuild_cards import main as rebuild_cards_main  # noqa: E402
from rebuild_kanban import main as rebuild_kanban_main  # noqa: E402
from rebuild_metrics import main as rebuild_metrics_main  # noqa: E402

# Layer A (tasks/plans/human-in-the-loop-notifications.md §2) is required
# on every move into these two phases, not just the sweep's own writes —
# the common caller of this script is an agent, and that path had no CAS
# protection at all before this.
CAS_REQUIRED_PHASES = ("validation", "done")


def latest_handoff(events, task_id):
    """Most recent non-empty --handoff note for a task_id, or None."""
    note = None
    phase = None
    for ev in events:
        if ev.get("task_id") != task_id or ev.get("type") != "task.phase_changed":
            continue
        payload = ev.get("payload") or {}
        if payload.get("handoff"):
            note = payload["handoff"]
            phase = payload.get("phase")
    return note, phase


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--to-phase", choices=PHASES, help="required unless --show-handoff is used")
    parser.add_argument("--actor-kind", default="agent", choices=["human", "agent", "swarm"])
    parser.add_argument("--actor-id", default="claude")
    parser.add_argument("--reason", help="short free-text note on why this moved (optional)")
    parser.add_argument("--handoff", help="what the next team/session needs to resume this task (optional)")
    parser.add_argument("--show-handoff", action="store_true", help="print the latest handoff note for --task-id and exit — no move happens")
    parser.add_argument("--team", help="which agent team did the work being closed out by this move")
    parser.add_argument("--tokens", type=int, help="tokens the team spent in the phase being left")
    parser.add_argument("--cost-usd", type=float, help="USD cost the team spent in the phase being left")
    parser.add_argument("--duration-seconds", type=int, help="wall-clock time spent in the phase being left")
    parser.add_argument("--cycles", type=int, help="retry/loop count spent in the phase being left")
    parser.add_argument(
        "--expect-last-event-id",
        help="Layer-A CAS guard: abort (exit 3) unless this task_id's last event still has this id. "
        "Required when --to-phase is validation or done.",
    )
    args = parser.parse_args()

    events = load_events()

    if args.show_handoff:
        note, phase = latest_handoff(events, args.task_id)
        if note is None:
            print(f"no handoff note recorded for {args.task_id!r}")
        else:
            print(f"[{args.task_id} @ {phase}]\n{note}")
        return

    if args.to_phase is None:
        print("error: --to-phase is required unless --show-handoff is given", file=sys.stderr)
        sys.exit(1)
    if args.to_phase in CAS_REQUIRED_PHASES and not args.expect_last_event_id:
        parser.error(
            f"--expect-last-event-id is required when --to-phase is {args.to_phase!r} "
            f"(Layer A CAS — see tasks/plans/human-in-the-loop-notifications.md §2)"
        )
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

    metrics = {}
    if args.team is not None:
        metrics["team"] = args.team
    if args.tokens is not None:
        metrics["tokens"] = args.tokens
    if args.cost_usd is not None:
        metrics["cost_usd"] = args.cost_usd
    if args.duration_seconds is not None:
        metrics["duration_seconds"] = args.duration_seconds
    if args.cycles is not None:
        metrics["cycles"] = args.cycles

    event = {
        "type": "task.phase_changed",
        "actor": {"kind": args.actor_kind, "id": args.actor_id},
        "session_id": None,
        "task_id": args.task_id,
        "parent_event_id": None,
        "payload": {
            "phase": args.to_phase,
            "from_phase": from_phase,
            "reason": args.reason,
            "handoff": args.handoff,
            "metrics": metrics or None,
        },
        "outcome": None,
        "failure_category": None,
        "event_id": str(uuid.uuid4()),
        "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }
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

    rebuild_kanban_main()
    rebuild_cards_main()
    if metrics:
        rebuild_metrics_main()
    print(f"moved {args.task_id}: {from_phase} -> {args.to_phase} (event_id={event['event_id']})")


if __name__ == "__main__":
    main()
