# 📊 Chronicle Prompts

**Purpose**: Reusable prompts for session analysis and workspace optimization via the `/chronicle` workflow.

---

## What Are Chronicle Prompts?

Chronicle prompts analyze Copilot session history to generate:
- **Tips**: Workflow optimization recommendations
- **Cost-Tips**: Token cost reduction opportunities
- **Improve**: Workspace instruction improvements
- **Standup**: Daily/weekly work summary reports

---

## Available Prompts

| Prompt | Purpose | Output | Frequency |
|--------|---------|--------|-----------|
| [`tips.prompt.md`](tips.prompt.md) | Workflow patterns & efficiency | 3-5 recommendations | Weekly |
| [`cost-tips.prompt.md`](cost-tips.prompt.md) | Token cost reduction | Model routing fixes & savings | Weekly |
| [`improve.prompt.md`](improve.prompt.md) | Instruction improvements | Skill/agent/doc enhancements | Weekly |
| [`standup.prompt.md`](standup.prompt.md) | Work summary & progress | Standup report | Daily/Weekly |

---

## How to Use

### Via `/chronicle` Command (Automatic)

```bash
/chronicle tips        # Run tips prompt on session history
/chronicle cost-tips   # Analyze cost optimization opportunities
/chronicle improve     # Suggest workspace improvements
/chronicle standup     # Generate standup report
```

These commands:
1. Pull session data from session store
2. Load appropriate prompt template
3. Pass to LLM for analysis
4. Generate report automatically

### Manual Usage

If you want to run these prompts manually:

```python
from tools.chronicle import ChronicleAnalyzer

analyzer = ChronicleAnalyzer()

# Load a prompt template
tips_prompt = analyzer.load_prompt("tips")

# Get session data
sessions = analyzer.get_recent_sessions(days=7)

# Generate analysis
result = analyzer.analyze(prompt=tips_prompt, sessions=sessions)
```

---

## Integration with Daily Optimization

These prompts are part of the daily optimization workflow:

```bash
/chronicle reindex      # Update session store
/chronicle tips         # Workflow optimization
/chronicle cost-tips    # Cost analysis
/chronicle improve      # Instruction improvements
```

See: `.agents/instructions/workspace-config/daily-optimization.instructions.md`

---

## Customization

### Override Default Model

Some prompts work better with specific models:

```python
analyzer.analyze(
    prompt=prompt,
    sessions=sessions,
    model="gpt-4-turbo",  # For complex analysis
    temperature=0.7
)
```

### Time Range

```python
# Last 7 days (default)
sessions = analyzer.get_recent_sessions(days=7)

# Custom date range
sessions = analyzer.get_sessions_in_range(
    start_date="2026-08-18",
    end_date="2026-08-25"
)
```

---

## Output Examples

### Tips Output
```
📊 WORKFLOW OPTIMIZATION TIPS

🔍 Finding 1: Sequential reads inefficient
- Pattern: 5 grep_search → manual read_file calls
- Impact: Save ~15 mins per session
- Recommendation: Use parallel batch operations
```

### Cost-Tips Output
```
💰 COST REDUCTION ANALYSIS

🚨 MISROUTED TASKS
- "Fix markdown grammar" used GPT-5 (cost: $3.20)
- Should use: Haiku (cost: $0.05)
- Savings potential: $5.60/week
```

### Improve Output
```
🔧 WORKSPACE IMPROVEMENTS

📋 Finding 1: Skill not discovered
- Issue: User doesn't know about new skill
- Recommendation: Update the relevant skill's own README (no central registry file in this repo)
- Location: `.agents/skills/<skill-name>/`
```

### Standup Output
```
📋 DAILY STANDUP — August 25

✅ COMPLETED
- Reorganized agentic_instructions v2.0 ✅
- Created templates and harness configs ✅

🔄 IN PROGRESS
- Phase 4 final touches

⏭️ NEXT STEPS
- Git commit and push
```

---

## Related

- Daily optimization: `.agents/instructions/workspace-config/daily-optimization.instructions.md`
- Session analysis: `.agents/skills/calls2database/`
- Prompts template: `../_templates/prompt-template.md`

---

**Version**: 1.0  
**Status**: Ready to use  
**Last Updated**: 2026-08-25
