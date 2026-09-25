---
task_id: dotfiles-tsk-header-persona-drift
title: "Header/persona RESONANCE drift: ~15 ficheiros com cópias divergentes do bloco de header (achado pelo plano do Output Frame)"
project: dotfiles
phase: review
created: "2026-09-24T22:02:12.013031+00:00"
touched: "2026-09-25T14:25:13.381687+00:00"
energy: mechanical
estimate: ""
deadline: ""
blocked_by: ""
origin: "Achado pelo agente Opus (Plan) ao investigar dotfiles-tsk-agent-output-tldr-format (2026-09-24), sinalizado pelo owner como algo que precisa de atenção própria. O header \"Biofeedback (RESONANCE)\" já existe copiado e divergente em ~15 ficheiros: SKILL.md de archi/diagramhits/mockuphits/projecthits/presenthits/documenthits/reviewhits (5 campos cada), os 6 ficheiros de .agents/instructions/task-personas/*.md (cada um com o seu próprio nome de MODE), _templates/agent-template.md, _templates/agent-README.md, .agents/workflows/architect_html_sciml.md, e simplifyhit/SKILL.md (que tem o typo RESSONANCE — ver dotfiles-tsk-simplifyhit-ressonance-typo). O master persona .agents/instructions/base-personas/archi.md tem 6 campos (adiciona DIALECTIC) e usa blockquote em vez de code block, divergindo também dos outros. Isto é um problema de qualidade/hygiene independente de o plano do Output Frame (tasks/plans/agent-output-tldr-format.md) ser aprovado ou não — as cópias já estão dessincronizadas hoje. O plano do Output Frame já descreve a correção como sua fase S3 (dedup para um header canónico com referência de 3 linhas por ficheiro) — este card serve para dar visibilidade própria ao achado, não duplica o trabalho: ao implementar S3 do plano, fechar este card também. Relacionado: dotfiles-tsk-agent-output-tldr-format, tasks/plans/agent-output-tldr-format.md §0.1 e §6 (S3)."
---

# dotfiles-tsk-header-persona-drift

Header/persona RESONANCE drift: ~15 ficheiros com cópias divergentes do bloco de header (achado pelo plano do Output Frame)

## History
- 2026-09-25T14:25:12.956103+00:00: backlog -> planning (actor: claude/agent) — folded into Output Frame rollout (plan §6)
- 2026-09-25T14:25:13.179103+00:00: planning -> in_progress (actor: claude/agent) — implemented on claude/output-frame-impl
- 2026-09-25T14:25:13.381687+00:00: in_progress -> review (actor: claude/agent) — fix in commit d284445, draft PR #83

Worktrees (this machine): [worktrees/dotfiles-tsk-header-persona-drift.md](worktrees/dotfiles-tsk-header-persona-drift.md) — `python3 ~/dotfiles/tasks/worktree.py list --task-id dotfiles-tsk-header-persona-drift`

## Latest handoff
_@ review_

Corrigido no commit d284445 (branch claude/output-frame-impl, draft PR #83, parte do rollout de dotfiles-tsk-agent-output-tldr-format). Fica em review até o PR #83 fazer merge; depois: move_task.py --to-phase validation, e --to-phase done --expect-last-event-id <id do move anterior>, sempre --actor-kind agent --actor-id claude.
