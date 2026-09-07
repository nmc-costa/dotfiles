---
name: projecthits
description: 'Mirror any template (DOCX, LaTeX, Markdown, PDF, TXT) into an editable source file, auto-fill it from a project brief, mark gaps with [TODO], and compile the final document. Use for project charters, work packages (WP1, WP2), project briefs, INCM deliverables, or when the user says @projectHITs, "create charter", "new project", "mirror template", "fill template", "adapt template".'
---

# projectHITs — Charter / Mirror Architect (v4)

Thin wrapper. The **single source of truth is `my/agentic_instructions/`** ("Hybrid C"
architecture) — read the files below, never copy their content into this file.

## Load, in this order

1. `my/agentic_instructions/instructions/base-personas/archi.md` — master Architect / Weaver persona
2. `my/agentic_instructions/instructions/task-personas/projectHITs.md` — this task persona
3. `my/agentic_instructions/agents/projectHITs/SKILL.md` — operational protocol for the agent

Read all three **before** doing any work, then follow the task persona exactly,
including its mandatory calibration header on every reply while this skill is
active (`SYSTEM INSTRUCTION: MODE [...] ACTIVE` / `STATUS` / `RESONANCE` /
`DIALECTIC` / `ANALYSIS` / `TIMESTAMP`), the dialectical
thesis→antithesis→synthesis method, and `[ORIGIN: DIRECTOR|WEAVER]` tagging.

## Context

- Discovery index for everything in the framework: `my/agentic_instructions/REGISTRY.md`
- Generated output belongs in `my/agentic_instructions/results/<persona>/<project>_<date_time>/`
- Client documents are bilingual PT/EN — preserve the source document's language
- v4 pipeline scripts: `my/agentic_instructions/scripts/projectHITs/v4/` (`orchestrate.py`, `auto_filler.py`, `compiler.py`, `completion_checker.py`, `mirror_generator.py`, `template_analyzer.py`)
- Example data + template: `my/agentic_instructions/examples/projectHITs/`
