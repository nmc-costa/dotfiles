---
task_id: dotfiles-tsk-gh-path-recursion
title: Fix infinite recursion in ~/.local/bin/gh wrapper (duplicate PATH entry)
project: dotfiles
phase: review
created: "2026-09-22T13:27:13.769285+00:00"
touched: "2026-09-22T13:36:18.186974+00:00"
energy: ""
estimate: ""
deadline: ""
blocked_by: ""
origin: ""
---

# dotfiles-tsk-gh-path-recursion

Fix infinite recursion in ~/.local/bin/gh wrapper (duplicate PATH entry)

## History
- 2026-09-22T13:35:47.491731+00:00: backlog -> planning (actor: claude-code-bg/agent) — Claimed via claim.py, investigating gh wrapper recursion
- 2026-09-22T13:36:02.043086+00:00: planning -> in_progress (actor: claude-code-bg/agent) — Root cause found: ~/.bash_profile sources ~/.bashrc then independently re-exports PATH with .local/bin (both added by Antigravity CLI installer) -> real duplicate PATH entry confirmed under login shell. Wrapper's 'exec mise x gh -- gh $@' relies on PATH lookup for the nested gh arg, which can resolve back to the wrapper itself. Could not reproduce an actual hang in this session even with the duplicate present (mise x seems to resolve its primary command target internally, not via plain PATH search) but the structural defect + self-reference hazard are real and worth closing regardless.
- 2026-09-22T13:36:18.186974+00:00: in_progress -> review (actor: claude-code-bg/agent) — Fix applied directly (neither ~/.bashrc, ~/.bash_profile, nor ~/.local/bin/gh are chezmoi/dotfiles-managed -- confirmed via 'chezmoi source-path', so no git repo/PR involved). Changes: (1) ~/.local/bin/gh now execs $(mise which gh) directly instead of 'mise x gh -- gh $@', removing all PATH-based self-reference risk. (2) ~/.bash_profile's redundant 'export PATH=.../.local/bin:$PATH' (added by Antigravity CLI installer) removed -- .bashrc already exports it and .bash_profile sources .bashrc first, so this was pure duplication for every login shell. Verified under bash -lc (real login shell): PATH now has exactly 1 .local/bin entry (was 2), gh --version and gh pr list both return promptly (exit 0). Needs owner eyes since it edited live shell rc files outside git.

Worktrees (this machine): [worktrees/dotfiles-tsk-gh-path-recursion.md](worktrees/dotfiles-tsk-gh-path-recursion.md) — `python3 ~/dotfiles/tasks/worktree.py list --task-id dotfiles-tsk-gh-path-recursion`
