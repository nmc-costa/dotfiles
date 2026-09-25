#!/usr/bin/env python3
"""Harness/provider/model-agnostic session handoff — the deterministic core
behind the `/handoff` skill (D14: "script before rule"). The skill only
tells an agent how to run this and which sections to fill in; everything
that can be computed (where the file goes, git/PR/tasks state, whether the
handoff is complete) lives here.

The output is a plain-markdown HANDOFF.md following the convention in
CHEATSHEET.md ("Leave/find a session-continuity handoff"): uppercase,
singular, at the root of the scope it describes. Each handoff is one
*block*, newest on top, delimited by a `<!-- handoff:block ... -->`
marker, and each block carries its own note to the receiver — so the
receiving side needs no skill at all: any harness, any model, told "read
this file", knows what to do.

Usage:
    handoff.py new --title "short title" [--by claude-code] [--model opus-5.5]
        | handoff.py new --title-from-branch
        Prepend a new block to HANDOFF.md: generated Snapshot filled in,
        narrative sections left as <!-- TODO --> placeholders for the agent
        to replace. --title-from-branch synthesizes the title from the
        current git branch (leading `<harness>/` prefix stripped) — for
        machines/hooks that have no human to ask. Prints the file path.

    handoff.py check
        Exit 1 (listing what's missing) unless the newest block has no
        TODO placeholders left and Goal / Done / Next step are non-empty.

    handoff.py prompt
        Print the one-line prompt to paste into any harness, plus launch
        examples for the CLIs tasks/dispatch.py knows about.

    handoff.py snapshot [--json]
        Print only the generated Snapshot section (to refresh one by hand).
        --json prints the same data as a JSON object instead — for callers
        that compose (e.g. the PreCompact hook) rather than paste prose.
        The JSON omits the tasks/brief.py block (machine callers don't need
        its cost); the markdown keeps it.

Scope (all subcommands): default is <git toplevel>/HANDOFF.md (or the cwd
outside git); --dir DIR for a subsystem (e.g. --dir tasks); --global for
~/HANDOFF.md, the cross-repo index.

Stdlib only, every external call (git, gh, tasks/brief.py) best-effort
with a timeout — a missing tool drops a Snapshot line, never the handoff.
"""
import argparse
import datetime as dt
import json
import os
import re
import shlex
import socket
import subprocess
import sys
from pathlib import Path

FILENAME = "HANDOFF.md"
MARKER_RE = re.compile(r"^<!-- handoff:block .* -->$", re.M)
TODO = "<!-- TODO"
REQUIRED_SECTIONS = ("Goal", "Done", "Next step")
# (heading, placeholder) — order is the order a receiver reads them in.
SECTIONS = (
    ("Goal", "what the human asked for, in their words, and why"),
    ("Done", "what is finished and verified (commits, PRs, files) — not what was merely attempted"),
    ("Decisions", "choices made and the reason for each, so the next session doesn't re-litigate them; 'None.' if none"),
    ("Open / risks", "unfinished work, known breakage, anything unverified, conflicts with other sessions; 'None.' if none"),
    ("Next step", "the single concrete next action — a command to run or a file to open — then the ones after it"),
)
# Mirrors tasks/dispatch.py's PROVIDER_BINARIES launch syntax.
LAUNCH_EXAMPLES = (
    ("Claude Code", 'claude {p}'),
    ("Copilot CLI", 'copilot -i {p}'),
    ("Antigravity", 'agy -i {p}'),
    ("Gemini CLI", 'gemini -i {p}'),
)


def run(cmd, cwd=None, timeout=10):
    """stdout of cmd, or None on any failure (missing binary, non-zero
    exit, timeout)."""
    try:
        r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    except (OSError, subprocess.SubprocessError):
        return None
    return r.stdout.rstrip() if r.returncode == 0 else None


def git_root(start):
    out = run(["git", "rev-parse", "--show-toplevel"], cwd=start)
    return Path(out) if out else None


def resolve_path(args):
    if args.global_:
        return Path.home() / FILENAME
    if args.dir:
        return Path(args.dir).expanduser().resolve() / FILENAME
    cwd = Path.cwd()
    return (git_root(cwd) or cwd) / FILENAME


def detect_harness():
    """Only env vars verified to be set by the harness itself (Claude Code
    sets CLAUDECODE=1 for its tool subprocesses). Other harnesses pass
    --by explicitly — 'unknown' beats a wrong guess."""
    if os.environ.get("CLAUDECODE"):
        return "claude-code"
    return "unknown"


def default_branch(root):
    ref = run(["git", "symbolic-ref", "--short", "refs/remotes/origin/HEAD"], cwd=root)
    return ref or "origin/main"


def collect(scope_dir, by=None, model=None, include_brief=True):
    """Gather the snapshot facts as data — rendering (render_snapshot) and
    JSON (cmd_snapshot --json) are two views over this one dict."""
    return {
        "written": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "host": socket.gethostname(),
        "by": by or detect_harness(),
        "model": model,
        "scope": str(scope_dir),
        "repo": git_root(scope_dir),
        "branch": None,
        "upstream": None,
        "ahead": None,
        "behind": None,
        "base": None,
        "pr": None,
        "commits": [],
        "uncommitted": [],
        "clean": None,
        "brief": None,
        "not_git": False,
    }


def fill_git_facts(data, scope_dir, include_brief=True):
    """Mutate data in place with git/gh/tasks facts for data["repo"].
    Best-effort: a missing tool drops a fact, never raises."""
    root = data["repo"]
    if not root:
        data["not_git"] = True
        return data

    data["branch"] = run(["git", "branch", "--show-current"], cwd=root) or "(detached)"
    upstream = run(["git", "rev-parse", "--abbrev-ref", "@{u}"], cwd=root)
    if upstream:
        data["upstream"] = upstream
        counts = run(["git", "rev-list", "--left-right", "--count", f"{upstream}...HEAD"], cwd=root)
        if counts:
            data["behind"], data["ahead"] = counts.split()
    data["base"] = default_branch(root)

    pr = run(["gh", "pr", "view", "--json", "number,state,url"], cwd=root, timeout=15)
    if pr:
        try:
            p = json.loads(pr)
            data["pr"] = {"number": p.get("number"), "state": p.get("state"), "url": p.get("url")}
        except json.JSONDecodeError:
            pass

    if data["branch"] != data["base"].split("/", 1)[-1]:
        log = run(["git", "log", "--oneline", "-15", f"{data['base']}..HEAD"], cwd=root)
        if log:
            data["commits"] = log.splitlines()

    status = run(["git", "status", "--short"], cwd=root)
    if status:
        st = status.splitlines()
        data["uncommitted"] = st[:30] + ([f"... {len(st) - 30} more"] if len(st) > 30 else [])
        data["clean"] = False
    else:
        data["clean"] = True

    if include_brief:
        brief = root / "tasks" / "brief.py"
        if brief.is_file():
            data["brief"] = run([sys.executable, str(brief)], cwd=root, timeout=20)
    return data


def snapshot(scope_dir, by=None, model=None):
    """The generated Snapshot section as markdown — the human view over
    collect()/fill_git_facts()."""
    data = collect(scope_dir, by, model)
    fill_git_facts(data, scope_dir)
    return render_snapshot(data)


def render_snapshot(data):
    lines = [
        "## Snapshot",
        "",
        "_Generated by `handoff.py` at write time — verify against live state before trusting it._",
        "",
        f"- **Written:** {data['written']} on `{data['host']}` by `{data['by']}`"
        + (f" / `{data['model']}`" if data["model"] else ""),
    ]
    if data["not_git"] or not data["repo"]:
        lines.append(f"- **Directory:** `{data['scope']}` (not a git repo)")
        return "\n".join(lines) + "\n"

    lines.append(f"- **Repo:** `{data['repo']}` — branch `{data['branch']}`")
    if data["upstream"]:
        lines.append(f"- **Upstream:** `{data['upstream']}` — {data['ahead']} ahead, {data['behind']} behind")
    else:
        lines.append("- **Upstream:** none — branch not pushed")

    if data["pr"]:
        p = data["pr"]
        lines.append(f"- **PR:** #{p['number']} {p['state']} {p['url']}")

    base = data["base"]
    if data["branch"] != base.split("/", 1)[-1] and data["commits"]:
        lines += ["", f"Commits on this branch not in `{base}`:", "", "```", *data["commits"], "```"]

    if not data["clean"]:
        lines += ["", "Uncommitted changes:", "", "```", *data["uncommitted"], "```"]
    else:
        lines += ["", "Working tree clean."]

    if data["brief"]:
        lines += ["", "`tasks/brief.py` at write time:", "", "```", data["brief"], "```"]
    return "\n".join(lines) + "\n"


def new_block(title, scope_dir, by, model):
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    parts = [
        f"<!-- handoff:block {stamp} -->",
        f"# Handoff — {title} ({stamp[:10]})",
        "",
        "> **To whoever picks this up (any harness, any model):** this top block is the",
        "> current handoff; blocks below it are history. Check the Snapshot against live",
        "> state (`git status`, `git log`, open PRs) before acting on it, then start at",
        "> **Next step**. When you stop with work unfinished, add a new block on top",
        "> (`/handoff`, or `handoff.py new`) rather than editing this one.",
        "",
    ]
    for heading, hint in SECTIONS:
        parts += [f"## {heading}", "", f"{TODO}: {hint} -->", ""]
    parts.append(snapshot(scope_dir, by, model))
    return "\n".join(parts)


def newest_block(text):
    starts = [m.start() for m in MARKER_RE.finditer(text)]
    if not starts:
        return None
    end = starts[1] if len(starts) > 1 else len(text)
    return text[starts[0]:end]


def section_body(block, heading):
    m = re.search(rf"^## {re.escape(heading)}\s*$(.*?)(?=^## |\Z)", block, re.M | re.S)
    return m.group(1).strip() if m else None


HARNESS_PREFIXES = ("claude", "copilot", "gemini", "agy", "codex", "opencode")


def branch_title(scope_dir):
    """--title-from-branch: title from the current branch, harness prefix
    stripped (opencode/dotfiles-tsk-x -> dotfiles-tsk-x). Falls back to the
    repo/dir name when detached or outside git — a machine caller gets a
    usable title, never an error."""
    root = git_root(scope_dir)
    branch = run(["git", "branch", "--show-current"], cwd=root) if root else None
    if not branch or branch == "(detached)":
        return (root.name if root else Path.cwd().name)
    parts = branch.split("/", 1)
    return parts[1] if len(parts) == 2 and parts[0] in HARNESS_PREFIXES else branch


def cmd_new(args):
    path = resolve_path(args)
    title = args.title if args.title else branch_title(path.parent)
    block = new_block(title, path.parent, args.by, args.model)
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if old and not MARKER_RE.search(old):
        # Pre-/handoff free-form content: keep it, visibly demoted.
        old = "# Earlier handoff notes (free-form, pre-`/handoff`)\n\n" + old
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(block + ("\n---\n\n" + old if old else ""), encoding="utf-8")
    print(path)


def cmd_check(args):
    path = resolve_path(args)
    if not path.exists():
        print(f"{path}: missing — run `handoff.py new` first", file=sys.stderr)
        return 1
    block = newest_block(path.read_text(encoding="utf-8"))
    if block is None:
        print(f"{path}: no handoff block — run `handoff.py new` first", file=sys.stderr)
        return 1
    problems = []
    todos = sum(1 for line in block.splitlines() if line.strip().startswith(TODO))
    if todos:
        problems.append(f"{todos} TODO placeholder(s) still unfilled")
    for heading in REQUIRED_SECTIONS:
        body = section_body(block, heading)
        if body is None:
            problems.append(f"section '## {heading}' missing")
        elif not body or body.startswith(TODO):
            problems.append(f"section '## {heading}' empty")
    if problems:
        print(f"{path}: incomplete handoff —", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        return 1
    print(f"{path}: OK")
    return 0


def receiver_prompt(path):
    return (f"Continue the work described in {path}. Read its top handoff block in full, "
            "verify its Snapshot against live state (git status, git log, open PRs), "
            "then start at its Next step section. Ask me before anything destructive "
            "or outward-facing.")


def cmd_prompt(args):
    path = resolve_path(args)
    if not path.exists():
        print(f"{path}: missing — run `handoff.py new` first", file=sys.stderr)
        return 1
    p = receiver_prompt(path)
    print(p)
    print("\n# Or launch directly (from the repo root):")
    for name, tmpl in LAUNCH_EXAMPLES:
        print(f"#   {name:<12} {tmpl.format(p=shlex.quote(p))}")
    return 0


def cmd_snapshot(args):
    scope = resolve_path(args).parent
    data = collect(scope)
    fill_git_facts(data, scope, include_brief=not args.json)
    if args.json:
        data["repo"] = str(data["repo"]) if data["repo"] else None
        print(json.dumps(data, indent=2))
    else:
        print(render_snapshot(data), end="")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    scope = argparse.ArgumentParser(add_help=False)
    g = scope.add_mutually_exclusive_group()
    g.add_argument("--dir", help="write HANDOFF.md in this directory (subsystem scope)")
    g.add_argument("--global", dest="global_", action="store_true", help="use ~/HANDOFF.md")
    sub = ap.add_subparsers(dest="cmd", required=True)
    n = sub.add_parser("new", parents=[scope], help="prepend a new handoff block")
    title = n.add_mutually_exclusive_group(required=True)
    title.add_argument("--title")
    title.add_argument("--title-from-branch", action="store_true",
                       help="synthesize the title from the current git branch")
    n.add_argument("--by", help="harness writing this (default: detected, else 'unknown')")
    n.add_argument("--model", help="model writing this, e.g. claude-opus-5-5")
    sub.add_parser("check", parents=[scope], help="validate the newest block")
    sub.add_parser("prompt", parents=[scope], help="print the paste-ready receiver prompt")
    s = sub.add_parser("snapshot", parents=[scope], help="print only the generated Snapshot")
    s.add_argument("--json", action="store_true",
                   help="print the snapshot as JSON instead of markdown (omits the brief block)")
    args = ap.parse_args(argv)
    return {"new": cmd_new, "check": cmd_check, "prompt": cmd_prompt,
            "snapshot": cmd_snapshot}[args.cmd](args) or 0


if __name__ == "__main__":
    sys.exit(main())
