---
mode: agent
---
Define the task to achieve, including specific requirements, constraints, and success criteria.

## Base agent instructions (apply across repositories)

The following is the canonical set of instructions that agents and automated workflows should follow for tasks in this organization. Treat these as the default behaviour unless a repo-specific prompt overrides them.

- Produce a clear, actionable task description that can be implemented by a developer or automated agent.
- For each task, include: functional requirements, non-functional constraints, measurable success criteria, a short contract (inputs/outputs/error modes), assumptions when details are missing, and 3–5 likely edge cases with handling guidance.
- Prefer minimal, low-risk changes. When code changes are required, also add or update tests (happy path + ≥1 edge case) and a short README or verification steps explaining how to run tests locally.
- Avoid network calls or exfiltrating secrets. If secrets are required, document how to stub or provide them via environment variables.
- Detect environment mismatches (language/runtime versions) and output exact requirements and setup instructions (virtualenv, pyenv, nvm, etc.).
- When editing files, follow repository style and conventions. Make the smallest clear edits needed to satisfy the task. If under-specified, make up to two reasonable assumptions and state them explicitly.
- Provide exact verification commands and expected outputs so the task can be validated automatically or manually.
- If implementing changes, run the repository's build/test/lint steps and report results. If failures occur outside the changes, report them and avoid force-fixing unrelated code.

Use this file as the base prompt for automated agents and as a template when creating task/issue descriptions in `.github/ISSUE_TEMPLATE` or PR templates.