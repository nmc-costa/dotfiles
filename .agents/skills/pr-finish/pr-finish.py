#!/usr/bin/env python3
"""pr-finish.py — preflight and finish the PR of a tasks/ card.

Thin deterministic core behind the /pr-finish skill (D4, card
dotfiles-tsk-chronicle-d4-d6). The skill is the prose; this script is the
state machine. Default is propose-only: it prints the exact commands a
human runs to finish the PR — merges happen by human direction.

--auto enables `gh pr merge --auto` and ONLY passes its gates when, right
now: the card exists and is still in phase `review` (a card in `validation`
or beyond is in human-required validation — the 2026-09-18 policy; the
loop-cap producer `review.judge_failed` doesn't exist yet, see
tasks/README.md, so phase is the conservative proxy), CI has no failing or
pending checks, and GitHub reports no conflicts. Any gate failure prints
the commands instead. Never force-merges, never deletes branches.

Idempotent by card+PR: a merged PR, an already-enabled auto-merge, or an
unverifiable card are reported and exit 0/2 without acting twice.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

AUTO_OK_MERGE_STATES = {"CLEAN", "HAS_HOOKS"}
BAD_CONCLUSIONS = {"FAILURE", "CANCELLED", "TIMED_OUT", "ACTION_REQUIRED"}
SQUASH = "--squash"  # repo convention: squash merges (e.g. PR #92 -> 20a8bf6)


def run(cmd: list[str], cwd: Path | None = None) -> tuple[int, str, str]:
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
    return p.returncode, p.stdout.strip(), p.stderr.strip()


def die(msg: str, code: int = 1) -> None:
    print(f"pr-finish: {msg}", file=sys.stderr)
    sys.exit(code)


def repo_root() -> Path:
    rc, out, _ = run(["git", "rev-parse", "--show-toplevel"])
    if rc != 0:
        die("not inside a git repository (run from the card's worktree)")
    return Path(out)


def current_branch(root: Path) -> str:
    rc, out, _ = run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=root)
    if rc != 0:
        die("cannot determine current branch")
    return out


def card_phase(root: Path, task_id: str) -> str | None:
    """Phase from the generated card view; None if the card doesn't exist."""
    card = root / "tasks" / "cards" / f"{task_id}.md"
    if not card.is_file():
        return None
    for line in card.read_text(encoding="utf-8").splitlines():
        if line.startswith("phase:"):
            return line.split(":", 1)[1].strip()
    return None


def resolve_pr(root: Path, task_id: str, pr_arg: int | None) -> dict:
    """Find the PR for this card's branch; detect already-merged (idempotency)."""
    repo = None
    rc, out, err = run(["gh", "repo", "view", "--json", "nameWithOwner", "-q", ".nameWithOwner"], cwd=root)
    if rc == 0:
        repo = out
    if pr_arg is not None:
        return {"number": pr_arg, "repo": repo}
    branch = current_branch(root)
    rc, out, err = run(
        ["gh", "pr", "list", "--head", branch, "--state", "all",
         "--limit", "5", "--json", "number,state,url"], cwd=root)
    if rc != 0:
        die(f"gh pr list failed: {err}")
    prs = json.loads(out) if out else []
    open_prs = [p for p in prs if p["state"] == "OPEN"]
    merged = [p for p in prs if p["state"] == "MERGED"]
    if len(open_prs) == 1:
        return {**open_prs[0], "repo": repo, "branch": branch}
    if not open_prs and merged:
        print(f"already merged: {merged[0]['url']} (nothing to do)")
        sys.exit(0)
    if len(open_prs) > 1:
        nums = ", ".join(f"#{p['number']}" for p in open_prs)
        die(f"multiple open PRs from branch {branch!r} ({nums}) — pass --pr <number>")
    die(f"no PR found for branch {branch!r} — open one first (task_id={task_id})")


def fetch_state(root: Path, number: int) -> dict:
    fields = ("state,mergeable,mergeStateStatus,statusCheckRollup,"
              "reviewDecision,headRefName,url,autoMergeRequest,title")
    rc, out, err = run(["gh", "pr", "view", str(number), "--json", fields], cwd=root)
    if rc != 0:
        die(f"gh pr view {number} failed: {err}")
    return json.loads(out)


def check_summary(state: dict) -> tuple[bool, list[str]]:
    """(all_green, problems). Pending or failed checks are problems for --auto."""
    problems: list[str] = []
    rollup = state.get("statusCheckRollup") or []
    for c in rollup:
        name = c.get("name") or "?"
        status = c.get("status")
        conclusion = c.get("conclusion")
        if status != "COMPLETED":
            problems.append(f"check {name!r} still {status}")
        elif conclusion != "SUCCESS":
            problems.append(f"check {name!r} concluded {conclusion}")
    return (not problems), problems


def auto_gates(root: Path, task_id: str, state: dict, phase: str | None) -> list[str]:
    """Return the list of FAILED gates for --auto (empty = all pass)."""
    failed: list[str] = []
    if state.get("state") != "OPEN":
        failed.append(f"PR state is {state.get('state')}, not OPEN")
    if phase is None:
        failed.append(f"card tasks/cards/{task_id}.md not found — cannot verify it isn't in human-required validation")
    elif phase != "review":
        failed.append(f"card phase is {phase!r}, not 'review' — validation is human-required (2026-09-18 policy); merge by human direction")
    if state.get("mergeable") != "MERGEABLE":
        failed.append(f"mergeable={state.get('mergeable')} (conflicts or unknown)")
    if state.get("mergeStateStatus") not in AUTO_OK_MERGE_STATES:
        failed.append(f"mergeStateStatus={state.get('mergeStateStatus')} (need one of {sorted(AUTO_OK_MERGE_STATES)})")
    green, problems = check_summary(state)
    if not green:
        failed.extend(problems)
    return failed


def finish_commands(number: int, task_id: str) -> list[str]:
    return [
        f"gh pr checks {number}                      # watch CI",
        f"gh pr merge {number} --squash               # repo convention: squash; human-directed",
        f"python3 tasks/move_task.py --task-id {task_id} --to-phase validation --actor-id <you>",
    ]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--task-id", required=True, help="tasks/ card id, e.g. dotfiles-tsk-chronicle-d4-d6")
    ap.add_argument("--pr", type=int, default=None, help="PR number (default: discover from the current branch)")
    ap.add_argument("--auto", action="store_true",
                    help="enable gh auto-merge — only when card is in 'review', CI green, no conflicts")
    ap.add_argument("--json", action="store_true", dest="as_json", help="machine-readable summary")
    args = ap.parse_args()

    if shutil.which("gh") is None:
        die("gh CLI not found")
    root = repo_root()
    pr = resolve_pr(root, args.task_id, args.pr)
    number = pr["number"]
    state = fetch_state(root, number)
    phase = card_phase(root, args.task_id)
    green, problems = check_summary(state)

    summary = {
        "task_id": args.task_id,
        "card_phase": phase,
        "pr": number,
        "url": state.get("url"),
        "state": state.get("state"),
        "mergeable": state.get("mergeable"),
        "mergeStateStatus": state.get("mergeStateStatus"),
        "checks_green": green,
        "check_problems": problems,
        "auto_merge_enabled": state.get("autoMergeRequest") is not None,
    }

    # Idempotency: nothing to do on a merged PR (resolve_pr exits) or enabled auto-merge.
    if state.get("autoMergeRequest") is not None:
        summary["action"] = "none (auto-merge already enabled)"
        print(json.dumps(summary, indent=2) if args.as_json else
              f"auto-merge already enabled for #{number} — nothing to do ({state.get('url')})")
        sys.exit(0)
    if state.get("state") == "MERGED":
        summary["action"] = "none (already merged)"
        print(json.dumps(summary, indent=2) if args.as_json else
              f"#{number} already merged — nothing to do ({state.get('url')})")
        sys.exit(0)

    cmds = finish_commands(number, args.task_id)
    if not args.auto:
        summary["action"] = "propose (default: propose-only)"
        if args.as_json:
            print(json.dumps({**summary, "commands": cmds}, indent=2))
        else:
            print(f"PR #{number}: {state.get('title')}")
            print(f"  state={state.get('state')} mergeable={state.get('mergeable')} "
                  f"mergeState={state.get('mergeStateStatus')} card_phase={phase} "
                  f"checks={'green' if green else 'NOT green'}")
            for p in problems:
                print(f"  ! {p}")
            print("  finish commands (propose-only — merges happen by human direction):")
            for c in cmds:
                print(f"    {c}")
        sys.exit(0)

    # --auto: every gate must pass, right now.
    failed_gates = auto_gates(root, args.task_id, state, phase)
    if failed_gates:
        summary["action"] = "refuse --auto (gates failed)"
        if args.as_json:
            print(json.dumps({**summary, "failed_gates": failed_gates, "commands": cmds}, indent=2))
        else:
            print(f"--auto refused for #{number} — gates failed:")
            for g in failed_gates:
                print(f"  ! {g}")
            print("  finish by hand instead:")
            for c in cmds:
                print(f"    {c}")
        sys.exit(2)

    rc, out, err = run(["gh", "pr", "merge", str(number), "--auto", SQUASH], cwd=root)
    if rc != 0:
        die(f"gh pr merge --auto failed: {err}")
    summary["action"] = "auto-merge enabled (merges when GitHub requirements are met)"
    print(json.dumps(summary, indent=2) if args.as_json else
          f"auto-merge enabled for #{number} (squash) — will merge on green. {state.get('url')}")


if __name__ == "__main__":
    main()
