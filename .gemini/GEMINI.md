# GEMINI.md — global pointer

This file is symlinked to `~/.gemini/GEMINI.md` (see `setup.sh`'s
`setup_agent_file_symlink`), the one versioned piece of Gemini CLI's
otherwise-local `~/.gemini/` state directory (`history/`, `state.json`,
`trustedFolders.json`, etc. stay real and untouched).

Real content lives in `.agents/instructions/workspace-config/` — read
every `*.instructions.md` there; they apply to every agent, not just
Gemini (see `.agents/instructions/README.md`).
