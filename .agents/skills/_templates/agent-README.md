# 🤖 Agent Templates

**Purpose**: Template and reference structure for creating new agents.

---

## What Is an Agent?

An agent is a specialized worker that extends the master persona (`archi.md`) with domain-specific capabilities. Agents:

- Inherit biofeedback headers and dialectical reasoning from `archi.md`
- Handle specific types of work (@projectHITs, @presentHITs, etc.)
- Use skills and tools to accomplish tasks
- Report progress via calibration headers

---

## Creating a New Agent

### Step 1: Copy Template
```bash
cp agent-template.md ../{agent-name}.md
```

### Step 2: Customize
1. Replace `[AGENT_NAME]` with your agent name
2. Update triggers (`@[agent-trigger]`)
3. Define capabilities specific to your domain
4. Add standards your agent enforces

### Step 3: Create Agent Directory
```bash
mkdir -p ../{agent-name}/
echo "# {Agent Name}" > ../{agent-name}/README.md
```

### Step 4: Link to Skills & Tools
Reference skills and tools your agent uses:
```markdown
## Skills This Agent Uses
- [`skill-name`](../../skills/{skill-name}/SKILL.md)

## Tools This Agent Accesses
- [`tool-name`](../../tools/{tool-name}/)
```

### Step 5: Register in REGISTRY
Add entry to `.agents/skills/` (no central registry file; just add a new skill directory):
```markdown
| **{Agent Name}** | `agents/{agent-name}.md` | {parent-persona} | ✅ Status |
```

---

## Standard Agent Template Structure

```
agents/
├── _templates/
│   ├── agent-template.md (this file's template)
│   └── README.md (this file)
│
├── architect/
│   ├── SKILL.md (agent definition)
│   └── README.md (documentation)
│
├── projectHITs/
│   ├── SKILL.md
│   └── README.md
│
└── [other agents]/
    ├── SKILL.md
    └── README.md
```

---

## Key Fields to Customize

| Field | Description | Example |
|-------|-------------|---------|
| `name` | Agent identifier | `projectHITs` |
| `description` | What the agent does | "Charter Architect - Creates project charters using Mirror Architect pattern" |
| `triggers` | How to activate the agent | `@projectHITs`, `create charter`, `new project` |
| `capabilities` | What the agent can do | `Mirror templates`, `Auto-fill from brief`, `Generate completion checklist` |
| `MODE` | Operational mode from `archi.md` | `ARCHITECT_ANALYST`, `MIRROR_ARCHITECT`, `WEAVER` |

---

## Inheriting from Master Persona

All agents inherit the Output Frame header by reference (never a pasted copy) — pick `archi-family` (as [`archi.md`](../../instructions/base-personas/archi.md) does) or `none`:

```
Header: inherits OUTPUT-FRAME (~/.agents/instructions/workspace-config/output-frame.instructions.md).
MODE = `YOUR_MODE`; Focus default = `{Concept}`.
Persona extension = archi-family (always full header + DIALECTIC) | none.
```

This ensures:
- ✅ Consistent operational protocol across all agents
- ✅ Dialectical reasoning (Thesis → Antithesis → Synthesis)
- ✅ Transparency about confidence and focus
- ✅ Compatibility with harnesses (VS Code, Claude Code, Gemini, OpenAI, LiteLLM)

---

## Best Practices

1. **Start with the template** — Don't create agents from scratch
2. **Document triggers clearly** — Users need to know how to activate
3. **Define capabilities explicitly** — List what the agent can do
4. **Link to standards** — Reference which rules the agent enforces
5. **Create agent directory** — Each agent should have its own folder with README.md
6. **Register in REGISTRY** — Add to central discovery index
7. **Use consistent mode** — Pick a MODE from archi.md and stick with it

---

## See Also

- [`instructions/base-personas/archi.md`](../../instructions/base-personas/archi.md) — Master persona all agents inherit from
- `.agents/skills/` (no central registry file in this repo; browse skill directories directly) — Central index of all agents
- [`skills/`](../../skills/) — Skills agents can use
- `.agents/skills/` (this repo has no separate tools/ dir; see `.agents/skills/calls2database/` for a tool-like skill) — Tools agents can access

---

**Version**: 1.0  
**Status**: Template Reference  
**Last Updated**: 2026-08-25
