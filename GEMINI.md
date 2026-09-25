# GEMINI.md

Instructions for Gemini when working in this repository.

## Context

`~/dotfiles` is the central repository for configuration and environment synchronization across machines. It contains:

- **Agents:** Crush, Copilot, Gemini, Cline configurations in `.agents/`
- **Skills:** Agent extensions in `.agents/skills/`
- **Workflows:** Personas and workflows in `.agents/workflows/`
- **Context:** `AGENTS.md`, `CLAUDE.md`, `docs/directory_tree.md`
- **Automation:** `setup.sh`, `sync.sh`

## At the start of a session, also read

- **`CHEATSHEET.md`** — where things go, and §4's persistent cross-session TODO list (survives longer than any single session's own tracking).
- **`tasks/board.md`** and **`tasks/README.md`** — the workspace's task tracker (an append-only event log projected into a table). Check it for open work before starting something new, and append an event with `tasks/append_event.py` when you finish something worth tracking there.
- **`HANDOFF.md`** at the repo/subsystem root, if present — read its top block (previous session's state + next step, possibly from another harness/model). When stopping with work unfinished, write one per `.agents/skills/handoff/SKILL.md` (`python3 ~/.agents/skills/handoff/handoff.py new|check|prompt`).

(Added 2026-09-16 — Claude Code gets this automatically via a `SessionStart` hook; Gemini has no equivalent hook yet, so this section is the manual substitute. See `CLAUDE.md`'s "Known Gaps" for the full finding.)

## Project Structure

Real projects live in:
- **`~/Projects/`** — Personal repos (agentic_instructions, HIcode, ibots, roi_lab, etc.)
- **`~/Work/`** — Professional repos (mobai, RAGFusion, sp_xai_nos, etc.)

Each project is an independent git repository with its own remote.

## Using This Repo

1. **View structure:** `cat ~/dotfiles/README.md`
2. **View available skills:** `ls -la ~/.agents/skills/`
3. **Add a new skill:** see `AGENTS.md` > "Adding a New Skill"
4. **Set up a new machine:** `cd ~/dotfiles && ./setup.sh --dotfiles`

## Best Practices

- Don't edit skills directly in `~/.agents/skills/` — always edit in `~/dotfiles/.agents/skills/` and sync
- For personal workflows: use `~/.agents/workflows/` (symlink to `~/dotfiles/.agents/workflows/`)
- For new skills: add to `~/dotfiles/.agents/skills/` and do `git commit + ./sync.sh`

## Full Documentation

See `AGENTS.md` for the detailed guide on agents, skills, workflows, and cross-machine synchronization.
