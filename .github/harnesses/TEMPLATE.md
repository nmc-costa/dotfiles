# 🔌 Harness Reference Template

**Status:** Template for new harnesses  
**Purpose:** Lightweight entry point for any LLM harness  
**Copy & Customize:** Replace `{HARNESS-NAME}` with actual name

---

## Quick Links

| What | Where |
|------|-------|
| **Workspace Config** | `.github/instructions/workspace-config.md` |
| **All Agents** | `/my/agentic_instructions/REGISTRY.md` |
| **This Harness Setup** | `/my/agentic_instructions/harnesses/{HARNESS-NAME}/integration-guide.md` |

---

## ⚡ Quick Start

### 1️⃣ Workspace Configuration (Global)

All harnesses follow these workspace rules:

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

### 3️⃣ Full Setup

For complete integration guide specific to `{HARNESS-NAME}`:

👉 `/my/agentic_instructions/harnesses/{HARNESS-NAME}/integration-guide.md`

---

## 🎯 Common Tasks

| Task | Agent | Location |
|------|-------|----------|
| Create project charter | `@projectHITs` | `/my/agentic_instructions/agents/projectHITs/` |
| Generate slides/presentation | `@presentHITs` | `/my/agentic_instructions/agents/presentHITs/` |
| Review manuscript/code | `@reviewHITs` | `/my/agentic_instructions/agents/reviewHITs/` |
| Create diagrams/visuals | `@diagramHITs` | `/my/agentic_instructions/agents/diagramHITs/` |
| Update documentation | `@documentHITs` | `/my/agentic_instructions/agents/documentHITs/` |
| Build interactive mockup | `@mockupHITs` | `/my/agentic_instructions/agents/mockupHITs/` |

---

## 🔗 Central Discovery

**Master Index:** `/my/agentic_instructions/REGISTRY.md`

Contains:
- All 7 agents with triggers
- All personas (base + task-specific)
- All skills & tools
- All harnesses
- All templates
- Cross-references everything

---

## 📞 Need Help?

1. **Setup:** See integration guide (link above)
2. **All Available Resources:** Check REGISTRY.md
3. **Architecture Decision:** See ARCHITECTURE_DECISION.md
4. **Workspace Config:** See `.github/instructions/workspace-config.md`

---

## ✨ That's It!

You're now ready to use all agents on `{HARNESS-NAME}`. 

All agents inherit from master persona and follow workspace rules automatically.
