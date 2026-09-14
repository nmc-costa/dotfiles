---
name: project-doc-lifecycle
description: 'Validate a formal project document (INCM Project Charter, WP1.md, work plan) against its project brief, auto-correct it in place, then compile it to .docx with the helper scripts. Use when the user asks to validate/check/finalize a charter or work package, or to convert a markdown deliverable to Word.'
---

# Project Doc Lifecycle (INCM)

This skill automates the validation, refinement, and compilation of formal project documents (such as INCM Project Charters and Work Plans).

## When to use this skill

Invoke this skill automatically when the user asks to:
- Validate a markdown document (e.g., `WP1.md`).
- Check document semantics against a project brief.
- Convert a markdown file to `.docx`.
- "Finalize" a project charter or document.

## Autonomous Workflow Steps

When triggered, follow these steps autonomously without stopping to ask the user, unless a critical blocking error occurs:

1. **Information Gathering**: Read the target `.md` document and the original project brief (if available in context or history).
2. **Semantic Validation** (not just structural):
   - Verify that the requirements, assumptions (pressupostos), and exclusions are scientifically accurate and align with the brief.
   - Ensure the structure adheres to bilingual (Portuguese/English) standards where the document uses one — preserve the source document's language, don't force a translation.
3. **Auto-Correction**: Fix formatting errors, improve clarity, or correct deviations **directly in the file** — don't just suggest changes, make them.
4. **Docx Conversion Execution**: Locate the `.md` → `.docx` conversion helper scripts (usually in the project's own `scripts/`, or the projectHITs v4 pipeline at
   `.agents/skills/projecthits/scripts/v4/`), then execute the script to generate the `.docx` file from the validated markdown. Never hand-roll the DOCX format yourself.
5. **Final Report**: Present the user with a brief summary of auto-corrections applied and confirm that the final `.docx` has been successfully generated.

Pairs with the `projecthits` skill, which produces these documents in the first place.

## Harness Tool Mapping

This workflow was originally written for GitHub Copilot's agent-mode tool names. Different
harnesses expose different tool names for the same actions — map accordingly:

| Action | GitHub Copilot (VS Code) | Claude Code |
|--------|---------------------------|--------------|
| Edit a file in place | `replace_string_in_file` | `Edit` tool |
| Run the docx conversion script | `run_in_terminal` | `Bash` tool |
| Report completion | `task_complete` | Just report the summary in your reply |
