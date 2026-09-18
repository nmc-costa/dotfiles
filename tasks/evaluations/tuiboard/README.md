# tuiboard evaluation (2026-09-18)

Fase-0 de-risking spike for the orchestration architecture decided in
`tasks/README.md`'s "Orchestration architecture" section — specifically the
"evaluate `tuiboard` before writing anything in Rust" item. **Result:
tuiboard passes.** It's a good candidate base for the eventual `tsk board`
UI layer.

## What was tested

[`NazzarenoGiannelli/tuiboard`](https://github.com/NazzarenoGiannelli/tuiboard)
(MIT, 114★, Bun + OpenTUI + SolidJS), installed from source into a scratch
directory (not this repo, not globally) and run against a throwaway board
file with our decided 6-stage lifecycle (`Backlog → Planning → In Progress →
Review → Validation → Done`), with one dummy task (`T-0001`) moved through
every column.

## Findings

**Safety.** Read `package.json` and grepped `src/` for network calls before
installing anything: no `postinstall`/`preinstall` scripts, dependencies are
all well-known (`@opentui/*`, `chokidar`, `js-yaml`, `solid-js`), and the
only network-capable feature (an optional Google/Microsoft 365 calendar
overlay) requires explicit interactive OAuth setup — never called
automatically. Left off in the test config.

**Local.** The board is plain markdown on disk. The "Agents (live)" panel
reads `~/.claude/`, `~/.codex/`, etc. read-only, locally, with zero network
calls — confirmed by the grep above, not just by the README's claim.

**Fast.** Near-instant startup, ~165MB RSS, CPU settles after the initial
render. Nothing alarming for a terminal app.

**Architecturally important finding: tuiboard has no interactive
"move task to another column" command.** It's a pure watch-and-render tool
(`chokidar` on the board files) — moving a task between columns means
editing which `##` heading the task line sits under, and the live-reload is
instant. This is exactly the shape our `tsk` CLI needs: `tsk` writes to the
task file, tuiboard just reflects it. Confirmed empirically (see `states/`)
by editing `example-board.md` directly six times and capturing the
re-rendered board after each edit — every transition (including the
`Done`-column-hides-and-counts-separately behavior the README promises)
worked exactly as documented.

**Bonus:** the live Agents panel showed real, current Claude Code sessions
on this machine with zero configuration — including the session that ran
this very evaluation.

## Files here

- `example-board.md` — the throwaway board file, left in its final state
  (`T-0001` in `Done`)
- `example-config.yaml` — the isolated `TUIBOARD_CONFIG` used (points at a
  scratch path outside this repo — not reusable as-is, kept for reference)
- `states/1-backlog.txt` … `states/6-done.txt` — `tmux capture-pane -p`
  text snapshots after each of the 6 transitions
- `all-states-combined.txt` — all 6 states concatenated with headers, for a
  single-file read-through

## Not yet tested

Multi-vendor session detection (only Claude Code sessions were live on this
machine during the test — Codex/OpenCode/Pi panels are implemented per the
tuiboard README but unverified here), the herdr integration path (`H` to
jump to a session), and whether contributing our state machine to tuiboard
vs. forking it is the better call — both still open per `tasks/README.md`.
