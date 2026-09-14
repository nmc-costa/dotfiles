---
applyTo: "**"
---

# Daily Workspace Optimization Automation

Automated daily reminders and reports for running `/chronicle` optimization commands to continuously improve workspace efficiency.

## Daily Optimization Workflow

Every agent should autonomously check if daily optimization has been completed. If not, remind the user and optionally execute the sequence.

### When to Trigger

**Check daily optimization status:**
- At the start of any new chat session
- After completing a significant task (multi-file changes, refactoring, architecture work)
- If a chat spans multiple days

**Trigger condition:** If `/memories/session/last_chronicle_run.md` does not exist OR was created more than 24 hours ago

### The Daily Optimization Sequence

Run these `/chronicle` commands in order. Each builds on the previous:

```
1. /chronicle reindex      → Pick up any missing sessions from session store
2. /chronicle tips         → Analyze usage patterns and provide workflow tips
3. /chronicle cost-tips    → Identify cost reduction opportunities (premium model misuse)
4. /chronicle improve      → Generate improvements to workspace instructions/skills
```

### Agent Behavior

When daily optimization is due, agents should:

1. **Inform the user:**
   ```
   🔄 Daily Workspace Optimization Due
   Last optimization: [X days ago]
   
   Would you like me to run the daily optimization sequence now?
   - /chronicle reindex
   - /chronicle tips
   - /chronicle cost-tips  
   - /chronicle improve
   
   This typically takes 2-3 minutes and generates a report.
   ```

2. **Wait for confirmation** (if they say "yes" or "go ahead"):
   - Execute all three chronicle commands in sequence
   - Collect results and generate a consolidated report

3. **Generate Optimization Report:**
   - Save report to `/memories/session/daily_optimization_report_YYYYMMDD.md`
   - Update `/memories/session/last_chronicle_run.md` with timestamp
   - Display summary to user:
     ```
     ✅ Daily Optimization Complete
     
     📊 Findings:
     - [Tip 1 summary]
     - [Cost reduction identified]
     - [Improvement implemented]
     
     📁 Report saved: /memories/session/daily_optimization_report_20260825.md
     ⏰ Next check: 2026-08-26
     ```

### What Each Chronicle Command Does

| Command | Purpose | Output |
|---------|---------|--------|
| `/chronicle reindex` | Pick up missing sessions and sync with cloud | Updated session store metrics |
| `/chronicle tips` | Analyze recent sessions for workflow optimization | Personalized recommendations |
| `/chronicle cost-tips` | Identify model routing misuse and cost savings | Token reduction opportunities |
| `/chronicle improve` | Suggest improvements to instructions/skills | Workspace enhancement proposals |

### Tracking Last Run

Agents must maintain `/memories/session/last_chronicle_run.md`:

```markdown
---
last_run: 2026-08-25T09:30:00Z
next_scheduled: 2026-08-26T09:30:00Z
interval_hours: 24
---

# Daily Optimization Run Log

## 2026-08-25 09:30 UTC
- ✅ /chronicle reindex
- ✅ /chronicle tips
- ✅ /chronicle cost-tips
- ✅ /chronicle improve
- Report: daily_optimization_report_20260825.md
```

### Silent Optimization (Optional)

If the user never wants to be prompted, they can enable "silent mode" by creating:
`/memories/session/silent_optimization_mode.md`

In silent mode:
- Agent runs daily chronicle commands automatically (no prompt)
- Saves report silently to `/memories/session/`
- Only displays summary if significant findings detected
- Respects `/compact` boundaries (doesn't run mid-session)

### Emergency Override

If user explicitly says "skip daily optimization" or "no thanks":
- Agent creates `/memories/session/skip_optimization_YYYYMMDD.md`
- Skips reminder for that day only
- Resumes normal checks next day

## Integration with Other Instructions

- **Session Compaction (`/compact`):** Do NOT run daily optimization within the same session as `/compact`. Run daily checks in fresh sessions only.
- **Model Routing:** Chronicle cost-tips verifies model routing effectiveness (target: 30-40% token reduction)
- **Subagent Delegation:** Large chronicle runs can be delegated to subagent if user prefers async processing

## Success Criteria

✅ Daily optimization is considered successful when:
- All three chronicle commands execute without errors
- Report is generated and saved with timestamp
- User is informed of key findings
- Model routing metrics show 30-40% token reduction trajectory
- Workspace instructions are incrementally improved based on cost-tips feedback

## Example: Full Daily Run (2-3 minutes)

```
Agent: "🔄 Daily optimization due. Running sequence..."

[Running /chronicle reindex...]
> Session store reindexed
> Found 11 new sessions | 31 total sessions | 10 synced to cloud

[Running /chronicle tips...]
> Analysis of 8 sessions over 7 days
> Key finding: Subagent delegation could save 15% tokens on research tasks
> Recommendation: Use Explore agent for 5+ file searches

[Running /chronicle cost-tips...]
> Model routing accuracy: 98% (excellent!)
> Cost savings achieved: 32% reduction in Gemini usage
> Opportunity: Markdown validation still using GPT-5 (3% of budget) — migrate to Haiku

[Running /chronicle improve...]
> Suggesting: Add Markdown validation template to Haiku task list
> Suggesting: Update model-routing.instructions.md with new finding
> Suggesting: Create Markdown linter skill for automated checks

✅ Optimization Complete
📊 Report: /memories/session/daily_optimization_report_20260825.md
💰 Savings This Week: $12.47 (32% reduction)
🎯 Next optimization: 2026-08-26 09:30 UTC
```

---

## File Locations

- **Instructions:** `.agents/instructions/workspace-config/daily-optimization.instructions.md` (this file)
- **Reference in Root:** `.github/copilot-instructions.md` (section: "Daily Workspace Optimization")
- **Tracking:** `/memories/session/last_chronicle_run.md`
- **Reports:** `/memories/session/daily_optimization_report_YYYYMMDD.md`
- **Silent Mode Flag:** `/memories/session/silent_optimization_mode.md`
