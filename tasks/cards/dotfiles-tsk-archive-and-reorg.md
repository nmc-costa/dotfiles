---
task_id: dotfiles-tsk-archive-and-reorg
title: "Archive done tasks out of live views + reorganize tasks/ directory tree so 'current' stays small (no infinite memory/context)"
project: dotfiles
phase: planning
created: "2026-09-21T21:39:17.544488+00:00"
touched: "2026-09-22T18:07:22.457365+00:00"
energy: ""
estimate: ""
deadline: ""
blocked_by: dotfiles-tsk-claim-protocol
origin: ""
---

# dotfiles-tsk-archive-and-reorg

Archive done tasks out of live views + reorganize tasks/ directory tree so 'current' stays small (no infinite memory/context)

## History
- 2026-09-22T18:07:22.457365+00:00: backlog -> planning (actor: nmc-costa/human) — Design verdict reached in conversation with the owner (2026-09-22), recording so it isn't lost before another session picks this up

Worktrees (this machine): [worktrees/dotfiles-tsk-archive-and-reorg.md](worktrees/dotfiles-tsk-archive-and-reorg.md) — `python3 ~/dotfiles/tasks/worktree.py list --task-id dotfiles-tsk-archive-and-reorg`

## Latest handoff
_@ planning_

Verdict: tasks/events.jsonl is ALREADY the full backup/history -- append-only, git-tracked, protected by the jsonl-union merge driver. No new backup mechanism is needed. kanban.md and tasks/cards/*.md are GENERATED VIEWS (rebuild_kanban/rebuild_cards, never hand-edited) -- the actual gap is that kanban.md's Done section has no trimming and grows forever (~30 entries already), which is view-layer noise, not a data-durability problem. Scope for this task: (1) kanban.md should show only a recent window of 'done' (e.g. last 7-30 days) plus everything still active; (2) older done items move to a separate GENERATED file, e.g. tasks/archive.md, still derived purely from events.jsonl (possibly split by month/quarter for browsability); (3) nothing is ever deleted from events.jsonl itself -- archiving is a view-layer change only, same 'generated, never hand-edited' discipline kanban.md/cards already follow. Directory reorg (the other half of this task's title) still open/undesigned -- whoever picks this up should look at tasks/ getting crowded (many .py scripts, plans/, evaluations/, demo/ at the top level) and propose a layout, same constraint: generated views regenerate correctly regardless of where their outputs live.
