---
name: project-doc-lifecycle
description: 'Validate a formal project document (INCM Project Charter, WP1.md, work plan) against its project brief, auto-correct it in place, then compile it to .docx with the helper scripts. Use when the user asks to validate/check/finalize a charter or work package, or to convert a markdown deliverable to Word.'
---

# project-doc-lifecycle (INCM)

Thin wrapper. The **single source of truth is `my/agentic_instructions/`** ("Hybrid C"
architecture) — read the file below, never copy its content into this file.

## Load

- `my/agentic_instructions/skills/project-doc-lifecycle/SKILL.md` — the autonomous workflow

## Translating it to Claude Code

That file was written for VS Code Copilot and names Copilot tools. Map them:

| It says | Use instead |
|---------|-------------|
| `replace_string_in_file` | the `Edit` tool |
| `run_in_terminal` | the `Bash` tool |
| `task_complete` | just report the summary in your reply |

## Workflow

1. Read the target `.md` and the original project brief.
2. **Semantic** validation (not just structural): requirements, pressupostos, and
   exclusions must be accurate and aligned with the brief; keep the bilingual
   PT/EN structure where the document uses one.
3. Fix problems **directly in the file** — don't just list suggestions.
4. Compile with the md→docx helper scripts in `scripts/` or
   `my/agentic_instructions/scripts/projectHITs/`; never hand-roll the DOCX format.
5. Report the corrections applied and confirm the `.docx` was generated.

Pairs with `/projecthits`, which produces these documents in the first place.
