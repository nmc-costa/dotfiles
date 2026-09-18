# CLAUDE.md — global pointer

This file is the one piece of `~/.claude/` (Claude Code's live state
directory — credentials, sessions, logs, caches) that's actually versioned.
`setup.sh`'s `setup_agent_file_symlink` links only this file into
`~/.claude/CLAUDE.md`; the directory itself stays real, local, and
untouched — see the comment above that function for why (whole-directory
symlinking would put live runtime state, including `.credentials.json`,
inside the git working tree).

Real content lives in `.agents/instructions/workspace-config/` — read
every `*.instructions.md` there. Those apply to every agent, not just
Claude Code (see `.agents/instructions/README.md`), and get distributed to
`~/.agents/instructions/` by `sync.sh`.
