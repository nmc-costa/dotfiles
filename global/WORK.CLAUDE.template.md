# CLAUDE.md

Professional project context — template for local use.

## ⚠️ Instructions

This is a **template file**. To use it:

1. Copy this file to `~/Work/CLAUDE.md` (NOT in dotfiles repo):
   ```bash
   cp ~/dotfiles/global/WORK.CLAUDE.template.md ~/Work/CLAUDE.md
   ```

2. Edit `~/Work/CLAUDE.md` with company-specific rules (NOT this template):
   - Architecture patterns and conventions
   - Code style rules specific to your employer
   - Required env vars, setup, or authentication steps
   - Non-disclosure requirements or sensitive content

3. **Do NOT commit `~/Work/CLAUDE.md` to the dotfiles repo** — it contains proprietary business rules and should remain local and private.

## Template content

```markdown
# CLAUDE.md

Professional work context — [Company/Organization Name]

## Company/employer guidelines

[Add architecture patterns, code standards, business rules, etc. specific to this employment context]

## Code style & conventions

[Add language-specific preferences, naming conventions, etc.]

## Required setup

[Any special env vars, authentication, or machine setup needed]

## Sensitive notes

[Any internal conventions or non-disclosure items Claude should know about — this file never gets committed to the shared dotfiles repo]

---

See parent `~/CLAUDE.md` and `@~/dotfiles/AGENTS.md` for workspace-wide guidance.
```

---

**Source of this template:** `~/dotfiles/global/WORK.CLAUDE.template.md` (you copy and customize it — don't edit the template itself)
