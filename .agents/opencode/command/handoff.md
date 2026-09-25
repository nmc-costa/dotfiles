---
description: Write a session handoff block any harness/model can resume (HANDOFF.md).
---

Use the `handoff` skill (loaded from `~/.agents/skills/handoff/SKILL.md`).

Arguments (optional handoff title or focus): $ARGUMENTS

Follow the skill's flow (`handoff.py new` → fill → `check` → `prompt`) and add
the new block on top of the repo's `HANDOFF.md` without editing older blocks.
