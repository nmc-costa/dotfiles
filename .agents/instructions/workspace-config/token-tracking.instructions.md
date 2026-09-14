---
applyTo: "**"
---

# Token Tracking & Routing Compliance Instructions

Standardized methodology for tracking token usage across sessions and monitoring model routing rule effectiveness.

## Tracking Methodology

### 1. Session-Level Metrics
For every session, automatically capture:
- **Session ID:** Unique identifier from session store
- **Model Assignments:** List of (task_id, assigned_model, expected_model)
- **Token Usage:** Total tokens consumed, broken down by model type
- **Duration:** Session start → completion time
- **Routing Accuracy:** % of tasks routed correctly per routing rule

### 2. Task-Level Classification

Each task must be classified into one of two categories:

**Category A: Haiku-Eligible (Predefined rules, low complexity)**
- Token budget: ~100-500 tokens per task
- Model assignment: Claude Haiku
- Tasks:
  - Markdown editing & formatting
  - Grammar & spelling reviews
  - Template validation
  - Document structure checks
  - Content refinement (clarity, conciseness)
  - Script-based conversions (md → docx)

**Category B: Expensive-Model Tasks (Discovery, complexity, domain expertise)**
- Token budget: ~1000-5000 tokens per task
- Model assignment: GPT-5 or Gemini
- Tasks:
  - Architectural design
  - Complex multi-step reasoning
  - Novel content generation with domain expertise
  - Strategic planning
  - Complex debugging & integrations
  - Validation requiring semantic analysis

### 3. Token Attribution

When logging tokens, track:
```json
{
  "session_id": "uuid",
  "timestamp": "2026-08-25T14:30:00Z",
  "task": {
    "id": "task_identifier",
    "category": "A or B",
    "expected_model": "claude_haiku or gpt5_or_gemini"
  },
  "actual_model": "actual model used",
  "tokens": {
    "input": 150,
    "output": 320,
    "total": 470
  },
  "routing_correct": true_or_false,
  "cost_estimate_usd": 0.00XX
}
```

## Weekly Review Cadence

### Monday Report (Start of Week)
1. Query baseline metrics from previous week
2. Compare with target routing accuracy (95%+)
3. Identify any systemic routing failures

### Friday Analysis (End of Week)
1. Aggregate all sessions from the week
2. Calculate token reduction: (expensive_tokens_baseline - expensive_tokens_current) / baseline
3. Update tracking dashboard

### Monthly Assessment (Last Friday)
1. Calculate 4-week rolling average
2. Verify 30-40% reduction target on track
3. Identify rules needing refinement

## Query Patterns (DuckDB via session_store_sql)

### Get Token Usage by Model (Past 7 Days)
```sql
SELECT 
  t.model,
  COUNT(*) as task_count,
  SUM(t.token_usage) as total_tokens,
  AVG(t.token_usage) as avg_tokens_per_task,
  ROUND(SUM(t.token_usage) * 0.000001, 2) as cost_estimate_usd
FROM turns t
JOIN sessions s ON t.session_id = s.id
WHERE s.created_at >= now() - INTERVAL '7 days'
GROUP BY t.model
ORDER BY total_tokens DESC
```

### Calculate Routing Accuracy
```sql
SELECT 
  COUNT(*) as total_tasks,
  SUM(CASE WHEN routing_correct = true THEN 1 ELSE 0 END) as correct_routes,
  ROUND(SUM(CASE WHEN routing_correct = true THEN 1 ELSE 0 END)::float / COUNT(*) * 100, 2) as accuracy_percent
FROM routing_log
WHERE logged_at >= now() - INTERVAL '7 days'
```

### Identify Misrouted Tasks (Expensive model used for Haiku tasks)
```sql
SELECT 
  task_id,
  expected_model,
  actual_model,
  token_usage,
  ROUND(token_usage * 0.000001, 6) as wasted_cost_usd
FROM routing_log
WHERE expected_model = 'claude_haiku'
  AND actual_model IN ('gpt5', 'gemini')
  AND logged_at >= now() - INTERVAL '7 days'
ORDER BY token_usage DESC
```

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Routing Accuracy** | ≥95% | % of tasks routed per rule |
| **Token Reduction** | 30-40% | Decrease in expensive model tokens |
| **Haiku Assignment Rate** | 80% | % of tasks using Haiku |
| **Average Task Tokens (Haiku)** | <500 | Total tokens per Haiku task |
| **Misroute Detection** | <5% | Tasks incorrectly routed |
| **Weekly Improvement** | +2-5% | Accuracy improvement per week |

## Troubleshooting Routing Failures

### If Haiku tasks are being misrouted to expensive models:
1. Check task category classification (is it truly Haiku-eligible?)
2. Review task description for hidden complexity indicators
3. Update routing rule boundaries if edge case identified
4. Document exception in routing_exceptions.md

### If expensive model tasks are being misrouted to Haiku:
1. Immediately escalate to human review (Haiku may underperform)
2. Check if task is at boundary (70-80% complexity)
3. Reclassify as Category B if needed
4. Retrain rule with new examples

## Integration Points

- **Copilot System:** Auto-log every task routing decision via model selection logging
- **Session Store:** Query turns table for token counts and model assignments
- **Reporting:** Generate weekly markdown reports in `docs/routing_compliance/`
- **Dashboards:** Feed metrics to monitoring systems for visualization

## Document Versioning

- **v1.0** (2026-08-25): Initial routing compliance tracking
- **v1.1** (TBD): Add cost attribution per department/project
- **v1.2** (TBD): Implement real-time alerts for routing anomalies
