---
task_id: dotfiles-tsk-agent-output-tldr-format
title: "Formato padrão de fecho para planos e outputs longos de agentes: TL;DR + índice, com opção visual/diagrama e possível artifact"
project: dotfiles
phase: in_progress
created: "2026-09-24T21:31:29.981641+00:00"
touched: "2026-09-24T22:05:16.470496+00:00"
energy: deep
estimate: ""
deadline: ""
blocked_by: ""
origin: "pedido direto do owner 2026-09-24 via /task-brief (criado por claude em nome do owner): owner quer que todos os planos e outputs longos de agentes terminem com uma secção TL;DR que resuma o conteúdo + um índice, para não ter de percorrer o chat todo para cima e para baixo — só lê o detalhe atrás se precisar. Ideias levantadas pelo owner, ainda por decidir/desenhar: (1) o resumo pode ser mais visual do que texto — um diagrama que sintetiza a big picture da informação; (2) alternativa mais radical: outputs longos passam a ser sempre um Artifact (em vez de texto solto no chat), o que pode também poupar tokens ao evitar reler/rescrever texto longo inline; (3) este comportamento devia ser consistente sempre que se fala com agentes, não só em planos formais. Por decidir na fase de plano: quando aplicar isto (todo output longo vs. só planos/entregáveis?), texto vs. diagrama vs. artifact como formato do resumo, e como isto se cruza com dotfiles-tsk-agent-autonomy-charter (TL;DR-only na escalação humano-agente — mesma ideia de TL;DR mas para outro momento: fim de output vs. pedir validação). Ver skills artifact-design/artifact-diagramming/dataviz já disponíveis como building blocks."
---

# dotfiles-tsk-agent-output-tldr-format

Formato padrão de fecho para planos e outputs longos de agentes: TL;DR + índice, com opção visual/diagrama e possível artifact

## History
- 2026-09-24T21:43:16.274864+00:00: backlog -> planning (actor: claude/agent) — Owner refinou o pedido via chat 2026-09-24: header e footer de metadados, não só TL;DR solto.
- 2026-09-24T22:05:16.470496+00:00: planning -> in_progress (actor: nmc-costa/human) — Owner aprovou Q1/Q2 do plano; plano fica aprovado como escrito, próximo passo é a implementação S1-S6.

## Latest handoff
_@ planning_

Requisitos refinados pelo owner (2026-09-24, em PT no chat, não em events.jsonl anteriores):

HEADER: igual ao padrão do skill archi (ver .agents/skills/archi/SKILL.md secção 'Biofeedback Header (RESONANCE)' — bloco SYSTEM INSTRUCTION/STATUS/RESONANCE/ANALYSIS/TIMESTAMP). Mas generalizado: hoje só o archi tem isto; o owner quer que TODOS os agentes/skills tenham um header equivalente. Isto implica que o header deixa de ser algo definido só no SKILL.md do archi e passa a ser um system prompt central em AGENTS.md (o guia que todos os harnesses leem), para que qualquer agente em qualquer skill o herde automaticamente.

FOOTER (dois níveis):
1. Genérico — sempre que um output é 'grande' (por definir o threshold: nº de linhas? de tokens? presença de secções?), acrescentar um resumo no fim. Analogia do owner: 'é quase como se tivesse um /compact sempre no final só para ter em hit-size' — ou seja, o footer funciona como uma compactação/TL;DR do que acabou de ser dito, não uma introdução do que vai vir.
2. Específico para planos e outputs longos — footer indexado (índice das secções/passos) COM um diagrama rápido de entender o fluxo do plano (ex: mermaid, estilo do 'Workflow' já usado no diagramhits/archi), para o owner conseguir ver a big picture sem ter de ler o detalhe todo, e só descer ao detalhe se precisar.

Ideia em aberto ainda não decidida (do pedido original que criou o card): outputs longos passarem a ser sempre publicados como Artifact em vez de texto solto no chat, para poupar tokens/scroll — a validar se isto é compatível ou concorrente com o header/footer inline (um Artifact pode ter o seu próprio header/footer dentro da página, não precisa necessariamente do padrão de chat).

Relacionado (mesma família de ideia, gatilho diferente): dotfiles-tsk-agent-autonomy-charter é TL;DR só no momento de ESCALAÇÃO humano-agente (pedir validação); este card é TL;DR no FIM de qualquer output longo/plano, independente de haver escalação. Reconciliar os dois na fase de plano — provavelmente o mesmo mecanismo de footer serve para ambos.

Próximo passo: um agente Opus em modo Plan deve desenhar a proposta concreta (texto exato do header/footer, onde entra no AGENTS.md, threshold de 'grande', formato do diagrama, decisão sobre Artifact) — ainda não implementar.
