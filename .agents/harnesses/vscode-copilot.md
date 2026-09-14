# 🔌 VS Code Copilot Reference

**Status:** Active  
**Auto-Discovery:** Yes (`.github/copilot-instructions.md`)  
**Task-Specific:** `/my/agentic_instructions/harnesses/vscode-copilot/`

---

## Quick Links

| What | Where |
|------|-------|
| **Workspace Config** | `.github/instructions/workspace-config.md` |
| **All Agents** | `/my/agentic_instructions/REGISTRY.md` |
| **VS Code Setup** | `/my/agentic_instructions/harnesses/vscode-copilot/integration-guide.md` |

---

## ⚡ Quick Start

### 1️⃣ Workspace Configuration (Global)

All VS Code Copilot sessions follow these workspace rules:

**Model Routing** (Haiku vs GPT-5/Gemini)
- See: `.github/instructions/workspace-config.md` → Model Routing section

**Daily Optimization** (chronicle workflow)
- See: `.github/instructions/workspace-config.md` → Daily Optimization section

**Token Tracking** (cost tracking & monitoring)
- See: `.github/instructions/workspace-config.md` → Token Tracking section

**Mermaid AI Skills** (diagram generation)
- See: `.github/instructions/workspace-config.md` → Mermaid section

### 2️⃣ Task-Specific Agents

For project-specific tasks, use these agents:

```
Trigger          | Agent            | Purpose
─────────────────┼──────────────────┼─────────────────────────────
@projectHITs     | Charter Architect| Project charters + WPs
@presentHITs     | Slide Architect  | Executive presentations
@reviewHITs      | Review Architect | Peer review & critique
@diagramHITs     | Diagram Architect| Mermaid diagrams
@documentHITs    | Doc Architect    | Documentation synthesis
@mockupHITs      | Mockup Architect | Interactive prototypes
@architect       | Meta-Orchestrator| Coordinate all agents
```

See full details: `/my/agentic_instructions/REGISTRY.md`

### 3️⃣ VS Code Copilot Setup

For complete integration guide:

👉 `/my/agentic_instructions/harnesses/vscode-copilot/integration-guide.md`

Includes:
- How to load personas in VS Code
- `.copilot-instructions` setup
- Agent trigger configuration
- Multi-harness compatibility

---

## 🎯 Common VS Code Tasks

| Task | Agent | Command |
|------|-------|---------|
| Create project charter | `@projectHITs` | `@projectHITs create charter` |
| Generate slides | `@presentHITs` | `@presentHITs create slides` |
| Peer review code | `@reviewHITs` | `@reviewHITs peer review` |
| Create diagram | `@diagramHITs` | `@diagramHITs create diagram` |
| Update docs | `@documentHITs` | `@documentHITs update document` |
| Build mockup | `@mockupHITs` | `@mockupHITs create mockup` |
| Coordinate agents | `@architect` | `@architect coordinate` |

---

## 🔗 Central Discovery

**Master Index:** `/my/agentic_instructions/REGISTRY.md`

Contains:
- All 7 agents with triggers
- All personas (base + task-specific)
- All skills & tools
- All 5 harnesses
- All templates
- Cross-references everything

---

## 📞 Need Help?

1. **VS Code Setup:** See integration guide (link above)
2. **All Available Resources:** Check REGISTRY.md
3. **Architecture Decision:** See `/my/agentic_instructions/ARCHITECTURE_DECISION.md`
4. **Workspace Config:** See `.github/instructions/workspace-config.md`

---

## ✨ Ready to Go!

VS Code Copilot is now configured with all 7 agents.

All agents inherit from master persona and follow workspace rules automatically.
