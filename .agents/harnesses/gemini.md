# 🔌 Gemini Reference

**Status:** Active  
**Setup:** Via system prompt + intent detection  
**Task-Specific:** `/my/agentic_instructions/harnesses/gemini/`

---

## Quick Links

| What | Where |
|------|-------|
| **Workspace Config** | `.github/instructions/workspace-config.md` |
| **All Agents** | `/my/agentic_instructions/REGISTRY.md` |
| **Gemini Setup** | `/my/agentic_instructions/harnesses/gemini/integration-guide.md` |

---

## ⚡ Quick Start

### 1️⃣ Workspace Configuration (Global)

All Gemini sessions follow these workspace rules:

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

### 3️⃣ Gemini Setup

For complete integration guide:

👉 `/my/agentic_instructions/harnesses/gemini/integration-guide.md`

Includes:
- API setup & configuration
- System prompt loading
- Intent detection for agent routing
- Function calling setup

---

## 🎯 Common Gemini Tasks

| Task | Agent | Trigger |
|------|-------|---------|
| Create project charter | `@projectHITs` | Mention "charter" or "project brief" |
| Generate slides | `@presentHITs` | Mention "presentation" or "slides" |
| Peer review | `@reviewHITs` | Mention "review" or "critique" |
| Create diagram | `@diagramHITs` | Mention "diagram" or "visualization" |
| Update docs | `@documentHITs` | Mention "document" or "documentation" |
| Build mockup | `@mockupHITs` | Mention "mockup" or "prototype" |
| Coordinate | `@architect` | Mention "orchestrate" or "coordinate" |

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

1. **Gemini Setup:** See integration guide (link above)
2. **All Available Resources:** Check REGISTRY.md
3. **Architecture Decision:** See `/my/agentic_instructions/ARCHITECTURE_DECISION.md`
4. **Workspace Config:** See `.github/instructions/workspace-config.md`

---

## ✨ Ready to Go!

Gemini is now configured with all 7 agents.

All agents inherit from master persona and follow workspace rules automatically.
