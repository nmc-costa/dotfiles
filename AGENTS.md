# AGENTS.md

Guidance for AI agents (Crush/Claude, Copilot, Gemini) working in this repository.

## Workspace standards (all repos, not just this one)

`.agents/instructions/workspace-config/standards/workspace-standards.yaml` defines the mandatory defaults for **every** repo in this workspace (clean root, README with fixed sections, technical language = English). Every agent, on any tool, should:

1. At the start of a session in this workspace, read `review.nextDue` in `~/dotfiles/.agents/instructions/workspace-config/standards/workspace-standards.yaml`.
2. If that date has passed, treat it as a strong reminder (not an absolute block) to do the SOTA review described in `review.sourcesToRecheck` before substantial unrelated work, propose the changes on a `claude/...` branch + PR (never a direct commit to `main`), and update `review.lastReviewed`/`nextDue`.
3. Run `python3 scripts/validate_workspace_standards.py .agents/instructions/workspace-config/standards/workspace-standards.yaml` after any edit to that file, before committing.

**Session hygiene (`sessionHygiene`, 2026-09-15):** when the current session reaches a natural conclusion, or has already gone through many rounds of agent dispatch/tool calls with a large context relative to what the next task actually needs, or the next request is unrelated to what filled the session so far — proactively suggest starting a new session, and **always hand back a ready-to-copy kickoff prompt** (don't just say "you should start a new session"). The concrete pattern is in this repo's `CHEATSHEET.md` §7: read `CLAUDE.md`+`CHEATSHEET.md`, rebuild the todo list from a persistent doc, and — this is the part every harness should also do, not just Claude Code — check `tasks/board.md` (and `tasks/README.md` for how to append events) for the workspace's cross-session task tracker, writing there (not only in-session) when something gets done.

(Claude Code has this automated via a `SessionStart` hook — see `CLAUDE.md`. Other tools follow this protocol in prose, here. **Known gap (2026-09-16):** this file and `CLAUDE.md` both reference `CHEATSHEET.md` §7 but neither used to mention `tasks/` explicitly, and `.github/copilot-instructions.md`/`GEMINI.md` had no startup pointer to either — see `CLAUDE.md`'s "Known Gaps" for the full finding and what's still needed to fix it for Copilot/Gemini/Antigravity.)

**Before writing to `tasks/` at all** (creating a task, moving a phase, or touching `tasks/events.jsonl`/`kanban.md`/`cards/` directly): read `tasks/README.md`'s "Agent actor-kind: never impersonate the human" and "`tasks/events.jsonl` is live and shared — don't run raw git ops on it" sections first (added 2026-09-24, after a real agent session did both wrong in the same afternoon). Short version — sign your own writes `actor.kind: agent`, never borrow a human's identity; and never `git checkout --`/`reset`/`stash`/`clean` that file in the shared checkout, since another session may be appending to it right now.

## Available Agents

| Agent | Config Location | When to Use |
|--------|-------------------|-------------|
| **Crush/Claude** | `~/.claude/`, `~/.claude.json` | Development, code analysis, debugging, automation |
| **Copilot CLI** | `~/.copilot/` | Terminal agent, own global instructions file — distinct from the VS Code extension, which reads `.github/copilot-instructions.md` per-project instead |
| **Gemini CLI** | `~/.gemini/` | Quick queries, brainstorming |
| **OpenAI Codex CLI** | `~/.codex/` | Terminal coding agent |
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

**Corrected 2026-09-16** — there is no single unified global file every
agent reads. Each tool has its own real, per-user global instructions file
at a fixed home-directory path (confirmed against each tool's own docs,
not assumed), symlinked file-level (never whole-directory — see
`setup.sh`'s `setup_agent_file_symlink` and the security fix it followed
from) to the versioned copy in this repo:

| File | Tool | Real path (symlink target) |
|----------|--------|----------|
| `dotfiles/.claude/CLAUDE.md` | Claude Code | `~/.claude/CLAUDE.md` |
| `dotfiles/.gemini/GEMINI.md` | Gemini CLI | `~/.gemini/GEMINI.md` |
| `dotfiles/.codex/AGENTS.md` | OpenAI Codex CLI | `~/.codex/AGENTS.md` |
| `dotfiles/.copilot/copilot-instructions.md` | GitHub Copilot CLI | `~/.copilot/copilot-instructions.md` |
| `.github/copilot-instructions.md` (this repo only) | GitHub Copilot (VS Code extension) | project-level, not global — auto-discovered per-repo |

All five of the per-tool pointer files above just redirect to the same
real source: `.agents/instructions/workspace-config/*.instructions.md`
(see `.agents/instructions/README.md`). No tool here has been confirmed to
read a plain `~/directory_tree.md`-style reference file either; don't
assume one exists without checking.

## Per-Agent Development Rules

### Crush/Claude
- **Reads:** `~/.claude/CLAUDE.md` (symlinked pointer → `.agents/instructions/workspace-config/`)
- **Preferences:** Deep analysis, technical explanations, script automation
- **Restrictions:** No automatic commits without explicit confirmation

### Copilot
- **Reads:** `.github/copilot-instructions.md` (project-level, VS Code extension) or `~/.copilot/copilot-instructions.md` (global, Copilot CLI — symlinked pointer, see above)
- **Preferences:** Fast inline suggestions, code completions
- **Restrictions:** Doesn't modify files without intervention

### Gemini
- **Reads:** `~/.gemini/GEMINI.md` (symlinked pointer → `.agents/instructions/workspace-config/`)
- **Preferences:** Brainstorming, ideation, concept verification
- **Restrictions:** Occasional use, no long-context storage

### OpenAI Codex CLI
- **Reads:** `~/.codex/AGENTS.md` (symlinked pointer → `.agents/instructions/workspace-config/`)
- **Restrictions:** Shares `~/.codex/` with the separate `herdr` tool's hook (`herdr-agent-state.sh`) — not part of Codex, don't edit it here

### Cline
- **Reads:** unverified — no per-tool global file confirmed for Cline yet, don't assume `~/.cline/` follows the same pattern until checked
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
readlink -f ~/.claude/CLAUDE.md   # confirm it resolves into dotfiles, not a real file

# Recreate manually — .agents/ and .vscode/ are whole-directory (safe: pure
# curated content / chezmoi+age-managed secret). The four per-tool
# instructions files are FILE-LEVEL ONLY — never symlink their directories,
# see setup.sh's setup_agent_file_symlink comment for why (their directories
# mix in credentials/session state that must never enter this repo).
ln -sf ~/dotfiles/.agents ~/.agents
ln -sf ~/dotfiles/.vscode ~/.vscode
ln -sf ~/dotfiles/.claude/CLAUDE.md ~/.claude/CLAUDE.md
ln -sf ~/dotfiles/.gemini/GEMINI.md ~/.gemini/GEMINI.md
ln -sf ~/dotfiles/.codex/AGENTS.md ~/.codex/AGENTS.md
ln -sf ~/dotfiles/.copilot/copilot-instructions.md ~/.copilot/copilot-instructions.md

# OR re-run setup
./setup.sh
```

### Agent Can't See Context
- Check that the relevant per-tool file is a symlink into this repo (see table above), e.g. `readlink -f ~/.claude/CLAUDE.md`
- Check permissions on the target: `ls -la .agents/instructions/workspace-config/`
- Reload the agent or restart the application

---

**Last Updated:** 2026-09-14
**Maintained by:** nmc-costa
