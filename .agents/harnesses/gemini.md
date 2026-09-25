# 🔌 Gemini CLI Reference

**Status:** Reference / partially verified — the old integration guide this replaces
described a fictional setup (it mixed the Anthropic Python SDK — `import anthropic`,
`anthropic.Anthropic(api_key="gemini-...")` — into a "Gemini API" example, which was never
real). This version sticks to what's actually true of file-based harnesses in this repo and
flags anything about Gemini CLI's exact plumbing that hasn't been independently re-verified.

---

## How This Should Actually Work

The convention this repo follows (already true for Claude Code and GitHub Copilot, see
`.agents/harnesses/claude-code.md` and `.agents/harnesses/vscode-copilot.md`) is:

1. A tool-specific context file (`CLAUDE.md` for Claude Code; Gemini CLI's equivalent is a
   `GEMINI.md` project-context file) carries project-wide instructions and is auto-loaded.
2. Reusable capabilities live once, under `.agents/skills/<name>/SKILL.md`, and each tool
   either reads that path directly or has its own directory **symlinked** to it (the way
   `.claude/skills/<name> -> ../../.agents/skills/<name>` is set up in this repo).

For Gemini CLI specifically: if/when you wire this repo up for it, symlink whatever
directory Gemini CLI expects (check `gemini --help` / current Gemini CLI docs for the exact
name, since this has changed across CLI versions) to `.agents/skills/`, the same pattern used
for `.claude/skills/` here — rather than duplicating skill content into a
Gemini-specific copy.

**Do not** hand-roll a Python script that loads `archi.md` and pastes it into a
`system` parameter for the Anthropic SDK and call that "Gemini integration" — that was the
mistake in the previous version of this file. If you're calling the Gemini API directly
(rather than using Gemini CLI), use Google's own SDK (`google-generativeai` /
`google-genai`), not `anthropic`.

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

If Gemini CLI doesn't support a native `@mention`-style skill trigger, fall back to intent
detection on keywords (e.g., "charter"/"project brief" → `projecthits`, "slides"/"deck" →
`presenthits`) inside your own `GEMINI.md` instructions, the same way the old guide proposed —
that part of the design is reasonable, it was only the API code sample that was wrong.

## Discovery

There is no central `REGISTRY.md` in this repo (the one in the old `agentic_instructions`
repo was aspirational and stale, and was not carried over). Browse instead:

- Skills: [`.agents/skills/`](../skills/)
- Instructions: [`.agents/instructions/`](../instructions/)
- Harnesses: [`.agents/harnesses/`](.)

## Deployment Checklist (adjust once Gemini CLI's real plumbing is confirmed)

- [ ] Confirm Gemini CLI's actual context-file name/location (`GEMINI.md` or current
      equivalent) and skill/extension directory in the CLI version you're using
- [ ] Symlink that directory (or point its config) at `.agents/skills/` rather than copying
      skill content
- [ ] Master persona (`.agents/instructions/base-personas/archi.md`) referenced from your
      `GEMINI.md`
- [ ] Task personas reachable from `.agents/instructions/task-personas/`
- [ ] If calling the Gemini API directly (not via CLI), use `google-generativeai` /
      `google-genai`, not the Anthropic SDK
