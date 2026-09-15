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

## Directory tree

```
dotfiles/
├── .agents/                    # Central source of truth for AI agent config
│   ├── AGENT.md                #   Agent registry/overview
│   ├── CONTRIBUTING.md
│   ├── automation/             #   Automation checklists (e.g. chronicle-daily-checklist.md)
│   ├── harnesses/               #   Per-harness guides (claude-code, gemini, litellm, openai, vscode-copilot)
│   ├── instructions/            #   base-personas/, task-personas/, workspace-config/, automation/
│   ├── prompts/                 #   Reusable prompts (chronicle/, _templates/)
│   ├── skills/                  #   Agent skills — 1 real copy per skill (archi, diagnose-crash, omarchy, projecthits, ...)
│   ├── validation/               #   Real validation outputs, keyed by skill
│   └── workflows/                #   Agent personas / init workflows
├── .chezmoisource/              # chezmoi source dir, scoped to one encrypted file
│   └── dot_vscode/encrypted_settings.json.age
├── .claude/                     # Claude Code config; .claude/skills/<name> are symlinks into .agents/skills/
├── .github/                     # GitHub config; automation/, CONTRIBUTING.md, harnesses/, instructions/,
│                                 #   prompts/ are symlinks into .agents/; workflows/, skills/, workflows dir,
│                                 #   copilot-instructions.md, and workflows/ (CI) are real here
├── .vscode/                     # VS Code config (settings.json holds the real API key, chezmoi-managed — see SECRETS.md)
├── docs/                        # Everything not auto-loaded by a tool by convention — see index below
├── scripts/                     # Utility scripts (VS Code docs monitor: monitor_vscode_docs.py, setup_vscode_monitor_cron.sh)
├── AGENTS.md                    # General agent guide (Crush/Claude, Copilot, Gemini, Cline) — auto-read by convention
├── CLAUDE.md                    # Claude Code-specific context — auto-read by Claude Code
├── GEMINI.md                    # Gemini-specific context — auto-read by Gemini
├── CHEATSHEET.md                # Living "where does X go" reference + persistent TODO list
├── SECRETS.md                   # Secrets-management doc (chezmoi + age) — kept at root, see note below
├── README.md                    # This file
├── setup.sh                     # One-click machine setup (run from root)
├── sync-skills.sh               # Synchronize skills to all agents (run from root)
├── test-subagents.sh            # Verification test script (run from root)
└── .gitignore
```

## What's where (index)

### Root files

| File | Purpose |
|---|---|
| `README.md` | This file — overview, structure, quick start |
| `CLAUDE.md` | Claude Code-specific context, structure summary, open-work table — auto-loaded by Claude Code from repo root |
| `AGENTS.md` | Complete agent guide (Crush/Claude, Copilot, Gemini, Cline), skills management, workflows — general agent-config convention |
| `GEMINI.md` | Gemini-specific context — auto-loaded by Gemini |
| `CHEATSHEET.md` | "Where does X go", the 3-repo map, the persistent cross-session TODO list, the agile-workspace roadmap |
| `SECRETS.md` | How the one real secret in this repo (a VS Code extension API key) is encrypted with chezmoi + age. Kept at root (not `docs/`) because it documents a live security mechanism readers need to find immediately, and was left in place after a content check confirmed it holds no plaintext secret — see the report footer of the commit that added this reorganization for the exact reason it wasn't relocated automatically. |
| `setup.sh` | One-click machine setup: clones repos, creates symlinks, sets up agents. Run from repo root (`./setup.sh`) |
| `sync-skills.sh` | Distributes `.agents/skills/` to `.claude/skills/`, `.github/skills/`, and optionally system-wide. Run from repo root (`./sync-skills.sh`) |
| `test-subagents.sh` | Quick sanity check for subagent setup. Run from repo root (`./test-subagents.sh`) |
| `.gitignore` | What never gets committed (real `.vscode/settings.json`, caches, logs, etc.) |

### Top-level directories

| Directory | Purpose |
|---|---|
| `.agents/` | **Source of truth** for all agent config: `skills/`, `instructions/`, `harnesses/`, `prompts/`, `workflows/`, `validation/`, `automation/`. Edit here, never in the synced copies. |
| `.claude/` | Claude Code config; `.claude/skills/<name>` are symlinks back into `.agents/skills/<name>` |
| `.github/` | GitHub config and CI; several subfolders (`automation/`, `CONTRIBUTING.md`, `harnesses/`, `instructions/`, `prompts/`) are symlinks into `.agents/` so Copilot/Actions read the same source of truth; `workflows/` holds real GitHub Actions (e.g. `vscode-docs-monitor.yml`) |
| `.vscode/` | VS Code config; `settings.json` contains the real API key and is generated locally by `chezmoi apply` (gitignored) — see `SECRETS.md` |
| `.chezmoisource/` | Dedicated chezmoi source directory, scoped only to the one encrypted `.vscode/settings.json` — see `SECRETS.md` |
| `scripts/` | Standalone utility scripts (currently the VS Code docs monitor) |
| `docs/` | Everything not auto-loaded by convention — see table below |

### `docs/` index

| File | Purpose |
|---|---|
| `docs/STANDARDS.md` | Naming conventions and structure standards (partly aspirational/stale — see `CLAUDE.md` known gaps) |
| `docs/AUDIT_REPORT.md` | Compliance/standards audit report (contains claims contradicted by current state — see `CLAUDE.md` known gaps) |
| `docs/SUBAGENTS_VERIFICATION.md` | Verification checklist for agent/subagent setup |
| `docs/VSCODE_MONITOR_QUICKSTART.md` | Quickstart guide for the VS Code docs monitor automation |
| `docs/directory_tree.md` | An older, narrower directory-tree doc (home-directory level, partly superseded by this README) |
| `docs/requirements.txt` | Python deps for `scripts/monitor_vscode_docs.py` (`requests`, `beautifulsoup4`, `pyyaml`) |
| `docs/vscode-docs-monitor.yml` | An older copy of the GitHub Actions workflow — the **active** one is `.github/workflows/vscode-docs-monitor.yml`; this copy still points at a dead path (`my/agentic_instructions/...`) from before the `agentic_instructions` merge and should not be treated as current |

## Integration with Agent Framework

This repository (`dotfiles`) is the **stable, synchronized configuration layer**. Development of new agents and skills happens in a separate repository:

- **`dotfiles`** (this repo) — Universal config for all agents, pinned versions, distributed config
- **`agent-framework`** — Active development of agents, skills, workflows, personas

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

For detailed standards, naming conventions, and linking patterns, see **`docs/STANDARDS.md`**.

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
- **Root stays clean:** only `README.md`, files a tool auto-loads by convention (`CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `.gitignore`), and scripts meant to be run from root live at top level — everything else belongs in `docs/`

## Maintenance

Run verification script regularly:

```bash
./test-subagents.sh           # Quick sanity check
```

For full verification checklist, see `docs/SUBAGENTS_VERIFICATION.md`.

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
**Last Updated:** 2026-09-15
