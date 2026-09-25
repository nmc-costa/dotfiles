# .agents/hooks/

Versioned source of truth for harness hooks — currently Claude Code's
`SessionStart` and `PreCompact` (dotfiles-tsk-chronicle-skill-layer,
2026-09-25). `dotfiles-tsk-hook-claude-code`: the first of this repo's
hooks to be tracked in git at all (the pre-existing `herdr-agent-state.sh`
and `workspace-standards-review-check.sh` in `~/.claude/hooks/` are still
local-only, not part of this convention yet).

## Layout

- `tsk-brief-session-start.sh` — SessionStart hook. Thin: it just shells
  out to `tasks/brief.py` (logic lives there, D14 "script before rule")
  and adapts its stdout to Claude Code's SessionStart JSON contract.
- `precompact_handoff.py` — PreCompact hook (dotfiles-tsk-chronicle-
  skill-layer D2). Runs seconds before Claude Code compacts a session's
  context, resolves the scope (card worktree → the one dirty worktree →
  main checkout → any dirty git repo), asks `handoff.py snapshot --json`
  for the facts, and prepends a machine-authored block to that scope's
  HANDOFF.md — no narrative, Goal/Done are the resumed session's to fill.
  Always exit 0, nothing on stdout: a hook must never break compaction.
- `session-and-compact-hooks.json` — declares which hook entries this
  workspace wants present in `~/.claude/settings.json`, per event:
  `events.SessionStart` and `events.PreCompact`. A legacy top-level
  `entries` list is still accepted as SessionStart. PreCompact entries
  carry no `matcher` (the event has none).
- `install_session_start_hooks.py` — merges the fragment into the live,
  local `~/.claude/settings.json`, iterating the fragment's event keys
  (earlier versions hardcoded SessionStart and silently ignored any other
  event — the regression `--self-test` now asserts against). Add-only and
  idempotent (dedups by the hook's `command` string); never touches hooks
  this workspace doesn't own. Run `--self-test` after changing the merge
  logic; sync.sh calls it on every sync.

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
2. Add an entry under the right event key in
   `session-and-compact-hooks.json`.
3. Run `./sync.sh` — it mirrors the script to `~/.claude/hooks/` and runs
   the installer to wire it into `~/.claude/settings.json`.
