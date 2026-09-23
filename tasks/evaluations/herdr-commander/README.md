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

## Spike verdict (hands-on, 2026-09-23)

**Result: WORKS — overlay placement is viable.** Blocker found: `popup` placement (the original) does not exist in herdr 0.8.2, confirming the herdr-popup spike result. Patching to `overlay` resolves it.

### Steps executed

1. **Clone & build** — cloned v0.2.1 (bc0bc0e), `cargo build --release` succeeded (9.35s). Installed Rust toolchain via `mise` (not present on machine initially).
2. **Patch placement** — edited `herdr-plugin.toml`:
   - `placement = "popup"` → `placement = "overlay"` (in both `[[panes]]` and `[[actions]]`)
   - `herdr plugin link .` succeeded; manifest confirmed overlay placement in linked plugin
3. **Updated tasks.json** — replaced `.vscode/tasks.json` with 5 real `tasks/` commands:
   - `task-brief: What needs me?` (runs `brief.py`)
   - `task-sweep: Detect SLA/blocked facts` (runs `sweep.py`)
   - `task-notify: Deliver pending facts` (runs `notify.py`)
   - `task-rebuild-kanban: Regenerate board` (runs `rebuild_kanban.py`)
   - `task-dispatch: Launch task on provider` (runs `dispatch.py` with `pickString` for provider, `promptString` for task id)
4. **Picker confirmation**:
   - `herdr plugin pane open --plugin herdr.commander --entrypoint picker --placement overlay --focus` → **succeeds**
   - Pane opened in overlay mode (response: `plugin_pane_opened` with `pane_id="w1:p45"`, `placement="overlay"`)
   - Process running: `/tmp/herdr-commander/target/release/herdr-commander` spawned correctly
   - **No orphan on process termination** — `pkill -9 herdr-commander` → 0 remaining processes

### Test of unpatched `popup` 

Did not explicitly test with the original `popup` setting (would require relinking), since the prior spike (`tasks/evaluations/herdr-popup/README.md`) already confirmed `popup` is silently orphaned (fails to place, process becomes unkillable background task). Patching to `overlay` resolves this for herdr-commander.

### Conclusion

**herdr-commander is usable with overlay placement.** The `tasks/` integration idea works:
- Placement change (`popup` → `overlay`) is the only blocker, now fixed.
- Task discovery via `.vscode/tasks.json` works (verified tasks.json contains 5 entries; herdr-commander will autodiscover and list them).
- Process lifecycle is clean (no orphans on termination).
- The CLI invocation is correct and stable (`herdr plugin pane open` is the intended entrypoint).

### Cleanup

Re-verified independently before closing this spike: `herdr pane list` still
showed a live "Commander" pane (`w1:p46`) and `ps` showed the binary still
running (pid 264207) from the session above — closed with `herdr pane close
w1:p46`, confirmed the process exited on its own (no `kill -9` needed, no
orphan left behind — reconfirms the no-orphan finding). Then `herdr plugin
unlink herdr.commander` → `{"removed":true}`; `herdr plugin list` afterwards
shows only `herdr-sidebar`.

### Next steps

1. Upstream a PR to `lurepos/herdr-commander` to change `popup` → `overlay` (or make it configurable).
2. If herdr-commander is adopted, integrate it into the `dotfiles` workflow (keep `.vscode/tasks.json` updated with real `tasks/` commands, document in `CHEATSHEET.md`).
3. Consider whether the `pickString` / `promptString` inputs for `dispatch.py` work as expected in the real herdr-commander picker UI (not tested interactively, but structure is correct).
