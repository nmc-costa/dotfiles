# copilot-instructions.md — global pointer (GitHub Copilot CLI)

This file is symlinked to `~/.copilot/copilot-instructions.md` (see
`setup.sh`'s `setup_agent_file_symlink`), the one versioned piece of
Copilot CLI's otherwise-local `~/.copilot/` state directory
(`session-store.db`, `logs/`, `config.json`, etc. stay real and untouched).

Distinct from this repo's own `.github/copilot-instructions.md`, which is
project-level and auto-discovered by GitHub Copilot inside this specific
repository — this file is Copilot CLI's personal, cross-project global
instructions file.

Real content lives in `.agents/instructions/workspace-config/` — read
every `*.instructions.md` there; they apply to every agent, not just
Copilot (see `.agents/instructions/README.md`).
