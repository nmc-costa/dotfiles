---
task_id: dotfiles-tsk-agent-output-tldr-format
title: "Formato padrão de fecho para planos e outputs longos de agentes: TL;DR + índice, com opção visual/diagrama e possível artifact"
project: dotfiles
phase: review
created: "2026-09-24T21:31:29.981641+00:00"
touched: "2026-09-25T14:25:12.728405+00:00"
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
- 2026-09-25T14:25:12.728405+00:00: in_progress -> review (actor: claude/agent) — S1-S4 implemented, draft PR #83 open (stacked on plan PR #80)

Worktrees (this machine): [worktrees/dotfiles-tsk-agent-output-tldr-format.md](worktrees/dotfiles-tsk-agent-output-tldr-format.md) — `python3 ~/dotfiles/tasks/worktree.py list --task-id dotfiles-tsk-agent-output-tldr-format`

## Latest handoff
_@ review_

Implementação S1-S4 em draft PR #83 (branch claude/output-frame-impl, stacked em PR #80 — merge #80 primeiro ou juntos). Commits: S1 3b4aa5f (output-frame.instructions.md + carve-out mermaid), S2 ea56fa3 (bloco OUTPUT-FRAME:CORE nos 8 ficheiros), S3 d284445 (17 personas/skills -> referência de 3 linhas + typo RESSONANCE), S4 151866c (scripts/check_core_blocks.sh + manifest + CI). validate_dotfiles.sh 37/0. Próximo passo (owner): rever PR #83 (secção 'Judgment calls'), correr o checklist S5 nos 4 harnesses (corpo do PR + CHEATSHEET §4), depois merge. S6 (Stop hook) só se compliance fraca após 2 semanas.
