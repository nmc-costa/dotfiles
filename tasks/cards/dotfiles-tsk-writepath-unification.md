---
task_id: dotfiles-tsk-writepath-unification
title: "lifecycle.py + LEGAL_TRANSITIONS + append() as the single writer, with CAS (Layer A)"
project: dotfiles
phase: done
created: "2026-09-21T13:25:25.308856+00:00"
touched: "2026-09-21T13:49:40.952832+00:00"
energy: ""
estimate: ""
deadline: ""
blocked_by: ""
origin: ""
---

# dotfiles-tsk-writepath-unification

lifecycle.py + LEGAL_TRANSITIONS + append() as the single writer, with CAS (Layer A)

## History
- 2026-09-21T13:25:38.147579+00:00: backlog -> planning (actor: nmc-costa/human) — Aprovado para arrancar imediatamente - item critico do plano de paralelizacao
- 2026-09-21T13:39:28.296622+00:00: planning -> in_progress (actor: nmc-costa/human) — A implementar lifecycle.py + CAS Layer A
- 2026-09-21T13:39:35.898647+00:00: in_progress -> review (actor: nmc-costa/human) — PR aberta, testes de regressao e concorrencia passaram
- 2026-09-21T13:49:34.677337+00:00: review -> validation (actor: nmc-costa/human) — PR #32 fundida em main
- 2026-09-21T13:49:40.952832+00:00: validation -> done (actor: nmc-costa/human)

Worktrees (this machine): [worktrees/dotfiles-tsk-writepath-unification.md](worktrees/dotfiles-tsk-writepath-unification.md) — `python3 ~/dotfiles/tasks/worktree.py list --task-id dotfiles-tsk-writepath-unification`

## Latest handoff
_@ review_

lifecycle.py criado com PHASES/LEGAL_TRANSITIONS/CAS Layer A. FACT_TYPES e dedup_key() deliberadamente adiados (dependem de policy.yaml/sweep.py, Wave 2). Verificado: demo sem regressao, transicao ilegal -> exit 2, CAS sem --expect-last-event-id -> exit 2, CAS com id errado -> exit 3, corrida a 10 processos -> 1 vence. Falta so o merge para desbloquear dotfiles-tsk-notify-sweep, dotfiles-tsk-brief, dotfiles-tsk-graph-dependency-edges, dotfiles-tsk-cards-frontmatter.
