<!-- mermaid-ai-skills:start -->
## Mermaid Diagrams

When the user asks to create, edit, or visualize a diagram, follow the
instructions in `my/agentic_instructions/instructions/workspace-config/mermaid.instructions.md`.
<!-- mermaid-ai-skills:end -->

## 🔄 Session Memory Management (/compact → /memorize → /recall)
**Workflow for token-efficient cross-chat persistence:**

1. **Within-session compaction:** Use VS Code's built-in `/compact [instructions]` to summarize chat history
2. **Cross-chat saving:** Use `/memorize` to persist compacted state to `my/agentic_instructions/memories/CURRENT_SESSION.md`
3. **Next chat recovery:** Use `/recall` to restore compacted context in a new session

- **Automatic Session Reminders:** Issue proactive reminder when:
  - Session exceeds **25 turns**, OR
  - Session duration exceeds **45 minutes**, OR
  - User performs **repeated edits to same file** (>5 edits in <20 turns)
  
  Message template: *"⚠️ This session is growing. You're at [N] turns over [T] minutes. Type `/compact` to compress history, then `/memorize` to save. This will reduce context overhead by ~60% on next chat."*

- **`/memorize` Command:** When the user says `/memorize`, use the `memory` tool to save compacted summary to `my/agentic_instructions/memories/CURRENT_SESSION.md`. This is typically done after using `/compact` to compress the conversation. Confirm completion with summary.
- **`/recall` Command & New Chats:** Whenever starting a new chat, or if the user says `/recall`, quietly check if `my/agentic_instructions/memories/CURRENT_SESSION.md` exists. Reply with: *"📋 Found compacted session about [Topic]. Do you want to continue with that work, or start a new topic?"* (If they choose to continue, use the memory file to resume context immediately).
- **Session Recovery:** If session.create fails (e.g., sendFailed error), attempt retry with exponential backoff (1s → 2s → 4s). If persistent failure, fall back to session-free mode and notify user. Track failures via `session_store_sql` for pattern analysis.

## 🛡️ Session Initialization & Error Recovery
- **Session Creation Failures:**
  - If `session.create` fails with `sendFailed` or `401 Unauthorized`:
    1. Check GitHub authentication: `gh auth status`
    2. If auth expired, re-authenticate: `gh auth login`
    3. Restart VS Code Copilot chat
    4. If failures persist, use session-free mode and create a new chat

- **Proactive Recovery:**
  - If a session starts but shows no initial response, wait 3 seconds before retrying
  - On persistent failures, offer user option to continue in session-free mode
  - Log authentication failures to help debug patterns

## 📋 Request Validation
- **Incomplete Input Detection:** If user's initial request is < 5 words or appears incomplete/malformed (e.g., truncated file refs like `@file:projectHITs.md` without context), ask clarifying questions before proceeding.
- **Locale Consistency:** Detect primary language from first request (Portuguese/English). Apply consistent locale throughout session. If code comments/docs require specific language, preserve original.
- **File Reference Validation:** Expand abbreviated file references (e.g., `@file:name.md`) into full context paths. Verify file exists before using in operations.

## 📁 Session File Context Tracking
- **Auto-Capture on Session Start:** Log the active editor file (from `editorContext`) as session context
- **Track File Modifications:** Record all files created, modified, or deleted during session in session memory
- **Pattern Detection:** Enable friction pattern analysis by ensuring `session_files` table captures complete file lineage
- **Reference Visibility:** Include read-only files accessed (imports, configs, shared templates) to support future friction analysis

## 🤖 Automated Subagent Delegation
- For deep research, broad codebase analysis, or multi-step planning, do not clutter the main chat. Autonomously invoke the `runSubagent` tool to offload the heavy lifting, then return just the summarized results to the user.

## ⚡ Slash Command Workflows
- **Pre-Flight Checks:** Before invoking any slash command (e.g., `/create-instructions`, `/create-agent`, `/create-skill`, `/chronicle`, `/analyze-prompt`), verify the command is registered and available.
- **Error Handling:** If a slash command is not recognized, do NOT silently fail. Instead, explain to the user which commands are actually available and suggest alternatives based on their intent.
- **File Reference in Commands:** When a slash command includes a file reference (e.g., `/create-agent based on @file:presentHITs.md`), expand and validate the path exists before executing.
- **Known Available Commands:** `/chronicle`, `/compact` (VS Code built-in), `/memorize`, `/recall`, and skill-based commands defined in `.github/skills/` and custom agent files.

**Slash Command Completion Pattern:**
- `/create-instructions` → If user provides file/requirements, auto-generate full file (no "need more details" pause)
- `/analyze-prompt` → Run analysis, then proactively ask: "Would you like me to fix these [N] issues automatically?"
- `/create-skill` → Complete the skill with examples, then ask for validation before closing

**Incomplete Request Handling:**
- If a slash command receives a vague request (< 20 words), ask clarifying questions
- BUT: After user responds, immediately proceed to completion—don't ask again
- Avoid multi-turn back-and-forth; aim for completion in 1-2 additional turns max

**Multi-Turn Clarification Anti-Pattern:**
- ❌ Turn 1: Show analysis, ask if you want fixes
- ❌ Turn 2: User says yes
- ❌ Turn 3: You ask which files to update
- ✅ Instead: In Turn 1, include "I'll auto-apply these 5 fixes:" and just do it

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

## 📊 Routing Rule Monitoring & Analytics (Session Store Approach)

To verify the routing rule is working end-to-end and achieving ~30-40% token reduction:

1. **Phase 1 - Validation (Completed):**
   - ✅ Test harness confirms 100% routing accuracy on 5 representative tasks
   - Results: `/home/user/github/.github/skills/routing_test_results_phase1.json`

2. **Phase 2 - Real Session Monitoring (Weekly):**
   - Use the `model-routing-monitor` skill to query session store
   - Execute DuckDB queries via `session_store_sql` tool (see `token-tracking.instructions.md`)
   - Collect baseline metrics: model assignments, token counts, cost per task
   - Generate compliance reports every Friday

3. **Phase 3 - Comparative Analysis (Monthly):**
   - Compare actual token usage against baseline (before routing rule)
   - Calculate percentage reduction: (Expensive tokens ↓ / Baseline) × 100%
   - Target: ≥30% reduction in expensive model usage
   - Document findings in `docs/routing_compliance/routing_compliance_YYYYMMDD.md`

**Instructions for monitoring:** See `my/agentic_instructions/instructions/workspace-config/token-tracking.instructions.md`  
**Skill for analytics:** See `.github/skills/model-routing-monitor/SKILL.md`

## � Daily Workspace Optimization

**Automated daily optimization of your workspace to continuously improve efficiency and reduce costs.**

Every new chat session should check if daily optimization is due (last run >24 hours ago). If so, remind the user:

```
🔄 Daily Workspace Optimization Due
Last run: [X days ago]

Ready to run: /chronicle tips → /chronicle cost-tips → /chronicle improve?
(2-3 mins, generates optimization report)

To compress + save this session: /compact [instructions] → /memorize
To resume from a previous session: /recall
```

**What gets optimized:**
- Workflow patterns (tips)
- Model routing effectiveness & cost reduction opportunities (cost-tips)
- Workspace instructions & skills improvements (improve)

**Results:** Automatic report saved to `my/agentic_instructions/memories/` with findings and recommendations.

See `my/agentic_instructions/instructions/workspace-config/daily-optimization.instructions.md` for full automation logic, including silent mode option.

## �📋 Project Documentation Patterns (INCM)
- Maintain formal bilingual (Portuguese/English) structures for Project Charters and WP files.
- Validate documents against project briefs before finalizing.
- Rely on helper scripts in `scripts/` (e.g., markdown to docx conversion) and standard templates in `docs/` rather than generating formats from scratch.
