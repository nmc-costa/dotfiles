#!/usr/bin/env python3
"""Compile a Gauntlet Loop kickoff prompt (D14: script before rule).

    render_prompt.py check-bar --bar REF
    render_prompt.py render --goal TEXT --bar REF --harness claude|copilot|agy
                            [--max-rounds N] [--slug SLUG] [--task-id ID]

check-bar: REF must be fetchable — an http(s) URL answering 2xx/3xx, an
existing local path, or `cmd:<command>` whose program is on PATH (the prefix
is required so a vague phrase like "make it great" can't pass as the command
`make`). Exit 0 = usable bar, 1 = not.

render: fills templates/gauntlet-prompt.md, injects the harness's delegation
block, and refuses (exit 1) if the result exceeds MAX_WORDS — the method
depends on a short prompt that leaves the "how" to the agent.
"""
import argparse
import datetime
import re
import shlex
import shutil
import sys
import urllib.error
import urllib.request
from pathlib import Path

MAX_WORDS = 250
DEFAULT_MAX_ROUNDS = 3
TEMPLATE = Path(__file__).resolve().parent.parent / "templates" / "gauntlet-prompt.md"

# Same split as plan-orchestra: Claude Code has a real delegation primitive,
# everything else plays the roles itself with an explicit context reset.
DELEGATION = {
    "claude": (
        "Harness: Claude Code. Use the Agent tool: one subagent per builder, "
        "and a brand-new subagent for every critic pass. Never resume a critic."
    ),
    "copilot": (
        "Harness: no subagents. Play each role yourself, in sequence. Before "
        "every critic pass, reset: set aside everything you know about the "
        "build, restate only A and B, and judge cold."
    ),
}
DELEGATION["agy"] = DELEGATION["copilot"] + (
    " Warning: Antigravity cost and plumbing are unverified "
    "(tasks/harness-provider-model-index.md); watch usage."
)


def bar_kind(ref):
    if re.match(r"https?://", ref):
        return "url"
    if ref.startswith("cmd:"):
        try:
            first = shlex.split(ref[4:])[0]
        except (ValueError, IndexError):
            return None
        return "command" if shutil.which(first) else None
    if Path(ref).expanduser().exists():
        return "path"
    return None


def url_ok(url, timeout=10):
    req = urllib.request.Request(url, headers={"User-Agent": "gauntlet-prompting/1"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return 200 <= resp.status < 400, f"HTTP {resp.status}"
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code}"
    except (urllib.error.URLError, OSError) as e:
        return False, str(getattr(e, "reason", e))


def check_bar(ref):
    """Return (ok, kind, detail)."""
    kind = bar_kind(ref)
    if kind == "url":
        ok, detail = url_ok(ref)
        return ok, kind, detail
    if kind:
        return True, kind, "exists"
    return False, None, "not a URL, an existing path, or cmd:<program on PATH>"


BAR_ACCESS = {"url": "open or fetch it", "path": "local path; open it", "command": "run it"}


def slugify(goal):
    base = re.sub(r"[^a-z0-9]+", "-", goal.lower()).strip("-")[:40].strip("-") or "run"
    return f"{base}-{datetime.date.today():%Y%m%d}"


def render(goal, bar, harness, max_rounds=DEFAULT_MAX_ROUNDS, slug=None, task_id=None):
    kind = bar_kind(bar)
    task_line = f"\n\nKanban card: {task_id} (~/dotfiles/tasks)." if task_id else ""
    values = {
        "goal": goal.strip().rstrip("."),
        "bar": bar,
        "bar_access": BAR_ACCESS.get(kind, "inspect it"),
        "slug": slug or slugify(goal),
        "max_rounds": str(max_rounds),
        "delegation_block": DELEGATION[harness],
        "task_line": task_line,
    }
    text = TEMPLATE.read_text()
    for key, val in values.items():
        text = text.replace("{{" + key + "}}", val)
    leftover = re.findall(r"\{\{\w+\}\}", text)
    if leftover:
        raise ValueError(f"unfilled placeholders: {leftover}")
    return text


def word_count(text):
    return len(text.split())


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check-bar")
    c.add_argument("--bar", required=True)
    r = sub.add_parser("render")
    r.add_argument("--goal", required=True)
    r.add_argument("--bar", required=True)
    r.add_argument("--harness", choices=sorted(DELEGATION), default="claude")
    r.add_argument("--max-rounds", type=int, default=DEFAULT_MAX_ROUNDS)
    r.add_argument("--slug")
    r.add_argument("--task-id")
    args = p.parse_args(argv)

    if args.cmd == "check-bar":
        ok, kind, detail = check_bar(args.bar)
        print(f"{'OK' if ok else 'FAIL'} {kind or '?'}: {args.bar} ({detail})")
        return 0 if ok else 1

    if args.max_rounds < 1:
        print("error: --max-rounds must be >= 1", file=sys.stderr)
        return 2
    text = render(args.goal, args.bar, args.harness, args.max_rounds, args.slug, args.task_id)
    n = word_count(text)
    if n > MAX_WORDS:
        print(f"error: prompt is {n} words (max {MAX_WORDS}) — shorten the goal", file=sys.stderr)
        return 1
    print(text.rstrip())
    return 0


if __name__ == "__main__":
    sys.exit(main())
