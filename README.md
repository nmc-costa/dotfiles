# dotfiles

Central repository for AI agent configurations, skills, workflows, and environment synchronization across machines.

## Quick Start

```bash
# New machine setup
cd ~
git clone https://github.com/nmc-costa/dotfiles.git dotfiles-tmp
cd dotfiles-tmp
./setup.sh --dotfiles      # Clone repos, create symlinks, setup agents
./sync-skills.sh           # Distribute skills to all agents
```

## Documentation

- **`STANDARDS.md`** — Nomenclatura, convenções e estrutura padrão (community standards + best practices)
- **`AGENTS.md`** — Complete guide for AI agents (Crush, Copilot, Gemini, Cline), skills management, and workflows
- **`CLAUDE.md`** — Claude Code-specific context and best practices
- **`GEMINI.md`** — Gemini-specific context and best practices
- **`SUBAGENTS_VERIFICATION.md`** — Verification checklist for agent setup
- **`AUDIT_REPORT.md`** — Compliance and standards audit report

## Repository Structure

```
dotfiles/
├── .agents/                    # AI agent configuration
│   ├── skills/                 # Agent skills (diagnose-crash, omarchy, etc.)
│   └── workflows/              # Agent personas and workflows
├── .claude/                    # Crush/Claude configuration
├── .vscode/                    # VS Code configuration
├── .github/                    # GitHub workflows and settings
├── setup.sh                    # One-click machine setup
├── sync-skills.sh              # Synchronize skills to all agents
├── test-subagents.sh           # Verification test script
└── scripts/                    # Utility scripts
```

## Integration with Agent Framework

This repository (`crush-config`) is the **stable, synchronized configuration layer**. Development of new agents and skills happens in a separate repository:

- **`crush-config`** (this repo) — Pinned versions, distributed config, symlinks to skill docs
- **`agent-framework`** — Active development of agents, skills, workflows

### Version Management

```bash
# Pinned versions in crush-config
cat agent-versions.json
# {
#   "framework": "2.1.0",
#   "skills": {"data-analyzer": "2.0.0", ...}
# }
```

### Updating Skills

```bash
# In agent-framework: develop, test, publish
npm version minor
npm publish

# In crush-config: pin and distribute
npm install @crush/agent-framework@2.1.1
./setup.sh --dotfiles
./sync-skills.sh
```

For detailed standards, naming conventions, and linking patterns, see **`STANDARDS.md`**.

### Project Repositories

- **`~/Projects/`** — Personal repositories (studies, experiments, frameworks)
- **`~/Work/`** — Professional/organization repositories
- **`~/dotfiles/`** — Configuration and environment (this repository)

Each project repository is independent with its own git remote.

### Agent Configuration

All AI agent configurations live in `.agents/`:
- **`.agents/skills/`** — Shared agent skills (extensions/plugins)
- **`.agents/workflows/`** — Agent personas and initialization workflows

### Symlinks to Home Directory

Configuration files are version-controlled in `~/dotfiles/` and symlinked to `~/` for system-wide availability:

```bash
~/.agents         → ~/dotfiles/.agents
~/.claude         → ~/dotfiles/.claude
~/.vscode         → ~/dotfiles/.vscode
~/.github         → ~/dotfiles/.github
```

## Managing Skills

### Add New Skill

```bash
mkdir -p ~/dotfiles/.agents/skills/my-skill
cat > ~/dotfiles/.agents/skills/my-skill/SKILL.md <<'EOF'
# My Skill

Brief description.

## Triggers
- keyword1
- keyword2
EOF

cd ~/dotfiles
git add .agents/skills/my-skill/
git commit -m "Add my-skill for [purpose]"
git push
./sync-skills.sh              # Distribute to ~/.agents/skills, ~/.claude/skills, etc.
```

### Synchronize Skills

```bash
./sync-skills.sh              # Sync to user-level (.agents/skills, .claude/skills)
./sync-skills.sh --system     # Also sync to system defaults (requires sudo)
./sync-skills.sh --dry-run    # Simulate without making changes
./sync-skills.sh --verbose    # Show details
```

## Setup and Installation

### First Machine Setup

```bash
cd ~/dotfiles
./setup.sh                    # Create symlinks, clone repos, setup agents
./sync-skills.sh              # Distribute skills
./test-subagents.sh           # Verify setup
```

### Subsequent Machines

```bash
cd ~/dotfiles
git pull
./setup.sh
./sync-skills.sh
```

## System Specifications

- **OS:** Omarchy Linux (Arch-based, opinionated system)
- **Editors:** NeoVim (native) and VS Code (via `yay -S visual-studio-code-bin`)
- **Git:** Single account for both personal and organization repositories

## Standards and Best Practices

- **Language:** English for technical documentation, Portuguese for user-facing content
- **Configuration:** Never edit agent configs directly in `~/.agents/` — always modify in `~/dotfiles/.agents/` and sync
- **Scripts:** All scripts are idempotent (safe to run multiple times)
- **Error Handling:** Scripts validate inputs and exit gracefully on errors

## Maintenance

Run verification script regularly:

```bash
./test-subagents.sh           # Quick sanity check
```

For full verification checklist, see `SUBAGENTS_VERIFICATION.md`.

## Troubleshooting

### Skills not appearing
```bash
cd ~/dotfiles
./sync-skills.sh --verbose
ls ~/.agents/skills/
```

### Broken symlinks
```bash
./setup.sh                    # Re-run setup to recreate symlinks
```

### Script errors
```bash
bash -n setup.sh              # Validate bash syntax
bash -n sync-skills.sh
```

---

**Maintained by:** nmc-costa  
**Last Updated:** 2026-09-14
