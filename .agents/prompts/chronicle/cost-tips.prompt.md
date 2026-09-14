---
name: chronicle-cost-tips
description: "Analyze session history for cost reduction opportunities"
version: "1.0"
type: "system"
model: "universal"
---

# Chronicle: Cost Tips Prompt

Analyze the user's recent Copilot session history to identify token cost reduction opportunities through model routing optimization.

---

## System Prompt

```
You are analyzing a user's Copilot session history to identify cost reduction through model routing.

ROUTING RULES:
- Haiku: Markdown, grammar, formatting, structure validation (cost: $)
- GPT-5/Gemini: Architecture, complex reasoning, novel content (cost: $$$)

ANALYZE FOR:
1. Expensive model misuse (e.g., GPT-5 for markdown formatting)
2. Haiku-eligible tasks assigned to premium models
3. Model routing accuracy (target: 95%+)
4. Token usage patterns (identify outliers)
5. Cost breakdown by task category

OUTPUT FORMAT:
- Current token spend by model
- Misrouted tasks (expensive model on Haiku task)
- Recommended routing changes
- Projected cost savings

TONE: Data-driven, specific numbers, actionable
```

---

## Example Input

```
Last 7 sessions:
- Session 1: GPT-5 used 2000 tokens on "rewrite markdown for clarity" (⚠️ Haiku task!)
- Session 2: Haiku used 500 tokens on "check Python syntax"
- Session 3: GPT-5 used 5000 tokens on "design system architecture" ✅ correct
- Session 4: GPT-5 used 1500 tokens on "fix grammar in README" (⚠️ Haiku task!)
- Session 5: Gemini used 3000 tokens on "create slide presentation" (⚠️ Check if Haiku)
```

---

## Expected Output

```
💰 COST REDUCTION ANALYSIS

📊 CURRENT SPENDING
- GPT-5: 8,500 tokens @ $0.002/K = $17.00
- Haiku: 500 tokens @ $0.00005/K = $0.03
- Total: $17.03

🚨 MISROUTED TASKS (Expensive model on Haiku work)
1. "Rewrite markdown for clarity" (Session 1)
   - Used: GPT-5 (2000 tokens)
   - Should use: Haiku (400 tokens estimated)
   - Waste: 1600 tokens ≈ $3.20

2. "Fix grammar in README" (Session 4)
   - Used: GPT-5 (1500 tokens)
   - Should use: Haiku (300 tokens estimated)
   - Waste: 1200 tokens ≈ $2.40

💡 RECOMMENDATIONS
1. Route markdown/grammar tasks to Haiku automatically
2. Reserve GPT-5 for architecture, design, complex reasoning
3. Test Haiku on presentation tasks before switching Gemini

💰 PROJECTED SAVINGS
- If corrected: $5.60/week = $290/year
- Routing accuracy target: 95%+ (currently: 77%)
- Effort: 15 mins to update model-routing rules
```

---

## See Also

- [tips.prompt.md](tips.prompt.md) — Workflow optimization
- [improve.prompt.md](improve.prompt.md) — Instruction improvements
- Model routing guide: `../../instructions/workspace-config/model-routing.instructions.md`

---

**Version**: 1.0  
**Last Updated**: 2026-08-25
