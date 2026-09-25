---
task_id: dotfiles-tsk-claim-protocol
title: "L2: claim protocol in a separate claims.jsonl -- locked conditional appends, closed role vocabulary, atomic preemption, human preempts swarm"
project: dotfiles
phase: done
created: "2026-09-21T18:41:13.821889+00:00"
touched: "2026-09-21T21:50:54.180071+00:00"
energy: ""
estimate: ""
deadline: ""
blocked_by: dotfiles-tsk-tasks-root-resolver
origin: ""
---

# dotfiles-tsk-claim-protocol

L2: claim protocol in a separate claims.jsonl -- locked conditional appends, closed role vocabulary, atomic preemption, human preempts swarm

## History
- 2026-09-21T21:45:32.559305+00:00: backlog -> planning (actor: nmc-costa/human) — pre-requisito tasks-root-resolver concluido, avancar
- 2026-09-21T21:45:35.799793+00:00: planning -> in_progress (actor: nmc-costa/human)
- 2026-09-21T21:50:47.196740+00:00: in_progress -> review (actor: nmc-costa/human) — PR #49 aberta, teste real de corrida a 5 vias confirma zero TOCTOU, todos os casos de autorizacao testados
- 2026-09-21T21:50:50.844031+00:00: review -> validation (actor: nmc-costa/human) — revisto: PR #49 fundida, testes de concorrencia real e autorizacao confirmados
- 2026-09-21T21:50:54.180071+00:00: validation -> done (actor: nmc-costa/human)

Worktrees (this machine): [worktrees/dotfiles-tsk-claim-protocol.md](worktrees/dotfiles-tsk-claim-protocol.md) — `python3 ~/dotfiles/tasks/worktree.py list --task-id dotfiles-tsk-claim-protocol`
