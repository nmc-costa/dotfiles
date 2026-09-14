# 🔌 VS Code Copilot Reference

**Status:** Active
**Auto-Discovery:** Yes — GitHub Copilot Chat in VS Code auto-discovers
`.github/copilot-instructions.md` at the workspace root; no separate copy or config file
needed.

The previous version of this guide had you copy `.github/copilot-instructions.md` to a
second file, `.copilot-instructions.md`, at the repo root, and routed persona triggers through
a `config/harness-config.json` file. Neither is needed nor present in this repo: Copilot only
reads `.github/copilot-instructions.md`, and the "trigger mapping" config was confirmed
broken/aspirational by the source-repo audit (it pointed at persona filenames that don't
exist) and was not migrated here.

---

## How It Actually Works

1. `.github/copilot-instructions.md` (this repo's root) is auto-discovered by Copilot Chat —
   nothing to enable, no setup step.
2. `.github/instructions`, `.github/harnesses`, `.github/prompts`, `.github/automation` are
   symlinks to the equivalent `.agents/` directories, so Copilot and every other tool read the
   exact same files, not copies.
3. Persona/skill "triggers" (`@projectHITs`, etc.) are a convention used *inside this repo's
   own instruction text*, not a native GitHub Copilot feature — Copilot doesn't parse `@name`
   as a persona-loading directive on its own. If you want Copilot to actually behave
   differently per persona, put the routing logic directly in
   `.github/copilot-instructions.md` (e.g., "if the user says @projectHITs, read and follow
   `.agents/instructions/task-personas/projectHITs.md`").

## Key Files (in this repo)

- **Copilot entry point:** `.github/copilot-instructions.md`
- **Master Persona:** `.agents/instructions/base-personas/archi.md`
- **Task Personas:** `.agents/instructions/task-personas/`
- **Skills:** `.agents/skills/<name>/SKILL.md`

There is no `config/harness-config.json`, `REGISTRY.md`, or `/memories/session/` in this repo
— those belonged to the old `agentic_instructions` repo and were either confirmed
broken/aspirational or simply never migrated. Session-memory-style state (if you need it) is
handled by the `session-memory` skill under `.github/skills/session-memory/SKILL.md`
(`/memorize` and `/recall`), not by a hardcoded `/memories/session/` path.

## Operational Workflow

1. User mentions a persona/skill trigger (e.g., `@projectHITs`) in Copilot Chat.
2. `.github/copilot-instructions.md` (read automatically) instructs Copilot to load the
   matching file from `.agents/instructions/task-personas/`.
3. That task persona inherits from `.agents/instructions/base-personas/archi.md` (master).
4. Copilot executes the task following that persona's operational protocol.

## Troubleshooting

### Persona not loading?
- Check `.github/copilot-instructions.md` actually references the trigger you're using
- Verify the persona file exists at `.agents/instructions/task-personas/<Name>.md`
- Confirm you're not relying on `@name` being natively understood by Copilot — it needs to be
  spelled out in `copilot-instructions.md`

### Model Routing / Daily Optimization / Token Tracking / Mermaid rules
- See `.agents/instructions/workspace-config/model-routing.instructions.md`
- See `.agents/instructions/workspace-config/daily-optimization.instructions.md`
- See `.agents/instructions/workspace-config/token-tracking.instructions.md`
- See `.agents/instructions/workspace-config/mermaid.instructions.md`

## Common VS Code Tasks

| Task | Trigger | Example |
|------|-------|---------|
| Create project charter | `@projectHITs` | "@projectHITs create charter" |
| Generate slides | `@presentHITs` | "@presentHITs create slides" |
| Peer review code | `@reviewHITs` | "@reviewHITs peer review" |
| Create diagram | `@diagramHITs` | "@diagramHITs create diagram" |
| Update docs | `@documentHITs` | "@documentHITs update document" |
| Build mockup | `@mockupHITs` | "@mockupHITs create mockup" |
| Coordinate skills | `@architect` | "@architect coordinate" |

## Discovery

There is no central `REGISTRY.md` in this repo. Browse instead:

- Skills: [`.agents/skills/`](../skills/)
- Instructions: [`.agents/instructions/`](../instructions/)
- Harnesses: [`.agents/harnesses/`](.)

## Ready to Go

Nothing to install — `.github/copilot-instructions.md` is read automatically the moment this
repo (or a repo that symlinks to it) is opened in VS Code with GitHub Copilot Chat enabled.
