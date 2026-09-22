#!/usr/bin/env bash
# SessionStart hook: runs tasks/brief.py (the tasks/ orchestration system's
# cross-provider startup briefing) and injects its output into a fresh
# Claude Code session's context — pending facts to act on, or a director
# prompt when nothing is pending. dotfiles-tsk-hook-claude-code, the "pull"
# side of Wave 3's cross-provider handoff (tasks/HANDOFF.md Verdict 2).
#
# Deliberately thin: all logic lives in tasks/brief.py (D14, "script
# before rule" — see tasks/README.md). This script only adapts brief.py's
# plain-text stdout to Claude Code's SessionStart hook JSON contract, the
# same pattern workspace-standards-review-check.sh already uses locally.
#
# Silent no-op on any failure (missing brief.py, no python3, brief.py
# erroring, empty output) — a hook must never break session startup over
# an optional briefing.
set -uo pipefail

BRIEF_SCRIPT="$HOME/dotfiles/tasks/brief.py"
[[ -f "$BRIEF_SCRIPT" ]] || exit 0
command -v python3 >/dev/null 2>&1 || exit 0

OUTPUT="$(python3 "$BRIEF_SCRIPT" 2>/dev/null)" || exit 0
[[ -n "$OUTPUT" ]] || exit 0

# json.dumps (not a heredoc) because OUTPUT is dynamic — task titles/
# reasons can contain quotes, backslashes, newlines that would otherwise
# produce invalid JSON.
python3 -c '
import json, sys
print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": sys.argv[1],
    }
}))
' "$OUTPUT"
