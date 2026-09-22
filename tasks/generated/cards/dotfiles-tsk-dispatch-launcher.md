---
task_id: dotfiles-tsk-dispatch-launcher
title: "tsk dispatch: launch a session on a provider with the task brief pre-loaded (claude \"<p>\"/--bg, copilot -i, agy -i) - push side of cross-provider handoff, pull side is dotfiles-tsk-brief"
project: dotfiles
phase: done
created: "2026-09-21T13:47:05.603199+00:00"
touched: "2026-09-22T13:37:00.384542+00:00"
energy: ""
estimate: ""
deadline: ""
blocked_by: dotfiles-tsk-brief
origin: ""
---

# dotfiles-tsk-dispatch-launcher

tsk dispatch: launch a session on a provider with the task brief pre-loaded (claude "<p>"/--bg, copilot -i, agy -i) - push side of cross-provider handoff, pull side is dotfiles-tsk-brief

## History
- 2026-09-22T13:28:33.582591+00:00: backlog -> planning (actor: nmc-costa/human) — Claim formal via tasks/claim.py adquirido
- 2026-09-22T13:28:41.982128+00:00: planning -> in_progress (actor: nmc-costa/human)
- 2026-09-22T13:36:36.200302+00:00: in_progress -> review (actor: nmc-costa/human) — dispatch.py implementado (dry-run por defeito, --launch para executar), testado sem lancamento real
- 2026-09-22T13:36:53.492162+00:00: review -> validation (actor: nmc-costa/human)
- 2026-09-22T13:37:00.384542+00:00: validation -> done (actor: nmc-costa/human)

## Latest handoff
_@ validation_

dispatch.py: --task-id + --provider {claude,copilot,agy}, gera prompt via brief.py --prompt-only e lanca o binario certo. Dry-run por defeito (so imprime o comando), --launch para correr a serio. claude usa --bg nativo; copilot/agy sao destacados manualmente (sem flag de background confirmada) para tasks/.dispatch-logs/. NAO usa .agents/providers/adapters/*.sh (isso e routing de modelo LLM via proxy, nao lancamento de CLI harness - descoberta feita ao verificar, o veredito Opus original estava errado nisto). Testado: dry-run dos 3 providers (incl. quoting correto de titulo com apostrofo), task inexistente -> exit 1, binario em falta -> exit 1. NAO testado: --launch real, deliberado (lancaria uma sessao autonoma real num ambiente ja com muitas sessoes concorrentes).
