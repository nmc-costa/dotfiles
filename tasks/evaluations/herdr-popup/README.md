# herdr popup-pane spike (2026-09-21)

Spike for `dotfiles-tsk-spike-herdr-popup`. **Result: `--placement popup` does
not exist on herdr 0.8.2 and, when passed anyway, silently produces an
orphaned, invisible pane — not a popup, not an error.** `--placement
overlay` is the real, working equivalent and does what a "popup" is
presumably meant to do: it opens a new, focused, listed pane on top of the
current layout.

## What was built

A trivial plugin at `tasks/evaluations/herdr-popup/plugin/`:

- `herdr-plugin.toml` — one `[[panes]]` entry, id `popup`, placement
  `overlay` (see findings below for why not `popup`), running
  `bash scripts/popup.sh`. Plugin id: `herdr-popup-spike`.
- `scripts/popup.sh` — prints a banner (`herdr-popup-spike: pane opened
  successfully`), its own PID, a UTC timestamp, then `exec sleep 300` so the
  pane/process stays alive long enough to inspect.

Modeled on `herdr-sidebar`'s manifest and its
`scripts/open-sidebar.sh` fallback (`herdr plugin pane open --plugin
herdr-sidebar --entrypoint filetree --placement split --direction right
--focus`), read from
`/home/nbugz/.config/herdr/plugins/github/herdr-sidebar-7ff2582a7c8a/plugins/herdr-sidebar/`
before writing anything here.

## Commands run, in order

```bash
herdr plugin link tasks/evaluations/herdr-popup/plugin
# -> {"result":{"plugin":{"plugin_id":"herdr-popup-spike", ...}}}

herdr plugin pane open --plugin herdr-popup-spike --entrypoint popup \
  --placement popup --focus
# -> {"id":"cli:plugin","result":{"type":"ok"}}   (as instructed by the task)

herdr plugin pane open --plugin herdr-popup-spike --entrypoint popup \
  --placement overlay --focus
# -> {"result":{"plugin_pane":{"pane":{"pane_id":"w1:p3E","label":"Popup Spike",
#     "focused":true,"workspace_id":"w1","tab_id":"w1:t9", ...}}}}

herdr pane close w1:p3E                 # clean up the overlay pane
kill 3678121                            # clean up the orphaned popup-placement process
herdr plugin unlink herdr-popup-spike
# -> {"result":{"plugin_id":"herdr-popup-spike","removed":true,"type":"plugin_unlinked"}}
```

## Findings

**`--placement popup` is not a real value.** `herdr plugin pane open
--help` on this install (herdr 0.8.2) lists exactly four possible values
for `--placement`: `overlay, split, tab, zoomed`. `popup` is not among
them. This matches the task brief's own instruction to try `popup`
literally — that instruction does not match what the CLI actually accepts.

**It doesn't fail loudly, though — it fails silently.** Running the exact
command from the task brief:

```
herdr plugin pane open --plugin herdr-popup-spike --entrypoint popup --placement popup --focus
```

returned `{"type":"ok"}` with exit code 0 — no validation error, no
rejection. But:

- `herdr pane list` right after showed no pane for it — none of the 34
  panes listed had our label ("Popup Spike") or plugin's cwd.
- Grepping `herdr plugin log --plugin herdr-popup-spike` returned an empty
  log list.
- The server log (`~/.config/herdr/herdr-server.log`) told the real story:
  ```
  17:26:29.814 spawning pane terminal pane_id=48 rows=18 cols=77
  17:26:29.816 pane child spawned pane_id=48 pid=3678121
  17:26:29.816 api request completed outcome="ok"
  ```
  A process *was* spawned server-side (confirmed independently with
  `ps -p 3678121` → `sleep 300`, i.e. our script's own tail command ran
  successfully), but it was never attached to any workspace/tab, so it
  never became a visible, addressable pane — no `w<n>:p<id>` id, absent
  from `herdr pane list`, absent from plugin logs. It was cleaned up with a
  plain `kill 3678121` since `herdr pane close` has no way to address it.

**`--placement overlay` is the working equivalent.** Same plugin, same
entrypoint, `--placement overlay` instead:

```
herdr plugin pane open --plugin herdr-popup-spike --entrypoint popup --placement overlay --focus
```

returned a full `plugin_pane` object — `pane_id: "w1:p3E"`, `label: "Popup
Spike"`, `focused: true`, attached to `workspace_id: "w1"` / `tab_id:
"w1:t9"` — and this pane *did* show up in `herdr pane list` immediately
after, confirming it is a real, visible, focused pane on top of the
existing layout (functionally a popup). Closed cleanly afterward with
`herdr pane close w1:p3E`.

## Confirmed vs. not confirmed

- **Confirmed:** plugin linking, manifest parsing, and pane-open work as
  documented for the `overlay` placement — verified via the command's own
  JSON response (`plugin_pane_opened`) and independently via `herdr pane
  list` showing the resulting pane.
- **Confirmed:** `--placement popup` is accepted by argument parsing (no
  CLI-level rejection) but produces an orphaned process, not a usable pane
  — verified via `herdr pane list` (absent), `herdr plugin log` (empty),
  the server log (spawn with no attach step), and `ps` (process alive but
  unaddressable through herdr).
- **Not tested:** `tab` and `zoomed` placements (out of scope — the task
  asked specifically about popup behavior; `overlay` already answers "is
  there a popup-like placement that works").
- **Confirmed:** `herdr plugin unlink herdr-popup-spike` was run at the end
  and returned `{"removed":true}`; a follow-up `herdr plugin list --json`
  shows only `herdr-sidebar` remaining — the spike plugin is not left
  registered on the shared herdr server.

## Recommendation

If a future plugin on this repo wants popup-like behavior, use
`--placement overlay` (and `placement = "overlay"` in the manifest's
`[[panes]]` entry) — not `popup`, which does not exist in herdr 0.8.2's
placement enum and silently leaks an orphaned process if used.

## Files here

- `plugin/herdr-plugin.toml` — the minimal manifest (kept as `overlay`,
  the value that actually works)
- `plugin/scripts/popup.sh` — the minimal pane script
