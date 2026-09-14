# 🔧 Tool Templates

**Purpose**: Template and reference structure for integrating external tools.

---

## What Is a Tool?

A tool is an external service, library, or API that agents and skills use to accomplish work. Tools:

- Integrate with external systems (APIs, databases, services)
- Provide capabilities agents don't have built-in
- Can be used by multiple agents and skills
- Are registered in the central REGISTRY

---

## Difference: Tool vs Skill

| Aspect | Tool | Skill |
|--------|------|-------|
| **What is it?** | External service/library | Domain logic using tools |
| **Example** | Gemini API, python-docx | "Mirror template from DOCX" |
| **Integration** | Direct API calls | Orchestration + tools |
| **Scope** | Single function (e.g., "call API") | Domain workflow (e.g., "create charter") |

---

## Creating a New Tool Integration

### Step 1: Copy Template
```bash
cp tool-template.md ../{tool-name}/README.md
```

### Step 2: Customize
1. Add tool name and description
2. Document installation steps
3. Provide API reference
4. Add error handling guide
5. Link from using agents/skills

### Step 3: Create Tool Directory
```bash
mkdir -p ../{tool-name}/
touch ../{tool-name}/examples.py
touch ../{tool-name}/config.json
```

### Step 4: Document Examples
Create `examples/` with working code samples:
- Basic usage
- Error handling
- Common patterns

### Step 5: Register in REGISTRY
Add entry to `.agents/skills/` (no central registry file; just add a new skill directory):
```markdown
| **{Tool Name}** | `tools/{tool-name}/` | {Purpose} | {Status} |
```

---

## Standard Tool Structure

```
tools/
├── _templates/
│   ├── tool-template.md (template definition)
│   └── README.md (this file)
│
├── calls2database/
│   ├── README.md (tool definition & API)
│   ├── examples/ (usage examples)
│   └── config.json (default config)
│
└── [other tools]/
    ├── README.md
    ├── examples/
    └── config.json
```

---

## Common Tool Patterns

### Pattern 1: API Integration
```
Agent → Skill → Tool → External API → Result
Example: Call Gemini API for content generation
```

### Pattern 2: Library Wrapper
```
Agent → Skill → Tool (wrapper) → Python library → Result
Example: python-docx for DOCX file manipulation
```

### Pattern 3: Service Integration
```
Agent → Skill → Tool → Database / Cloud Service → Result
Example: Connect to project database, fetch schema
```

---

## Best Practices

1. **Single responsibility** — One tool = one external system
2. **Clear API** — Document all methods and parameters
3. **Error handling** — List common errors and fixes
4. **Examples** — Provide working code samples
5. **Discoverable** — Register in REGISTRY and link from agents
6. **Config-driven** — Use JSON config, not hardcoded values
7. **Testable** — Include examples that agents can copy

---

## Tool Categories

### Data Sources
- Database connections
- File system access
- API data fetching

### File Manipulation
- DOCX/PDF editing (python-docx, pypdf)
- Markdown processing
- HTML generation

### External APIs
- Gemini, OpenAI, Claude APIs
- Cloud service integrations
- Third-party SaaS APIs

### Services
- GitHub integration
- CI/CD service APIs
- Deployment platforms

---

## See Also

- Skills: `.agents/skills/` — this repo folds tools into skills; see `calls2database`
- Skills: `.agents/skills/` — this repo has no separate agents/ dir; agent-like orchestration lives in skills such as `archi`
- Skill Index: `.agents/skills/` — no central registry file in this repo
- Examples: Check specific tool folder for usage patterns

---

**Version**: 1.0  
**Status**: Template Reference  
**Last Updated**: 2026-08-25
