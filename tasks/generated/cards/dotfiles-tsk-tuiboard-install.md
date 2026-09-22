---
task_id: dotfiles-tsk-tuiboard-install
title: "Install tuiboard for real (not a scratch install), point it at tasks/kanban.md"
project: dotfiles
phase: done
created: "2026-09-21T13:25:25.235106+00:00"
touched: "2026-09-21T17:34:20.722122+00:00"
energy: ""
estimate: ""
deadline: ""
blocked_by: ""
origin: ""
---

# dotfiles-tsk-tuiboard-install

Install tuiboard for real (not a scratch install), point it at tasks/kanban.md

## History
- 2026-09-21T17:25:51.174356+00:00: backlog -> planning (actor: team-tuiboard/agent)
- 2026-09-21T17:25:54.811775+00:00: planning -> in_progress (actor: team-tuiboard/agent)
- 2026-09-21T17:34:15.192898+00:00: in_progress -> review (actor: team-tuiboard/agent) — PASS: bun+tuiboard instalados a serio (nao scratch), config a apontar para o tasks/kanban.md real do checkout principal, render confirmado via tmux capture-pane
- 2026-09-21T17:34:20.664933+00:00: review -> validation (actor: nmc-costa/human) — revisto manualmente pelo diretor: config real confirmada, captura tmux mostra board real
- 2026-09-21T17:34:20.722122+00:00: validation -> done (actor: nmc-costa/human)

## Latest handoff
_@ review_

mise use -g bun@latest (bun 1.4.2). bun install -g github:NazzarenoGiannelli/tuiboard, binario em ~/.cache/.bun/bin/tuiboard. Config em ~/.config/tuiboard/config.yaml apontando para /home/nbugz/dotfiles/tasks/kanban.md (caminho absoluto do repo principal, nao a copia transitoria da worktree). Captura tmux confirma renderizacao real (15 open, 13 done, 7 cols) e painel Agents(live) a detetar sessoes Claude Code reais desta maquina. Nota: instalacao bun/tuiboard e so-de-maquina, nao aparece no diff git -- so o README de avaliacao e a captura ficam versionados. tuiboard --help/--version nao sao flags reconhecidas, lancam o TUI interativo -- usar sempre q ou tmux kill-session.
