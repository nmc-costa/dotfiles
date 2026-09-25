---
task_id: dotfiles-tsk-spike-herdr-popup
title: "Spike: confirm a trivial herdr plugin can open a popup (herdr plugin pane open)"
project: dotfiles
phase: done
created: "2026-09-21T13:25:25.201461+00:00"
touched: "2026-09-21T17:34:08.522290+00:00"
energy: ""
estimate: ""
deadline: ""
blocked_by: ""
origin: ""
---

# dotfiles-tsk-spike-herdr-popup

Spike: confirm a trivial herdr plugin can open a popup (herdr plugin pane open)

## History
- 2026-09-21T17:25:38.399045+00:00: backlog -> planning (actor: team-herdr-popup/agent)
- 2026-09-21T17:25:38.434743+00:00: planning -> in_progress (actor: team-herdr-popup/agent)
- 2026-09-21T17:34:03.235946+00:00: in_progress -> review (actor: team-herdr-popup/agent) — PARCIAL: --placement popup nao existe no herdr 0.8.2 (falha silenciosa, processo orfao); --placement overlay e o equivalente real que funciona e foi confirmado (pane visivel, focado, listado)
- 2026-09-21T17:34:08.463089+00:00: review -> validation (actor: nmc-costa/human) — revisto manualmente pelo diretor: README excelente, achado bem evidenciado (server log, herdr pane list, ps), cleanup confirmado
- 2026-09-21T17:34:08.522290+00:00: validation -> done (actor: nmc-costa/human)

Worktrees (this machine): [worktrees/dotfiles-tsk-spike-herdr-popup.md](worktrees/dotfiles-tsk-spike-herdr-popup.md) — `python3 ~/dotfiles/tasks/worktree.py list --task-id dotfiles-tsk-spike-herdr-popup`

## Latest handoff
_@ review_

Comando exato do card (--placement popup) foi corrido honestamente -- retorna ok mas produz processo orfao nunca anexado a um workspace (confirmado via herdr pane list vazio, log vazio, server log mostrando spawn sem attach). --placement overlay confirmado como o real equivalente funcional (pane_id w1:p3E, focused:true, apareceu em herdr pane list). Cleanup feito: unlink do plugin confirmado (removed:true), processo orfao morto. Recomendacao registada no README para qualquer plugin futuro usar overlay, nao popup.
