#!/usr/bin/env python3
"""CLI over tasks/claims.py — the claim/coordination layer, separate from
tasks/move_task.py (the phase-lifecycle CLI). See tasks/plans/
claim-protocol.md for the design and tasks/CHEATSHEET.md for usage
examples once this lands there.

    ./claim.py acquire --task-id X --role implementer --actor-kind agent --actor-id team-x
    ./claim.py release --task-id X --claim-id <id> --actor-kind human --actor-id nmc-costa
    ./claim.py preempt --task-id X --claim-id <old-id> --role implementer --actor-kind human --actor-id nmc-costa --reason "..."
    ./claim.py list --task-id X

Exit codes: 0 success; 1 malformed input; 2 unknown task_id or invalid
role; 3 unauthorized release or nothing to preempt (same family as
append_event.py's Layer-A CAS abort — an authorization/state invariant,
not a generic error).
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from claims import (  # noqa: E402
    InvalidRoleError,
    NotPreemptableError,
    UnauthorizedReleaseError,
    UnknownTaskError,
    acquire,
    active_claims,
    load_claims,
    release,
    preempt,
)


def cmd_acquire(args):
    try:
        mine, others = acquire(
            task_id=args.task_id,
            role=args.role,
            actor_kind=args.actor_kind,
            actor_id=args.actor_id,
            ttl_seconds=args.ttl_seconds,
            session_id=args.session_id,
        )
    except InvalidRoleError as exc:
        print(f"rejected: {exc}", file=sys.stderr)
        sys.exit(2)
    except UnknownTaskError as exc:
        print(f"rejected: {exc}", file=sys.stderr)
        sys.exit(2)

    print(f"claimed {mine['payload']['claim_id']} on {args.task_id} as {args.role} "
          f"(expires {mine['payload']['expires_at']})")
    if others:
        print(f"NOTE: {len(others)} other active claim(s) on this task — see escalation flow "
              f"(tasks/plans/claim-protocol.md section D) before proceeding if any share your role:",
          file=sys.stderr)
        for c in others:
            print(f"  - {c['claim_id']} role={c['role']} actor={c['actor']['kind']}:{c['actor']['id']} "
                  f"expires={c['expires_at']}", file=sys.stderr)


def cmd_release(args):
    try:
        rec = release(
            claim_id=args.claim_id,
            task_id=args.task_id,
            actor_kind=args.actor_kind,
            actor_id=args.actor_id,
            reason=args.reason or "",
        )
    except UnauthorizedReleaseError as exc:
        print(f"rejected: {exc}", file=sys.stderr)
        sys.exit(3)
    except ValueError as exc:
        print(f"rejected: {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"released {rec['payload']['claim_id']} on {args.task_id}")


def cmd_preempt(args):
    try:
        rec = preempt(
            task_id=args.task_id,
            old_claim_id=args.claim_id,
            role=args.role,
            actor_kind=args.actor_kind,
            actor_id=args.actor_id,
            reason=args.reason or "",
            ttl_seconds=args.ttl_seconds,
            session_id=args.session_id,
        )
    except (InvalidRoleError, NotPreemptableError) as exc:
        print(f"rejected: {exc}", file=sys.stderr)
        sys.exit(3)

    print(f"preempted {args.claim_id} -> {rec['payload']['claim_id']} on {args.task_id} "
          f"(reason: {args.reason})")


def cmd_list(args):
    claims = load_claims()
    active = active_claims(claims, args.task_id)
    if not active:
        print(f"no active claims on {args.task_id}")
        return
    for c in active:
        print(f"{c['claim_id']} role={c['role']} actor={c['actor']['kind']}:{c['actor']['id']} "
              f"expires={c['expires_at']}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    p_acquire = sub.add_parser("acquire", help="claim a task (or renew your own existing claim)")
    p_acquire.add_argument("--task-id", required=True)
    p_acquire.add_argument("--role", required=True, choices=["implementer", "reviewer", "validator", "planner"])
    p_acquire.add_argument("--actor-kind", required=True, choices=["human", "agent", "swarm"])
    p_acquire.add_argument("--actor-id", required=True)
    p_acquire.add_argument("--ttl-seconds", type=int, default=None)
    p_acquire.add_argument("--session-id")
    p_acquire.set_defaults(func=cmd_acquire)

    p_release = sub.add_parser("release", help="release a claim you own (or any claim, if you're human)")
    p_release.add_argument("--task-id", required=True)
    p_release.add_argument("--claim-id", required=True)
    p_release.add_argument("--actor-kind", required=True, choices=["human", "agent", "swarm"])
    p_release.add_argument("--actor-id", required=True)
    p_release.add_argument("--reason")
    p_release.set_defaults(func=cmd_release)

    p_preempt = sub.add_parser("preempt", help="human (or agent-for-human) takes over a swarm claim")
    p_preempt.add_argument("--task-id", required=True)
    p_preempt.add_argument("--claim-id", required=True, help="the swarm claim_id being preempted")
    p_preempt.add_argument("--role", required=True, choices=["implementer", "reviewer", "validator", "planner"])
    p_preempt.add_argument("--actor-kind", required=True, choices=["human", "agent"])
    p_preempt.add_argument("--actor-id", required=True)
    p_preempt.add_argument("--reason", required=True)
    p_preempt.add_argument("--ttl-seconds", type=int, default=None)
    p_preempt.add_argument("--session-id")
    p_preempt.set_defaults(func=cmd_preempt)

    p_list = sub.add_parser("list", help="show active claims on a task")
    p_list.add_argument("--task-id", required=True)
    p_list.set_defaults(func=cmd_list)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
