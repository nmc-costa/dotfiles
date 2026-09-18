---
name: [SKILL_NAME]
description: "[Brief description of what this skill does]"
status: "template"
version: "1.0"
triggers:
  - "[skill activation trigger]"
related_agents:
  - "[agent that uses this skill]"
dependencies:
  - "[tool or library required]"
---

# [Skill Name]

**Purpose**: [One-sentence description of what this skill accomplishes]

**Related**: Used by agents in `.agents/skills/` (agents and skills are unified under one directory in this repo)

---

## What This Skill Does

[Paragraph explaining the skill's purpose and capabilities]

### Key Capabilities

- **Capability 1**: [Description]
- **Capability 2**: [Description]  
- **Capability 3**: [Description]

---

## How Agents Use This Skill

Agents reference this skill like this:

```markdown
## Skills This Agent Uses

- [`skill-name`](../../skills/{skill-name}/SKILL.md)
  - Implements [what capability]
  - Called during [phase/step]
```

---

## Workflow

### Phase 1: Input
- Accept [input type]
- Validate [constraints]

### Phase 2: Processing
- [Process step 1]
- [Process step 2]
- [Process step 3]

### Phase 3: Output
- Generate [output type]
- Format as [format]
- Save to [location]

---

## Configuration

### Required Parameters
```json
{
  "param_1": "description",
  "param_2": "description",
  "param_3": "description"
}
```

### Optional Parameters
```json
{
  "opt_param_1": "description (default: value)",
  "opt_param_2": "description (default: value)"
}
```

---

## Examples

### Example 1: [Use Case 1]

```python
# Pseudocode showing how to use this skill
from skills.skill_name import skill_function

result = skill_function(
    input_data=data,
    param_1="value_1",
    param_2="value_2"
)
```

### Example 2: [Use Case 2]

[Another example demonstrating different usage pattern]

---

## Standards & Compliance

This skill enforces:
- ✅ [Standard 1]
- ✅ [Standard 2]
- ✅ [Standard 3]

---

## Dependencies

 HEAD
- **Tool**: `tool-name` (see `../../tools/{tool-name}/`) — What it provides
- **Library**: `package-name` — What it provides
- **Skill**: `other-skill-name` (see `../other-skill-name/`) — What it provides
 origin/main

---

## Related Resources

- Master Persona: [`instructions/base-personas/archi.md`](../../instructions/base-personas/archi.md)
- Agents that use this: `.agents/skills/` (agents and skills are unified under one directory in this repo)
- Registry: `.agents/skills/` (no central registry file in this repo; browse skill directories directly)

---

**Status**: Template (Customize for your skill)  
**Version**: 1.0  
**Last Updated**: 2026-08-25
