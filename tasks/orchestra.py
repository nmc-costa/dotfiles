#!/usr/bin/env python3
"""Fan a task out across harness+provider+model combos — tasks/plans/
cross-harness-orchestra.md §1. Adopts agent-deck as the L2 execution
engine (`agent-deck launch/status/session output/worktree`); this file is
only the thin layer specific to tasks/ (D14: "script before rule").

Handoff format (amended 2026-09-25, overrides the plan's own §2 template):
one format repo-wide, via `.agents/skills/handoff/handoff.py`. Each
agent's handoff/brief live at
tasks_root()/handoffs/<run_id>/<label>/{HANDOFF.md,brief.md}.

Usage:
    python3 tasks/orchestra.py launch --task-id X \\
        --agent 'claude:opus:<subtask>' --agent 'copilot:gpt-5.5:<subtask>' \\
        [--permissions auto|yolo] [--lead-harness claude] [--launch]
        Dry-run by default: prints the agent-deck commands and briefs,
        creates nothing. Pass --launch for real side effects (worktrees,
        agent-deck sessions, claims, events).

    python3 tasks/orchestra.py status --run-id R
        Read-only: folds orchestra.* events for R with live agent-deck
        status, commits-ahead-of-main, handoff completeness and PR url.

    python3 tasks/orchestra.py collect --run-id R
        Concatenates the HANDOFF.md of finished/blocked agents, releases
        their claims, and prints a summary for the lead to hand to
        move_task.py. Never removes worktrees, never merges.
"""
import argparse
import contextlib
import datetime
import io
import json
import re
import shlex
import subprocess
import sys
from pathlib import Path

TASKS_DIR = Path(__file__).parent
sys.path.insert(0, str(TASKS_DIR))
from append_event import append, load_events  # noqa: E402
from claims import active_claims, acquire, load_claims, release  # noqa: E402
from lifecycle import current_phase  # noqa: E402
from paths import tasks_root  # noqa: E402
import brief  # noqa: E402

REPO_ROOT = Path.home() / "dotfiles"
HANDOFF_SCRIPT = REPO_ROOT / ".agents" / "skills" / "handoff" / "handoff.py"
BRANCH_PREFIX = {"claude": "claude/", "copilot": "copilot/", "agy": "agy/"}
CLAUDE_ALIASES = {"opus", "sonnet", "haiku"}
LAUNCHED_TYPE = "orchestra.agent_launched"
FINISHED_TYPE = "orchestra.agent_finished"

_MODEL_CACHE = {}


def _run(cmd, timeout=20):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        return subprocess.CompletedProcess(cmd, 1, stdout="", stderr=str(exc))


def valid_copilot_models():
    if "copilot" not in _MODEL_CACHE:
        out = _run(["copilot", "help", "config"]).stdout
        _MODEL_CACHE["copilot"] = sorted(set(re.findall(r"\bgpt-[A-Za-z0-9.\-]+\b", out)))
    return _MODEL_CACHE["copilot"]


def valid_agy_models():
    if "agy" not in _MODEL_CACHE:
        out = _run(["agy", "models"]).stdout
        _MODEL_CACHE["agy"] = sorted(set(re.findall(r"\b(?:gemini|claude)-[A-Za-z0-9.\-]+\b", out)))
    return _MODEL_CACHE["agy"]


def validate_model(harness, model):
    """Raises ValueError, listing the valid models, before anything is
    created (plan §1 step 1)."""
    if harness == "claude":
        if model in CLAUDE_ALIASES or model.startswith("claude-"):
            return
        raise ValueError(f"unknown claude model {model!r}; valid models: aliases {sorted(CLAUDE_ALIASES)} or a 'claude-…' id")
    if harness == "copilot":
        valid = valid_copilot_models()
        if model not in valid:
            raise ValueError(f"unknown copilot model {model!r}; valid models: {valid or '(none — is `copilot` installed?)'}")
        return
    if harness == "agy":
        valid = valid_agy_models()
        if model not in valid:
            raise ValueError(f"unknown agy model {model!r}; valid models: {valid or '(none — is `agy` installed?)'}")
        return
    raise ValueError(f"unknown harness {harness!r}; valid harnesses: {sorted(BRANCH_PREFIX)}")


def parse_agent_spec(spec):
    parts = spec.split(":", 2)
    if len(parts) != 3:
        raise ValueError(f"--agent must be 'harness:model:subtask', got {spec!r}")
    harness, model, subtask = parts
    if harness not in BRANCH_PREFIX:
        raise ValueError(f"unknown harness {harness!r} in {spec!r}; valid harnesses: {sorted(BRANCH_PREFIX)}")
    return harness, model, subtask


def task_short(task_id):
    prefix = "dotfiles-tsk-"
    return task_id[len(prefix):] if task_id.startswith(prefix) else task_id


def model_slug(model):
    return re.sub(r"[^A-Za-z0-9]+", "-", model).strip("-")


def build_command(harness, model, permissions, add_dir):
    add_dir_flag = f"--add-dir {add_dir}"
    if harness == "claude":
        perm = "--permission-mode auto" if permissions == "auto" else "--dangerously-skip-permissions"
        return f"claude --model {model} {perm} {add_dir_flag}"
    if harness == "copilot":
        perm = "--allow-all-tools --no-ask-user" if permissions == "auto" else "--yolo"
        return f"copilot --model {model} {perm} {add_dir_flag}"
    if harness == "agy":
        perm = "--mode accept-edits" if permissions == "auto" else "--dangerously-skip-permissions"
        return f"agy --model {model} {perm} {add_dir_flag}"
    raise ValueError(f"unknown harness {harness!r}")


def build_deck_command(repo, cmd, branch, worktree, label, run_id, brief_path):
    return [
        "agent-deck", "launch", str(repo),
        "-c", cmd,
        "-w", branch,
        "-b",
        "--location", str(worktree),
        "-t", label,
        "-g", f"orchestra/{run_id}",
        "-message-file", str(brief_path),
        "-json",
    ]


def render_brief(task_id, run_id, label, harness, subtask, handoff_dir):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        brief.prompt_for_task(task_id, orchestra={
            "run_id": run_id,
            "agent_label": label,
            "harness": harness,
            "subtask": subtask,
            "handoff_path": str(handoff_dir),
            "owned_files": [],
        })
    return buf.getvalue()


def build_plan(task_id, agent_specs, permissions):
    """Validates every agent spec before returning anything (plan §1 step
    1: an unknown model fails before anything is created)."""
    specs = [parse_agent_spec(a) for a in agent_specs]
    for harness, model, _ in specs:
        validate_model(harness, model)

    run_id = f"{task_id}-{datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d%H%M')}"
    add_dir = tasks_root()
    short = task_short(task_id)

    plan = []
    for harness, model, subtask in specs:
        slug = model_slug(model)
        label = f"{harness}-{slug}"
        branch = f"{BRANCH_PREFIX[harness]}{short}-{slug}"
        worktree = Path.home() / "dotfiles.worktrees" / f"{harness}+{short}-{slug}"
        handoff_dir = tasks_root() / "handoffs" / run_id / label
        brief_path = handoff_dir / "brief.md"
        cmd = build_command(harness, model, permissions, add_dir)
        deck_cmd = build_deck_command(REPO_ROOT, cmd, branch, worktree, label, run_id, brief_path)
        brief_text = render_brief(task_id, run_id, label, harness, subtask, handoff_dir)
        plan.append({
            "harness": harness, "model": model, "subtask": subtask, "label": label,
            "branch": branch, "worktree": worktree, "handoff_dir": handoff_dir,
            "brief_path": brief_path, "cmd": cmd, "deck_cmd": deck_cmd, "brief_text": brief_text,
        })
    return run_id, plan


def cmd_launch(args):
    events = load_events()
    if current_phase(events, args.task_id) is None:
        raise ValueError(f"{args.task_id!r} has no task.created event yet")

    run_id, plan = build_plan(args.task_id, args.agent, args.permissions)

    if not args.launch:
        print(f"DRY RUN — run_id={run_id}, {len(plan)} agent(s). Pass --launch for real side effects.\n")
        for p in plan:
            print(f"=== {p['label']} ({p['harness']}:{p['model']}) ===")
            print(f"subtask:    {p['subtask']}")
            print(f"branch:     {p['branch']}")
            print(f"worktree:   {p['worktree']}")
            print(f"handoff:    {p['handoff_dir']}")
            print(f"command:    {p['cmd']}")
            print(f"agent-deck: {shlex.join(p['deck_cmd'])}")
            print("--- brief ---")
            print(p["brief_text"])
        return

    for p in plan:
        p["handoff_dir"].mkdir(parents=True, exist_ok=True)
        p["brief_path"].write_text(p["brief_text"], encoding="utf-8")
        result = _run(p["deck_cmd"], timeout=60)
        if result.returncode != 0:
            raise ValueError(f"agent-deck launch failed for {p['label']}: {result.stderr.strip()}")
        try:
            deck_out = json.loads(result.stdout)
        except json.JSONDecodeError:
            deck_out = {}
        deck_session = deck_out.get("session_id") or deck_out.get("id")

        acquire(args.task_id, role="implementer", actor_kind="agent", actor_id=p["harness"])
        append({
            "type": LAUNCHED_TYPE,
            "actor": {"kind": "agent", "id": args.lead_harness},
            "task_id": args.task_id,
            "payload": {
                "run_id": run_id,
                "label": p["label"],
                "harness": p["harness"],
                "model": p["model"],
                "branch": p["branch"],
                "worktree": str(p["worktree"]),
                "deck_session": deck_session,
                "handoff_path": str(p["handoff_dir"]),
                "permissions": args.permissions,
            },
        })
        print(f"launched {p['label']}: deck_session={deck_session} branch={p['branch']}")

    print(f"\nrun_id: {run_id}")


def _launched_for_run(events, run_id):
    return [e for e in events if e["type"] == LAUNCHED_TYPE and e["payload"].get("run_id") == run_id]


def _finished_for_run(events, run_id):
    return {
        e["payload"]["label"]: e
        for e in events
        if e["type"] == FINISHED_TYPE and e["payload"].get("run_id") == run_id
    }


def cmd_status(args):
    events = load_events()
    launched = _launched_for_run(events, args.run_id)
    if not launched:
        raise ValueError(f"no {LAUNCHED_TYPE} events found for run_id={args.run_id!r}")
    finished = _finished_for_run(events, args.run_id)

    for ev in launched:
        p = ev["payload"]
        print(f"=== {p['label']} ({p['harness']}:{p['model']}) ===")
        print(f"branch: {p['branch']}")

        deck_session = p.get("deck_session")
        if deck_session:
            r = _run(["agent-deck", "session", "status", str(deck_session), "-json"])
            print(f"deck session: {(r.stdout or r.stderr).strip()}")
        else:
            print("deck session: (none recorded)")

        r = _run(["git", "rev-list", "--count", f"main..{p['branch']}"])
        print(f"commits ahead of main: {r.stdout.strip() if r.returncode == 0 else '?'}")

        handoff_dir = p.get("handoff_path")
        check = _run(["python3", str(HANDOFF_SCRIPT), "check", "--dir", handoff_dir])
        print(f"handoff: {'complete' if check.returncode == 0 else 'incomplete'} ({handoff_dir})")

        r = _run(["gh", "pr", "list", "--head", p["branch"], "--json", "url"])
        try:
            prs = json.loads(r.stdout) if r.returncode == 0 else []
        except json.JSONDecodeError:
            prs = []
        print(f"pr: {prs[0]['url'] if prs else '(none)'}")

        fin = finished.get(p["label"])
        print(f"finished: {fin['payload'].get('status') if fin else 'no'}")
        print()


def cmd_collect(args):
    events = load_events()
    launched = _launched_for_run(events, args.run_id)
    if not launched:
        raise ValueError(f"no {LAUNCHED_TYPE} events found for run_id={args.run_id!r}")
    finished = _finished_for_run(events, args.run_id)
    task_id = launched[0]["task_id"]
    active = active_claims(load_claims(), task_id)

    sections = []
    pr_lines = []
    for ev in launched:
        p = ev["payload"]
        fin = finished.get(p["label"])
        status = fin["payload"].get("status") if fin else None
        if status not in ("done", "blocked"):
            print(f"skip {p['label']}: not finished yet (status={status!r})", file=sys.stderr)
            continue

        handoff_md = Path(p["handoff_path"]) / "HANDOFF.md"
        body = handoff_md.read_text(encoding="utf-8") if handoff_md.exists() else f"(no HANDOFF.md at {handoff_md})"
        sections.append(f"## {p['label']} ({p['harness']}:{p['model']}, status={status})\n\n{body}")

        pr_url = fin["payload"].get("pr_url")
        if pr_url:
            pr_lines.append(f"- {p['label']}: {pr_url}")

        mine = next((c for c in active if c["actor"]["id"] == p["harness"] and c["role"] == "implementer"), None)
        if mine:
            release(mine["claim_id"], task_id, actor_kind="agent", actor_id=p["harness"], reason=f"orchestra collect {args.run_id}")

    print(f"# Orchestra collect — {task_id} / {args.run_id}\n")
    print("\n\n".join(sections) if sections else "(no finished or blocked agents yet)")
    if pr_lines:
        print("\n## PRs\n")
        print("\n".join(pr_lines))


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    launch = sub.add_parser("launch", help="fan a task out across harness+model agents")
    launch.add_argument("--task-id", required=True)
    launch.add_argument("--agent", action="append", required=True, help="'harness:model:subtask', repeatable")
    launch.add_argument("--permissions", choices=["auto", "yolo"], default="auto")
    launch.add_argument("--lead-harness", default="claude", help="actor.id on orchestra.agent_launched (default: claude)")
    launch.add_argument("--launch", action="store_true", help="perform real side effects; default is dry-run")
    launch.set_defaults(func=cmd_launch)

    status = sub.add_parser("status", help="read-only status of a run")
    status.add_argument("--run-id", required=True)
    status.set_defaults(func=cmd_status)

    collect = sub.add_parser("collect", help="concatenate handoffs, release claims")
    collect.add_argument("--run-id", required=True)
    collect.set_defaults(func=cmd_collect)

    args = parser.parse_args()
    try:
        args.func(args)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
