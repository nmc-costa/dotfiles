---
automation: daily
category: optimization
trigger: daily-08:00
priority: high
---

# Daily Chronicle Automation Checklist

**Purpose:** Automatically optimize Copilot workspace costs and workflows by running chronicle analysis daily.

**Frequency:** Once per day (recommended: morning, before work starts)  
**Time commitment:** ~2 minutes  
**Expected impact:** 30-40% token reduction + workflow improvements

---

## Daily Command Sequence (Copy & Paste)

Run these commands **in order** in a fresh Copilot Chat, one at a time:

### 1️⃣ Morning Optimization (08:00 - Start of Day)
```
/chronicle tips
```
**Purpose:** Get personalized workflow recommendations  
**Output:** Identifies session patterns, token usage trends, cost-saving opportunities  
**Action:** Review the 5 tips and apply to today's work

---

### 2️⃣ Weekly Deep Dive (Every Friday 17:00 - End of Week)
```
/chronicle standup
```
**Purpose:** Get comprehensive weekly summary  
**Output:** Sessions worked on, files touched, models used, total tokens consumed  
**Action:** Note any sessions that consumed excessive tokens and plan compaction

---

### 3️⃣ Monthly Cost Analysis (First Friday of Month)
```
/chronicle search "routing accuracy"
```
**Purpose:** Search past sessions for model routing compliance  
**Output:** Sessions where model routing was applied correctly  
**Action:** Calculate % reduction in premium model usage vs. baseline

---

## Automated Reminders

### In VS Code Chat
Agents will **proactively remind** you when:
- ✅ Session length exceeds 20 turns → *"Suggest `/compact`"*
- ✅ Friday 17:00 approaches → *"Time for `/chronicle standup`?"*
- ✅ Monthly 1st Friday → *"Monthly cost analysis time"*

### Pseudo-Automation (Manual Trigger Points)

| Time | Command | Purpose |
|------|---------|---------|
| **Daily (8 AM)** | `/chronicle tips` | Get daily optimization tips |
| **Friday (5 PM)** | `/chronicle standup` | Weekly summary + cost review |
| **1st Fri of Month** | `/chronicle search "routing"` | Monthly routing compliance check |
| **Any 20+ turn session** | `/compact` | Auto-save state and reset |

---

## What Each Command Does

### `/chronicle tips` (Daily)
- Analyzes last 7 days of sessions
- Identifies token usage patterns
- Recommends workflow improvements
- Shows model routing effectiveness
- **Output:** 5 actionable tips with metrics

### `/chronicle standup` (Weekly)
- Weekly summary of all sessions
- Files modified, repositories touched
- Total token consumption by model
- Session durations and turn counts
- **Output:** Comprehensive week overview

### `/chronicle search "keyword"` (Ad-hoc)
- Search session history by keyword
- Find related sessions and PRs
- Identify patterns across sessions
- **Output:** Filtered session list with context

---

## Integration with Copilot Instructions

These commands are automatically triggered by agents when:

1. **Compaction Reminder:** After ~15-20 turns in a session
   - Agent notices length
   - Suggests: *"This session is getting long. Type `/compact` to save state."*
   - User types `/compact` → saves to `/memories/session/current_state.md`

2. **Weekly Optimization Check:** Every Friday
   - Agent suggests: *"Time for `/chronicle standup`?"*
   - User runs command → gets weekly metrics
   - Agent highlights cost-saving opportunities

3. **Model Routing Verification:** During routing decisions
   - Agent internally logs: `[Model: claude-haiku] [Reason: template validation]`
   - `/chronicle search "routing"` shows accuracy over time

---

## Expected Outcomes (First Month)

| Week | Metric | Target | Evidence |
|------|--------|--------|----------|
| **Week 1** | Model routing adoption | 100% | All agents routing correctly |
| **Week 2** | Haiku task % | 80-85% | `/chronicle tips` report |
| **Week 3** | Token reduction vs baseline | 15-20% | `/chronicle standup` metrics |
| **Week 4** | Cumulative reduction | 30-40% | Month-end `/chronicle search` |

---

## How to Track Progress

### Daily (after `/chronicle tips`)
- Note any new patterns identified
- Apply 1-2 tips to today's workflow
- Estimate time saved

### Weekly (after `/chronicle standup`)
- Compare token usage to previous week
- Check model distribution (Haiku % vs Premium %)
- Identify sessions that could have been compacted

### Monthly (after `/chronicle search`)
- Calculate total token reduction: `(baseline - current) / baseline * 100%`
- Document in `/home/user/github/docs/routing_compliance/routing_compliance_YYYYMMDD.md`
- Update target for next month

---

## Automation Code (For VS Code Tasks)

Add to `.vscode/tasks.json` to create a daily reminder:

```json
{
  "label": "Daily Chronicle Optimization",
  "type": "shell",
  "command": "echo",
  "args": [
    "⏰ Time for daily optimization! Run these in Copilot Chat:",
    "/chronicle tips",
    "(Copy & paste the command above)"
  ],
  "presentation": {
    "reveal": "always",
    "panel": "shared"
  },
  "runOptions": {
    "runOn": "default"
  }
}
```

Then set a VS Code reminder to run this task daily at 8 AM.

---

## Quick Reference Card

**Print or bookmark this:**

```
┌─────────────────────────────────────────────────────────┐
│         DAILY CHRONICLE AUTOMATION COMMANDS              │
├─────────────────────────────────────────────────────────┤
│ EVERY MORNING:    /chronicle tips                       │
│ EVERY FRIDAY:     /chronicle standup                    │
│ MONTHLY (1st Fri): /chronicle search "routing accuracy" │
│                                                          │
│ WHEN SESSIONS HIT 20+ TURNS:  /compact                 │
│                                                          │
│ Expected Result: 30-40% token reduction in 4 weeks      │
└─────────────────────────────────────────────────────────┘
```

---

## Troubleshooting

**Q: Can I automate these without manual triggers?**  
A: Not directly—`/chronicle` are chat commands requiring Copilot Chat active. However, agents will **proactively remind** you at optimal times (see "Automated Reminders" section above).

**Q: What if I miss a day?**  
A: No problem. `/chronicle tips` analyzes the last 7 days, so you'll still get patterns from missed days.

**Q: How do I verify the 30-40% reduction is working?**  
A: Run `/chronicle standup` on Friday and compare Haiku tokens to Premium tokens. Should be ~80/20 split.

**Q: Can I customize the timing?**  
A: Yes! Edit the `trigger:` field above and update agent instructions in `.github/copilot-instructions.md`.

---

## Status

- ✅ `/chronicle tips` implemented
- ✅ `/chronicle standup` implemented  
- ✅ `/chronicle search` implemented
- ✅ Agent proactive reminders ready
- ✅ Model routing integrated
- ⏳ Daily execution (manual triggers, agent-guided)

**Next step:** Start tomorrow morning with `/chronicle tips` and track the metrics!
