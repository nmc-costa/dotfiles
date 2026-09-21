---
name: task-brief
description: >
  Cross-provider session-startup briefing for the tasks/ orchestration system
  in dotfiles. Use at the start of a session working in ~/dotfiles (or any repo
  with its own tasks/ directory) to check whether anything needs the human's
  attention before picking new work, or when the user explicitly asks for a
  briefing, asks "what needs me", "what's pending", or invokes /task-brief.
  Thin shell over tasks/brief.py — all real logic lives there (D14: script
  before rule), this skill only tells the agent how to run it and act on the
  output.
---

# /task-brief

Cross-provider startup briefing described in
`tasks/plans/human-in-the-loop-notifications.md` §5. Not `/kanban-orchestra`
— deliberately avoids colliding semantically with `plan-orchestra` (fan-out
multi-agent planning, the opposite of this: a single deterministic check).

## What to do

1. Run `python3 tasks/brief.py` from the repo root (or `cd` into it first).
   This is deterministic Python — never re-derive its logic by hand, never
   guess at pending facts by reading `tasks/kanban.md` yourself instead.
2. If it prints a stale/missing heartbeat banner, surface that to the human
   first, verbatim — it means `tasks/sweep.py` hasn't run recently and the
   facts below it may be incomplete or stale.
3. If it lists pending facts, summarize them for the human (task, fact type,
   whether it's P0) and ask what they want to do about each — **never**
   silently act on a fact yourself (move a task, ack it) without the human
   directing that. Once they do, translate their answer into the matching
   `tasks/move_task.py`/`tasks/notify.py --ack` command yourself.
4. If it prints "Nothing pending. What do you want to work on?" — ask
   exactly that, in your own words, and wait. Do **not** pick a task
   yourself and start working on it unprompted (§5: "nunca escolhe trabalho
   sozinha" — this mirrors `tasks/README.md`'s "the owner is the director"
   rule: a human tells the agent what to do, the agent moves the card).
5. Once the human names a task (or you're dispatching a *different* session
   to work one), you can generate that task's ready-to-paste brief with:
   ```bash
   python3 tasks/brief.py --prompt-only --task-id <task-id>
   ```
   This is the same contract `dotfiles-tsk-dispatch-launcher` uses to launch
   a session on another CLI provider (Claude Code, Copilot CLI, Antigravity)
   with the task pre-loaded — see `tasks/handoff.md`'s cross-provider
   dispatch verdict for why no daemon is needed for this.

## What NOT to do

- Don't read `tasks/events.jsonl` or `tasks/kanban.md` directly to compute
  "what's pending" — `brief.py` already does that correctly, including the
  P0-first ordering and the un-acked-fact filtering. Reimplementing it here
  risks drifting from the real logic.
- Don't treat this skill as a task picker. It reports; the human (or
  whoever they delegate to) decides.
- Don't skip the heartbeat check even if you're in a hurry — a dead sweep
  silently showing "nothing pending" is exactly the failure mode
  `tasks/plans/human-in-the-loop-notifications.md` §4's heartbeat exists to
  catch.

## Not yet wired up automatically

No hook triggers this skill on session start yet — `dotfiles-tsk-hook-
claude-code` (a real `SessionStart` hook), `dotfiles-tsk-cpx-copilot` (a
wrapper, since Copilot CLI's own `sessionStart` hook is confirmed broken),
and `dotfiles-tsk-hook-antigravity` are still backlog. Until one of those
lands, invoke this skill manually or via `/task-brief`.
