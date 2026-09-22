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

Providers other than `claude` have no documented background-launch flag
(tasks/HANDOFF.md's Verdict 2 only confirmed `--bg` for Claude Code) — for
those, this script detaches the process itself (new session, stdio to a
log file) so it never blocks the caller either way.
"""
import argparse
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


def launch(provider, cmd):
    if provider == "claude":
        # claude's own --bg already detaches — a plain run is enough,
        # this call itself returns as soon as the background job starts.
        subprocess.run(cmd, check=False)
        return
    # copilot/agy have no confirmed background flag — detach manually so
    # this script never blocks waiting for an interactive session.
    LOG_DIR.mkdir(exist_ok=True)
    log_path = LOG_DIR / f"{provider}.log"
    with log_path.open("a", encoding="utf-8") as log:
        subprocess.Popen(cmd, stdout=log, stderr=log, stdin=subprocess.DEVNULL, start_new_session=True)
    print(f"detached, logging to {log_path}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--provider", required=True, choices=sorted(PROVIDER_BINARIES))
    parser.add_argument("--launch", action="store_true", help="actually launch (default: print the command, dry-run)")
    args = parser.parse_args()

    prompt = get_prompt(args.task_id)
    cmd = build_command(args.provider, prompt)

    binary = PROVIDER_BINARIES[args.provider]
    if not shutil.which(binary):
        print(f"error: {binary!r} not found on PATH", file=sys.stderr)
        sys.exit(1)

    if not args.launch:
        print(" ".join(shlex.quote(part) for part in cmd))
        print("(dry-run — pass --launch to actually run this)", file=sys.stderr)
        return

    print(f"launching {args.provider} on {args.task_id}", file=sys.stderr)
    launch(args.provider, cmd)


if __name__ == "__main__":
    main()
