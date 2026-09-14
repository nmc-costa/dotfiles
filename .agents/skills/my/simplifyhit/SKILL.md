---
name: simplifyhit
description: 'Optimize a system-instruction / persona / SKILL.md file for agent efficiency — semantic density, explicit critical rules, named anti-patterns, token budget, optional persona injection. Use when writing or auditing agent instructions, personas, skills, or *.instructions.md files, or when the user says @simplifyHIT, "simplify these instructions", "optimize this prompt".'
---

# simplifyHIT — Instruction Optimization Framework

Thin wrapper. The **single source of truth is `my/agentic_instructions/`** ("Hybrid C"
architecture) — read the file below, never copy its content into this file.

## Load

- `my/agentic_instructions/skills/simplifyHIT/SKILL.md` (v1.2, ~3.5k token budget) — the full framework

Applies to `instructions/**/*.md`, `agents/**/SKILL.md`, `skills/**/SKILL.md`,
`*.instructions.md`, and the `.claude/skills/` wrappers in this workspace.

## Companion check

After rewriting instructions in `my/agentic_instructions`, run its linter and compliance suite:

```bash
cd my/agentic_instructions
python3 scripts/audit_instruction_health.py
pytest tests/agents/ -v
```
