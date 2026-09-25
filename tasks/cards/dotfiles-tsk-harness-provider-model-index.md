---
task_id: dotfiles-tsk-harness-provider-model-index
title: Build a validated harness x provider x model orchestration index
project: dotfiles
phase: done
created: "2026-09-23T11:52:17.170402+00:00"
touched: "2026-09-25T21:53:08.497011+00:00"
energy: ""
estimate: ""
deadline: ""
blocked_by: ""
origin: ""
---

# dotfiles-tsk-harness-provider-model-index

Build a validated harness x provider x model orchestration index

## History
- 2026-09-23T11:59:38.966240+00:00: backlog -> planning (actor: nmc-costa/human) — Owner flagged high priority, requested real planning + branch execution
- 2026-09-23T12:00:09.249287+00:00: planning -> in_progress (actor: claude/agent)
- 2026-09-23T12:02:25.508135+00:00: in_progress -> review (actor: claude/agent)
- 2026-09-23T21:49:00.824912+00:00: review -> validation (actor: claude/agent) — PR #72 merged (merge commit 67cec54044e66abbef11c86bbfc282f4ea47463e), owner authorized the merge directly
- 2026-09-25T21:53:08.497011+00:00: validation -> done (actor: claude/agent) — Doc validated against machine state 2026-09-25: dispatch.py PROVIDER_BINARIES includes agy, harness-matrix.instructions.md points back here, hardware claims match (38GB RAM, Iris Xe). 5 documented gaps stay open by design; unblocks dotfiles-tsk-task-brief-assistant

Worktrees (this machine): [worktrees/dotfiles-tsk-harness-provider-model-index.md](worktrees/dotfiles-tsk-harness-provider-model-index.md) — `python3 ~/dotfiles/tasks/worktree.py list --task-id dotfiles-tsk-harness-provider-model-index`

## Latest handoff
_@ validation_

Merged tasks/harness-provider-model-index.md into main, including the Antigravity phase-routing content folded in per owner's 2026-09-23 reconciliation decision (fuse into one doc rather than merge origin/antigravity/harness-model-matrix separately). Added the previously-missing Antigravity/Gemini CLI row (agy 1.2.9 + gemini 0.60.0, both installed and dispatchable via tasks/dispatch.py -- neither original draft had this). Left .agents/instructions/workspace-config/harness-matrix.instructions.md as a short pointer back to this file so nothing stays duplicated. Open gaps still listed in the doc itself (Ollama model not pulled, omp setup undocumented, dtx-glm53-flash cost unconfirmed, RTX 3070 Ti unverified, Antigravity/Gemini cost+plumbing unconfirmed) -- validation here means confirming the doc itself is sound and unblocks dotfiles-tsk-task-brief-assistant, not that every gap is closed. Separately noticed a third, unrelated model-routing.instructions.md file in the same directory (task-type-based routing, references GPT-5/copilot-instructions.md/.github/skills) that looks like it belongs to a different subsystem -- did not touch it, flagged to the owner for a future session.
