---
name: task-worktree
description: >
  One git worktree per (harness, tasks/ card), identical for Claude Code,
  Copilot CLI, Gemini CLI, Antigravity and Codex. Use before writing code for
  a tasks/ card in ~/dotfiles, when asked to "work card X in its own
  worktree", "isolate this task", "where is the worktree for X", "list/clean
  up task worktrees", or when dispatching a card to another harness. Thin
  shell over tasks/worktree.py — all real logic lives there.
---

# /task-worktree

Thin shell over `tasks/worktree.py` (design: `tasks/plans/card-worktrees.md`).
Never re-implement it with raw `git worktree` calls, and never use a
harness-native worktree (`claude -w`, `gemini -w`, `codex --worktree`,
`EnterWorktree`) for tasks work — each one picks its own location and naming,
which is exactly the non-uniformity this exists to remove.

Layout: `~/dotfiles.worktrees/<harness>/<task-id>` on branch
`<harness>/<task-id>`. `<harness>` is one of `claude copilot gemini agy codex`
— pass your own name, or rely on `$TSK_HARNESS` (set by `dispatch.py`).

## What to do

1. **Am I already in it?**
   `python3 ~/dotfiles/tasks/worktree.py path --task-id <id> --harness <you>`
   — if your process cwd is that path, just work and commit there.
2. **If not:** create it (idempotent — returns the existing one):
   `python3 ~/dotfiles/tasks/worktree.py create --task-id <id> --harness <you>`
   → `path<TAB>branch<TAB>created|existing` (exit 1 = bad input; read stderr,
   do not work around it).
   Then **relaunch inside it** rather than `cd`-ing mid-session — several
   harnesses pin file tools/sandbox to their startup directory:
   `python3 ~/dotfiles/tasks/dispatch.py --task-id <id> --provider <you> --worktree --launch`
   (claude/copilot/agy today), or tell the human to start the CLI from that
   path. Never keep editing the main checkout.
3. **Branch already exists** (exit 1 mentioning `--reuse-branch`): it may be
   someone else's work — ask the human before passing `--reuse-branch`.
4. **Show the human:** `tasks/cards/worktrees/<id>.md` (gitignored,
   per-machine; each card links to it) or
   `python3 ~/dotfiles/tasks/worktree.py list [--task-id <id>] [--json]`.
5. **Cleanup** only when asked: `remove --task-id <id> --harness <h>`, or
   `prune` (dry-run; `--apply` only after the human agrees). Both refuse
   (exit 2) dirty, locked, or currently-occupied worktrees, and never delete
   the branch.

## What NOT to do

- No `--force`, no `git worktree remove` by hand, no branch deletion.
- Don't create worktrees for review/validation-only work — only for code.
- Don't write events from inside a worktree by hand; `tasks/*.py` already
  resolve the one real log via `tasks_root()`.
