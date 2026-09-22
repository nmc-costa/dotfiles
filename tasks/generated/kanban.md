## Backlog
- [ ] dotfiles-tsk-cpx-copilot cpx wrapper for Copilot CLI (its own sessionStart hook is broken)
- [ ] dotfiles-tsk-hook-antigravity Antigravity hook (inherited hook mechanism)
- [ ] dotfiles-tsk-systemd-units ensure-tsk-sweep.sh + systemd units, following the existing ensure-*.sh convention
- [ ] dotfiles-tsk-graph-dependency-edges Add blocked_by dependency edges to rebuild_graph.py's flowchart (needs blocked_by as a list, not prose)
- [ ] dotfiles-tsk-agent-os-pr2-pr7 Agent-OS unification: PR2-PR7 (docs/AGENT_OS_UNIFICATION_PLAN.md)
- [ ] dotfiles-tsk-archive-agentic-instructions Archive agentic_instructions repo on GitHub
- [ ] dotfiles-tsk-antigravity-reverify Re-verify Antigravitys startup file-discovery from inside ~/dotfiles
- [ ] dotfiles-tsk-agile-workspace-see Agile Workspace roadmap step 1 (See): agtop + Claude Code Langfuse/OTel observability
- [ ] dotfiles-tsk-agile-workspace-limit Agile Workspace roadmap step 3 (Limit): per-machine limit profiles
- [ ] dotfiles-tsk-agile-workspace-schedule Agile Workspace roadmap step 4 (Schedule): jobs/*.yaml manifest + systemd timers
- [ ] dotfiles-tsk-autolaunch-test dotfiles-tsk-autolaunch-test: Verify dispatch auto-launch across providers

## Planning
- [ ] dotfiles-tsk-archive-and-reorg Archive done tasks out of live views + reorganize tasks/ directory tree so 'current' stays small (no infinite memory/context)

## In Progress

## Review
- [ ] dotfiles-tsk-gh-path-recursion Fix infinite recursion in ~/.local/bin/gh wrapper (duplicate PATH entry)

## Validation

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
- [x] dotfiles-tsk-cards-frontmatter L1: markdown+YAML-frontmatter card per task (rebuild_cards.py, generated view, never hand-edited)
- [x] dotfiles-tsk-dispatch-launcher tsk dispatch: launch a session on a provider with the task brief pre-loaded (claude "<p>"/--bg, copilot -i, agy -i) - push side of cross-provider handoff, pull side is dotfiles-tsk-brief
- [x] dotfiles-tsk-tasks-root-resolver tasks_root() resolver: one canonical write path for events.jsonl, the CAS lock and every rebuild_*.py (fixes 4 divergent copies + 1 orphaned event)
- [x] dotfiles-tsk-claim-protocol L2: claim protocol in a separate claims.jsonl -- locked conditional appends, closed role vocabulary, atomic preemption, human preempts swarm
- [x] dotfiles-tsk-jsonl-merge-driver Custom git merge driver (merge=union or equivalent) for tasks/*.jsonl so a conflict resolution can never silently drop an append-only line
- [x] dotfiles-handoff-standardization Adopt HANDOFF.md convention (global index + per-repo/subsystem), rename tasks/handoff.md

## Blocked

## Deferred
