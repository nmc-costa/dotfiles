---
task_id: dotfiles-tsk-notify-sweep
title: notify.py + sweep.py - the notification producer side
project: dotfiles
phase: done
created: "2026-09-21T13:25:25.342455+00:00"
touched: "2026-09-21T18:55:14.801560+00:00"
energy: ""
estimate: ""
deadline: ""
blocked_by: dotfiles-tsk-writepath-unification
origin: ""
---

# dotfiles-tsk-notify-sweep

notify.py + sweep.py - the notification producer side

## History
- 2026-09-21T18:45:20.365349+00:00: backlog -> planning (actor: nmc-costa/human) — Coordenado com sessao concorrente via SendMessage, sem overlap
- 2026-09-21T18:45:25.980727+00:00: planning -> in_progress (actor: nmc-costa/human)
- 2026-09-21T18:54:55.653239+00:00: in_progress -> review (actor: nmc-costa/human) — notify.py+sweep.py implementados e testados (scratch dir), escopo deliberadamente reduzido - ver README
- 2026-09-21T18:55:05.108027+00:00: review -> validation (actor: nmc-costa/human)
- 2026-09-21T18:55:14.801560+00:00: validation -> done (actor: nmc-costa/human)

Worktrees (this machine): [worktrees/dotfiles-tsk-notify-sweep.md](worktrees/dotfiles-tsk-notify-sweep.md) — `python3 ~/dotfiles/tasks/worktree.py list --task-id dotfiles-tsk-notify-sweep`

## Latest handoff
_@ validation_

notify.py+sweep.py implementados: sla_expired (validation >4h) + blocked_too_long (blocked >24h, P0). Deliberadamente fora de escopo: auto-validacao real (precisa CAS Layer B, nao implementada - risco demasiado alto para apressar), loop_cap_exceeded/agent_session_stalled (sem produtor/session_id ainda), escalada ao 5o raised->notification.undeliverable. validate_herdr_contract.sh confirmado contra herdr 0.8.2 real nesta maquina. Testado em dir scratch isolado: deteccao, supressao por janela de escalonamento, self-heal sem duplicar no digest, --ack. Ver tasks/README.md para detalhe completo do que falta.
