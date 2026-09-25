# VS Code Copilot Workspace Workflow (Global)

> **Note:** This file serves as a reference log of the global Copilot workspace configuration. The canonical source of truth is located in the workspace root:
> - **Root Level:** `AGENTS.md` → `.agents/AGENT.md`
> - **Feature Instructions:** `.agents/instructions/workspace-config/model-routing.instructions.md`
> - **Skills:** `.agents/skills/project-doc-lifecycle/SKILL.md`

All agents automatically discover and apply these rules without explicit prompting.

## 🔄 Session Management & Compaction (/compact & /continue)
- **Proactive Reminder:** If a conversation spans multiple complex steps or feels bloated, politely warn the user: *"This session is getting long. Type `/compact` to save our state so you can open a fresh chat."*
- **`/compact` Trigger:** When the user says `/compact`, immediately use the `memory` tool to save a thorough summary of the current state, progress, matched files, and next steps to `/memories/session/current_state.md`. 
- **`/continue` Trigger & New Chats:** Whenever starting a new chat, or if the user says `/continue`, quietly check if `/memories/session/current_state.md` exists. Reply with: *"I see a saved session state about [Topic]. Do you want to `/continue` where we left off, or start a new topic?"* (If they choose to continue, use the memory file to resume context immediately).

## 🤖 Automated Subagent Delegation
- For deep research, broad codebase analysis, or multi-step planning, do not clutter the main chat. Autonomously invoke the `runSubagent` tool to offload the heavy lifting, then return just the summarized results to the user.

## 🧠 Model Routing

**Use Claude Haiku for:**
- Markdown editing, formatting, indentation fixes
- Grammar & spelling reviews
- Template-based conversions (md → docx, using helper scripts)
- Document structure validation (checking against templates)
- Content refinement & rephrasing
- Any task with predefined rules/scripts (no discovery needed)

**Use GPT-5 or Gemini for:**
- Architectural design & system design decisions
- Complex multi-step reasoning (race conditions, algorithm design)
- Content generation that requires domain expertise or novel thinking
- Strategic planning & high-level decisions
- Debugging complex logic or integrations
- Validation against business requirements (requires semantic analysis, not just template checking)

**Explicit Model Selection Logging:** When selecting a model, internally note: `[Model: <model_name>] [Reason: <task_category>]` to enable tracking and verification of routing decisions.

## 📊 Routing Rule Monitoring & Analytics

To verify routing rule is working end-to-end and achieving ~30-40% token reduction:

1. **Phase 1 - Validation (Completed):**
   - ✅ Test harness confirms routing accuracy
   - Results tracked in session store

2. **Phase 2 - Real Session Monitoring (Weekly):**
   - Use session store queries to track model usage
   - Execute DuckDB queries to collect metrics
   - Generate compliance reports every Friday

3. **Phase 3 - Comparative Analysis (Monthly):**
   - Compare token usage vs. baseline
   - Calculate % reduction in expensive model usage
   - Target: ≥30% reduction

## 🔄 Daily Workspace Optimization

**Automated daily optimization of your workspace to continuously improve efficiency and reduce costs.**

Every new chat session should check if daily optimization is due (last run >24 hours ago). If so, remind the user about running `/chronicle` commands.

**What gets optimized:**
- Workflow patterns (tips)
- Model routing effectiveness & cost reduction opportunities (cost-tips)
- Workspace instructions & skills improvements (improve)

## 📋 Project Documentation Patterns (INCM)
- Maintain formal bilingual (Portuguese/English) structures for Project Charters and WP files.
- Validate documents against project briefs before finalizing.
- Rely on helper scripts in `scripts/` and standard templates in `docs/`.

---

**Base Persona:** Master global configuration for all Copilot agents  
**Version:** 1.0  
**Status:** Global Configuration Ready ✅  
**Last Updated:** 2026-08-25
