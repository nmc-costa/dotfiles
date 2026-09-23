# herdr-commander fit check (2026-09-23)

Desk review of [`lurepos/herdr-commander`](https://github.com/lurepos/herdr-commander)
(v0.2.1, Rust, `herdr-plugin.toml` id `herdr.commander`) for
`dotfiles-tsk-spike-herdr-commander`. **Nothing installed yet** — this is
the pre-spike verdict; the card stays in `backlog` until someone runs the
hands-on check below.

## What it is

A herdr popup command palette: autodiscovers `.vscode/tasks.json`,
`package.json` scripts, `Cargo.toml` and `Makefile` targets in the current
workspace, fuzzy-filters them, and runs the chosen one in a new tab, a
right/bottom split, or the current pane. Process-group kill on cancel.

## Fit with tasks/

**Partial — useful idea, not usable as-is.**

What fits:
- The daily `tasks/` loop is a handful of CLI calls (`brief.py`,
  `sweep.py`, `notify.py`, `dispatch.py`, `move_task.py --show-handoff`,
  `rebuild_*`). A one-key palette inside herdr for those is exactly the
  "human director" ergonomics the Workspace Agil doc asks for, and it
  reuses herdr, which is already our notification surface.
- Placement choice (tab/split) maps well onto `dispatch.py --launch`
  opening a provider session beside the board.

Blockers / risks found:
1. **Uses `placement = "popup"`** in both the `[[panes]]` entry and the
   `open-picker` action. Our own spike
   (`tasks/evaluations/herdr-popup/README.md`) showed `popup` is not in
   herdr 0.8.2's placement enum (`overlay, split, tab, zoomed` — re-checked
   today with `herdr plugin pane open --help`) and fails *silently*,
   leaving an orphaned process. Expect the picker to never appear on this
   machine unless patched to `overlay` (fork, or `herdr plugin link` a
   local checkout with the manifest edited).
2. **Nothing to discover in dotfiles today.** No `Makefile`,
   `package.json` or `Cargo.toml`; `.vscode/tasks.json` is an unedited
   Kedro template (`/path/to/kedro/script` placeholders). We'd have to
   add a real `.vscode/tasks.json` (or `Makefile`) exposing the `tasks/`
   commands — which is worth doing anyway, and would also serve VS Code.
3. **`bin/run.sh` downloads a prebuilt binary** from GitHub Releases of
   `lurepos/herdr-commander` *or* `lurepos/herdr-vscode-tasks`, with no
   checksum, before falling back to `cargo build`. Prefer building from a
   pinned commit.
4. **Young, tiny project** — created 2026-08-12, 2 stars, last push
   2026-09-20. Fine for an optional convenience layer; nothing in
   `tasks/` should depend on it (same rule as R1 in
   `tasks/plans/human-in-the-loop-notifications.md`: the CLI is the
   contract, the UI is decoration).

## Proposed spike (hands-on)

1. Clone at a pinned commit, `cargo build --release`, patch
   `herdr-plugin.toml` → `overlay`, `herdr plugin link .`.
2. Replace `.vscode/tasks.json` with real entries for `brief.py`,
   `sweep.py`, `notify.py`, `rebuild_kanban.py`, `dispatch.py` (with a
   `pickString` input for provider and `promptString` for task id).
3. Confirm: picker opens (overlay), lists those tasks, runs one in a right
   split; `Ctrl+C` leaves no orphan (`ps`). Also try unpatched `popup` to
   see whether it reproduces the herdr-popup orphan.
4. Verdict here; if good, upstream a PR switching `popup` → `overlay`
   (or making it configurable) and unlink when done.
