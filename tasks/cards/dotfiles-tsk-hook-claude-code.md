---
task_id: dotfiles-tsk-hook-claude-code
title: Claude Code SessionStart hook + versioned settings.json fragment
project: dotfiles
phase: validation
created: "2026-09-21T13:25:25.414731+00:00"
touched: "2026-09-22T17:07:45.057926+00:00"
energy: ""
estimate: ""
deadline: ""
blocked_by: dotfiles-tsk-brief
origin: ""
---

# dotfiles-tsk-hook-claude-code

Claude Code SessionStart hook + versioned settings.json fragment

## History
- 2026-09-22T16:51:12.561262+00:00: backlog -> planning (actor: claude-code-bg/agent) — Picking up Wave 3 pull-side hook, now unblocked (brief.py done)
- 2026-09-22T16:52:41.161438+00:00: planning -> in_progress (actor: claude-code-bg/agent) — Implementing in worktree tsk-hook-claude-code
- 2026-09-22T16:57:44.426879+00:00: in_progress -> review (actor: claude-code-bg/agent) — Implemented .agents/hooks/ convention (tsk-brief-session-start.sh + session-start-hooks.json + install_session_start_hooks.py, sync.sh wiring). Verified end-to-end against an isolated fake HOME: hook script's JSON output, installer dry-run/real-run/idempotency/key-preservation, full sync.sh pass. Fixed a real bug along the way: $HOME inside single quotes in the generated settings.json command doesn't shell-expand -- switched to a {{HOME}} placeholder substituted at install time. PR opening now.
- 2026-09-22T17:07:45.057926+00:00: review -> validation (actor: claude-code-bg/agent) — PR #60 merged into main by owner authorization
