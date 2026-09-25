---
task_id: dotfiles-tsk-cross-harness-orchestra
title: "Skill /harness-orchestra: fan-out de tarefas entre harness+provider+model (ex: 1 Claude Code Opus + 1 Copilot CLI GPT-5), cada um no seu worktree, fecho via handoff md"
project: dotfiles
phase: review
created: "2026-09-24T15:42:27.359311+00:00"
touched: "2026-09-25T20:05:27.651853+00:00"
energy: deep
estimate: ""
deadline: ""
blocked_by: dotfiles-tsk-card-worktrees
origin: "pedido direto do owner 2026-09-24 via /task-brief (criado por claude em nome do owner): skill parecida com /plan-orchestra mas que distribui tarefas por DIFERENTES harnesses/providers/models. Invocável a partir de qualquer harness (\"quero 1 agente claude code opus e 1 agente github copilot gpt 5\"). Mecanismo: script Python determinístico cria um git worktree por agente (branch com prefixo do harness: claude/*, copilot/*, agy/*), lança cada harness com --model e o brief pré-carregado (estende tasks/dispatch.py, que hoje não aceita --model nem worktree), e o fecho/comunicação entre harnesses — que comunicam pouco entre si — faz-se por ficheiros md de handoff (tasks/HANDOFF.md / handoff notes do move_task.py) + events.jsonl, nunca IPC. Referências: tasks/dispatch.py, tasks/brief.py, tasks/harness-provider-model-index.md, .agents/skills/plan-orchestra, tasks/claim.py. Planeamento atribuído a Claude Code Opus em plan mode."
---

# dotfiles-tsk-cross-harness-orchestra

Skill /harness-orchestra: fan-out de tarefas entre harness+provider+model (ex: 1 Claude Code Opus + 1 Copilot CLI GPT-5), cada um no seu worktree, fecho via handoff md

## History
- 2026-09-24T15:42:27.395559+00:00: backlog -> planning (actor: nmc-costa/human) — owner pediu Opus em /plan para este card
- 2026-09-25T14:21:15.853612+00:00: planning -> blocked (actor: claude/agent) — prerequisite: needs the per-card worktree layer first (owner-approved plan, PR #78)
- 2026-09-25T14:29:44.664468+00:00: blocked -> in_progress (actor: nmc-costa/human) — owner: implementer=Claude Sonnet, agent-deck como L2, plano #81 merged
- 2026-09-25T20:05:27.651853+00:00: in_progress -> review (actor: claude/agent)

Worktrees (this machine): [worktrees/dotfiles-tsk-cross-harness-orchestra.md](worktrees/dotfiles-tsk-cross-harness-orchestra.md) — `python3 ~/dotfiles/tasks/worktree.py list --task-id dotfiles-tsk-cross-harness-orchestra`

## Latest handoff
_@ review_

Implemented plan §1-§3,§5: tasks/orchestra.py (launch/status/collect, dry-run default, agent-deck L2), brief.py orchestra contract flags, harness-orchestra skill+symlinks, docs (tasks/CHEATSHEET.md, harness-provider-model-index.md, tasks/README.md status, CLAUDE.md, root CHEATSHEET.md). Amended plan §2 to route handoffs through handoff.py (PR #84) per 2026-09-25 agreement. Checks: py_compile clean, Verification 1-2 pass (dry-run creates nothing + correct commands; copilot:gpt-5:x and agy:foo:x both fail listing real valid models), validate_dotfiles.sh 35/35. PR: https://github.com/nmc-costa/dotfiles/pull/88 (draft). Copilot cross-vendor review COULD NOT RUN: this account's Copilot CLI has no usable quota right now (gpt-5.5 'not available'; gpt-5.4/gpt-5-mini/gpt-5.3-codex/gpt-5.4-mini/mai-code-1.1-flash all 'no quota') - not substituted with a Claude review since the point was zero-Claude-token cross-vendor verification. Next: owner creates dotfiles-tsk-orchestra-smoke then run plan §Verification 3; also re-run the Copilot review once quota is available.
