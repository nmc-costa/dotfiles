# 🔌 Harness Reference Template

**Status:** Template for new harnesses
**Purpose:** Lightweight entry point for any LLM harness
**Copy & Customize:** Replace `{HARNESS-NAME}` with the actual name

---

## Quick Links

| What | Where |
|------|-------|
| **Workspace Config** | `.agents/instructions/workspace-config/` |
| **All Skills** | `.agents/skills/` (no central registry file in this repo — browse the directory) |
| **This Harness Setup** | `.agents/harnesses/{HARNESS-NAME}.md` |

---

## ⚡ Quick Start

### 1️⃣ Workspace Configuration (Global)

All harnesses follow these workspace rules:

**Model Routing** — `.agents/instructions/workspace-config/model-routing.instructions.md`
**Daily Optimization** (chronicle workflow) — `.agents/instructions/workspace-config/daily-optimization.instructions.md`
**Token Tracking** — `.agents/instructions/workspace-config/token-tracking.instructions.md`
**Mermaid AI Skills** — `.agents/instructions/workspace-config/mermaid.instructions.md`

### 2️⃣ Task-Specific Skills

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

See the skills directly: [`.agents/skills/`](../skills/) (no central registry file in this repo).

### 3️⃣ Full Setup

For the complete integration guide specific to `{HARNESS-NAME}`:

👉 `.agents/harnesses/{HARNESS-NAME}.md`

---

## 🎯 Common Tasks

| Task | Skill | Location |
|------|-------|----------|
| Create project charter | `projecthits` | `.agents/skills/projecthits/` |
| Generate slides/presentation | `presenthits` | `.agents/skills/presenthits/` |
| Review manuscript/code | `reviewhits` | `.agents/skills/reviewhits/` |
| Create diagrams/visuals | `diagramhits` | `.agents/skills/diagramhits/` |
| Update documentation | `documenthits` | `.agents/skills/documenthits/` |
| Build interactive mockup | `mockuphits` | `.agents/skills/mockuphits/` |

---

## What Is a "Harness" Here?

A harness is whatever surface actually loads instructions/skills for an LLM tool — an IDE
extension (VS Code Copilot), a CLI (Claude Code, Gemini CLI), a proxy layer (LiteLLM), or a
raw API integration you build yourself (OpenAI API). Concretely, when adding a new harness,
decide:

**Type** — pick one:
- `native` — built into an IDE/CLI that auto-discovers files (e.g. Claude Code reading
  `CLAUDE.md` / `SKILL.md`, Copilot reading `AGENTS.md`)
- `api` — you write the glue code that loads persona/skill files and calls a provider API
  directly (see `.agents/harnesses/openai.md`)
- `abstraction` — a multi-provider proxy/router (see `.agents/harnesses/litellm.md`)
- `local` — runs locally with no external API calls

**Status** — pick one:
- `active` — real, verified, in use
- `ready` — implemented, not yet exercised in anger
- `experimental` — in development
- `template` — not yet implemented, this file is the placeholder

### Required Content for a New Harness Doc

A single `.agents/harnesses/{harness-name}.md` file is enough — this repo does not use a
per-harness subdirectory with separate config/README/integration-guide files, and does not use
a central `REGISTRY.md`. The file should cover, at minimum:

1. **How this harness actually discovers instructions** — file-based auto-discovery (like
   Claude Code / Copilot) vs. code you have to write yourself (like the OpenAI/LiteLLM guides)
   — be explicit about which one it is; don't invent an auto-discovery mechanism that isn't
   real. If you're not sure how the tool actually loads context, say so rather than guessing.
2. Key file paths **in this repo** (`.agents/instructions/...`, `.agents/skills/...`) — no
   references to `/my/agentic_instructions/`, `REGISTRY.md`, or `config/harness-config.json`;
   none of those exist here.
3. A skill/persona trigger table (see the "Common Tasks" table above for the shape).
4. A deployment/verification checklist specific to that harness.

---

## Checklist: Adding a New Harness

- [ ] Create `.agents/harnesses/{harness-name}.md` (a single file, following this template)
- [ ] Verify — don't assume — how the harness actually discovers instructions; describe only
      what you've confirmed is real
- [ ] Fix every path reference to point at real files under `.agents/` in this repo
- [ ] Add a skill/persona trigger table
- [ ] Add a deployment checklist specific to that harness
- [ ] If the harness needs a symlinked directory (like `.claude/skills/` does for Claude Code), set that
      up rather than duplicating skill/instruction content into a harness-specific copy

---

## 📞 Need Help?

1. **Setup:** See the harness-specific file linked above
2. **All Available Resources:** Browse `.agents/skills/` and `.agents/instructions/` directly
   — there is no central `REGISTRY.md` in this repo
3. **Workspace Config:** See `.agents/instructions/workspace-config/`

---

## ✨ That's It!

Once `.agents/harnesses/{HARNESS-NAME}.md` exists and is accurate, that harness is ready to
use all skills. Skills inherit from the master persona (`archi`) and follow workspace rules
automatically where the harness actually supports loading them.
