---
task_id: dotfiles-tsk-spike-agent-deck
title: "Spike: install Agent Deck, confirm it detects Claude Code + Copilot CLI sessions side by side"
project: dotfiles
phase: done
created: "2026-09-21T13:25:25.096210+00:00"
touched: "2026-09-21T17:33:42.286135+00:00"
energy: ""
estimate: ""
deadline: ""
blocked_by: ""
origin: ""
---

# dotfiles-tsk-spike-agent-deck

Spike: install Agent Deck, confirm it detects Claude Code + Copilot CLI sessions side by side

## History
- 2026-09-21T17:25:15.169968+00:00: backlog -> planning (actor: team-agent-deck/agent) — spike: verificar releases GitHub antes de go install
- 2026-09-21T17:25:18.641168+00:00: planning -> in_progress (actor: team-agent-deck/agent)
- 2026-09-21T17:33:33.214622+00:00: in_progress -> review (actor: team-agent-deck/agent) — PASS: instalacao limpa (binario pre-compilado, sem Go), deteccao lado a lado confirmada via agent-deck status -v com sessoes reais Claude Code + Copilot CLI
- 2026-09-21T17:33:37.856729+00:00: review -> validation (actor: nmc-costa/human) — revisto manualmente pelo diretor: README consistente, instalacao verificada, achado de assimetria Claude/Copilot confirmado com evidencia
- 2026-09-21T17:33:42.286135+00:00: validation -> done (actor: nmc-costa/human)

Worktrees (this machine): [worktrees/dotfiles-tsk-spike-agent-deck.md](worktrees/dotfiles-tsk-spike-agent-deck.md) — `python3 ~/dotfiles/tasks/worktree.py list --task-id dotfiles-tsk-spike-agent-deck`

## Latest handoff
_@ review_

Repo confirmado real (935 estrelas, releases com binarios linux/amd64 e checksums). Instalado sem arrastar Go. Testado com sessoes tmux reais: deteccao completa para Claude Code ([awaiting menu choice]), superficial para Copilot (so '-', consistente com o README oficial do agent-deck que documenta Copilot como 'Organization, launch' sem status detection). Veredito sobre sobreposicao com herdr: complementares, nao redundantes -- agent-deck vai mais fundo em orquestracao/execucao (fork, worktree mgmt, MCP por sessao, bridges). Screenshot da TUI nao obtido (bloqueio do sandbox tmux aninhado, nao do agent-deck) -- documentado como 'Not yet tested', repetir numa shell limpa antes de integrar a camada L3.
