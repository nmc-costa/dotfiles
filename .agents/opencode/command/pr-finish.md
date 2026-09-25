---
description: Preflight the current card's PR (CI, conflicts, merge commands; propose-only by default).
---

Use the `pr-finish` skill (loaded from `~/.agents/skills/pr-finish/SKILL.md`).

Arguments (optional): $ARGUMENTS

Resolve the card id from the current git branch (`opencode/<card-id>` worktree
naming) or from the arguments if given. Default to the propose-only preflight
(`pr-finish.py --task-id <card> --pr <n>`): check CI, conflicts and card
phase, then print the exact merge commands. Never pass `--auto` unless the
arguments explicitly ask for auto-merge.
