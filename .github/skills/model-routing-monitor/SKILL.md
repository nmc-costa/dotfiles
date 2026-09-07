# Model Routing Monitor (Session Analytics)

Autonomous skill for monitoring and verifying the model routing rule effectiveness through real session data analysis.

## When to use this skill

Invoke this skill automatically when:
- Performing weekly session analytics and token usage reviews
- Comparing actual model assignments against routing rule predictions
- Calculating token reduction metrics (target: ~30-40% savings)
- Generating routing compliance reports
- Debugging routing rule mismatches

## Autonomous Workflow Steps

### 1. **Session Store Query** (Collect baseline data)
Use `session_store_sql` tool with DuckDB queries:
- Query all sessions in the time window (default: past 7 days)
- Extract model assignments from `turns` table
- Aggregate token counts by model (Haiku vs. Expensive models)
- Calculate cost per task

Example query structure:
```sql
SELECT 
  sessions.id,
  turns.model,
  COUNT(*) as turn_count,
  SUM(turns.token_usage) as total_tokens
FROM sessions
LEFT JOIN turns ON sessions.id = turns.session_id
WHERE sessions.created_at >= now() - INTERVAL '7 days'
GROUP BY sessions.id, turns.model
```

### 2. **Routing Compliance Analysis**
- Compare actual model assignments with routing rule predictions
- Identify misrouted tasks (expensive model used for Haiku-eligible task)
- Calculate accuracy percentage: (correct_routes / total_tasks) × 100

### 3. **Token Reduction Calculation**
- **Baseline:** Sum total tokens for all tasks
- **Current:** Sum tokens filtered by model type
- **Delta:** (Expensive tokens - Current expensive tokens) / Baseline tokens
- **Goal:** Achieve ≥ 30% reduction in expensive model usage

### 4. **Generate Compliance Report**
Auto-generate markdown report with:
- Total tasks processed
- Routing accuracy (%)
- Token counts by model
- Cost savings realized
- Misroute patterns (if any)
- Recommendations for rule refinement

## Tool Usage

### Primary Tools
- `session_store_sql` — Query session store with DuckDB
  - Action: `query` (default)
  - Use action: `reindex` if rebuilding index needed
  
### Output
- JSON report: `routing_compliance_report_YYYYMMDD.json`
- Markdown summary: `routing_compliance_YYYYMMDD.md`
- Visualization: Token reduction graph

## Success Criteria

✅ **Phase 2 (Monitoring):**
- Collect ≥1 week of real session data
- Achieve ≥95% accuracy in routing rule enforcement
- Generate baseline token metrics

✅ **Phase 3 (Validation):**
- Verify 30-40% token reduction achieved
- Identify any systemic routing failures
- Provide actionable insights for rule optimization

## Rule Reference

### Haiku Tasks (Expected: 80% of workload)
- Markdown editing, formatting, indentation fixes
- Grammar & spelling reviews
- Template-based conversions (md → docx, using helper scripts)
- Document structure validation (checking against templates)
- Content refinement & rephrasing
- Any task with predefined rules/scripts

### Expensive Model Tasks (Expected: 20% of workload)
- Architectural design & system design decisions
- Complex multi-step reasoning (race conditions, algorithm design)
- Content generation requiring domain expertise or novel thinking
- Strategic planning & high-level decisions
- Debugging complex logic or integrations
- Validation against business requirements (semantic analysis required)
