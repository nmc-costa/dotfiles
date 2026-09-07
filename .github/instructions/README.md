# 🔗 Workspace Configuration Instructions

**⚠️ All instructions are centralized in `/my/agentic_instructions/` (Hybrid C architecture)**

This directory contains **references only**. For the actual instructions, see:

## 📍 Centralized Location

All workspace configuration instructions are stored in:
```
/my/agentic_instructions/instructions/workspace-config/
```

## 📋 What's Available

| Instruction | Purpose | Location |
|-------------|---------|----------|
| **Daily Optimization** | Automated daily workspace optimization workflow | [`workspace-config/daily-optimization.instructions.md`](../../my/agentic_instructions/instructions/workspace-config/daily-optimization.instructions.md) |
| **Model Routing** | Model selection rules (Haiku vs GPT-5/Gemini) | [`workspace-config/model-routing.instructions.md`](../../my/agentic_instructions/instructions/workspace-config/model-routing.instructions.md) |
| **Token Tracking** | Token usage monitoring and routing compliance | [`workspace-config/token-tracking.instructions.md`](../../my/agentic_instructions/instructions/workspace-config/token-tracking.instructions.md) |
| **Mermaid Diagrams** | Mermaid diagram generation rules and validation | [`workspace-config/mermaid.instructions.md`](../../my/agentic_instructions/instructions/workspace-config/mermaid.instructions.md) |

## 🏗️ Hybrid C Architecture

This structure follows the **Hybrid C pattern**:
- ✅ **Single Source of Truth**: All instructions in `/my/agentic_instructions/`
- ✅ **GitHub Compliance**: `.github/copilot-instructions.md` auto-discovered by GitHub Copilot
- ✅ **Zero Duplication**: Only references here, no duplication
- ✅ **Flexibility**: Easy to update, reference, or switch harnesses

## 🔄 How It Works

1. GitHub Copilot discovers `.github/copilot-instructions.md`
2. That file points to `REGISTRY.md` in `/my/agentic_instructions/`
3. REGISTRY.md links to all agents, harnesses, and workspace config
4. This README points you to the actual instructions

## 📝 Note for Contributors

Do NOT edit files in this directory. Instead:

1. Make changes in `/my/agentic_instructions/instructions/workspace-config/`
2. The changes automatically apply (referenced here)
3. Commit to `agentic_instructions` repo
4. This `.github/` folder stays clean and small

## 🎯 Quick Links

- **Main Registry**: `/my/agentic_instructions/REGISTRY.md`
- **Master Organization Policy**: `/my/agentic_instructions/docs/MASTER_INSTRUCTIONS_ORGANIZATION.md`
- **All Agents**: `/my/agentic_instructions/agents/`
- **All Harnesses**: `/my/agentic_instructions/harnesses/`

---

**Last Updated**: 2026-08-26
**Architecture**: Hybrid C (Centralized)
