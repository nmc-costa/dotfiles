# AGENTS.md

Guidance for AI agents (Crush/Claude, Copilot, Gemini) working in this repository.

## Workspace standards (all repos, not just this one)

`.agents/instructions/workspace-config/standards/workspace-standards.yaml` defines the mandatory defaults for **every** repo in this workspace (clean root, README with fixed sections, technical language = English). Every agent, on any tool, should:

1. At the start of a session in this workspace, read `review.nextDue` in `~/dotfiles/.agents/instructions/workspace-config/standards/workspace-standards.yaml`.
2. If that date has passed, treat it as a strong reminder (not an absolute block) to do the SOTA review described in `review.sourcesToRecheck` before substantial unrelated work, propose the changes on a `claude/...` branch + PR (never a direct commit to `main`), and update `review.lastReviewed`/`nextDue`.
3. Run `python3 scripts/validate_workspace_standards.py .agents/instructions/workspace-config/standards/workspace-standards.yaml` after any edit to that file, before committing.

**Session hygiene (`sessionHygiene`, 2026-09-15):** when the current session reaches a natural conclusion, or has already gone through many rounds of agent dispatch/tool calls with a large context relative to what the next task actually needs, or the next request is unrelated to what filled the session so far — proactively suggest starting a new session, and **always hand back a ready-to-copy kickoff prompt** (don't just say "you should start a new session"). The concrete pattern is in this repo's `CHEATSHEET.md` §7: read `CLAUDE.md`+`CHEATSHEET.md`, rebuild the todo list from a persistent doc, and — this is the part every harness should also do, not just Claude Code — check `tasks/board.md` (and `tasks/README.md` for how to append events) for the workspace's cross-session task tracker, writing there (not only in-session) when something gets done.

(Claude Code has this automated via a `SessionStart` hook — see `CLAUDE.md`. Other tools follow this protocol in prose, here. **Known gap (2026-09-16):** this file and `CLAUDE.md` both reference `CHEATSHEET.md` §7 but neither used to mention `tasks/` explicitly, and `.github/copilot-instructions.md`/`GEMINI.md` had no startup pointer to either — see `CLAUDE.md`'s "Known Gaps" for the full finding and what's still needed to fix it for Copilot/Gemini/Antigravity.)

## Available Agents

| Agent | Config Location | When to Use |
|--------|-------------------|-------------|
| **Crush/Claude** | `~/.claude/`, `~/.claude.json` | Development, code analysis, debugging, automation |
| **Copilot** | `~/.copilot/` | Inline suggestions, completions in VS Code |
| **Gemini** | `~/.gemini/` | Quick queries, brainstorming |
| **Cline** | `~/.cline/` | Complex multi-file task execution |

## Custom Skills

This repository centralizes skills (extensions/plugins) in the standard `.agents/skills/` folder:

```
dotfiles/
└── .agents/
    ├── skills/                     ← Central source of truth
    │   ├── diagnose-crash/
    │   │   ├── SKILL.md
    │   │   └── reporting.md
    │   ├── omarchy/
    │   │   ├── SKILL.md
    │   │   └── [other files]
    │   └── [new-skills]/
    │       └── SKILL.md
    └── workflows/                  ← Agent personas
        ├── init.md
        └── architect_html_sciml.md
```

When you sync, skills are propagated to:
- **`~/.agents/skills/`** — Shared across agents (always synced)
- **`~/.claude/skills/`** — Crush-specific (if it exists)
- **`/usr/share/omarchy/default/agents/skills/`** — System-wide (optional, requires sudo)

### Adding a New Skill

1. Create a folder at `dotfiles/.agents/skills/my-skill/`
2. Add `SKILL.md` (required):
   ```markdown
   # My Skill

   Brief description of what it does.

   ## Triggers (when to use)
   - Keyword 1
   - Keyword 2
   ```
3. Add other files as needed
4. Commit:
   ```bash
   cd ~/dotfiles
   git add .agents/skills/my-skill/
   git commit -m "Add my-skill for [purpose]"
   git push
   ```
5. Sync:
   ```bash
   ./sync.sh
   ```
   Options:
   - `./sync.sh` — Sync to `~/.agents/skills/` and `~/.claude/skills/`
   - `./sync.sh --system` — Also copy to `/usr/share/omarchy/default/agents/skills/` (requires sudo)
   - `./sync.sh --dry-run` — Simulate without making changes
   - `./sync.sh --verbose` — Show sync details

### Adding a New Skill and Propagating It (Full Flow)

```bash
# 1. Create the skill
mkdir -p ~/dotfiles/.agents/skills/new-skill
cat > ~/dotfiles/.agents/skills/new-skill/SKILL.md <<'EOF'
# New Skill

Description.

## Triggers
- keyword
EOF

# 2. Add other files (optional)
# cp script.sh ~/dotfiles/.agents/skills/new-skill/

# 3. Version on GitHub
cd ~/dotfiles
git add .agents/skills/new-skill/
git commit -m "Add new-skill for [purpose]"
git push

# 4. Sync to local agents
./sync.sh

# 5. (Optional) Also sync to the system
./sync.sh --system

# 6. On another machine: pull + sync
cd ~/dotfiles && git pull
./sync.sh
```

## Context Variables for Agents

### Directory Structure
- `~/Projects/` — Personal repos (studies, own IP)
- `~/Work/` — Professional/organization repos
- `~/dotfiles/` — This repo (cross-machine synchronization)

### Global Context Files

| File | Access | Purpose |
|----------|--------|----------|
| `~/.context-global.md` | All agents | General context (structure, conventions, preferences) |
| `~/claude.md` | Crush/Claude | Claude-specific rules |
| `~/.github/copilot-instructions.md` | Copilot | Copilot-specific instructions |
| `~/directory_tree.md` | All (reference) | Directory structure map |

## Per-Agent Development Rules

### Crush/Claude
- **Reads:** `claude.md`, `.context-global.md`, `directory_tree.md`
- **Preferences:** Deep analysis, technical explanations, script automation
- **Restrictions:** No automatic commits without explicit confirmation

### Copilot
- **Reads:** `.github/copilot-instructions.md`, `.context-global.md`
- **Preferences:** Fast inline suggestions, code completions
- **Restrictions:** Doesn't modify files without intervention

### Gemini
- **Reads:** `.context-global.md`
- **Preferences:** Brainstorming, ideation, concept verification
- **Restrictions:** Occasional use, no long-context storage

### Cline
- **Reads:** All instructions above (fallback: `.context-global.md`)
- **Preferences:** Multi-step tasks, refactoring, tests
- **Restrictions:** Respects user permissions, doesn't modify system configs without sudo

## Cross-Machine Synchronization

### First Setup (New Machine)
```bash
cd ~
git clone https://github.com/nmc-costa/dotfiles.git dotfiles-tmp
cd dotfiles-tmp
./setup.sh --dotfiles
# Follow on-screen instructions for config checkout
```

### Updating Existing Configs
```bash
cd ~/dotfiles
git pull
./setup.sh      # Runs symlinks + sync.sh
```

## Troubleshooting

### Skills don't appear after clone
```bash
# Check location
ls ~/.agents/skills/
ls ~/.claude/skills/

# Sync manually
cd ~/dotfiles
./sync.sh --verbose

# Or for the system (requires sudo)
./sync.sh --system
```

### Broken Symlinks
```bash
# Check
ls -la ~/  # Look for red arrows

# Recreate manually
ln -sf ~/dotfiles/.claude ~/.claude
ln -sf ~/dotfiles/.agents ~/.agents
ln -sf ~/dotfiles/.vscode ~/.vscode

# OR re-run setup
./setup.sh
```

### Agent Can't See Context
- Check that `~/.context-global.md` exists (should be a symlink)
- Check permissions: `ls -la ~/.context-global.md`
- Reload the agent or restart the application

---

**Last Updated:** 2026-09-14
**Maintained by:** nmc-costa
