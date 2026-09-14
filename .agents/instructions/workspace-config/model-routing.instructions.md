---
applyTo: "**"
---

# Model Routing Instructions

This document elaborates on the Model Routing rules defined in `copilot-instructions.md`.

## When These Instructions Apply

These instructions apply to **every agent interaction** across the workspace. The agent should autonomously apply these routing rules without explicit prompting.

## Routing Decision Logic

### **Use Claude Haiku for:**
- Markdown editing, formatting, indentation fixes
- Grammar & spelling reviews
- Template-based conversions (md → docx, using helper scripts)
- Document structure validation (checking against templates)
- Content refinement & rephrasing
- Any task with predefined rules/scripts (no discovery needed)

### **Use GPT-5 or Gemini for:**
- Architectural design & system design decisions
- Complex multi-step reasoning (race conditions, algorithm design)
- Content generation that requires domain expertise or novel thinking
- Strategic planning & high-level decisions
- Debugging complex logic or integrations
- Validation against business requirements (requires semantic analysis, not just template checking)

## Autonomous Routing Workflow

The agent should follow this logic automatically for every task request:

1. **Task Classification:** Analyze the user's request and categorize it into one of the above buckets.
2. **Model Selection:** Select the appropriate model based on the category.
3. **Silent Execution:** Execute the task using the selected model without announcing the routing decision (unless relevant for transparency).
4. **Result Delivery:** Return results with same quality, regardless of model chosen.

## Distinction: Template vs. Semantic Validation

This is the critical differentiator for ambiguous tasks:

| Validation Type | Definition | Model |
|-----------------|-----------|-------|
| **Template Validation** | Does the document follow the predefined structure? (sections present, hierarchy correct, formatting rules met) | Claude Haiku |
| **Semantic Validation** | Does the document align with business requirements and project brief? (requires interpretation, domain knowledge, logical reasoning) | GPT-5 / Gemini |

### Example:
- **Task:** "Validate WP1.md"
  - If asking: "Is it in the right structure?" → Haiku (template check)
  - If asking: "Does it align with the project brief?" → GPT-5 (semantic check)

## Integration with Skills and Workflows

Skills in `.github/skills/` inherit these routing rules. For example:

- `project-doc-lifecycle/SKILL.md` uses Haiku for template-based doc conversion
- Any complex research delegated to `runSubagent` should respect these guidelines

## Monitoring & Verification

The session store queries in `token-tracking.instructions.md` track model usage to verify this routing is working as intended. Expected outcome: ~30-40% reduction in premium model usage.
