# 🔗 Workspace Configuration Instructions

**Instructions live directly in this repo, under `.agents/instructions/` — there is no external "centralized" repo.**

This directory used to describe a "Hybrid C" architecture that pointed at `/my/agentic_instructions/`, a path that
never existed on this machine. The real source repo was `~/Projects/agentic_instructions`; its content has now been
merged into this repo (`dotfiles`) directly, which is the single source of truth going forward. The old repo is kept
around only to be archived on GitHub for history — do not treat it as a live source anymore.

## 📍 Layout

```
.agents/instructions/
├── base-personas/        # archi.md (master persona) + related base personas
├── task-personas/        # per-agent personas (projectHITs.md, presentHITs.md, ...)
├── workspace-config/      # workspace-wide rules
└── automation/            # scheduled/automated instruction sets
```

## 📋 What's Available

| Instruction | Purpose | Location |
|-------------|---------|----------|
| **Daily Optimization** | Automated daily workspace optimization workflow | [`workspace-config/daily-optimization.instructions.md`](workspace-config/daily-optimization.instructions.md) |
| **Model Routing** | Model selection rules (Haiku vs. more expensive models) | [`workspace-config/model-routing.instructions.md`](workspace-config/model-routing.instructions.md) |
| **Token Tracking** | Token usage monitoring and routing compliance | [`workspace-config/token-tracking.instructions.md`](workspace-config/token-tracking.instructions.md) |
| **Mermaid Diagrams** | Mermaid diagram generation rules and validation | [`workspace-config/mermaid.instructions.md`](workspace-config/mermaid.instructions.md) |
| **Machine Environment** | Standing environment facts for this machine (e.g. `sudo` has no TTY, use `pkexec`) | [`workspace-config/machine-environment.instructions.md`](workspace-config/machine-environment.instructions.md) |
| **Proactive Memory Capture** | Persist what works from every interaction, not just corrections, without being asked | [`workspace-config/memory-capture.instructions.md`](workspace-config/memory-capture.instructions.md) |
| **VS Code Docs Monitor** | Weekly VS Code docs change monitoring | [`automation/vscode-docs-monitor.instructions.md`](automation/vscode-docs-monitor.instructions.md) |
| **Master Persona** | Master Architect / Weaver persona | [`base-personas/archi.md`](base-personas/archi.md) |
| **Copilot Workspace Workflow** | Copilot-specific workspace workflow notes | [`base-personas/copilot_workspace_workflow.md`](base-personas/copilot_workspace_workflow.md) |
| **Master Continuous Optimization** | Design-only future roadmap (NOT implemented) | [`base-personas/master-continuous-optimization.md`](base-personas/master-continuous-optimization.md) |
| **Task Personas** | Per-agent personas | [`task-personas/`](task-personas/) |

## 🏗️ Current Architecture

- ✅ **Single Source of Truth**: `.agents/instructions/` in this repo (`~/dotfiles`)
- ✅ **GitHub Compliance**: `.github/copilot-instructions.md` is auto-discovered by GitHub Copilot; `.github/instructions` is a symlink to `.agents/instructions` so both tools read the same files
- ✅ **Zero Duplication**: `.github/instructions` and `.agents/instructions` are the same files on disk (symlink), not copies
- ⚠️ **No central REGISTRY.md**: the old repo's `REGISTRY.md` was aspirational/stale and was not carried over. Browse `.agents/skills/` and `.agents/instructions/` directly instead.

## 🔄 How It Works

1. GitHub Copilot discovers `.github/copilot-instructions.md`.
2. Claude Code, Cursor, Gemini CLI, etc. read `.agents/skills/*/SKILL.md` and `.agents/instructions/` directly.
3. `.github/instructions` is a symlink to `.agents/instructions`, so editing either path edits the same file.

## 📝 Note for Contributors

Edit files directly in this directory (`.agents/instructions/`) — there is no other copy to keep in sync, aside from
the `.github/instructions` symlink which always resolves here automatically.

---

**Last Updated**: 2026-09-14
**Architecture**: Single source of truth in `.agents/` (dead "Hybrid C" pointer to `/my/agentic_instructions/` removed)
