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

---

## Branch naming policy & client hook

This workspace enforces harness-prefixed branch names (e.g. `copilot/*`, `claude/*`, `agy/*`). A server-side CI workflow rejects pushes/PRs without one. To help local contributors and harnesses opt in to this policy, a client-side pre-push hook is provided at `tasks/scripts/pre-push.sample` and an installer script at `tasks/scripts/setup_git_hooks.sh`.

To install the hook manually:

  bash tasks/scripts/setup_git_hooks.sh

Or opt-in during initial setup/sync by running `./setup.sh --install-hooks` or `./sync.sh --install-hooks`. This is optional and never forced by the scripts; it requires explicit consent from the machine's user.

When creating branches or worktrees, include your harness name as a prefix so CI and reviewers can trace which harness created the branch (example: `copilot/feature-x`).
