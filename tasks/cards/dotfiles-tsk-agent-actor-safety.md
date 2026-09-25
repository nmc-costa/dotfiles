---
task_id: dotfiles-tsk-agent-actor-safety
title: "[HIGH PRIORITY] Agents must sign tasks/ events as actor-kind=agent for their own writes, and must not run unguarded git ops on the shared tasks/events.jsonl working tree"
project: dotfiles
phase: validation
created: "2026-09-23T12:05:25.335490+00:00"
touched: "2026-09-25T21:09:18.484780+00:00"
energy: mechanical
estimate: ""
deadline: ""
blocked_by: ""
origin: "recurring problem, flagged again 2026-09-23: an agent session (1) wrote a restorative move_task.py call under --actor-kind human --actor-id nmc-costa impersonating the owner instead of signing as agent/claude, and (2) separately ran git checkout -- tasks/events.jsonl directly in the shared ~/dotfiles working tree, wiping a concurrent human-authored event mid-write (recovered only because the agent had a git diff saved). Owner says this is not the first time this class of mistake has happened. Investigate + add an explicit, hard-to-miss instruction (tasks/README.md and/or CLAUDE.md/AGENTS.md, wherever agents actually read it on session start) covering: (a) an agent writing/restoring an events.jsonl entry always signs actor-kind=agent for that write, even when the payload/reason describes a human decision made elsewhere -- never borrow the human actor identity; (b) never run a raw git checkout/reset/stash/clean against tasks/events.jsonl (or any shared, actively-written file) in the main checkout -- it can silently discard another concurrent session's uncommitted append; safe alternatives are: isolate in a worktree before any speculative edit, or use append_event.py/move_task.py exclusively (additive, never destructive) instead of hand-reverting the file."
---

# dotfiles-tsk-agent-actor-safety

[HIGH PRIORITY] Agents must sign tasks/ events as actor-kind=agent for their own writes, and must not run unguarded git ops on the shared tasks/events.jsonl working tree

## History
- 2026-09-23T12:05:38.473729+00:00: backlog -> planning (actor: claude/agent)
- 2026-09-23T12:05:38.545893+00:00: planning -> in_progress (actor: claude/agent)
- 2026-09-24T15:35:49.244340+00:00: in_progress -> review (actor: claude/agent) — PR #76 opened: adds tasks/README.md 'Agent actor-kind' + 'events.jsonl is live and shared' sections, with pointers from AGENTS.md/CLAUDE.md's session-start reading.
- 2026-09-24T15:46:01.074072+00:00: review -> validation (actor: claude/agent) — PR #76 merged (b6cf32d): tasks/README.md + AGENTS.md + CLAUDE.md all carry the new actor-kind/git-safety sections on main now

Worktrees (this machine): [worktrees/dotfiles-tsk-agent-actor-safety.md](worktrees/dotfiles-tsk-agent-actor-safety.md) — `python3 ~/dotfiles/tasks/worktree.py list --task-id dotfiles-tsk-agent-actor-safety`

## Latest handoff
_@ in_progress_

Will add explicit agent-facing rules to tasks/README.md (actor-kind convention) and CLAUDE.md/AGENTS.md (no raw destructive git ops on shared tasks/events.jsonl; isolate in a worktree before speculative edits). Bundling with dotfiles-tsk-verify-setup-skill-gaps in the same branch/PR since both came out of the same session.
