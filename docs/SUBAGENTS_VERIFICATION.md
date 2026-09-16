# SUBAGENTS_VERIFICATION.md

Verification checklist to ensure every subagent has access to the correct dotfiles information.

## Configured Agents

- ✅ **Crush/Claude** — `~/.claude/`
- ✅ **Copilot** — `~/.copilot/`
- ✅ **Gemini** — `~/.gemini/`
- ✅ **Cline** — `~/.cline/`

## Global Context Files (Symlinks)

Every agent should have access to:

| File | Location | Status | Verification |
|----------|------------|--------|-------------|
| `directory_tree.md` | `~/dotfiles/directory_tree.md` → `~/directory_tree.md` | ⏳ | `ls -la ~/directory_tree.md` |
| `.context-global.md` | `~/dotfiles/.context-global.md` → `~/.context-global.md` | ⏳ | `ls -la ~/.context-global.md` |
| `claude.md` | `~/dotfiles/claude.md` → `~/claude.md` | ⏳ | `ls -la ~/claude.md` |
| `.agents/` | `~/dotfiles/.agents/` → `~/.agents/` | ✅ | `ls -la ~/.agents/` |
| `.claude/` | `~/dotfiles/.claude/` → `~/.claude/` | ✅ | `ls -la ~/.claude/` |
| `.vscode/` | `~/dotfiles/.vscode/` → `~/.vscode/` | ✅ | `ls -la ~/.vscode/` |
| `.github/` | `~/dotfiles/.github/` → `~/.github/` | ✅ | `ls -la ~/.github/` |

**Status:**
- ✅ = Confirmed working
- ⏳ = To verify (should exist in dotfiles)
- ❌ = Still needs creating

## Available Skills

Skills in `~/.agents/skills/`:

```bash
ls ~/.agents/skills/
```

Expected:
- ✅ `diagnose-crash/` — SKILL.md + reporting.md
- ✅ `omarchy/` — SKILL.md + hyprland.md + theming.md + ...

To sync:
```bash
cd ~/dotfiles
./sync.sh --verbose
```

## Available Workflows

Workflows in `~/.agents/workflows/`:

```bash
ls ~/.agents/workflows/
```

Expected:
- ✅ `init.md` — New-agent initialization
- ✅ `architect_html_sciml.md` — Persona for Architect

## Root Documentation

Every root-level `.md` in dotfiles should be up to date:

| File | Last Update | Status |
|----------|-------------------|--------|
| `README.md` | Structure and setup | ✅ Updated |
| `AGENTS.md` | Skills in `.agents/` | ✅ Updated |
| `CLAUDE.md` | dotfiles context | ✅ Updated |
| `GEMINI.md` | dotfiles context | ✅ Updated |
| `VSCODE_MONITOR_QUICKSTART.md` | Legacy (verify) | ⏳ |
| `directory_tree.md` | Directory map | ⏳ Verify it exists |

## Spinning Up Subagents

When to spin up (activate) a new subagent:

1. **Copy global context:**
   ```bash
   ln -sf ~/dotfiles/.claude ~/.claude
   ln -sf ~/dotfiles/.agents ~/.agents
   ln -sf ~/dotfiles/.vscode ~/.vscode
   ```

2. **Sync skills:**
   ```bash
   ~/dotfiles/sync.sh
   ```

3. **Verify access:**
   ```bash
   ls ~/.agents/skills/
   cat ~/.agents/skills/diagnose-crash/SKILL.md
   ```

4. **Test skill trigger:**
   ```bash
   # The agent should recognize keywords
   # e.g. "segfault" should activate the diagnose-crash skill
   ```

## Full Setup Checklist

- [ ] `.agents/` folder exists and is a symlink
- [ ] `.agents/skills/` contains skills (diagnose-crash, omarchy)
- [ ] `.agents/workflows/` contains workflows (init.md, architect_html_sciml.md)
- [ ] `sync.sh` runs without errors: `./sync.sh --dry-run`
- [ ] Every root `.md` (`README.md`, `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`) mentions `.agents/`
- [ ] No `.agent/` folder exists (it was migrated to `.agents/`)
- [ ] `setup.sh` creates symlinks correctly: `./setup.sh --dry-run`

## How to Use This Document

1. Run all the checks above
2. Mark the status of each item
3. If anything fails, check the matching section in `AGENTS.md` or `README.md`
4. Commit any fix: `git add -A && git commit -m "Fix [subagent] setup"`

---

**Last Updated:** 2026-09-14
**Maintained by:** nmc-costa

When new subagents are added, update this file with their config locations.
