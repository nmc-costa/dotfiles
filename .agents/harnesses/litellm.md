# 🔌 LiteLLM Reference

**Status:** Active  
**Setup:** Via multi-provider proxy + routing  
**Task-Specific:** `/my/agentic_instructions/harnesses/litellm/`

---

## Quick Links

| What | Where |
|------|-------|
| **Workspace Config** | `.github/instructions/workspace-config.md` |
| **All Agents** | `/my/agentic_instructions/REGISTRY.md` |
| **LiteLLM Setup** | `/my/agentic_instructions/harnesses/litellm/integration-guide.md` |

---

## ⚡ Quick Start

### 1️⃣ Workspace Configuration (Global)

All LiteLLM sessions follow these workspace rules:

**Model Routing** (Haiku vs GPT-5/Gemini)
- See: `.github/instructions/workspace-config.md` → Model Routing section
- Automatic provider selection based on task complexity
- Cost optimization with fallback routing

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

### 3️⃣ LiteLLM Setup

For complete integration guide:

👉 `/my/agentic_instructions/harnesses/litellm/integration-guide.md`

Includes:
- Multi-provider configuration (OpenAI, Gemini, Claude, etc.)
- Routing rules & cost optimization
- Fallback handling
- Cost tracking & monitoring

---

## 🎯 Common LiteLLM Tasks

| Task | Agent | Provider Selection |
|------|-------|---|
| Complex charter | `@projectHITs` | Premium (GPT-4/Claude 3) |
| Quick brief | `@projectHITs` | Budget (GPT-3.5/Claude Haiku) |
| Detailed presentation | `@presentHITs` | Premium |
| Thorough review | `@reviewHITs` | Premium |
| Complex diagram | `@diagramHITs` | Premium |
| Documentation | `@documentHITs` | Premium |
| Cost tracking | System | LiteLLM native |

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

1. **LiteLLM Setup:** See integration guide (link above)
2. **Multi-Provider Config:** Check integration-guide.md
3. **All Available Resources:** Check REGISTRY.md
4. **Architecture Decision:** See `/my/agentic_instructions/ARCHITECTURE_DECISION.md`
5. **Workspace Config:** See `.github/instructions/workspace-config.md`

---

## ✨ Ready to Go!

LiteLLM is now configured with all 7 agents and multi-provider routing.

All agents inherit from master persona and follow workspace rules automatically.
