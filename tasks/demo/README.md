# tasks/demo/

A self-contained, runnable test of `move_task.py`'s metrics and handoff
features. Not docs — an actual working example, isolated from the real
`tasks/`. See `tasks/CHEATSHEET.md` for the quick command reference this
demo exercises.

## Run it

```bash
cd tasks/demo
./run_demo.sh
```

Takes a few seconds. Wipes and rebuilds its own state every time, so it's
safe to re-run. It never touches the real `tasks/events.jsonl` — see
"Why this is isolated" below.

## What it does

Creates 2 tasks (`demo-report`, `demo-cleanup`), each worked by 2 different
teams across the full 6-phase lifecycle:

- **team-scout** does `planning`
- **team-forge** does `in_progress` → `review` → `validation` → `done`

Every phase transition that closes out real work calls `move_task.py` with
`--team`/`--tokens`/--cost-usd`/`--duration-seconds`/`--cycles` (all
simulated numbers, distinct per task so the totals are actually comparing
something). `demo-cleanup`'s review phase deliberately uses `--cycles 2` to
show a retry in the data. `demo-report`'s handoff from team-scout to
team-forge also carries a `--handoff` note, retrieved at the end with
`--show-handoff` — a worked example of the "what does the next
team/session need to resume this" mechanism.

## What it produces

- `kanban.md` — both tasks end in `Done` (tuiboard-format board; point
  tuiboard at this file to watch it live, same shape verified in
  `tasks/evaluations/tuiboard/`)
- `metrics.md` — three tables: every metered phase-transition, totals by
  team, totals by task. This is the part meant to eventually inform
  "which team/model tier is actually cost-effective at which phase" —
  nothing analyzes it yet, this only proves the data collects correctly.

## Why this is isolated

The scripts here (`append_event.py`, `move_task.py`, `rebuild_kanban.py`,
`rebuild_metrics.py`, `rebuild_view.py`) are copies of the real ones in
`tasks/`. Each script resolves its data files relative to its own location
(`Path(__file__).parent`), so running the copies here reads and writes
`tasks/demo/events.jsonl`, never the real `tasks/events.jsonl` — no flags,
env vars, or extra setup needed. `events.jsonl`/`kanban.md`/`metrics.md`/
`board.md` in this folder are gitignored — `run_demo.sh` regenerates them
from nothing every time, there's nothing here worth keeping between runs.

## Metrics field semantics — the one non-obvious thing

`move_task.py`'s metrics flags describe the phase being **left**, not the
one being entered — you report what a team spent on `in_progress` when you
call `--to-phase review` (the move that closes `in_progress` out), not on
the call that opened it. `run_demo.sh` is deliberately commented at the
point this matters, since it's easy to get backwards once.
