---
task_id: dotfiles-tsk-cross-harness-orchestra
title: "Skill /harness-orchestra: fan-out de tarefas entre harness+provider+model (ex: 1 Claude Code Opus + 1 Copilot CLI GPT-5), cada um no seu worktree, fecho via handoff md"
project: dotfiles
phase: planning
created: "2026-09-24T15:42:27.359311+00:00"
touched: "2026-09-24T15:42:27.395559+00:00"
energy: deep
estimate: ""
deadline: ""
blocked_by: ""
origin: "pedido direto do owner 2026-09-24 via /task-brief (criado por claude em nome do owner): skill parecida com /plan-orchestra mas que distribui tarefas por DIFERENTES harnesses/providers/models. Invocável a partir de qualquer harness (\"quero 1 agente claude code opus e 1 agente github copilot gpt 5\"). Mecanismo: script Python determinístico cria um git worktree por agente (branch com prefixo do harness: claude/*, copilot/*, agy/*), lança cada harness com --model e o brief pré-carregado (estende tasks/dispatch.py, que hoje não aceita --model nem worktree), e o fecho/comunicação entre harnesses — que comunicam pouco entre si — faz-se por ficheiros md de handoff (tasks/HANDOFF.md / handoff notes do move_task.py) + events.jsonl, nunca IPC. Referências: tasks/dispatch.py, tasks/brief.py, tasks/harness-provider-model-index.md, .agents/skills/plan-orchestra, tasks/claim.py. Planeamento atribuído a Claude Code Opus em plan mode."
---

# dotfiles-tsk-cross-harness-orchestra

Skill /harness-orchestra: fan-out de tarefas entre harness+provider+model (ex: 1 Claude Code Opus + 1 Copilot CLI GPT-5), cada um no seu worktree, fecho via handoff md

## History
- 2026-09-24T15:42:27.395559+00:00: backlog -> planning (actor: nmc-costa/human) — owner pediu Opus em /plan para este card
