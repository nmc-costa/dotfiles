# STANDARDS.md

Naming, conventions, and standard directory structure for the `crush-config` (dotfiles) and `agent-framework` (agents) repositories.

**Community Standards Base:** LangChain, Mem0, Anthropic, GitHub Copilot, OpenAI Skills

> ⚠️ **Status (verified 2026-09-15):** This file mixes **real** structure (what actually exists today in `~/dotfiles`) with **proposed** structure (conventions designed but never implemented). Sections marked **[PROPOSED — not implemented]** below don't exist on this machine — confirmed via `ls`/`find` in the real repo. Treat the rest of this document as aspirational/partly outdated until it's fully reviewed (see `CLAUDE.md` § Known Gaps). The `agent-framework` repo mentioned throughout the document also doesn't exist as a separate repo on this machine — it's a proposed destination, not a current fact.

---

## 📋 GLOSSARY

| Term | Meaning | Example |
|-------|------------|---------|
| **Skill** | A discrete capability/tool an agent can use | `data-analyzer`, `web-research`, `code-reviewer` |
| **Agent** | An intelligent persona/entity with specific abilities | `architect`, `engineer`, `reviewer` |
| **Tool** | An executable function/API (synonym for skill in some contexts) | bash, grep, file-read |
| **Prompt** | An instruction/context template | system prompt, task instruction |
| **Instruction** | A domain-specific rule ("prompt" is preferred) | — |
| **Workflow** | A sequence of steps for an agent (don't use "instruction") | agent initialization, persona setup |
| **Framework** | A complete agent-orchestration system | agent-framework |
| **Config/Configuration** | A settings file or dotfiles | crush-config |

---

## 📁 DIRECTORY STRUCTURE

### Repository: `dotfiles` (Universal Configuration)

**Purpose:** Stable configuration, synced across machines. Universal for all agents (Crush, Copilot, Gemini, Cline, etc.)

**Current real structure** (verified 2026-09-15 — see `README.md` for the complete, always up-to-date tree):

```
dotfiles/
├── .agents/                     # Universal agents config (13 skills, incl. HITs + calls2database + _templates)
├── .claude/                     # Claude Code config (.claude/skills/ = symlinks into .agents/skills/)
├── .vscode/                     # VS Code config
├── .chezmoisource/              # chezmoi source dir (only .vscode/settings.json)
├── .github/                     # GitHub config (several subfolders = symlinks into .agents/)
├── docs/                        # STANDARDS.md, AUDIT_REPORT.md, SECRETS.md, etc.
├── scripts/                     # validate_dotfiles.sh and VS Code monitor utilities
├── AGENTS.md                    # Agent registry
├── CLAUDE.md                    # Claude context
├── GEMINI.md                    # Gemini context
├── CHEATSHEET.md                # Persistent tracker
├── README.md                    # Setup + structure
├── setup.sh
├── sync.sh
└── test-subagents.sh
```

**Additional structure [PROPOSED — not implemented on this machine]:** the conventions below were designed for a broader multi-harness scenario but were never built. Don't assume they exist without confirming with `ls`:

```
dotfiles/
├── .copilot/                    # [PROPOSED] Dedicated Copilot config (today: .github/copilot-instructions.md covers this)
├── .gemini/                     # [PROPOSED] Dedicated Gemini config (today: GEMINI.md at root covers this)
├── .cursor/                     # [PROPOSED] Cursor config
├── agent-versions.json          # [PROPOSED] agent-framework version pinning — see dedicated section below
```

### Repository: `agent-framework` (Development) — [PROPOSED — repository doesn't exist on this machine]

**Note:** Everything in this section describes a separate repository, `agent-framework`, that **doesn't exist** in `~/Projects/` or `~/Work/` on this machine (verified 2026-09-15). It's an architecture proposal, not a current fact. What exists today is `.agents/` inside `dotfiles` itself, serving as the single source of truth (see the real structure above).

**Purpose (proposed):** A complete agent-orchestration framework. Source of truth for personas, agents, skills, workflows, and multi-harness compliance enforcement.

**What it includes:**
- Base personas (Master Architect)
- Task-specific personas (Charter, Review, Diagram, etc.)
- Specialized agents (7+ agents with SKILL.md)
- Multi-harness support (Copilot, Claude, Gemini, OpenAI, LiteLLM)
- Reusable skills and prompts
- Central configuration
- Compliance enforcement via CI/CD

```
agent-framework/
├── skills/                              # "Canonical" skills
│   ├── data-analyzer/
│   │   ├── SKILL.md                     # Complete documentation
│   │   ├── scripts/
│   │   │   ├── analyzer.py
│   │   │   └── utils.py
│   │   ├── references/
│   │   │   └── api-guide.md
│   │   ├── assets/
│   │   │   └── template.html
│   │   └── tests/
│   │       └── test_analyzer.py
│   └── code-reviewer/
│       └── SKILL.md
├── agents/                              # Agent definitions
│   ├── architect/
│   │   ├── AGENTS.md                    # Persona definition
│   │   ├── config.yaml                  # Agent configuration
│   │   └── references/
│   │       └── reasoning-strategy.md
│   └── engineer/
│       └── AGENTS.md
├── workflows/                           # Agent workflows/initialization
│   ├── init.md
│   ├── onboarding.md
│   └── troubleshooting.md
├── prompts/                             # Prompt templates (optional)
│   ├── system/
│   │   └── architect-system.md
│   └── task/
│       └── code-review-task.md
├── config/                              # Global configuration
│   ├── model-config.yaml                # Model routing, token budgets
│   ├── tools-config.yaml                # Available tools registry
│   └── capabilities.json                # Feature matrix
├── scripts/                             # Utilities
│   ├── validate-skills.sh
│   ├── lint-prompts.py
│   └── publish-release.sh
├── docs/                                # General documentation
│   ├── ARCHITECTURE.md
│   ├── CONTRIBUTING.md
│   └── FAQ.md
├── package.json                         # Versioning + publishing
├── CHANGELOG.md                         # Version history
├── AGENTS.md                            # Skills registry
├── README.md
├── STANDARDS.md                         # This file (copy/ref)
└── .github/
    └── workflows/
        └── release.yml                  # Publish to npm/registry
```

---

## 📝 NAMING CONVENTIONS

### Repository Names

| Name | Use | Status |
|------|-----|--------|
| `dotfiles` | Universal configuration (agents, config, setup) | ✅ RECOMMENDED |
| `agent-framework` | Agents + personas + skills framework | ✅ RECOMMENDED |
| `agents-core` | Smaller-scope alternative | ✅ OK |
| ❌ ~~`agentic_instructions`~~ | Inadequate (undersells the scope) | ❌ RENAME |
| ❌ ~~`crush-config`~~ | Specific to Crush only | ❌ DON'T USE |
| ❌ ~~`skills`~~ | Ambiguous (use inside the framework instead) | ❌ AVOID |

**Note:** If you already have a repo called `agentic_instructions` with a complete structure, **RENAME IT TO `agent-framework`** — the real scope (agents + skills + personas + harnesses) justifies it.

### Directory Names
- **Kebab-case** (lowercase with hyphens): `my-skill`, `code-analyzer`, `web-research`
- **No spaces or underscores**
- **64 characters max**

Examples:
```
✅ data-processor
✅ nlp-pipeline
✅ system-validator
❌ dataProcessor (camelCase)
❌ data_processor (snake_case)
❌ Data Processor (spaces)
```

### File Names

| Type | Pattern | Example |
|------|---------|---------|
| Skill doc | `SKILL.md` | `data-analyzer/SKILL.md` |
| Agent doc | `AGENTS.md` | `agents/architect/AGENTS.md` |
| Agent config | `config.yaml` | `agents/architect/config.yaml` |
| Workflow | `[name].md` | `workflows/init.md` |
| Prompt template | `.prompt.md` | `prompts/system-prompt.md` |
| Instruction | — use `[name].md` | `docs/best-practices.md` |
| Script | `[name].sh`, `[name].py` | `scripts/validate-skills.sh` |
| Global config | `config.yaml`, `settings.json` | `config/model-config.yaml` |

### Skill Names

**Format:** `kebab-case`, descriptive, 64 chars max

```
✅ data-analyzer
✅ web-research
✅ code-reviewer
✅ nlp-text-processor
❌ skill-data-analyzer (redundant)
❌ DataAnalyzer (camelCase)
❌ my_data_analyzer (underscores)
```

### Agent Names

**Format:** `kebab-case`, persona/role-based

```
✅ architect
✅ code-engineer
✅ security-validator
✅ project-manager
❌ Agent (too generic)
❌ my_architect (underscores)
```

---

## 📄 SKILL.md STRUCTURE

Emerging community pattern (Agent Skills Spec):

```markdown
# Skill Name

Brief one-sentence description.

Longer paragraph explaining what this skill does, when to use it, and what value it provides.

## Triggers

Keywords that activate the skill when the agent detects them:
- trigger-word-1
- trigger-word-2
- "multi-word trigger"
- regex pattern optional

## Usage

### Basic Example
```code
example_code_here
```

### Advanced Usage
```code
more_complex_example
```

## Requirements

- Required tool/capability 1
- Required tool/capability 2
- Python 3.9+ or similar

## Limitations

- Known limitation 1
- Known limitation 2

## Related Skills

- [Other Skill](../other-skill/SKILL.md)
- [Another Skill](../another-skill/SKILL.md)

## Implementation Details

How this skill is implemented, dependencies, etc.

## See Also

- Reference docs
- External links
```

**Optional: YAML Frontmatter** (emerging as a standard)

```yaml
---
name: data-analyzer
description: Analyze and process structured data
model: gpt-4
tools: [bash, python, grep]
triggers:
  - analyze data
  - data processing
  - compute statistics
user-invocable: true
estimated-cost: medium
---
```

---

## 📄 AGENTS.md STRUCTURE

**Purpose:** Registry of available agents and skills.

```markdown
# Agents Registry

## Available Agents

| Agent | Role | Status | Version |
|-------|------|--------|---------|
| architect | System design, orchestration | Stable | 2.1.0 |
| engineer | Implementation, coding | Stable | 2.1.0 |
| reviewer | Code/design review | Stable | 1.9.0 |

## Available Skills

| Skill | Category | Triggers | Version |
|-------|----------|----------|---------|
| data-analyzer | Analytics | analyze, compute | 2.0.0 |
| web-research | Research | search, research | 1.8.0 |
| code-reviewer | Review | review, audit | 2.1.0 |

## Skill Definitions

### data-analyzer
- **Location:** `skills/data-analyzer/SKILL.md`
- **Version:** 2.0.0 (pinned in crush-config)
- **Status:** Production
- **Last Updated:** 2026-09-14

...
```

---

## 📄 agent-versions.json FILE STRUCTURE [PROPOSED — not implemented]

**Status:** This file doesn't exist in `~/dotfiles` on this machine (verified 2026-09-15, `agent-versions.json` MISSING at root). The section below describes the proposed design, not a real file. Don't reference `agent-versions.json` as if it existed in other documentation without this caveat.

**Location (proposed):** `crush-config/agent-versions.json`

**Purpose:** Explicit version pinning for cross-machine reproducibility.

```json
{
  "metadata": {
    "snapshot_date": "2026-09-14",
    "snapshot_by": "setup.sh v1.2.0",
    "crush_config_version": "1.0.0"
  },
  "framework": {
    "name": "agent-framework",
    "version": "2.1.0",
    "repository": "https://github.com/nmc-costa/agent-framework",
    "branch": "main"
  },
  "skills": {
    "data-analyzer": "2.0.0",
    "web-research": "1.8.0",
    "code-reviewer": "2.1.0",
    "omarchy": "1.0.0"
  },
  "agents": {
    "architect": "2.1.0",
    "engineer": "2.1.0",
    "reviewer": "1.9.0"
  },
  "compatibility": {
    "min_crush_version": "1.0.0",
    "min_node_version": "18.0.0",
    "supported_os": ["linux", "macos"]
  }
}
```

---

## 🔗 LINKING BETWEEN REPOSITORIES [PROPOSED — assumes the `agent-framework` repo, which doesn't exist]

### Recommended Pattern: NPM Packages + Symlinks (Docs)

**agent-framework** publishes as an npm package:
```json
{
  "name": "@crush/agent-framework",
  "version": "2.1.0",
  "main": "dist/index.js",
  "exports": {
    ".": "./dist/index.js",
    "./skills": "./skills/index.js",
    "./agents": "./agents/index.js"
  }
}
```

**crush-config** references a specific version:
```bash
# .agents/skills/ contains symlinks to documentation
ln -sf ~/agent-framework/skills/data-analyzer/SKILL.md \
       ~/crush-config/.agents/skills/data-analyzer-ref.md

# agent-versions.json pins the version
"data-analyzer": "2.0.0"

# AGENTS.md documents the status
## data-analyzer v2.0.0
- Status: Pinned in crush-config
- Location: @crush/agent-framework/skills/data-analyzer
```

### Update Flow

```
1. Development in agent-framework/
   - Create a feature branch
   - Update SKILL.md, test
   - Merge to main
   - CI publishes v2.1.1

2. Automatic notification
   - A GitHub issue is created in crush-config
   - "New agent-framework: 2.1.1 available"

3. Manual upgrade in crush-config
   - Maintainer reviews the CHANGELOG
   - npm install @crush/agent-framework@2.1.1
   - Tests locally
   - Updates agent-versions.json
   - git commit, push
   - ./sync.sh propagates

4. Other machines
   - git pull
   - ./setup.sh (reads agent-versions.json)
   - Automatically uses v2.1.1
```

---

## ✅ COMPLIANCE CHECKLIST

### When Creating a New Skill

- [ ] Name in kebab-case (64 chars max)
- [ ] Directory at `agent-framework/skills/<name>/`
- [ ] `SKILL.md` present with required sections
- [ ] Triggers documented
- [ ] Usage examples included
- [ ] Scripts in a `scripts/` subdirectory
- [ ] References in a `references/` subdirectory
- [ ] Tests in a `tests/` subdirectory
- [ ] Version updated in `package.json`
- [ ] CHANGELOG.md updated
- [ ] Registered in `AGENTS.md`

### When Updating crush-config

- [ ] `agent-versions.json` updated *(only applicable once this proposed file exists — see the section above)*
- [ ] `AGENTS.md` reflects pinned versions
- [ ] Symlinks point to the right location
- [ ] `./test-subagents.sh` passes
- [ ] `./scripts/validate_dotfiles.sh` passes
- [ ] AUDIT_REPORT.md redone
- [ ] README.md updated with dates

### Git Commits

**Format:** `[repo] type: description`

```
agent-framework: Add data-analyzer skill for structured data processing
crush-config: Update agent-framework to v2.1.0
crush-config: Pin data-analyzer v2.0.0 from agent-framework
```

---

## 🔄 SYNCHRONIZATION

### When to Sync

| Change | Sync Immediately? | Note |
|---------|---------------------------|------|
| Patch version (2.1.0 → 2.1.1) | ✅ Yes | Bug fixes |
| Minor version (2.1.0 → 2.2.0) | ⏳ Assess | New features |
| Major version (2.1.0 → 3.0.0) | ❌ Plan it | Breaking changes |
| Doc updates | ✅ Yes | No functional impact |
| Bug fix in an already-pinned skill | ✅ Yes | Same major.minor |

### Sync Scripts

```bash
# In crush-config
./sync.sh              # Copy docs/references
./setup.sh                    # Create symlinks, install versions
npm install @crush/agent-framework@2.1.0  # Pin version
```

---

## 📚 REFERENCES

- **LangChain Standard:** github.com/langchain-ai/langchain (monorepo pattern)
- **Mem0 Pattern:** github.com/mem0ai/mem0 (plugin registry)
- **Anthropic:** Claude SDK + instructions pattern
- **Agent Skills Spec:** agentskills.io/specification
- **GitHub Copilot:** .github/{agents,skills,prompts,instructions}

---

## 📌 FINAL NOTES

1. **Keep Separate [PROPOSED]:** `crush-config`/`dotfiles` (stable) vs. `agent-framework` (dev) — today both live together in `dotfiles/.agents/`, not separated
2. **Clear Semantics:** Skills/Agents, not "instructions"
3. **Versioning [PROPOSED]:** SemVer in `agent-framework`, explicit pinning in `crush-config` — no `agent-versions.json` and no SemVer applied today
4. **Documentation:** SKILL.md is the standard (with optional YAML frontmatter) — this is already followed by the real skills in `.agents/skills/`
5. **Linking [PROPOSED]:** NPM packages + symlinks for docs (not submodules) — today direct symlinks inside the same repo are used instead (`.claude/skills/<name>` → `.agents/skills/<name>`, `.github/{harnesses,instructions,prompts,automation}` → `.agents/`), no npm/packages
6. **Compliance:** Use `test-subagents.sh`, `./scripts/validate_dotfiles.sh`, and `AUDIT_REPORT.md` regularly

---

**Last Updated:** 2026-09-15 (accuracy revision — aspirational sections marked `[PROPOSED]`; naming/convention content unchanged)
**Based on:** Community research (LangChain, Mem0, Anthropic, GitHub)
**Maintained by:** nmc-costa
