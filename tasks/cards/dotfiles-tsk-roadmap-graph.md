---
task_id: dotfiles-tsk-roadmap-graph
title: "rebuild_graph.py: project events.jsonl into a Mermaid roadmap (tasks/roadmap.md + .mmd) - phases + per-project grouping + done timeline, no dependency edges yet"
project: dotfiles
phase: done
created: "2026-09-21T13:25:25.274091+00:00"
touched: "2026-09-21T17:34:33.694246+00:00"
energy: ""
estimate: ""
deadline: ""
blocked_by: ""
origin: ""
---

# dotfiles-tsk-roadmap-graph

rebuild_graph.py: project events.jsonl into a Mermaid roadmap (tasks/roadmap.md + .mmd) - phases + per-project grouping + done timeline, no dependency edges yet

## History
- 2026-09-21T17:26:03.469761+00:00: backlog -> planning (actor: team-roadmap-graph/agent)
- 2026-09-21T17:26:06.636393+00:00: planning -> in_progress (actor: team-roadmap-graph/agent)
- 2026-09-21T17:34:28.651570+00:00: in_progress -> review (actor: team-roadmap-graph/agent) — PASS: rebuild_graph.py corre sem erro, roadmap.md/.mmd validados com mermaid-cli real (mmdc), flowchart+timeline corretos, sem arestas de dependencia (fora de ambito, como pedido)
- 2026-09-21T17:34:33.642716+00:00: review -> validation (actor: nmc-costa/human) — revisto manualmente pelo diretor: corri rebuild_graph.py eu mesmo, output correto e idempotente
- 2026-09-21T17:34:33.694246+00:00: validation -> done (actor: nmc-costa/human)

## Latest handoff
_@ review_

Padrao de rebuild_kanban.py/rebuild_metrics.py seguido. subgraph por payload.project (4 projetos reais: dotfiles, architect, notes, Work/notes -- usou o valor real do payload, nao inventou 'worknotes'). classDef por fase (8 fases de lifecycle.PHASES). timeline separada agregando so eventos task.phase_changed com phase=done. roadmap.mmd contem so o flowchart (nao o timeline) -- decisao consciente por causa da convencao 'um diagrama por .mmd' do repo; timeline fica so no .md. Validado com npx @mermaid-js/mermaid-cli real, SVGs renderizados sem erros. Re-corri eu mesmo o script (idempotente, exit 0, 27 tasks/4 projects/58-70 events dependendo do momento).
