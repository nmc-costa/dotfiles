---
task_id: dotfiles-tsk-skill-gauntlet-prompting
title: "Skill: gauntlet prompting (desenhar e criar skill .agents/skills/gauntlet-prompting)"
project: dotfiles
phase: validation
created: "2026-09-24T11:19:09.455211+00:00"
touched: "2026-09-25T22:30:29.746384+00:00"
energy: deep
estimate: ""
deadline: ""
blocked_by: ""
origin: pedido direto do owner 2026-09-24 via /task-brief; plano delegado a agente Opus (Plan)
---

# dotfiles-tsk-skill-gauntlet-prompting

Skill: gauntlet prompting (desenhar e criar skill .agents/skills/gauntlet-prompting)

## History
- 2026-09-24T11:19:09.597347+00:00: backlog -> planning (actor: claude/agent) — owner pediu plano por agente Opus
- 2026-09-25T14:27:03.717149+00:00: planning -> in_progress (actor: claude/agent) — owner respondeu: 3 rondas/peca, sempre hand-off, PR e merge
- 2026-09-25T14:33:56.078214+00:00: in_progress -> review (actor: claude/agent) — PR #86 opened
- 2026-09-25T14:34:02.628032+00:00: review -> validation (actor: claude/agent) — PR #86 merged (aa9f3f016ceda688119b035ac3cf2011d5e2887d), owner authorized PR+merge

Worktrees (this machine): [worktrees/dotfiles-tsk-skill-gauntlet-prompting.md](worktrees/dotfiles-tsk-skill-gauntlet-prompting.md) — `python3 ~/dotfiles/tasks/worktree.py list --task-id dotfiles-tsk-skill-gauntlet-prompting`

## Latest handoff
_@ validation_

Skill em .agents/skills/gauntlet-prompting/ (merged em main). 15 testes unitarios + validate_dotfiles.sh 35/35 OK. Falta para done: (1) ./sync.sh para copiar para ~/.agents (o prompt gerado aponta para ~/.agents/skills/gauntlet-prompting/scripts/gauntlet_ledger.py); (2) evals comportamentais E1-E5 de tasks/plans/skill-gauntlet-prompting.md numa sessao nova, sobretudo E4 end-to-end; (3) confirmar em Copilot CLI/agy.
