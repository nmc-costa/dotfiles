# 🔌 Antigravity Reference

**Status:** template — not yet verified. This file exists to close a
gap found 2026-09-16 (a direct Antigravity diagnostic run by the workspace
owner found zero startup wiring to this repo's task tracker), but nobody
has yet confirmed how Antigravity actually discovers context files in a
repo (a project-context file it auto-loads by convention, an extension/
skill directory, or neither). **Don't assume any of the mechanics below
are real until someone verifies them against the actual tool** — follow
the same discipline as `.agents/harnesses/gemini.md`, which flagged the
same kind of uncertainty rather than inventing a plausible-sounding setup.

---

## 📌 Session Startup (the concrete fix for the 2026-09-16 gap)

Until Antigravity has a real auto-loaded entrypoint wired to this repo,
the working substitute is a manual first message, same pattern as
`CHEATSHEET.md` §7's Claude Code kickoff prompt:

> Read `~/dotfiles/CLAUDE.md`, `~/dotfiles/CHEATSHEET.md`, and
> `~/dotfiles/tasks/board.md` + `tasks/README.md`. Build a todo list from
> `CHEATSHEET.md` §4 (persistent TODO) and the task tracker, and continue
> from there.

Paste this as the first message of a new Antigravity session in this repo
until real auto-discovery is confirmed and wired below.

---

## Workspace Configuration (Global)

Regardless of harness, these rules apply repo-wide, defined under
`.agents/instructions/workspace-config/`:

- **Model Routing** — `.agents/instructions/workspace-config/model-routing.instructions.md`
- **Daily Optimization** (chronicle workflow) — `.agents/instructions/workspace-config/daily-optimization.instructions.md`
- **Token Tracking** — `.agents/instructions/workspace-config/token-tracking.instructions.md`
- **Mermaid Diagrams** — `.agents/instructions/workspace-config/mermaid.instructions.md`

## Task-Specific Skills

```
Trigger          | Skill          | Purpose
─────────────────┼────────────────┼─────────────────────────────
@projectHITs     | projecthits    | Project charters + WPs
@presentHITs     | presenthits    | Executive presentations
@reviewHITs      | reviewhits     | Peer review & critique
@diagramHITs     | diagramhits    | Mermaid diagrams
@documentHITs    | documenthits   | Documentation synthesis
@mockupHITs      | mockuphits     | Interactive prototypes
@architect       | archi          | Meta-orchestrator, coordinates the rest
```

If Antigravity doesn't support a native `@mention`-style skill trigger,
fall back to intent detection on keywords in whatever project-instructions
file it does load, the same fallback `gemini.md` proposes.

## Discovery

No central `REGISTRY.md` in this repo — browse instead:

- Skills: [`.agents/skills/`](../skills/)
- Instructions: [`.agents/instructions/`](../instructions/)
- Harnesses: [`.agents/harnesses/`](.)

## Deployment Checklist (fill in once Antigravity's real plumbing is confirmed)

- [ ] Confirm whether Antigravity auto-loads a project-context file by
      convention (like `CLAUDE.md`/`GEMINI.md`/`.github/copilot-instructions.md`)
      or requires explicit configuration — don't guess, check the tool's
      actual docs/behavior
- [ ] If it does auto-load a file, add the Session Startup pointer above
      into that file directly (same as was done for `GEMINI.md` and
      `.github/copilot-instructions.md` on 2026-09-16) instead of relying
      on a manual first message
- [ ] If it has a skill/extension directory, symlink it to `.agents/skills/`
      rather than copying skill content
- [ ] Master persona (`.agents/instructions/base-personas/archi.md`)
      referenced from wherever Antigravity reads project context
- [ ] Update this file's **Status** line once any of the above is verified
