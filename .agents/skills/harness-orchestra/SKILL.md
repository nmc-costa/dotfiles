---
name: harness-orchestra
description: >
  Fan a tasks/ card out across several harness+provider+model combos (e.g.
  "1 Claude Code Opus + 1 Copilot CLI GPT-5"), each in its own git
  worktree on a harness-prefixed branch, closing via handoff.py + events —
  never IPC. Use when the user asks to run a task on multiple
  harnesses/models at once, mentions /harness-orchestra, or asks to
  parallelize a tasks/ card across agents. Thin shell over
  tasks/orchestra.py — all real logic lives there (D14: script before
  rule), this skill only tells the agent how to parse the request, dry-run
  it, and act on the output.
---

# /harness-orchestra

Plan: `tasks/plans/cross-harness-orchestra.md`. Adopts `agent-deck` as the
L2 execution engine (`tasks/README.md`, 2026-09-18) — this skill and
`tasks/orchestra.py` are only the thin layer specific to `tasks/`.

## What to do

1. **Parse** the human's request ("1 claude opus + 1 copilot gpt 5") into
   `harness:model:subtask` specs. **Confirm with the human** any resolved
   model name that isn't exact (e.g. "gpt 5" → `gpt-5.5`?) before dry-running.
2. **Split into disjoint subtasks with explicit file ownership.** If the
   task doesn't actually split into independent slices, say so and don't
   fan out gratuitously — same rule as `plan-orchestra`.
3. **Dry-run** (the default — never pass `--launch` without the human
   confirming the printed plan first):
   ```bash
   python3 tasks/orchestra.py launch --task-id <task-id> \
     --agent 'claude:opus:<subtask 1>' \
     --agent 'copilot:gpt-5.5:<subtask 2>' \
     [--permissions auto|yolo]
   ```
   Read the printed branches/worktrees/commands/briefs back to the human.
4. **Launch** only after the human confirms, by re-running the same
   command with `--launch` appended. The lead then moves the card
   `planning -> in_progress` with `tasks/move_task.py`.
5. **Follow up** with `python3 tasks/orchestra.py status --run-id <run-id>`
   (read-only), `agent-deck` (fleet TUI), or `tmux attach`.
6. **Collect** once agents report done/blocked:
   ```bash
   python3 tasks/orchestra.py collect --run-id <run-id>
   ```
   This concatenates each agent's `HANDOFF.md` and releases their claims.
   Use its output as the `--handoff` for moving the parent card to
   `review` — the lead is the only one who moves the parent card.

## Rules

- `yolo` permissions only on the human's explicit request; `auto` is the
  default for every harness.
- **Never merge** — the human runs `agent-deck worktree finish --no-merge`
  or `cleanup` after merging the agents' PRs by hand.
- More than 4 agents needs the human's confirmation (cost, not just
  mechanics — see `tasks/plans/cross-harness-orchestra.md` §3).
- Never run `orchestra.py launch --launch` speculatively "to see what
  happens" — dry-run is silent about side effects for a reason: it's the
  human's go/no-go gate.

## Handoff format (one format repo-wide)

Each agent's handoff lives at
`tasks_root()/handoffs/<run_id>/<label>/HANDOFF.md`, created by the agent
itself with `.agents/skills/handoff/handoff.py new`, filled in, and
checked with `handoff.py check` before it signs off — see the contract
`tasks/brief.py --prompt-only` appends to each agent's prompt
(`orchestra_contract`) for the exact commands. `orchestra.py status` and
`collect` both shell out to `handoff.py check`/read `HANDOFF.md` directly
instead of re-parsing anything by hand.

## What NOT to do

- Don't hand-write the `agent-deck launch` command yourself — always go
  through `tasks/orchestra.py`, which builds it from the verified CLI
  facts in the plan and validates models first.
- Don't skip the dry-run step even for a "trivial" task — it's what lets
  the human catch a wrong branch name or a mis-resolved model before any
  worktree or agent-deck session exists.
- Don't treat `status`/`collect` as ways to nudge an agent along — they're
  read-only (plus claim release on `collect`), never a way to steer a
  running agent.
