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
├── .vscode/                     # VS Code config (settings.json holds the real API key, chezmoi-managed — see docs/SECRETS.md)
├── docs/                        # Everything not auto-loaded by a tool by convention — see index below
│   └── SECRETS.md               #   Secrets-management doc (chezmoi + age)
├── scripts/                     # Utility scripts (VS Code docs monitor: monitor_vscode_docs.py, setup_vscode_monitor_cron.sh)
├── AGENTS.md                    # General agent guide (Crush/Claude, Copilot, Gemini, Cline) — auto-read by convention
├── CLAUDE.md                    # Claude Code-specific context — auto-read by Claude Code
├── GEMINI.md                    # Gemini-specific context — auto-read by Gemini
├── CHEATSHEET.md                # Living "where does X go" reference + persistent TODO list
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
| `.vscode/` | VS Code config; `settings.json` contains the real API key and is generated locally by `chezmoi apply` (gitignored) — see `docs/SECRETS.md` |
| `.chezmoisource/` | Dedicated chezmoi source directory, scoped only to the one encrypted `.vscode/settings.json` — see `docs/SECRETS.md` |
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
| `docs/SECRETS.md` | How the one real secret in this repo (a VS Code extension API key) is encrypted with chezmoi + age |

## Guidelines

### For you (human)

- **Start here, then `CHEATSHEET.md`.** This README is the map; `CHEATSHEET.md` is the living "where does X go" + persistent TODO list — check it before starting new work, and expect it to change often.
- **Real repos on this machine:** `~/dotfiles` (this one), `~/Projects/architect`, `~/Projects/notes`, `~/Work/notes`, `~/Projects/agentic_instructions` (archived, read-only — see `CHEATSHEET.md` §3). If you're looking for `~/Work/mobai`, `~/Work/RAGFusion`, etc. — those are in `setup.sh`'s repo lists but **not cloned on this machine**; don't assume they exist without checking.
- **`~/.agents`, `~/.claude`, `~/.vscode`, `~/.github` are NOT symlinks on this machine**, despite what older docs in this repo may still imply — see `CLAUDE.md`'s "Known Gaps" section. `setup.sh` can create them, but the sync direction (repo→system vs. system→repo) is an open decision, not yet standard. Don't trust a claim of "it's symlinked" here without running `readlink -f <path>` first.
- **Before deleting or rewriting a doc, check `git log` for it** — several docs here (`docs/STANDARDS.md`, `docs/AUDIT_REPORT.md`) are known to contain stale/aspirational claims, flagged rather than silently fixed, because the fix is a content decision, not a hygiene one.
- **There is no separate `agent-framework` repo or `agent-versions.json` on this machine.** An earlier version of this README described one; that content was removed as inaccurate for the current setup, not because the idea is rejected — if you want that separation, it needs to be built, not assumed.

### For agents (Claude Code and others)

- **Load order:** `CLAUDE.md` (Claude Code auto-loads this from root) → this `README.md` for the full directory map → `CHEATSHEET.md` §4 for current open work → `docs/` only for the specific doc you need.
- **Edit `.agents/skills/<name>/` — never `.claude/skills/<name>` or `.github/skills/<name>` directly.** Those are meant to be symlinks/synced copies; on this machine confirm with `readlink -f` before assuming symlink behavior, since the "Known Gaps" note above applies here too.
- **Root stays clean.** Only `README.md` and files a tool auto-loads by convention (`CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `.gitignore`) plus root-run scripts belong at top level. Anything else you create — a report, an audit, a new doc — goes in `docs/`. `scripts/validate_dotfiles.sh` (see below) enforces this; run it before considering a change here "done."
- **Any structural change to `.agents/` (new skill, new harness, a resolved TODO) must update `CHEATSHEET.md` in the same commit** — this is a hard rule stated in `CLAUDE.md`, not a suggestion.
- **Don't push to `main` directly.** Work on a `claude/<topic>` branch, push it, leave the PR for the human to open/merge — `gh` is not authenticated in most sessions here, so you generally can't open the PR yourself; give the compare URL `git push` prints instead.
- **Treat `docs/STANDARDS.md` and `docs/AUDIT_REPORT.md` content with suspicion** — they're known to contain claims contradicted by the current repo state (see `CLAUDE.md` known gaps). Verify before repeating a claim from them.

## Project Repositories

- **`~/Projects/`** — Personal repositories
- **`~/Work/`** — Professional/organization repositories
- **`~/dotfiles/`** — Configuration and environment (this repository)

Each project repository is independent, with its own git remote. See `CHEATSHEET.md` §3 for what each one is for.

## Validating This Repo

`scripts/validate_dotfiles.sh` checks that this repo actually matches what this README claims: root only has the allowed files, `docs/` holds everything else, the key guideline docs exist and aren't empty, and the directory tree above matches the real filesystem. Run it after any structural change:

```bash
./scripts/validate_dotfiles.sh
```

See `docs/SUBAGENTS_VERIFICATION.md` for the separate agent/subagent setup checklist, and `./test-subagents.sh` for that quick sanity check.

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
- **Root stays clean:** see the Guidelines section above

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
