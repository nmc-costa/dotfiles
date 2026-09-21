#!/usr/bin/env python3
"""Single source of truth for where tasks/ DATA lives — events.jsonl,
kanban.md, claims.jsonl, and everything else `rebuild_*.py`/
`append_event.py` read or write.

Deliberately has zero imports from the rest of tasks/ (not even
lifecycle.py) — lifecycle.py itself imports from rebuild_view.py
(`payload_get`), so if this lived inside lifecycle.py and rebuild_view.py
tried to import it back, that would be a circular import. Keeping the
resolver in its own leaf module lets every script (including
rebuild_view.py) import it safely.

Before this existed, every rebuild_*.py and append_event.py derived both
their data root AND their sibling-module import path from the same
`Path(__file__).parent` — so a script copy running inside a git worktree
silently wrote (and read) that worktree's own divergent copy of the log
instead of the one real, shared log. Confirmed on 2026-09-21 to have
produced 4 divergent copies of events.jsonl at once and one silently
orphaned event (see tasks/plans/claim-protocol.md, section B, and the
dotfiles-tsk-dispatch-launcher recovery in the same session).
"""
import os
import sys
from pathlib import Path

_CANONICAL_TASKS_ROOT = Path("~/dotfiles/tasks").expanduser().resolve()


def tasks_root():
    """Canonical directory for tasks/ DATA files — never derived from
    `__file__`, so it stays correct regardless of which worktree's copy of
    the calling script happens to be running.

    Resolution order:
    1. `$TSK_ROOT` if set — explicit opt-in, e.g. `demo/run_demo.sh`'s
       isolated scratch log, or developing tasks/ itself inside a worktree
       against a throwaway log.
    2. Otherwise always `~/dotfiles/tasks`, regardless of where the calling
       .py file physically lives.

    Deliberately no path-pattern guard (a `.claude/worktrees/` substring
    check would only catch `EnterWorktree`-made worktrees, not a manual
    `git worktree add`, and would still block the legitimate `$TSK_ROOT`
    opt-in case) — when the resolved root isn't the canonical one, one
    line goes to stderr so it's visible, never a hard failure.
    """
    env = os.environ.get("TSK_ROOT")
    root = Path(env).expanduser().resolve() if env else _CANONICAL_TASKS_ROOT
    if root != _CANONICAL_TASKS_ROOT:
        print(f"tasks: using non-canonical tasks_root {root} (canonical: {_CANONICAL_TASKS_ROOT})", file=sys.stderr)
    return root
