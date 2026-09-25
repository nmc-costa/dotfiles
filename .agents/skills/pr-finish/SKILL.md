---
name: pr-finish
description: >
  Preflight and finish the PR of a tasks/ card in ~/dotfiles: resolves the
  PR from the card's branch, checks CI/conflicts/card phase, and prints the
  exact finish commands (propose-only). Use when the user says "finish the
  PR", "pr-finish", "is the PR ready", "wrap up the card's PR", or asks to
  auto-merge a card PR. Thin shell over pr-finish.py — all real logic lives
  there.
---

# /pr-finish

Thin shell over `pr-finish.py` (same directory; D14: script before rule).
Default is **propose-only**: merges happen by human direction — this skill
prints the commands, it does not merge. `--auto` is the single exception,
and only under the owner's 2026-09-25 decision (see below).

## What to do

1. Run it from the card's worktree (the branch is the PR head):
   ```bash
   python3 .agents/skills/pr-finish/pr-finish.py --task-id <task-id>
   ```
   It resolves the PR from the current branch (or pass `--pr <number>`),
   then reports: PR state, `mergeable`, `mergeStateStatus`, CI rollup, and
   the card's phase — plus the finish commands.
2. **Read the report to the owner keyword-compact** (output-frame): one
   status line + the command list. Don't re-derive what the script already
   checked.
3. **`--auto`** (owner asks for auto-merge, or a `Next:` chain says so):
   ```bash
   python3 .agents/skills/pr-finish/pr-finish.py --task-id <id> --auto
   ```
   The script enables `gh pr merge --auto --squash` **only** when all
   gates pass right now: card still in `review`, CI green (no pending, no
   failed checks), GitHub reports mergeable + `CLEAN`/`HAS_HOOKS`. Any
   failed gate → it refuses and prints the hand-run commands (exit 2).
4. Relay the exit honestly: `0` = proposal printed or auto-merge enabled;
   `2` = `--auto` refused (read the gate list); `1` = input/environment
   error.

## Why the gates are what they are

- **Card in `validation` or beyond → never `--auto`.** Reaching validation
  via the loop cap makes it human-required (2026-09-18 policy). The
  loop-cap producer (`review.judge_failed`) doesn't exist yet
  (tasks/README.md), so the card's phase is the conservative proxy: `--auto`
  only fires from `review`.
- **No branch deletion, no force.** Branch cleanup stays with
  `tasks/worktree.py prune` / human hands.
- **Idempotent by card+PR**: merged PR or already-enabled auto-merge are
  reported and exit 0 without acting again.

## What NOT to do

- Don't run `gh pr merge` by hand to "help" — that's a merge without the
  gates; merges happen by human direction.
- Don't pass `--auto` when the owner only asked "is it ready?" — that is a
  propose-only question.
- Don't retry `--auto` after a gate refusal without changing something
  (fix CI, rebase, or the owner explicitly directing it).

## Chains

- `→ /task-brief` — after a merge lands and the card moves to
  `validation`/`done`, check what's next for the owner.
