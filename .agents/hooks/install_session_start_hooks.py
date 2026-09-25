#!/usr/bin/env python3
"""Idempotently merge this workspace's hook entries (session-and-compact-
hooks.json, this script's sibling) into the live, local
~/.claude/settings.json.

Why a separate installer instead of symlinking settings.json itself: that
file also holds live runtime state Claude Code writes into directly
(theme, autoMode, remoteControlAtStartup, credentials-adjacent config) --
symlinking it would put that state inside the git working tree, the exact
mistake ~/dotfiles/.claude/CLAUDE.md documents avoiding for CLAUDE.md
itself (see setup_agent_file_symlink there). So settings.json stays a
real, local file; this script is the repeatable step that keeps its
hooks in sync with the versioned fragment.

Per-event (dotfiles-tsk-chronicle-skill-layer, 2026-09-25): the fragment's
top-level `events` object maps a Claude Code hook event name (SessionStart,
PreCompact, ...) to that event's entry list, and each event's entries are
merged into `settings.hooks[<event>]`. Earlier versions of this script
hardcoded `SessionStart` -- a PreCompact entry in the fragment was then
silently ignored (the failure mode the --self-test below exists to make
loud). A legacy top-level `entries` list is still accepted, as SessionStart.

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
    python3 install_session_start_hooks.py [--fragment PATH] [--settings PATH]
                                           [--dry-run] [--self-test]

Defaults: --fragment is this script's own sibling session-and-compact-
hooks.json (falling back to the pre-rename session-start-hooks.json for
older sync.sh copies that still pass it), --settings is
~/.claude/settings.json. Silent no-op (exit 0) if either file is missing,
or if the live settings.json fails to parse as JSON -- this must never
break sync.sh or a session over a malformed optional local file.

--self-test builds throwaway settings/fragment fixtures in a temp dir
(foreign hook included), runs the merge twice, and asserts: per-event
placement, foreign hooks untouched, and second-run byte-identical
idempotency. Exits 1 on any regression -- CI/setup should run it so a
merge-logic regression fails loudly instead of silently dropping a hook.
"""
import argparse
import json
import shutil
import sys
import tempfile
from pathlib import Path

LEGACY_EVENTS = {"entries": "SessionStart"}
SELF_TEST = "__self_test__"


def default_fragment(script_dir):
    new = script_dir / "session-and-compact-hooks.json"
    if new.is_file():
        return new
    return script_dir / "session-start-hooks.json"


def merge(fragment, settings):
    """Mutate settings in place from a parsed fragment. Returns True if
    anything changed. Pure function of its inputs -- --self-test feeds it
    fixtures instead of live files."""
    home = str(Path.home())
    changed = False
    events = fragment.get("events")
    if not isinstance(events, dict):
        events = {LEGACY_EVENTS["entries"]: fragment.get("entries", [])}

    for event, entries in events.items():
        if not isinstance(entries, list):
            continue
        groups = settings.setdefault("hooks", {}).setdefault(event, [])
        for entry in entries:
            hook = entry.get("hook")
            if not isinstance(hook, dict) or "command" not in hook:
                continue
            matcher = entry.get("matcher")
            cmd = hook["command"].replace("{{HOME}}", home)
            merged_hook = {**hook, "command": cmd}
            group = next((g for g in groups if g.get("matcher") == matcher), None)
            if group is None:
                group = {"hooks": []}
                if matcher is not None:
                    group["matcher"] = matcher
                groups.append(group)
                changed = True
            if cmd not in {h.get("command") for h in group["hooks"]}:
                group["hooks"].append(merged_hook)
                changed = True
    return changed


def load_json(path):
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as e:
        print(f"install_session_start_hooks: invalid JSON, skipping: {e}", file=sys.stderr)
        return None


def run_merge(fragment_path, settings_path, dry_run):
    """One pass against real files. Returns the exit code."""
    if not fragment_path.is_file():
        print(f"install_session_start_hooks: no fragment at {fragment_path}, skipping", file=sys.stderr)
        return 0
    if not settings_path.is_file():
        print(f"install_session_start_hooks: no settings.json at {settings_path}, skipping", file=sys.stderr)
        return 0

    fragment = load_json(fragment_path)
    settings = load_json(settings_path)
    if fragment is None or settings is None:
        return 0

    if not merge(fragment, settings):
        print("install_session_start_hooks: already up to date")
        return 0

    if dry_run:
        print(f"install_session_start_hooks: would update {settings_path}")
        return 0

    backup = settings_path.with_suffix(settings_path.suffix + ".bak")
    shutil.copy2(settings_path, backup)
    settings_path.write_text(json.dumps(settings, indent=2) + "\n")
    print(f"install_session_start_hooks: updated {settings_path} (backup at {backup})")
    return 0


def self_test():
    """Fixture-driven regression gate: per-event placement, foreign hooks
    untouched, idempotency. Exits 1 loudly on any failure -- the whole
    point (the flaw this fixes was a silent no-op)."""
    failures = []

    def check(name, ok, detail=""):
        if not ok:
            failures.append(f"{name}: {detail}" if detail else name)

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        settings_path = tmp / "settings.json"
        settings_path.write_text(json.dumps({
            "hooks": {"SessionStart": [
                {"matcher": "*", "hooks": [
                    {"type": "command", "command": "bash /foreign/herdr-agent-state.sh"}]}
            ]}
        }, indent=2))
        fragment_path = tmp / "session-and-compact-hooks.json"
        fragment_path.write_text(json.dumps({
            "events": {
                "SessionStart": [{"matcher": "*", "hook": {
                    "type": "command", "command": "bash '{{HOME}}/.claude/hooks/tsk-brief-session-start.sh'",
                    "timeout": 10}}],
                "PreCompact": [{"hook": {
                    "type": "command", "command": "python3 '{{HOME}}/.claude/hooks/precompact_handoff.py'",
                    "timeout": 30}}],
            }
        }))

        run_merge(fragment_path, settings_path, dry_run=False)
        first = settings_path.read_text()
        merged = json.loads(first)
        hooks = merged.get("hooks", {})

        ss = [h["command"] for g in hooks.get("SessionStart", []) for h in g["hooks"]]
        check("SessionStart merge", any("tsk-brief-session-start.sh" in c for c in ss), f"got {ss}")
        check("foreign SessionStart kept", any("herdr-agent-state.sh" in c for c in ss), f"got {ss}")
        pc = [h["command"] for g in hooks.get("PreCompact", []) for h in g["hooks"]]
        check("PreCompact merged under its own event key", any("precompact_handoff.py" in c for c in pc), f"got {pc}")
        check("{{HOME}} substituted", not any("{{HOME}}" in c for c in ss + pc))

        # PreCompact group must carry no matcher key (event has no matcher).
        pc_group = hooks.get("PreCompact", [])
        check("PreCompact has no matcher", all("matcher" not in g for g in pc_group), f"got {pc_group}")

        run_merge(fragment_path, settings_path, dry_run=False)
        second = settings_path.read_text()
        check("idempotent second run", first == second, "settings changed on a no-op merge")

        # Legacy `entries` fragment still lands as SessionStart.
        legacy_path = tmp / "session-start-hooks.json"
        legacy_path.write_text(json.dumps({"entries": [{"matcher": "*", "hook": {
            "type": "command", "command": "echo legacy"}}]}))
        run_merge(legacy_path, settings_path, dry_run=False)
        ss2 = [h["command"] for g in json.loads(settings_path.read_text())["hooks"]["SessionStart"] for h in g["hooks"]]
        check("legacy entries -> SessionStart", "echo legacy" in ss2, f"got {ss2}")

    if failures:
        print("install_session_start_hooks: SELF-TEST FAILED", file=sys.stderr)
        for f in failures:
            print(f"  - {f}", file=sys.stderr)
        return 1
    print("install_session_start_hooks: self-test passed "
          "(per-event merge, foreign hooks kept, idempotent, legacy schema)")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--fragment", type=Path, default=None,
                        help="fragment file (default: sibling session-and-compact-hooks.json)")
    parser.add_argument("--settings", type=Path, default=Path.home() / ".claude" / "settings.json")
    parser.add_argument("--dry-run", action="store_true", help="report what would change, write nothing")
    parser.add_argument("--self-test", action="store_true", help="run fixture assertions and exit")
    args = parser.parse_args()

    if args.self_test:
        return self_test()

    fragment = args.fragment or default_fragment(Path(__file__).resolve().parent)
    return run_merge(fragment, args.settings, args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
