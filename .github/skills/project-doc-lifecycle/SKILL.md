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
2. **Semantic Validation**:
   - Verify that the requirements, assumptions (pressupostos), and exclusions are scientifically accurate and align with the brief.
   - Ensure the structure adheres to bilingual (Portuguese/English) standards where requested.
3. **Auto-Correction**: Use the `replace_string_in_file` tool to fix formatting errors, improve clarity, or correct deviations directly in the markdown file. Do not just suggest changes—make them.
4. **Docx Conversion Execution**:
   - Locate the `.md` to `.docx` conversion helper scripts (usually located in `scripts/`, `my/agentic_instructions/scripts/projectHITs/`, or the active directory).
   - Use the `run_in_terminal` tool to immediately execute the script to generate the `.docx` file from the validated markdown.
5. **Final Report**: Call `task_complete` and present the user with a brief summary of auto-corrections applied and confirm that the final `.docx` has been successfully generated.