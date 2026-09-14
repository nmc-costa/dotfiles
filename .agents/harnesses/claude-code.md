# 🔌 Claude Code Reference

**Status:** Active
**Manual Setup Required:** No — Claude Code auto-discovers the files below, nothing to register
**Skills:** `.agents/skills/` (real files, plus `.claude/skills/*` symlinks — see below)

---

## How Claude Code Actually Loads Instructions

There is no `api.anthropic.com/v1/claude-code` endpoint, no central "registry" file, and no
`.claude/.instructions.md` single-file auto-discovery mechanism. The real mechanism is much
simpler and is all file-based, read directly from the working directory tree:

| File(s) | What it does | Loaded when |
|---|---|---|
| `CLAUDE.md` (repo root, and per-subdirectory) | Persistent project memory/instructions | Automatically, at session start, for every session in that directory tree |
| `.claude/skills/<name>/SKILL.md` | A Skill: name + description in frontmatter, body loaded on demand | Claude reads the frontmatter of every `SKILL.md` up front; it loads the **body** only when the task matches the `description` |
| `.claude/agents/*.md` | Subagent definitions (name, tools, model, system prompt) | When a task is delegated to that subagent via the `Agent`/Task tool |
| `.claude/settings.json` / `.claude/settings.local.json` | Permissions, hooks, env vars, model config | At startup |
| `.claude/commands/*.md` | Slash commands (`/command-name`) | When the user types the slash command |

In this repo, `.agents/skills/<name>/SKILL.md` is the canonical file for each skill, and
`.claude/skills/<name>` is a **symlink** to `.agents/skills/<name>` (e.g.
`.claude/skills/archi -> ../../.agents/skills/archi`) — not a separate copy, and not a thin
markdown wrapper that tells you to go read somewhere else. Claude Code sees the real content
directly through the symlink.

---

## ⚡ Quick Start

### 1️⃣ Workspace Configuration (Global)

All Claude Code sessions in this repo follow these workspace rules, defined under
`.agents/instructions/workspace-config/`:

- **Model Routing** — `.agents/instructions/workspace-config/model-routing.instructions.md`
- **Daily Optimization** (chronicle workflow) — `.agents/instructions/workspace-config/daily-optimization.instructions.md`
- **Token Tracking** — `.agents/instructions/workspace-config/token-tracking.instructions.md`
- **Mermaid Diagrams** — `.agents/instructions/workspace-config/mermaid.instructions.md`

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

`@name` here is a convention used *inside this repo's persona text* for a human/agent to
explicitly invoke a persona in conversation — it is not a Claude Code platform feature. What
Claude Code itself actually does is scan every `SKILL.md`'s `description` field and
auto-invoke the matching skill when the request matches, in addition to responding to an
explicit mention of the skill by name.

Full skill list: [`.agents/skills/`](../skills/) (no central registry file in this repo —
browse the directory).

### 3️⃣ Setup (nothing to install)

Claude Code needs no `.claude/` bootstrapping step in this repo — clone `dotfiles`, and any
Claude Code session started under it (or with `~/.claude` pointed at `dotfiles/.claude`) picks
up `CLAUDE.md` and every `.claude/skills/*/SKILL.md` automatically.

---

## 🎯 Common Claude Code Tasks

| Task | Skill | Example prompt |
|------|-------|--------|
| Create project charter | `projecthits` | "@projectHITs create charter" |
| Generate slides | `presenthits` | "@presentHITs create slides" |
| Peer review code | `reviewhits` | "@reviewHITs peer review" |
| Create diagram | `diagramhits` | "@diagramHITs create diagram" |
| Update docs | `documenthits` | "@documentHITs update document" |
| Build mockup | `mockuphits` | "@mockupHITs create mockup" |
| Coordinate skills | `archi` | "@architect coordinate" |

---

## 🔗 Discovery

There is no central `REGISTRY.md` in this repo (the old one, from the now-retired
`agentic_instructions` repo, was aspirational and stale). To discover what's available:

- Skills: [`.agents/skills/`](../skills/) — one directory per skill, each with `SKILL.md`
- Instructions: [`.agents/instructions/`](../instructions/) — base personas, task personas, workspace config
- Harnesses: [`.agents/harnesses/`](.) — this directory

---

## 📞 Need Help?

1. **Setup:** Nothing to set up beyond cloning the repo — see "Setup" above
2. **All Available Resources:** Browse `.agents/skills/` and `.agents/instructions/` directly
3. **Workspace Config:** See `.agents/instructions/workspace-config/`

---

## ✨ Ready to Go!

Claude Code reads `CLAUDE.md` and every `.claude/skills/*/SKILL.md` (symlinked to
`.agents/skills/`) automatically — no manual registration step, no config file to maintain.
