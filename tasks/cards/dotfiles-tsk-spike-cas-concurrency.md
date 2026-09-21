---
task_id: dotfiles-tsk-spike-cas-concurrency
title: "Spike: confirm git-ref compare-and-swap claiming survives concurrent writers"
project: dotfiles
phase: done
created: "2026-09-21T13:25:25.130377+00:00"
touched: "2026-09-21T13:42:12.628263+00:00"
energy: ""
estimate: ""
deadline: ""
blocked_by: ""
origin: ""
---

# dotfiles-tsk-spike-cas-concurrency

Spike: confirm git-ref compare-and-swap claiming survives concurrent writers

## History
- 2026-09-21T13:41:50.453511+00:00: backlog -> planning (actor: nmc-costa/human) — Verificado como parte de PR #32 (write-path unification), nao precisa de sessao dedicada
- 2026-09-21T13:41:54.992385+00:00: planning -> in_progress (actor: nmc-costa/human)
- 2026-09-21T13:42:00.765174+00:00: in_progress -> review (actor: nmc-costa/human) — Confirmado empiricamente durante o T3: flock CAS a 10 processos concorrentes -> 1 vence, 9 abortam
- 2026-09-21T13:42:05.852470+00:00: review -> validation (actor: nmc-costa/human)
- 2026-09-21T13:42:12.628263+00:00: validation -> done (actor: nmc-costa/human)

## Latest handoff
_@ done_

Confirmado dentro de PR #32 (dotfiles-tsk-writepath-unification): flock(LOCK_EX) sobre tasks/.events.lock, 10 processos a competir pelo mesmo --expect-last-event-id -> exatamente 1 vence (exit 0), 9 abortam com ConcurrentModificationError (exit 3). Metodo em tasks/README.md, secao Orchestration architecture -> Status.
