---
task_id: dotfiles-tsk-task-brief-assistant
title: Upgrade /task-brief into a full tasks/ management assistant
project: dotfiles
phase: planning
created: "2026-09-23T11:52:17.210731+00:00"
touched: "2026-09-23T12:00:35.578840+00:00"
energy: ""
estimate: ""
deadline: ""
blocked_by: dotfiles-tsk-harness-provider-model-index
origin: ""
---

# dotfiles-tsk-task-brief-assistant

Upgrade /task-brief into a full tasks/ management assistant

## History
- 2026-09-23T12:00:35.578840+00:00: backlog -> planning (actor: nmc-costa/human)

## Latest handoff
_@ planning_

Design recorded (not executed yet -- stays blocked_by dotfiles-tsk-harness-provider-model-index, which is in_progress on branch claude/harness-provider-model-index). Plan: extend .agents/skills/task-brief/SKILL.md (confirmed real path) so that after brief.py's existing heartbeat+pending-facts check, it also (a) prints a board-shape summary reusing lifecycle.project() -- counts per phase, no new script needed, (b) once the human names a task, reads tasks/harness-provider-model-index.md and suggests a harness+model, (c) optionally flags repos under ~/Projects/~/Work with no matching project value in any open task -- lowest-confidence, scoped as nice-to-have. tasks/brief.py itself stays unchanged (D14: script before rule) -- the suggestion logic is simple enough to live as skill instructions reading a static table, only becomes a script if a first pass shows it needs real parsing. Pick this up once the index file is merged.
