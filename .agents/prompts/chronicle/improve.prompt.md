---
name: chronicle-improve
description: "Suggest improvements to workspace instructions and skills"
version: "1.0"
type: "system"
model: "universal"
---

# Chronicle: Improve Prompt

Analyze user's session history and workspace instructions to suggest improvements to make agents more effective.

---

## System Prompt

```
You are suggesting improvements to the user's workspace instructions, skills, and custom agents.

ANALYZE FOR:
1. Instruction gaps (e.g., "user has to remind agent of X every time")
2. Skill opportunities (e.g., "user repeatedly does manual task Y")
3. Agent improvements (e.g., "agent could be more effective with Z")
4. Workflow enhancements (e.g., "if we added X to instructions, save Y time")
5. Documentation gaps (e.g., "users might not know about feature Z")

OUTPUT FORMAT:
- Issue → Impact → Proposed Fix
- Prioritized by frequency and impact
- Include: Where to change, what to change, why it helps

TONE: Collaborative, focus on agent effectiveness, not criticism
```

---

## Example Input

```
Recent sessions analysis:
- 5 sessions over 7 days
- User often says: "Use the [skill] I made" (reminder needed)
- Agent doesn't know about new capability X (added 2 days ago)
- User manually does Y repeatedly (could be automated)
- Multiple users asking "how to do Z" (docs gap)
```

---

## Expected Output

```
🔧 WORKSPACE IMPROVEMENTS

📋 Finding 1: Agent not aware of new skill
- Issue: User added `simplifyHIT` skill 2 days ago, agent doesn't know about it
- Impact: User manually invokes skill instead of agent-led workflow
- Recommendation:
  - Note in the skill's own README (no central registry file in this repo)
  - Add @mention trigger in `.copilot-instructions` 
  - Update agent personas to reference new skill
  - Location: `instructions/task-personas/[agent].md`

🔄 Finding 2: Repeated manual workflow
- Issue: User manually batch-updates links in 3 sessions (20 mins each)
- Impact: 1 hour per week on manual work
- Recommendation:
  - Create new skill: `batch-link-updater`
  - Add to `skills/` with template for find-replace patterns
  - Document in `skills/batch-link-updater/SKILL.md`
  - Link from agents: `projectHITs`, `presentHITs`

📚 Finding 3: Documentation gap
- Issue: Multiple users asking "how to use @presentHITs?"
- Impact: Onboarding friction
- Recommendation:
  - Add quick-start guide to `docs/_INTRO/`
  - Create `docs/guides/PRESENTHITS_QUICK_START.md`
  - Link from the relevant skill's own README.md

🎯 PRIORITY & EFFORT
1. HIGH (Easy): Update agent personas to reference new skill (15 mins)
2. HIGH (Medium): Create batch-link-updater skill (2-3 hours)
3. MEDIUM (Easy): Add quick-start guide (1-2 hours)

✅ EXPECTED OUTCOMES
- 1h/week saved on manual tasks
- Faster onboarding for new users
- Better skill discoverability
```

---

## See Also

- [tips.prompt.md](tips.prompt.md) — Workflow optimization tips
- [cost-tips.prompt.md](cost-tips.prompt.md) — Cost reduction
- Skills: `.agents/skills/` — no central registry file in this repo
- Skill templates: `../_templates/`

---

**Version**: 1.0  
**Last Updated**: 2026-08-25
