# 💡 Skill Templates

**Purpose**: Template and reference structure for creating reusable skills.

---

## What Is a Skill?

A skill is a reusable capability that agents invoke to accomplish specific tasks. Skills:

- Encapsulate domain-specific logic
- Can be used by multiple agents
- Accept well-defined inputs and produce outputs
- Are registered in the central REGISTRY

---

## Creating a New Skill

### Step 1: Copy Template
```bash
cp skill-template.md ../{skill-name}/SKILL.md
```

### Step 2: Customize
1. Replace `[SKILL_NAME]` with your skill name
2. Update triggers (how agents activate this skill)
3. Define what the skill does and how
4. Document parameters and outputs

### Step 3: Create Skill Directory
```bash
mkdir -p ../{skill-name}/
echo "# {Skill Name}" > ../{skill-name}/README.md
touch ../{skill-name}/examples.md
```

### Step 4: Document Examples
Create `examples.md` with real usage patterns showing:
- Input data
- Parameters
- Expected output

### Step 5: Register in REGISTRY
Add entry to `.agents/skills/` (no central registry file; just add a new skill directory):
```markdown
| **{Skill Name}** | `skills/{skill-name}/SKILL.md` | {Purpose} | {Examples} |
```

---

## Standard Skill Structure

```
skills/
├── _templates/
│   ├── skill-template.md (template definition)
│   └── README.md (this file)
│
├── project-doc-lifecycle/
│   ├── SKILL.md (skill definition)
│   ├── README.md (documentation)
│   └── examples/ (example implementations)
│
├── simplifyHIT/
│   ├── SKILL.md
│   ├── README.md
│   └── examples/
│
└── [other skills]/
    ├── SKILL.md
    ├── README.md
    └── examples/
```

---

## Key Differences: Skills vs Tools vs Agents

| Aspect | Skill | Tool | Agent |
|--------|-------|------|-------|
| **Definition** | Reusable capability | External service/library | Orchestrator using skills+tools |
| **Scope** | Domain logic (e.g., doc templating) | External integration (e.g., API) | High-level workflow |
| **Reusability** | Used by many agents | Used by skills & agents | Typically one-to-one with task |
| **Example** | "Mirror template from DOCX" | "Call Gemini API" | "Create project charter" |

---

## Skill Lifecycle

### 1. Design
- Identify reusable capability
- Define inputs and outputs
- Check if similar skill exists

### 2. Document
- Write SKILL.md from template
- Create examples
- Document parameters

### 3. Implement
- Write actual code/logic
- Add to examples/
- Test with real agents

### 4. Register
- Note it in this skill's own README (no central registry file in this repo)
- Link from related agents
- Announce availability

### 5. Maintain
- Monitor usage
- Refine based on feedback
- Update documentation

---

## Best Practices

1. **Single responsibility** — One skill = one capability
2. **Clear inputs/outputs** — Document exactly what the skill needs and produces
3. **Reusable** — Design so multiple agents can use it
4. **Testable** — Provide examples agents can copy
5. **Documented** — Include real-world usage patterns
6. **Discovered** — Register in REGISTRY and link from agents
7. **Version tracked** — Track changes and deprecations

---

## Common Skill Patterns

### Pattern 1: Data Transformation
```
Input: Raw data (email, markdown, JSON)
↓
Skill: Normalize → Validate → Transform
↓
Output: Structured data (config, template, artifact)
```

### Pattern 2: Template Manipulation
```
Input: Base template + new content
↓
Skill: Parse → Map → Fill → Preserve structure
↓
Output: Updated template (DOCX, PDF, HTML)
```

### Pattern 3: Analysis & Reporting
```
Input: Codebase / documents / metrics
↓
Skill: Scan → Analyze → Categorize → Rank
↓
Output: Report with findings & recommendations
```

---

## See Also

- `.agents/skills/` (agents and skills are unified under one directory in this repo) — Agents that use skills
- `.agents/skills/` (this repo has no separate tools/ dir; see `.agents/skills/calls2database/` for a tool-like skill) — External tools skills integrate with
- `.agents/skills/` (no central registry file in this repo; browse skill directories directly) — Central skill index
- [`instructions/base-personas/archi.md`](../../instructions/base-personas/archi.md) — Operational standards

---

**Version**: 1.0  
**Status**: Template Reference  
**Last Updated**: 2026-08-25
