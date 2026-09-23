# Antigravity: branch-name policy & client hook

This workspace enforces harness-prefixed branch names (for example: `copilot/*`, `claude/*`, `agy/*`). The policy is enforced server-side by the CI workflow `.github/workflows/branch-name-policy.yml` and encouraged locally with a client-side pre-push hook.

Why
- Makes authorship and origin explicit for branches and worktrees created by automated harnesses.
- Helps CI, reviewers, and automation attribute work to a harness.

How to comply
1. When creating a branch or worktree, prefix it with your harness name, for example:
   - `copilot/dotfiles-tsk-archive-and-reorg`
   - `claude/some-investigation`

2. Install the optional client hook locally to warn or block non-conforming pushes:
   - Manual: `bash tasks/scripts/setup_git_hooks.sh`
   - Opt-in during setup/sync: `./setup.sh --install-hooks` or `./sync.sh --install-hooks`

Notes
- Installation is opt-in and requires explicit consent on the machine.
- The hook installer copies `tasks/scripts/pre-push.sample` to `.git/hooks/pre-push` for each repo you want protected.
- Server-side CI rejects pushes/PRs without a harness prefix; ensure your branch name follows the pattern.

Files of interest
- tasks/scripts/pre-push.sample — sample hook (edit before installing if you want stricter behavior)
- tasks/scripts/setup_git_hooks.sh — installer script used by `--install-hooks`
- .github/workflows/branch-name-policy.yml — server-side enforcement workflow
