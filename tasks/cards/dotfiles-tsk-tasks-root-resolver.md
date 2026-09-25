---
task_id: dotfiles-tsk-tasks-root-resolver
title: "tasks_root() resolver: one canonical write path for events.jsonl, the CAS lock and every rebuild_*.py (fixes 4 divergent copies + 1 orphaned event)"
project: dotfiles
phase: done
created: "2026-09-21T18:41:10.050054+00:00"
touched: "2026-09-21T21:44:40.243218+00:00"
energy: ""
estimate: ""
deadline: ""
blocked_by: ""
origin: ""
---

# dotfiles-tsk-tasks-root-resolver

tasks_root() resolver: one canonical write path for events.jsonl, the CAS lock and every rebuild_*.py (fixes 4 divergent copies + 1 orphaned event)

## History
- 2026-09-21T21:39:55.562895+00:00: backlog -> planning (actor: nmc-costa/human) — aprovado para implementar imediatamente
- 2026-09-21T21:39:58.614761+00:00: planning -> in_progress (actor: nmc-costa/human)
- 2026-09-21T21:44:17.284588+00:00: in_progress -> review (actor: nmc-costa/human) — PR #46 aberta, testado contra scratch TSK_ROOT + ciclo de vida completo com CAS
- 2026-09-21T21:44:36.257759+00:00: review -> validation (actor: nmc-costa/human) — revisto: testes de scratch TSK_ROOT + ciclo de vida completo confirmados, demo/ confirmado nao afetado
- 2026-09-21T21:44:40.243218+00:00: validation -> done (actor: nmc-costa/human)

Worktrees (this machine): [worktrees/dotfiles-tsk-tasks-root-resolver.md](worktrees/dotfiles-tsk-tasks-root-resolver.md) — `python3 ~/dotfiles/tasks/worktree.py list --task-id dotfiles-tsk-tasks-root-resolver`
