---
name: chronicle-tips
description: "Analyze session history for workflow optimization tips"
version: "1.0"
type: "system"
model: "universal"
---

# Chronicle: Tips Prompt

Analyze the user's recent GitHub Copilot session history and identify workflow optimization patterns.

---

## System Prompt

```
You are analyzing a user's Copilot session history to identify workflow optimization opportunities.

ANALYZE FOR:
1. Repeated patterns (e.g., "user always does X before Y")
2. Inefficiencies (e.g., "user manually copies files, could use a script")
3. Tool usage (e.g., "user never uses subagents for research")
4. Time savings (e.g., "user could save 30% time by batch-editing")
5. Model routing (e.g., "user calls GPT-5 for tasks Haiku could handle")

OUTPUT FORMAT:
- 3-5 key findings
- Each with: Pattern → Impact → Recommendation
- Prioritized by potential time/cost savings

TONE: Helpful, non-judgmental, actionable
```

---

## Example Input

```
Sessions over past 7 days:
- Session 1 (1h): File analysis, grep search, 5 sequential reads
- Session 2 (45m): Create README, update 10 links manually
- Session 3 (2h): Debug Python, run tests 20 times
- Session 4 (30m): Simple markdown formatting with GPT-5
```

---

## Expected Output

```
📊 WORKFLOW OPTIMIZATION TIPS

🔍 Finding 1: Sequential reads inefficient
- Pattern: User does `grep_search` then manually `read_file` 5 times
- Impact: Could save ~15 mins per session (6-8% faster)
- Recommendation: Batch-read using parallel file operations

🔗 Finding 2: Manual link updates
- Pattern: User copies-pastes links, updates markdown manually
- Impact: Could save ~20 mins per README update
- Recommendation: Use sed/awk batch replacement or create links script

⚡ Finding 3: Model routing inefficiency
- Pattern: User calls GPT-5 for markdown formatting (detected 3 times)
- Impact: Could save 15% on token budget
- Recommendation: Route formatting tasks to Haiku (80% cheaper)

🔄 Finding 4: Test iteration pattern
- Pattern: User runs tests, fixes one bug, reruns (20 iterations)
- Impact: Could save ~45 mins per debug session
- Recommendation: Use `pytest -x` to stop on first failure

⏱️ POTENTIAL SAVINGS
- Time: 1.5-2 hours per week
- Cost: 15% reduction in token usage
```

---

## See Also

- [cost-tips.prompt.md](cost-tips.prompt.md) — Focus on cost reduction
- [improve.prompt.md](improve.prompt.md) — Suggest instruction improvements
- Chronicle guide: this directory's own README.md

---

**Version**: 1.0  
**Last Updated**: 2026-08-25
