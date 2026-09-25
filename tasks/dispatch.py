#!/usr/bin/env python3
"""tsk dispatch: launch a session on another CLI provider with a task's
brief pre-loaded — the "push" side of cross-provider handoff (tasks/
HANDOFF.md's cross-provider dispatch verdict). The "pull" side is
tasks/brief.py itself (a session reads its own inbox on startup); this is
for an agent actively handing a task to a DIFFERENT session/provider.

No daemon involved — all three CLIs already accept a launch-time prompt:
    claude "<prompt>" --bg     (backgrounds natively)
    copilot -i "<prompt>"
    agy -i "<prompt>"          (Antigravity)
State only ever flows back through tasks/events.jsonl, never IPC — this
script never waits for or reads the launched session's output.

NOT `.agents/providers/adapters/*.sh` — that system is unrelated (LLM API
model-provider routing via a local litellm proxy, e.g. `claude-<provider>`
launchers for a GLM backend). This is about launching a CLI *harness*
(Claude Code / Copilot CLI / Antigravity) with a task pre-loaded, a
different concern entirely.

Usage:
    python3 tasks/dispatch.py --task-id dotfiles-my-task --provider claude
        Prints the command that WOULD run — dry-run by default, since
        launching is a real side effect (spawns a live, autonomous
        session). Add --launch to actually run it.

    python3 tasks/dispatch.py --task-id dotfiles-my-task --provider claude --launch

    python3 tasks/dispatch.py --task-id dotfiles-my-task --provider agy --worktree --launch
        Creates (or reuses) the card's worktree via tasks/worktree.py and
        launches the CLI with its process cwd there — the one mechanism that
        works for every harness, including agy, which has no cwd/worktree
        flag. The prompt gets a fixed preamble naming the worktree and the
        child gets TSK_HARNESS=<provider>. Dry-run prints the expected path
        and creates nothing.

Providers other than `claude` have no documented background-launch flag
(tasks/HANDOFF.md's Verdict 2 only confirmed `--bg` for Claude Code) — for
those, this script detaches the process itself (new session, stdio to a
log file) so it never blocks the caller either way.
"""
import argparse
import os
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

TASKS_DIR = Path(__file__).parent
LOG_DIR = TASKS_DIR / ".dispatch-logs"

PROVIDER_BINARIES = {
    "claude": "claude",
    "copilot": "copilot",
    "agy": "agy",
}


def get_prompt(task_id):
    result = subprocess.run(
        [sys.executable, str(TASKS_DIR / "brief.py"), "--prompt-only", "--task-id", task_id],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(result.stderr.strip(), file=sys.stderr)
        sys.exit(result.returncode)
    return result.stdout.strip()


def build_command(provider, prompt):
    binary = PROVIDER_BINARIES[provider]
    if provider == "claude":
        return [binary, prompt, "--bg"]
    if provider in ("copilot", "agy"):
        return [binary, "-i", prompt]
    raise ValueError(f"unknown provider: {provider}")


def worktree_preamble(path, branch):
    return (f"Your worktree for this card: {path} (branch {branch}). Work and commit only there; "
            f"do not create another worktree and do not edit the main checkout.\n\n")


def launch(provider, cmd, cwd=None):
    env = {**os.environ, "TSK_HARNESS": provider}
    if provider == "claude":
        # claude's own --bg already detaches — a plain run is enough,
        # this call itself returns as soon as the background job starts.
        subprocess.run(cmd, check=False, cwd=cwd, env=env)
        return
    # copilot/agy have no confirmed background flag — detach manually so
    # this script never blocks waiting for an interactive session.
    LOG_DIR.mkdir(exist_ok=True)
    log_path = LOG_DIR / f"{provider}.log"
    with log_path.open("a", encoding="utf-8") as log:
        subprocess.Popen(cmd, stdout=log, stderr=log, stdin=subprocess.DEVNULL, start_new_session=True,
                         cwd=cwd, env=env)
    print(f"detached, logging to {log_path}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--provider", required=True, choices=sorted(PROVIDER_BINARIES))
    parser.add_argument("--launch", action="store_true", help="actually launch (default: print the command, dry-run)")
    parser.add_argument("--worktree", action="store_true",
                        help="launch inside the card's worktree (tasks/worktree.py create), cwd set there")
    args = parser.parse_args()

    prompt = get_prompt(args.task_id)
    cwd = None
    if args.worktree:
        import worktree  # sibling module; imported lazily so plain dispatch never touches git
        branch = f"{args.provider}/{args.task_id}"
        try:
            if args.launch:
                cwd, branch, status = worktree.create(args.task_id, args.provider)
                worktree.write_view()
                print(f"worktree {status}: {cwd}", file=sys.stderr)
            else:
                cwd = str(worktree.managed_path(worktree.main_repo(), args.provider, args.task_id))
        except worktree.WorktreeError as exc:
            print(f"error: {exc}", file=sys.stderr)
            sys.exit(exc.code)
        prompt = worktree_preamble(cwd, branch) + prompt
    cmd = build_command(args.provider, prompt)

    binary = PROVIDER_BINARIES[args.provider]
    if not shutil.which(binary):
        print(f"error: {binary!r} not found on PATH", file=sys.stderr)
        sys.exit(1)

    if not args.launch:
        prefix = f"cd {shlex.quote(cwd)} && " if cwd else ""
        print(prefix + " ".join(shlex.quote(part) for part in cmd))
        print("(dry-run — pass --launch to actually run this)", file=sys.stderr)
        return

    print(f"launching {args.provider} on {args.task_id}", file=sys.stderr)
    launch(args.provider, cmd, cwd=cwd)


if __name__ == "__main__":
    main()
