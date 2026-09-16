# AGENTS.md — global pointer (OpenAI Codex CLI)

This file is symlinked to `~/.codex/AGENTS.md` (see `setup.sh`'s
`setup_agent_file_symlink`), the one versioned piece of Codex CLI's
otherwise-local `~/.codex/` state directory (its sqlite state/goals/logs/
memories/queue databases stay real and untouched — as does
`herdr-agent-state.sh`, a hook installed by the separate `herdr` tool,
not part of Codex itself, that also lives in this directory).

Real content lives in `.agents/instructions/workspace-config/` — read
every `*.instructions.md` there; they apply to every agent, not just
Codex (see `.agents/instructions/README.md`).
