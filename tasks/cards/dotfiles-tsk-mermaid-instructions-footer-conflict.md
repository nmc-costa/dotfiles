---
task_id: dotfiles-tsk-mermaid-instructions-footer-conflict
title: "mermaid.instructions.md (Regras 1, 2 e 5) entra em conflito com qualquer diagrama Mermaid devolvido inline (ex. footer do Output Frame)"
project: dotfiles
phase: backlog
created: "2026-09-24T22:02:31.608308+00:00"
touched: "2026-09-24T22:02:31.608308+00:00"
energy: mechanical
estimate: ""
deadline: ""
blocked_by: ""
origin: "Achado pelo agente Opus (Plan) ao investigar dotfiles-tsk-agent-output-tldr-format (2026-09-24), sinalizado pelo owner como algo que precisa de atenção própria. .agents/instructions/workspace-config/mermaid.instructions.md, Regras 1/2/5, obriga: escrever diagramas para ficheiros .mmd, chamar sempre a tool mermaid-diagram-validator, e nunca devolver Mermaid não validado. Essas tools só existem no VS Code Copilot, e um diagrama de footer/resumo (não pedido como entregável) não é o mesmo caso de uso que a regra tinha em mente — hoje já é ambíguo se um Mermaid inline numa resposta viola a regra. O plano do Output Frame (tasks/plans/agent-output-tldr-format.md §3) já propõe um carve-out (\"diagramas que o utilizador pede como entregável\" fica sujeito à regra; diagramas de footer ficam isentos de .mmd/validador mas continuam limitados a um subset seguro de Mermaid, e continuam a chamar o validador quando existe). Este card é para o carve-out em si ficar visível e não se perder dentro da PR maior do Output Frame — pode e deve ser resolvido junto com essa PR (S1), não precisa de decisão adicional do owner além da aprovação geral do plano. Relacionado: dotfiles-tsk-agent-output-tldr-format, tasks/plans/agent-output-tldr-format.md §3 e §6 (S1)."
---

# dotfiles-tsk-mermaid-instructions-footer-conflict

mermaid.instructions.md (Regras 1, 2 e 5) entra em conflito com qualquer diagrama Mermaid devolvido inline (ex. footer do Output Frame)

## History
- (no phase_changed events yet — still in its original created phase)
