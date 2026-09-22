#!/usr/bin/env python3
"""Idempotently merge this workspace's SessionStart hook entries
(session-start-hooks.json, this script's sibling) into the live, local
~/.claude/settings.json.

Why a separate installer instead of symlinking settings.json itself: that
file also holds live runtime state Claude Code writes into directly
(theme, autoMode, remoteControlAtStartup, credentials-adjacent config) --
symlinking it would put that state inside the git working tree, the exact
mistake ~/dotfiles/.claude/CLAUDE.md documents avoiding for CLAUDE.md
itself (see setup_agent_file_symlink there). So settings.json stays a
real, local file; this script is the repeatable step that keeps its
hooks.SessionStart in sync with the versioned fragment.

Add-only and idempotent: an entry already present (matched by its exact
"command" string, the part that's actually unique per hook) is left
untouched; missing entries are appended to the matching matcher group (or
a new group is created if none matches). Hooks this workspace doesn't own
(e.g. herdr-agent-state.sh, or anything added by another tool) are never
touched or removed.

Claude Code execs a hook's "command" string literally -- no shell
variable expansion -- so any `{{HOME}}` placeholder in the fragment's
command is substituted with the real, resolved home directory before
comparing or writing, matching the absolute paths the pre-existing hooks
already hardcode.

Usage:
    python3 install_session_start_hooks.py [--fragment PATH] [--settings PATH] [--dry-run]

Defaults: --fragment is this script's own sibling session-start-hooks.json,
--settings is ~/.claude/settings.json. Silent no-op (exit 0) if either
file is missing, or if the live settings.json fails to parse as JSON --
this must never break sync.sh or a session over a malformed optional
local file.
"""
import argparse
import json
import shutil
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--fragment", type=Path, default=Path(__file__).resolve().parent / "session-start-hooks.json")
    parser.add_argument("--settings", type=Path, default=Path.home() / ".claude" / "settings.json")
    parser.add_argument("--dry-run", action="store_true", help="report what would change, write nothing")
    args = parser.parse_args()

    if not args.fragment.is_file():
        print(f"install_session_start_hooks: no fragment at {args.fragment}, skipping", file=sys.stderr)
        return 0
    if not args.settings.is_file():
        print(f"install_session_start_hooks: no settings.json at {args.settings}, skipping", file=sys.stderr)
        return 0

    try:
        fragment = json.loads(args.fragment.read_text())
        settings = json.loads(args.settings.read_text())
    except json.JSONDecodeError as e:
        print(f"install_session_start_hooks: invalid JSON, skipping: {e}", file=sys.stderr)
        return 0

    session_start = settings.setdefault("hooks", {}).setdefault("SessionStart", [])

    home = str(Path.home())
    changed = False
    for entry in fragment.get("entries", []):
        matcher = entry["matcher"]
        hook = {**entry["hook"], "command": entry["hook"]["command"].replace("{{HOME}}", home)}
        group = next((g for g in session_start if g.get("matcher") == matcher), None)
        if group is None:
            group = {"matcher": matcher, "hooks": []}
            session_start.append(group)
            changed = True
        if hook["command"] not in {h.get("command") for h in group["hooks"]}:
            group["hooks"].append(hook)
            changed = True

    if not changed:
        print("install_session_start_hooks: already up to date")
        return 0

    if args.dry_run:
        print(f"install_session_start_hooks: would update {args.settings}")
        return 0

    backup = args.settings.with_suffix(args.settings.suffix + ".bak")
    shutil.copy2(args.settings, backup)
    args.settings.write_text(json.dumps(settings, indent=2) + "\n")
    print(f"install_session_start_hooks: updated {args.settings} (backup at {backup})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
