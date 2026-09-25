---
task_id: dotfiles-tsk-simplifyhit-ressonance-typo
title: "Fix typo: simplifyhit/SKILL.md escreve RESSONANCE em vez de RESONANCE no bloco de header"
project: dotfiles
phase: review
created: "2026-09-24T22:02:20.701720+00:00"
touched: "2026-09-25T14:25:14.041652+00:00"
energy: mechanical
estimate: ""
deadline: ""
blocked_by: ""
origin: "Achado pelo agente Opus (Plan) ao investigar dotfiles-tsk-agent-output-tldr-format (2026-09-24), sinalizado pelo owner como algo que precisa de atenção própria. .agents/skills/simplifyhit/SKILL.md tem o campo do header escrito RESSONANCE (typo) em vez de RESONANCE, divergindo de todos os outros ficheiros com o mesmo bloco. Fix mecânico de uma linha, independente do resto do plano do Output Frame — não precisa de esperar pela aprovação de Q1/Q2 em tasks/plans/agent-output-tldr-format.md. Relacionado: dotfiles-tsk-header-persona-drift (mesma família de achado, mas este é o único que é claramente um bug e não só uma divergência de formato)."
---

# dotfiles-tsk-simplifyhit-ressonance-typo

Fix typo: simplifyhit/SKILL.md escreve RESSONANCE em vez de RESONANCE no bloco de header

## History
- 2026-09-25T14:25:13.566239+00:00: backlog -> planning (actor: claude/agent) — folded into Output Frame rollout (plan §6)
- 2026-09-25T14:25:13.804382+00:00: planning -> in_progress (actor: claude/agent) — implemented on claude/output-frame-impl
- 2026-09-25T14:25:14.041652+00:00: in_progress -> review (actor: claude/agent) — fix in commit d284445, draft PR #83

Worktrees (this machine): [worktrees/dotfiles-tsk-simplifyhit-ressonance-typo.md](worktrees/dotfiles-tsk-simplifyhit-ressonance-typo.md) — `python3 ~/dotfiles/tasks/worktree.py list --task-id dotfiles-tsk-simplifyhit-ressonance-typo`

## Latest handoff
_@ review_

Corrigido no commit d284445 (branch claude/output-frame-impl, draft PR #83, parte do rollout de dotfiles-tsk-agent-output-tldr-format). Fica em review até o PR #83 fazer merge; depois: move_task.py --to-phase validation, e --to-phase done --expect-last-event-id <id do move anterior>, sempre --actor-kind agent --actor-id claude.
