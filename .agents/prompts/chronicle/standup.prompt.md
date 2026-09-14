---
name: chronicle-standup
description: "Generate session summary and standup report"
version: "1.0"
type: "system"
model: "universal"
---

# Chronicle: Standup Prompt

Generate a standup report summarizing recent Copilot session activity, work completed, and blockers.

---

## System Prompt

```
You are generating a standup report from recent Copilot session history.

STANDUP ELEMENTS:
1. What was worked on (projects, files, task categories)
2. What was completed (commits, PRs, closed issues)
3. What's in progress (open branches, incomplete work)
4. Blockers (errors, auth issues, design decisions pending)
5. Next steps (upcoming priorities, planned work)
6. Metrics (time spent, commits, tokens used)

OUTPUT FORMAT:
- Daily standup (1 day) or Weekly standup (5-7 days)
- Clear sections: ✅ Done | 🔄 In Progress | 🚫 Blockers | ⏭️ Next
- Focus on facts (commits, files) not interpretation
- Include: Time spent, model usage, key files touched

TONE: Concise, professional, ready to share with team
```

---

## Example Output: Daily Standup

```
📋 STANDUP REPORT — August 25, 2026

✅ COMPLETED TODAY
- ✅ Reorganized agentic_instructions repo (v2.0)
  - Moved 6 markdown files to docs/ structure
  - Created personas: projectHITs, presentHITs, reviewHITs, diagramHITs, documentHITs, mockupHITs
  - Created 5 harness integration guides (VS Code, Claude Code, Gemini, OpenAI, LiteLLM)
  - Archived versions: v1-v4 projectHITs in /versions/instructions/
- ✅ Deleted legacy /system_instructions/ folder
- ✅ Created template structure for agents, skills, prompts, tools

🔄 IN PROGRESS
- ⏳ Creating config overrides for multi-harness support
- ⏳ Filling template structures with examples

🚫 BLOCKERS
- None currently

⏭️ NEXT STEPS
- Complete config/.harnesses/ with 5 JSON files
- Create example implementations for prompts/chronicle
- Note new file locations in the relevant skill/instruction README (no central registry file in this repo)
- Git commit + verify structure

📊 METRICS
- Files created: 23
- Lines of code/content: ~4500
- Session duration: ~2.5 hours
- Model used: Claude (Haiku for templates, GPT-5 for architecture)
```

---

## Example Output: Weekly Standup

```
📋 WEEKLY STANDUP — Week of August 18-25

✅ COMPLETED THIS WEEK
- Phase 1: Analyzed current repository structure ✅
- Phase 2: Created personas, harnesses, versions ✅
- Phase 3: Documentation cleanup (moved files to /docs/) ✅
- Git commits: 7 | Files created: 23 | Total lines: ~4500

🔄 IN PROGRESS
- Phase 4: Template structures (agents, skills, prompts, tools)
- Multi-harness config overrides

🚫 BLOCKERS
- None

⏭️ NEXT WEEK
- Complete Phase 4 (templates, configs)
- Verify against directory tree
- Git commit final reorganization
- Update cloud repository

📊 METRICS BY DAY
- Mon: 45m (planning)
- Tue: 1.5h (analysis)
- Wed: 1.5h (creation)
- Thu: 45m (cleanup)
- Fri: 2.5h (validation & final push)
- Total: ~7.25 hours this week
```

---

## See Also

- [tips.prompt.md](tips.prompt.md) — Workflow tips
- [cost-tips.prompt.md](cost-tips.prompt.md) — Cost analysis
- [improve.prompt.md](improve.prompt.md) — Improvement suggestions

---

**Version**: 1.0  
**Last Updated**: 2026-08-25
