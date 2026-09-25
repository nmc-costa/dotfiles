---
description: Mine this machine's interaction history for skill-improvement proposals (propose-only, evidence-cited).
---

Use the `chronicle` skill (loaded from `~/.agents/skills/chronicle/SKILL.md`).

Arguments (optional focus, e.g. "this week", "pr-finish usage"): $ARGUMENTS

Run the miner read-only, rank candidates by evidence, and propose changes as
`chronicle/*` branches with cited evidence. Human-only merge; never apply
changes directly.
