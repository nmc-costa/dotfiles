---
task_id: dotfiles-tsk-worktree-model-suffix
title: "tasks/worktree.py v2: optional [-<model>] suffix in path/branch when a harness has >1 agent on the same card"
project: dotfiles
phase: backlog
created: "2026-09-25T20:38:23.354520+00:00"
touched: "2026-09-25T20:38:23.354520+00:00"
energy: mechanical
estimate: ""
deadline: ""
blocked_by: ""
origin: "owner decision 2026-09-25 (questionário de alinhamento do card dotfiles-tsk-task-plan, resposta \"híbrido\"); written by claude on the owner explicit instruction. tasks/worktree.py (#78, já com merge) documenta o layout como \"fixed, never configurable in v1\" — <repo>.worktrees/<harness>/<task-id>, branch <harness>/<task-id>. Decisão: layout híbrido <harness>/<task-id>[-<model>] (path e branch), sufixo -<model> só quando o mesmo harness tem mais de um agente no mesmo card. tasks/orchestra.py (#81, ainda não construído) deve chamar worktree.py para o caminho em vez do agent-deck escolher sozinho. Ver tasks/plans/task-plan.md (secção \"Out of scope\") para o contexto completo. Não bloqueia dotfiles-tsk-task-plan (esse card só referencia o layout-alvo, não implementa lógica de caminho)."
---

# dotfiles-tsk-worktree-model-suffix

tasks/worktree.py v2: optional [-<model>] suffix in path/branch when a harness has >1 agent on the same card

## History
- (no phase_changed events yet — still in its original created phase)

Worktrees (this machine): [worktrees/dotfiles-tsk-worktree-model-suffix.md](worktrees/dotfiles-tsk-worktree-model-suffix.md) — `python3 ~/dotfiles/tasks/worktree.py list --task-id dotfiles-tsk-worktree-model-suffix`
