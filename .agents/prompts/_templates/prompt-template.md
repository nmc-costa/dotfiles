---
name: [PROMPT_NAME]
description: "[Brief description of what this prompt does]"
version: "1.0"
type: "[system|user|workflow]"
model: "[claude|gpt|gemini|universal]"
use_cases:
  - "[Use case 1]"
  - "[Use case 2]"
---

# [Prompt Name]

**Purpose**: [One-sentence description]

**Best For**: [Which agents/scenarios should use this]

---

## Template

```
[SYSTEM PROMPT HEADER]

[Core instruction]

[Constraints]

[Output format]

[Examples]
```

---

## Customization Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `{variable_1}` | What to fill in | `value_1` |
| `{variable_2}` | What to fill in | `value_2` |
| `{variable_3}` | What to fill in | `value_3` |

---

## How to Use

### 1. Copy the template above
### 2. Replace variables with your values
### 3. Pass to LLM as system prompt or user message
### 4. Process response according to "Output Format"

---

## Related Prompts

- [`prompt-name-2.md`]() — When to use instead
- [`prompt-name-3.md`]() — Similar pattern, different domain

---

## See Also

- Prompt Index: `.agents/prompts/` (no central registry file in this repo)
- Related Skills: [`.agents/skills/`](../../skills/)
- All Templates: [`../`](./)

---

**Version**: 1.0  
**Status**: Template  
**Last Updated**: 2026-08-25
