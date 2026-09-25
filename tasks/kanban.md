## Backlog
- [ ] dotfiles-tsk-cpx-copilot cpx wrapper for Copilot CLI (its own sessionStart hook is broken)
- [ ] dotfiles-tsk-hook-antigravity Antigravity hook (inherited hook mechanism)
- [ ] dotfiles-tsk-graph-dependency-edges Add blocked_by dependency edges to rebuild_graph.py's flowchart (needs blocked_by as a list, not prose)
- [ ] dotfiles-tsk-agent-os-pr2-pr7 Agent-OS unification: PR2-PR7 (docs/AGENT_OS_UNIFICATION_PLAN.md)
- [ ] dotfiles-tsk-archive-agentic-instructions Archive agentic_instructions repo on GitHub
- [ ] dotfiles-tsk-antigravity-reverify Re-verify Antigravitys startup file-discovery from inside ~/dotfiles
- [ ] dotfiles-tsk-agile-workspace-see Agile Workspace roadmap step 1 (See): agtop + Claude Code Langfuse/OTel observability
- [ ] dotfiles-tsk-agile-workspace-limit Agile Workspace roadmap step 3 (Limit): per-machine limit profiles
- [ ] dotfiles-tsk-agile-workspace-schedule Agile Workspace roadmap step 4 (Schedule): jobs/*.yaml manifest + systemd timers
- [ ] dotfiles-tsk-autolaunch-test dotfiles-tsk-autolaunch-test: Verify dispatch auto-launch across providers
- [ ] dotfiles-tsk-sweep-validate Test and validate sweep.py end-to-end (never run on this machine yet)
- [ ] dotfiles-tsk-card-priority Add priority levels (P0-P3) to tasks/ cards
- [ ] dotfiles-tsk-recurring-cards Recurring cards: spawn new task instances on a cadence
- [ ] dotfiles-tsk-spike-herdr-commander Spike: evaluate herdr-commander (lurepos) as herdr palette for tasks/ commands
- [ ] dotfiles-tsk-tree-tidy-core [P1] Tree-tidy core: root check in validate_workspace_standards.py + allowlist reconcile, tree_tidy.py scope/map/metrics, root-guard PreToolUse hook, 3 AGENTS.md lines, delete docs/directory_tree.md
- [ ] dotfiles-tsk-tree-tidy-skill [P1] Rung 2: /tree-tidy skill (map, research, plan, /simplify + /simplifyhit, gate, draft PR) + tree_tidy.py gate
- [ ] dotfiles-tsk-tree-tidy-recurring [P2] Rung 3: recurring card template - run /tree-tidy on next repo in rotation every 14 days
- [ ] dotfiles-tsk-tree-tidy-tournament [P1] Rung 4a: sandboxed haiku/sonnet worktree tournament, opus judge vs baseline, draft PR (manual runs first)
- [ ] dotfiles-tsk-tree-tidy-schedule [P2] Rung 4b: weekly tree-tidy tournament job in .agents/automation/jobs/ manifest
- [ ] dotfiles-tsk-dispatch-interactive-fix dispatch.py: copilot/agy lançados com -i e stdin=/dev/null (TUI sem terminal) — encaminhar via agent-deck launch
- [ ] dotfiles-tsk-card-worktrees tasks/worktree.py: one git worktree per (harness, card), visible from tasks/cards/, same for Claude/Copilot/Gemini/agy/Codex
- [ ] dotfiles-tsk-orchestra-smoke Smoke test real do tasks/orchestra.py --launch (plan §Verification 3): 1 agente claude + 1 agente copilot
- [ ] dotfiles-tsk-worktree-model-suffix tasks/worktree.py v2: optional [-<model>] suffix in path/branch when a harness has >1 agent on the same card
- [ ] dotfiles-tsk-dispatch-quota-check dispatch.py: post-launch liveness probe + record provider quota status/reset time

## Planning
- [ ] dotfiles-tsk-archive-and-reorg Archive done tasks out of live views + reorganize tasks/ directory tree so 'current' stays small (no infinite memory/context)
- [ ] dotfiles-tsk-agent-autonomy-charter Agent autonomy charter: shared system prompt for all harnesses with no-ask domains + TL;DR-only escalation
- [ ] dotfiles-tsk-task-plan dotfiles-tsk-task-plan

## In Progress
- [ ] dotfiles-tsk-researcher-radar researcher-radar family: omarchy-radar + agents-radar (headless daily digests, human approves everything)

## Review
- [ ] dotfiles-tsk-gh-path-recursion Fix infinite recursion in ~/.local/bin/gh wrapper (duplicate PATH entry)
- [ ] dotfiles-tsk-task-brief-assistant Upgrade /task-brief into a full tasks/ management assistant
- [ ] worknotes-siac-colab-portfolio-report [HIGH PRIORITY] SIAC CoLAB (COMPETE2030 transferencia, ~1.2M EUR/24m): planear portfolio de demonstradores + report com tabela para o CEO (Work/notes/projects)
- [ ] dotfiles-tsk-cross-harness-orchestra Skill /harness-orchestra: fan-out de tarefas entre harness+provider+model (ex: 1 Claude Code Opus + 1 Copilot CLI GPT-5), cada um no seu worktree, fecho via handoff md
- [ ] dotfiles-tsk-agent-output-tldr-format Formato padrão de fecho para planos e outputs longos de agentes: TL;DR + índice, com opção visual/diagrama e possível artifact
- [ ] dotfiles-tsk-header-persona-drift Header/persona RESONANCE drift: ~15 ficheiros com cópias divergentes do bloco de header (achado pelo plano do Output Frame)
- [ ] dotfiles-tsk-simplifyhit-ressonance-typo Fix typo: simplifyhit/SKILL.md escreve RESSONANCE em vez de RESONANCE no bloco de header
- [ ] dotfiles-tsk-mermaid-instructions-footer-conflict mermaid.instructions.md (Regras 1, 2 e 5) entra em conflito com qualquer diagrama Mermaid devolvido inline (ex. footer do Output Frame)
- [ ] dotfiles-tsk-chronicle-daily-improve Chronicle daily background improve: timer, headless opencode run, gated auto-merge PRs
- [ ] dotfiles-tsk-radar-opencode-backend Radar family: commit skills+automation+units, omarchy-radar backend routing (opencode default)

## Validation
- [ ] dotfiles-tsk-skill-gauntlet-prompting Skill: gauntlet prompting (desenhar e criar skill .agents/skills/gauntlet-prompting)

## Done
- [x] dotfiles-repo-hygiene-dotfiles Abrir PR: claude/repo-hygiene-dotfiles
- [x] dotfiles-workspace-standards-schema Abrir PR: claude/workspace-standards-schema
- [x] dotfiles-todo-continuation-and-notes-backlog Abrir PR: claude/todo-continuation-and-notes-backlog
- [x] architect-repo-hygiene-architect Abrir PR: claude/repo-hygiene-architect
- [x] architect-workspace-standards-schema Abrir PR: claude/workspace-standards-schema
- [x] architect-env-leak-fix Abrir PR: claude/env-leak-fix
- [x] notes-repo-hygiene-notes Abrir PR: claude/repo-hygiene-notes
- [x] notes-ideas-review-fixes Abrir PR: claude/ideas-review-fixes
- [x] notes-workspace-standards-schema Abrir PR: claude/workspace-standards-schema
- [x] worknotes-repo-hygiene-worknotes Abrir PR: claude/repo-hygiene-worknotes
- [x] worknotes-workspace-standards-schema Abrir PR: claude/workspace-standards-schema
- [x] dotfiles-tsk-spike-agent-deck Spike: install Agent Deck, confirm it detects Claude Code + Copilot CLI sessions side by side
- [x] dotfiles-tsk-spike-cas-concurrency Spike: confirm git-ref compare-and-swap claiming survives concurrent writers
- [x] dotfiles-tsk-spike-workflow-model Spike: confirm a Workflow script with a real per-phase model override runs as expected
- [x] dotfiles-tsk-spike-herdr-popup Spike: confirm a trivial herdr plugin can open a popup (herdr plugin pane open)
- [x] dotfiles-tsk-tuiboard-install Install tuiboard for real (not a scratch install), point it at tasks/kanban.md
- [x] dotfiles-tsk-roadmap-graph rebuild_graph.py: project events.jsonl into a Mermaid roadmap (tasks/roadmap.md + .mmd) - phases + per-project grouping + done timeline, no dependency edges yet
- [x] dotfiles-tsk-writepath-unification lifecycle.py + LEGAL_TRANSITIONS + append() as the single writer, with CAS (Layer A)
- [x] dotfiles-tsk-notify-sweep notify.py + sweep.py - the notification producer side
- [x] dotfiles-tsk-brief brief.py - heartbeat + inbox consumer
- [x] dotfiles-tsk-hook-claude-code Claude Code SessionStart hook + versioned settings.json fragment
- [x] dotfiles-tsk-task-brief-skill /task-brief skill - thin shell over brief.py
- [x] dotfiles-tsk-systemd-units ensure-tsk-sweep.sh + systemd units, following the existing ensure-*.sh convention
- [x] dotfiles-tsk-cards-frontmatter L1: markdown+YAML-frontmatter card per task (rebuild_cards.py, generated view, never hand-edited)
- [x] dotfiles-tsk-dispatch-launcher tsk dispatch: launch a session on a provider with the task brief pre-loaded (claude "<p>"/--bg, copilot -i, agy -i) - push side of cross-provider handoff, pull side is dotfiles-tsk-brief
- [x] dotfiles-tsk-tasks-root-resolver tasks_root() resolver: one canonical write path for events.jsonl, the CAS lock and every rebuild_*.py (fixes 4 divergent copies + 1 orphaned event)
- [x] dotfiles-tsk-claim-protocol L2: claim protocol in a separate claims.jsonl -- locked conditional appends, closed role vocabulary, atomic preemption, human preempts swarm
- [x] dotfiles-tsk-jsonl-merge-driver Custom git merge driver (merge=union or equivalent) for tasks/*.jsonl so a conflict resolution can never silently drop an append-only line
- [x] dotfiles-handoff-standardization Adopt HANDOFF.md convention (global index + per-repo/subsystem), rename tasks/handoff.md
- [x] dotfiles-tsk-harness-provider-model-index Build a validated harness x provider x model orchestration index
- [x] dotfiles-tsk-chezmoi-config-drift Corrigir ~/.config/chezmoi/chezmoi.toml pos-PR1 (destDir=$HOME, sourceDir=home/) + limpar ~/dotfiles/.dtx-providers/ + corrigir PROVIDERS.md e render-litellm-config.sh
- [x] dotfiles-tsk-verify-setup-skill-gaps Investigate 2 findings from first real run of setup-dotfiles/verify_setup.sh: _templates flagged missing from synced skills dirs, chezmoi status failure
- [x] dotfiles-tsk-agent-actor-safety [HIGH PRIORITY] Agents must sign tasks/ events as actor-kind=agent for their own writes, and must not run unguarded git ops on the shared tasks/events.jsonl working tree
- [x] dotfiles-tsk-spike-herdr-commander-build Spike (hands-on): patch herdr-commander to overlay placement, wire real .vscode/tasks.json, verify picker end-to-end
- [x] dotfiles-tsk-github-to-agents Migrar .github/ para .agents/ e apagar .github (Copilot já lê AGENTS.md)
- [x] dotfiles-tsk-chronicle-skill-layer Chronicle-like skill layer: mine interactions into skills/instructions, resume-after-timeout, PR-finish, skill chaining + chat autocomplete
- [x] dotfiles-tsk-chronicle-d4-d6 Chronicle slice D4-D6: /pr-finish, /chronicle miner, footer+questionario conventions
- [x] dotfiles-tsk-chronicle-d7 Chronicle D7: opencode custom commands + tui.prompt.append chain bridge

## Blocked

## Deferred
