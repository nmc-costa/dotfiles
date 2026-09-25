---
task_id: dotfiles-tsk-jsonl-merge-driver
title: "Custom git merge driver (merge=union or equivalent) for tasks/*.jsonl so a conflict resolution can never silently drop an append-only line"
project: dotfiles
phase: done
created: "2026-09-21T18:41:17.108344+00:00"
touched: "2026-09-21T21:55:37.515799+00:00"
energy: ""
estimate: ""
deadline: ""
blocked_by: ""
origin: ""
---

# dotfiles-tsk-jsonl-merge-driver

Custom git merge driver (merge=union or equivalent) for tasks/*.jsonl so a conflict resolution can never silently drop an append-only line

## History
- 2026-09-21T21:52:33.379135+00:00: backlog -> planning (actor: nmc-costa/human) — independente, sem bloqueadores, avancar
- 2026-09-21T21:52:36.723091+00:00: planning -> in_progress (actor: nmc-costa/human)
- 2026-09-21T21:55:30.499685+00:00: in_progress -> review (actor: nmc-costa/human) — PR #52 aberta, reproduzi o bug real num repo scratch e confirmei a correcao
- 2026-09-21T21:55:34.294755+00:00: review -> validation (actor: nmc-costa/human) — revisto: PR #52 fundida, teste reproduzindo o bug real confirma a correcao
- 2026-09-21T21:55:37.515799+00:00: validation -> done (actor: nmc-costa/human)

Worktrees (this machine): [worktrees/dotfiles-tsk-jsonl-merge-driver.md](worktrees/dotfiles-tsk-jsonl-merge-driver.md) — `python3 ~/dotfiles/tasks/worktree.py list --task-id dotfiles-tsk-jsonl-merge-driver`
