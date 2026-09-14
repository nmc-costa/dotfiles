# 🔌 OpenAI Reference

**Status:** Active  
**Setup:** Via API + model routing  
**Task-Specific:** `/my/agentic_instructions/harnesses/openai/`

---

## Quick Links

| What | Where |
|------|-------|
| **Workspace Config** | `.github/instructions/workspace-config.md` |
| **All Agents** | `/my/agentic_instructions/REGISTRY.md` |
| **OpenAI Setup** | `/my/agentic_instructions/harnesses/openai/integration-guide.md` |

---

## ⚡ Quick Start

### 1️⃣ Workspace Configuration (Global)

All OpenAI sessions follow these workspace rules:

**Model Routing** (Haiku vs GPT-5/Gemini)
- See: `.github/instructions/workspace-config.md` → Model Routing section
- gpt-4-turbo for complex tasks
- gpt-3.5-turbo for fast responses

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

### 3️⃣ OpenAI Setup

For complete integration guide:

👉 `/my/agentic_instructions/harnesses/openai/integration-guide.md`

Includes:
- API key configuration
- Model selection (gpt-4-turbo vs gpt-3.5-turbo)
- Function calling setup
- Cost optimization strategy

---

## 🎯 Common OpenAI Tasks

| Task | Agent | Model |
|------|-------|-------|
| Complex charter | `@projectHITs` | gpt-4-turbo |
| Quick brief | `@projectHITs` | gpt-3.5-turbo |
| Detailed presentation | `@presentHITs` | gpt-4-turbo |
| Thorough review | `@reviewHITs` | gpt-4-turbo |
| Complex diagram | `@diagramHITs` | gpt-4-turbo |
| Documentation | `@documentHITs` | gpt-4-turbo |

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

1. **OpenAI Setup:** See integration guide (link above)
2. **All Available Resources:** Check REGISTRY.md
3. **Architecture Decision:** See `/my/agentic_instructions/ARCHITECTURE_DECISION.md`
4. **Workspace Config:** See `.github/instructions/workspace-config.md`

---

## ✨ Ready to Go!

OpenAI is now configured with all 7 agents and model routing.

All agents inherit from master persona and follow workspace rules automatically.
