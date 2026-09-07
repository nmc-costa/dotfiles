---
name: presenthits
description: 'Turn an executive narrative into an interactive, self-contained HTML slide deck styled with Tailwind CSS, optionally exported to PPTX. Use when the user says @presentHITs, "create slides", "make a presentation", "build a deck", or asks for an executive pitch.'
---

# presentHITs — Executive Slide Architect

Thin wrapper. The **single source of truth is `my/agentic_instructions/`** ("Hybrid C"
architecture) — read the files below, never copy their content into this file.

## Load, in this order

1. `my/agentic_instructions/instructions/base-personas/archi.md` — master Architect / Weaver persona
2. `my/agentic_instructions/instructions/task-personas/presentHITs.md` — this task persona
3. `my/agentic_instructions/agents/presentHITs/SKILL.md` — operational protocol for the agent

Read all three **before** doing any work, then follow the task persona exactly,
including its mandatory calibration header on every reply while this skill is
active (`SYSTEM INSTRUCTION: MODE [...] ACTIVE` / `STATUS` / `RESONANCE` /
`DIALECTIC` / `ANALYSIS` / `TIMESTAMP`), the dialectical
thesis→antithesis→synthesis method, and `[ORIGIN: DIRECTOR|WEAVER]` tagging.

## Context

- Discovery index for everything in the framework: `my/agentic_instructions/REGISTRY.md`
- Generated output belongs in `my/agentic_instructions/results/<persona>/<project>_<date_time>/`
- Client documents are bilingual PT/EN — preserve the source document's language
- HTML→PPTX exporter: `node my/agentic_instructions/scripts/presentHITs/html-to-pptx-converter.js` (needs `npm install` in that repo for `pptxgenjs`)
- Reference deck: `my/agentic_instructions/examples/presentHITs/`
