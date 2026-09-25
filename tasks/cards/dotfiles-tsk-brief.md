---
task_id: dotfiles-tsk-brief
title: brief.py - heartbeat + inbox consumer
project: dotfiles
phase: done
created: "2026-09-21T13:25:25.376148+00:00"
touched: "2026-09-21T21:37:48.970805+00:00"
energy: ""
estimate: ""
deadline: ""
blocked_by: dotfiles-tsk-writepath-unification
origin: ""
---

# dotfiles-tsk-brief

brief.py - heartbeat + inbox consumer

## History
- 2026-09-21T21:33:13.408281+00:00: backlog -> planning (actor: nmc-costa/human) — Sequencia natural apos notify-sweep, sem colisao reportada
- 2026-09-21T21:33:19.191212+00:00: planning -> in_progress (actor: nmc-costa/human)
- 2026-09-21T21:37:33.683181+00:00: in_progress -> review (actor: nmc-costa/human) — brief.py implementado e testado, incluindo --prompt-only para o dispatch-launcher
- 2026-09-21T21:37:43.004513+00:00: review -> validation (actor: nmc-costa/human)
- 2026-09-21T21:37:48.970805+00:00: validation -> done (actor: nmc-costa/human)

Worktrees (this machine): [worktrees/dotfiles-tsk-brief.md](worktrees/dotfiles-tsk-brief.md) — `python3 ~/dotfiles/tasks/worktree.py list --task-id dotfiles-tsk-brief`

## Latest handoff
_@ validation_

brief.py: heartbeat check + inbox por prioridade (P0 primeiro) + so pergunta ao diretor se nada pendente. Sem tasks/inbox.md separado - le events.jsonl diretamente, mesma fonte do notify.py. --prompt-only --task-id gera o prompt de dispatch pronto a colar (titulo/fase/handoff/aviso de duas transicoes se ainda em backlog) - o contrato que dotfiles-tsk-dispatch-launcher precisa. Testado: banner de heartbeat morto/inexistente, lista ordenada com P0 primeiro, --ack remove da lista, tarefa inexistente -> exit 1, --prompt-only contra tarefas reais em backlog/done. Desbloqueia toda a Onda 3 (hooks/cpx/skill/dispatch-launcher).
