---
task_id: dotfiles-tsk-chronicle-skill-layer
title: "Chronicle-like skill layer: mine interactions into skills/instructions, resume-after-timeout, PR-finish, skill chaining + chat autocomplete"
project: dotfiles
phase: done
created: "2026-09-25T20:56:46.453899+00:00"
touched: "2026-09-25T21:41:16.427167+00:00"
energy: deep
estimate: ""
deadline: ""
blocked_by: ""
origin: me
---

# dotfiles-tsk-chronicle-skill-layer

Chronicle-like skill layer: mine interactions into skills/instructions, resume-after-timeout, PR-finish, skill chaining + chat autocomplete

## History
- 2026-09-25T21:09:18.695274+00:00: backlog -> planning (actor: nmc-costa/human) — human answered plan-orchestra questionnaire: move to planning
- 2026-09-25T21:32:25.642057+00:00: planning -> in_progress (actor: opencode/agent) — owner directed: build D1-D3 in opencode session (Claude Pro weekly limit hit; Copilot timing out)
- 2026-09-25T21:36:14.457941+00:00: in_progress -> review (actor: opencode/agent) — D1-D3 implemented + verified in worktree; PR #92 open
- 2026-09-25T21:41:16.037275+00:00: review -> validation (actor: opencode/agent) — owner accepted in chat without review and directed the merge ('eu aceito o que fizeste só de olhar para o chat; quero que faças merge') — PR #92 squash-merged, deploy done (hook live in settings.json)
- 2026-09-25T21:41:16.427167+00:00: validation -> done (actor: opencode/agent) — D1-D3 shipped: PR #92 merged (20a8bf6), PreCompact hook live, handoff --json + title-from-branch shipped

Worktrees (this machine): [worktrees/dotfiles-tsk-chronicle-skill-layer.md](worktrees/dotfiles-tsk-chronicle-skill-layer.md) — `python3 ~/dotfiles/tasks/worktree.py list --task-id dotfiles-tsk-chronicle-skill-layer`

## Latest handoff
_@ planning_

PLAN (plan-orchestra, 2 rounds, critique PASS). Build order: D1 installer per-event-keys + self-test -> D3 handoff.py snapshot --json + --title-from-branch -> D2 PreCompact hook (.agents/hooks/precompact_handoff.py: stdin JSON cwd -> worktree.py list --json, fallback chain, exit-0 silent, never blocks compaction, NO Stop hook) -> D4 pr-finish (validate -> gh pr view --json mergeable,mergeStateStatus; OWNER DECISION: --auto flag does gh pr merge --auto only when CI green+no conflicts; never for cards past loop cap/human-required validation; default = print commands) -> D5 chronicle miner (events.jsonl + ~/.claude/projects JSONL + PR churn -> proposals PR with cited evidence, human-only merge) -> D6 stacking (/a /b one message) + Chains section in SKILL.md BODY (descriptions stay tight) -> D7 opencode v1 = custom commands + tui.prompt.append, follow FR #5971 for real panel -> D8 OWNER CHOICE: voxtype (Rust whisper.cpp push-to-talk Wayland) + phrase->macro map, inject via ydotoold. Research evidence: Chronicle exists (Copilot CLI /chronicle improve, propose-only); skill triggering is LLM-description-driven everywhere; no tool combines hotkeys+parameterized prompts+chaining. Worktree per card: tasks/worktree.py create --task-id dotfiles-tsk-chronicle-skill-layer --harness claude
