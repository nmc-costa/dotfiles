# .agents/hooks/

Versioned source of truth for harness startup hooks — currently just
Claude Code's `SessionStart`. `dotfiles-tsk-hook-claude-code`: the first
of this repo's hooks to be tracked in git at all (the pre-existing
`herdr-agent-state.sh` and `workspace-standards-review-check.sh` in
`~/.claude/hooks/` are still local-only, not part of this convention yet).

## Layout

- `tsk-brief-session-start.sh` — the hook script. Thin: it just shells out
  to `tasks/brief.py` (logic lives there, D14 "script before rule") and
  adapts its stdout to Claude Code's SessionStart JSON contract.
- `session-start-hooks.json` — declares which hook entries this workspace
  wants present in `~/.claude/settings.json`'s `hooks.SessionStart`.
- `install_session_start_hooks.py` — merges `session-start-hooks.json`
  into the live, local `~/.claude/settings.json`. Add-only and idempotent
  (dedups by the hook's `command` string); never touches hooks this
  workspace doesn't own.

## Why settings.json isn't just symlinked

`~/.claude/settings.json` holds live runtime state Claude Code itself
writes into (theme, `autoMode`, `remoteControlAtStartup`, ...) alongside
the hooks config — the same reason `~/.claude/CLAUDE.md` is a file-level
symlink and not a whole-directory one (see `~/dotfiles/.claude/CLAUDE.md`).
So the hook *scripts* mirror to `~/.claude/hooks/` (`sync.sh`, same
pattern as `skills/` -> `~/.claude/skills`), but the *settings.json wiring*
goes through `install_session_start_hooks.py` instead of a symlink.

## Adding a new hook

1. Add the script here, matching `tsk-brief-session-start.sh`'s
   fail-silent style (a hook must never break session startup).
2. Add an entry to `session-start-hooks.json`.
3. Run `./sync.sh` — it mirrors the script to `~/.claude/hooks/` and runs
   the installer to wire it into `~/.claude/settings.json`.
