# 🔌 VS Code Copilot Reference

**Status:** Active
**Auto-Discovery:** Yes — GitHub Copilot in VS Code reads the root `AGENTS.md` natively
(`chat.useAgentsMdFile`, default `true`) and discovers skills in `.agents/skills/` natively
(`chat.agentSkillsLocations` default includes it). Both confirmed against the VS Code docs on
2026-09-25.

Until 2026-09-25 this repo used `.github/copilot-instructions.md` as Copilot's entry point, plus
`.github/{instructions,prompts,harnesses,automation,skills}` symlinks into `.agents/`. Once
Copilot adopted `AGENTS.md` that layer became redundant and was removed
(`dotfiles-tsk-github-to-agents`); only `.github/workflows/` remains, because GitHub Actions
runs workflows from nowhere else.

---

## How It Actually Works

1. The root `AGENTS.md` is auto-discovered by Copilot Chat. It points Copilot to
   `.agents/AGENT.md`, which holds the Copilot-specific session rules (`/compact` →
   `/memorize` → `/recall`, slash-command handling, model routing, daily optimization).
2. Skills: `.agents/skills/<name>/SKILL.md`, discovered natively — no mirror needed.
3. Prompt files (`.agents/prompts/`, e.g. `/chronicle`) and `*.instructions.md` files
   (`.agents/instructions/`) are **not** in VS Code's default search paths (those default to
   `.github/prompts` and `.github/instructions`). Add this to your VS Code **user**
   `settings.json` (not versioned here — this repo's `.vscode/settings.json` is gitignored and
   chezmoi-managed, see `docs/SECRETS.md`):

   ```jsonc
   "chat.promptFilesLocations": { ".agents/prompts": true },
   "chat.instructionsFilesLocations": { ".agents/instructions": true }
   ```

   (VS Code marks these settings as deprecated in favour of newer customization settings but
   still honours them; re-check the VS Code settings reference if they stop working.)
4. Persona/skill "triggers" (`@projectHITs`, etc.) are a convention used *inside this repo's
   own instruction text*, not a native GitHub Copilot feature — Copilot doesn't parse `@name`
   as a persona-loading directive on its own. If you want Copilot to actually behave
   differently per persona, put the routing logic directly in `.agents/AGENT.md` (e.g., "if
   the user says @projectHITs, read and follow
   `.agents/instructions/task-personas/projectHITs.md`").

## Key Files (in this repo)

- **Copilot entry point:** `AGENTS.md` → `.agents/AGENT.md`
- **Master Persona:** `.agents/instructions/base-personas/archi.md`
- **Task Personas:** `.agents/instructions/task-personas/`
- **Skills:** `.agents/skills/<name>/SKILL.md`

There is no `config/harness-config.json`, `REGISTRY.md`, or `/memories/session/` in this repo
— those belonged to the old `agentic_instructions` repo and were either confirmed
broken/aspirational or simply never migrated. Session-memory-style state (if you need it) is
handled by the `session-memory` skill under `.agents/skills/session-memory/SKILL.md`
(`/memorize` and `/recall`), not by a hardcoded `/memories/session/` path.

## Operational Workflow

1. User mentions a persona/skill trigger (e.g., `@projectHITs`) in Copilot Chat.
2. `AGENTS.md` (read automatically) → `.agents/AGENT.md` instructs Copilot to load the
   matching file from `.agents/instructions/task-personas/`.
3. That task persona inherits from `.agents/instructions/base-personas/archi.md` (master).
4. Copilot executes the task following that persona's operational protocol.

## Troubleshooting

### Persona not loading?
- Check `.agents/AGENT.md` actually references the trigger you're using
- Verify the persona file exists at `.agents/instructions/task-personas/<Name>.md`
- Confirm you're not relying on `@name` being natively understood by Copilot — it needs to be
  spelled out in `.agents/AGENT.md`

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

Nothing to install for the instructions — `AGENTS.md` is read automatically the moment this
repo (or a repo that symlinks to it) is opened in VS Code with GitHub Copilot Chat enabled.
