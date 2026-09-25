#!/usr/bin/env python3
"""Claude Code PreCompact hook — capture where the session stopped BEFORE
context compaction throws the details away (dotfiles-tsk-chronicle-skill-
layer D2; evidence E5: no harness triggers "imminent death -> write
handoff", and a model that is about to be compacted cannot self-invoke a
skill).

What it does, in order:
1. Read the hook's stdin JSON (best-effort) and take its `cwd` — else the
   process cwd (Claude Code runs hooks in the session's cwd).
2. Resolve the scope to write HANDOFF.md into, with a fallback chain:
   a. cwd's git root IS a managed card worktree (…/.worktrees/<harness>/
      <task-id>) -> that worktree;
   b. cwd's git root is the main dotfiles checkout -> ask
      `tasks/worktree.py list --json` for managed worktrees; exactly one
      dirty one wins; several or none dirty -> the main checkout's own
      global HANDOFF.md (never guess between concurrent cards);
   c. any other git repo -> its root, but only when there is something to
      resume (uncommitted changes or unpushed commits);
   d. nothing meaningful -> exit 0 silently.
3. Ask `handoff.py snapshot --json` for the facts (structured; the brief
   block is skipped to stay inside the hook's 30s budget) and prepend a
   machine-authored block to <scope>/HANDOFF.md: marker + title from
   branch/PR + one pointer line + compact snapshot. NO synthesized
   narrative — Goal/Done are the resumed session's to fill (critique F3:
   `handoff.py new`'s TODO scaffold cannot be filled by a hook).

Contract: ALWAYS exit 0 (errors go to stderr, never block compaction),
nothing on stdout, every subprocess timeout-bounded. Idempotency note:
each compaction legitimately writes a new block (newest on top, same as
`handoff.py new`) — the block IS the record of that compaction.

This file lives in the shared hooks dir and is mirrored to
~/.claude/hooks/ by sync.sh; it finds handoff.py through the skills
mirror, never through a repo-relative path, so it works from any checkout.
"""
import datetime as dt
import json
import os
import re
import subprocess
import sys
from pathlib import Path

MARKER_RE = re.compile(r"^<!-- handoff:block .* -->$", re.M)
STAMP_FMT = "%Y-%m-%dT%H:%MZ"
HARNESS_PREFIXES = ("claude", "copilot", "gemini", "agy", "codex", "opencode")


def say(msg):
    print(f"precompact_handoff: {msg}", file=sys.stderr)


def run(cmd, cwd=None, timeout=10):
    try:
        r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    except (OSError, subprocess.SubprocessError):
        return None
    return r.stdout.rstrip() if r.returncode == 0 else None


def git_root(start):
    out = run(["git", "rev-parse", "--show-toplevel"], cwd=start, timeout=5)
    return Path(out).resolve() if out else None


def find_handoff_py():
    """First existing handoff.py. Script-relative first: in the mirrored
    runtime (~/.claude/hooks/) it resolves to ~/.claude/skills/handoff/ —
    the same file as the Claude mirror — while run-from-source (a card
    worktree) picks that checkout's own, freshest copy. The ~/.agents
    mirror (a symlink into the MAIN checkout) is last: it lags any
    unmerged worktree branch."""
    candidates = [
        Path(__file__).resolve().parent.parent / "skills" / "handoff" / "handoff.py",
        Path.home() / ".claude" / "skills" / "handoff" / "handoff.py",
        Path.home() / ".agents" / "skills" / "handoff" / "handoff.py",
    ]
    return next((c for c in candidates if c.is_file()), None)


def worktree_dotfiles(main_root):
    """Map a cwd inside the main dotfiles checkout to a scope, per the
    fallback chain. Returns (scope, context_wording)."""
    out = run([sys.executable, str(main_root / "tasks" / "worktree.py"), "list", "--json"],
              cwd=main_root, timeout=10)
    dirty = []
    if out:
        try:
            dirty = [w for w in json.loads(out) if w.get("clean") is False]
        except json.JSONDecodeError:
            pass
    if len(dirty) == 1:
        return Path(dirty[0]["path"]), f"card `{dirty[0]['task_id']}`"
    return main_root, None


def resolve_scope(cwd):
    """The fallback chain. Returns (scope_dir, context_wording) or None."""
    root = git_root(cwd)
    if not root:
        return None
    # Managed worktree layout: <repo>.worktrees/<harness>/<task-id> (see
    # tasks/worktree.py base_dir) — the repo segment always ends in
    # ".worktrees".
    if any(p.endswith(".worktrees") for p in root.parts) and re.match(r"^[a-z0-9][a-z0-9-]*$", root.name):
        return root, f"card `{root.name}`"

    main_worktree_py = root / "tasks" / "worktree.py"
    if main_worktree_py.is_file():
        return worktree_dotfiles(root)

    dirty = run(["git", "status", "--porcelain"], cwd=root, timeout=5)
    unpushed = run(["git", "rev-list", "--count", "@{u}..HEAD"], cwd=root, timeout=5)
    has_work = (dirty and dirty.strip()) or (unpushed and unpushed != "0")
    if has_work:
        return root, None
    return None


def compact_markdown(data, context):
    """Machine view of the snapshot JSON — compact, factual, no narrative."""
    lines = ["## Snapshot (machine, pre-compaction)", "",
             "_Written by the PreCompact hook seconds before context compaction — "
             "verify against live state before trusting it._", ""]
    lines.append(f"- **Written:** {data.get('written')} on `{data.get('host')}` by `precompact-hook`")
    if data.get("repo"):
        lines.append(f"- **Repo:** `{data['repo']}` — branch `{data.get('branch')}`")
    if data.get("upstream"):
        lines.append(f"- **Upstream:** `{data['upstream']}` — {data.get('ahead')} ahead, {data.get('behind')} behind")
    else:
        lines.append("- **Upstream:** none — branch not pushed")
    if data.get("pr"):
        p = data["pr"]
        lines.append(f"- **PR:** #{p.get('number')} {p.get('state')} {p.get('url')}")
    if data.get("commits"):
        lines.append(f"- **Unpushed commits:** {len(data['commits'])}")
    if data.get("clean"):
        lines.append("- **Working tree:** clean")
    elif data.get("uncommitted"):
        uc = data["uncommitted"]
        lines.append(f"- **Uncommitted changes:** {len(uc)} entr(ies):")
        lines += [f"  - {c}" for c in uc[:10]]
        if len(uc) > 10:
            lines.append(f"  - ... {len(uc) - 10} more")
    if context:
        lines.append(f"- **Scope reason:** {context}")
    return "\n".join(lines)


def block_title(data, scope):
    branch = data.get("branch")
    title = branch if branch and branch != "(detached)" else scope.name
    if title and "/" in title:
        parts = title.split("/", 1)
        if parts[0] in HARNESS_PREFIXES:
            title = parts[1]
    if data.get("pr") and data["pr"].get("number"):
        title += f" (PR #{data['pr']['number']})"
    return title


def next_step(context, scope):
    if context and "card `" in context:
        task_id = context.split("card `", 1)[1].rstrip("`")
        return (f"Verify the Snapshot above against live state, then resume the work for "
                f"{context}: see `tasks/cards/{task_id}.md` in the main checkout and run "
                f"`python3 ~/dotfiles/tasks/brief.py`; ask the human what to resume.")
    return ("Verify the Snapshot above against live state, then ask the human what to "
            "resume. This block was machine-written seconds before context compaction — "
            "fill Goal/Done (or add a fresh block with `handoff.py new`) once you know more.")


def prepend_block(scope, block):
    path = scope / "HANDOFF.md"
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if old and not MARKER_RE.search(old):
        old = "# Earlier handoff notes (free-form, pre-`/handoff`)\n\n" + old
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(block + ("\n---\n\n" + old if old else ""), encoding="utf-8")
    return path


def main():
    try:
        raw = "" if sys.stdin.isatty() else sys.stdin.read()
        try:
            hook_input = json.loads(raw) if raw.strip() else {}
        except json.JSONDecodeError:
            hook_input = {}
        cwd = hook_input.get("cwd") or os.getcwd()

        resolved = resolve_scope(Path(cwd))
        if not resolved:
            say("nothing to snapshot (clean tree, no card worktree) — exiting silently")
            return 0
        scope, context = resolved

        handoff_py = find_handoff_py()
        if not handoff_py:
            say("handoff.py not found — cannot snapshot")
            return 0
        out = run([sys.executable, str(handoff_py), "snapshot", "--json", "--dir", str(scope)],
                  cwd=scope, timeout=20)
        if not out:
            say("handoff.py snapshot --json failed")
            return 0
        try:
            data = json.loads(out)
        except json.JSONDecodeError:
            say("handoff.py snapshot --json returned non-JSON")
            return 0

        if data.get("clean") and not data.get("commits") and not data.get("pr") and not context:
            say("clean tree, no commits, no PR — nothing to resume, exiting silently")
            return 0

        stamp = dt.datetime.now(dt.timezone.utc).strftime(STAMP_FMT)
        block = "\n".join([
            f"<!-- handoff:block {stamp} -->",
            f"# Handoff — auto-snapshot before compaction — {block_title(data, scope)} ({stamp[:10]})",
            "",
            "> **To whoever picks this up (any harness, any model):** machine-written by the",
            "> PreCompact hook right before this session's context was compacted. Check the",
            "> Snapshot against live state, then start at **Next step**.",
            "",
            compact_markdown(data, context),
            "",
            "## Next step",
            "",
            next_step(context, scope),
            "",
        ])
        path = prepend_block(scope, block)
        say(f"wrote {path}")
        return 0
    except Exception as exc:  # noqa: BLE001 — a hook must never break compaction
        say(f"unexpected error ignored: {exc}")
        return 0


if __name__ == "__main__":
    sys.exit(main())
