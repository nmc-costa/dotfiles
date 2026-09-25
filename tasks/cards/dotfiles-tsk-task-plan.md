---
task_id: dotfiles-tsk-task-plan
title: dotfiles-tsk-task-plan
project: ""
phase: planning
created: "2026-09-25T14:25:19.028106+00:00"
touched: "2026-09-25T14:25:19.028106+00:00"
energy: ""
estimate: ""
deadline: ""
blocked_by: "dotfiles-tsk-task-brief-assistant, dotfiles-tsk-card-worktrees, dotfiles-tsk-cross-harness-orchestra"
origin: ""
---

# dotfiles-tsk-task-plan

dotfiles-tsk-task-plan

## History
- 2026-09-25T14:25:19.028106+00:00: backlog -> planning (actor: claude/agent) — owner respondeu ao questionário de alinhamento 2026-09-25

Worktrees (this machine): [worktrees/dotfiles-tsk-task-plan.md](worktrees/dotfiles-tsk-task-plan.md) — `python3 ~/dotfiles/tasks/worktree.py list --task-id dotfiles-tsk-task-plan`

## Latest handoff
_@ planning_

Decisões do owner (questionário 2026-09-25): (1) Nome: família de skills pequenas (task-brief, task-card, task-plan, task-worktree) + router fino /task-flow que encadeia brief -> card -> plan -> worktree -> dispatch/harness-orchestra; NÃO renomear para *-orchestra*. (2) 'task-setup' = ajudar a orquestrar agentes por fase (planeamento, criação do card, equipa por fase) -> coberto por /task-flow + /task-card + /task-plan; sem skill task-setup separada, sem card de bootstrap de tasks/ noutro repo. (3) Worktrees HÍBRIDO: tasks/worktree.py (#78) é o motor; layout ~/dotfiles.worktrees/<harness>/<task-id>[-<model>], branch <harness>/<task-id>[-<model>] — segmento de modelo só quando o mesmo harness tem >1 agente no card; orchestra.py (#81) chama worktree.py em vez de deixar o agent-deck escolher o caminho. (4) blocked_by passa a incluir dotfiles-tsk-card-worktrees (card criado por outra sessão). Próximo: aplicar (3) em #78/#81; depois task-card, task-plan, task-flow.
