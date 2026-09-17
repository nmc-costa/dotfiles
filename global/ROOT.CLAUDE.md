# CLAUDE.md

Root-level context for Claude Code when working from `~` (home directory) and any subdirectories outside `~/dotfiles`.

## Quick summary

This file provides context for the unified home directory workspace:
- `~/Projects/` → Personal projects and studies (isolated context)
- `~/Work/` → Professional/employment repositories (isolated context, non-shared)
- `~/.agents/`, `~/.claude/` → Symlinks reflecting `~/dotfiles/.agents/` (source of truth)

See `@~/dotfiles/AGENTS.md` for the complete agent guide and skill reference.

## Directory conventions

Use these paths consistently in all communications about files and repositories:

| Context | Path convention | Example |
|---------|-----------------|---------|
| Personal projects | `Projects/<repo-name>/...` | `Projects/roi_lab/src/main.py` |
| Work/employment | `Work/<repo-name>/...` | `Work/dtx-dashboard/README.md` |
| Configuration/rules | `.dotfiles/<file>` | `.dotfiles/AGENTS.md`, `.dotfiles/CLAUDE.md` |
| Tools/scripts | `.dotfiles/<item>` | `.dotfiles/setup.sh`, `.dotfiles/sync.sh` |

Never assume a folder called `github/`, `gitlab/`, `bitbucket/` exists at the root — repos are organized by **context (personal vs. professional)**, not by platform.

## Getting help

- **AI agent reference:** `@~/dotfiles/AGENTS.md` (complete guide for Claude Code, Copilot, Gemini CLI, and other harnesses)
- **Quick cheatsheet:** `@~/dotfiles/CHEATSHEET.md` (where things go, workspace conventions, persistent TODOs)
- **Available skills:** listed in `@~/dotfiles/AGENTS.md` and available as `/skill-name` in Claude Code

## Workspace structure

For project-specific guidance, see `CLAUDE.md` files within each context:
- `~/Projects/CLAUDE.md` — Personal project conventions
- `~/Work/CLAUDE.md` — Professional project conventions and company rules (local, not shared via dotfiles)

---

**Source of this file:** `~/dotfiles/global/ROOT.CLAUDE.md` (symlinked as `~/CLAUDE.md`)
