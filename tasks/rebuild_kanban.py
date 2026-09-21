#!/usr/bin/env python3
"""Project tasks/events.jsonl into tasks/kanban.md — a tuiboard-format board.

Generated view, never hand-edited (same rule as board.md — D9/D10). Column
headings and task lines follow tuiboard's plain-markdown convention (every
`##` heading is a column, every `- [ ]`/`- [x]` line is a task) so tuiboard
can render it with zero configuration beyond pointing a board path at this
file. See tasks/README.md's "Orchestration architecture" section for the
6-phase lifecycle this implements and tasks/evaluations/tuiboard/ for the
spike that confirmed this file shape works.

A task's phase comes from the last `task.phase_changed` event for its
task_id. Tasks that predate this tool (they only have old-vocabulary
`task.status_changed`/`tarefa.estado_mudou` events, never a
`task.phase_changed`) get a one-time migrated phase via the lossless
mapping already decided in tasks/README.md's "Orchestration architecture"
section (`new`/`todo` -> backlog, `in progress` -> in_progress,
`in review` -> review, `done`/`feito` -> done) — the first
`task.phase_changed` event for a task_id permanently takes over from then
on. `blocked` and `deferred` aren't pipeline stages (they're documented as
parallel side lanes, not steps in the main sequence) so they get their own
columns, appended after Done. Move a task with move_task.py — never edit
this file directly, it's overwritten on every rebuild.

The phase model itself (`PHASES`/`LEGAL_TRANSITIONS`/the migration map)
lives in tasks/lifecycle.py, not here — this file only owns rendering.
"""
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))
from lifecycle import PIPELINE_PHASES, project, tasks_root  # noqa: E402

TASKS_DIR = tasks_root()
EVENTS_FILE = TASKS_DIR / "events.jsonl"
VIEW_FILE = TASKS_DIR / "kanban.md"

# Order matters — this is the column order tuiboard renders. "Done" is
# named exactly that on purpose: tuiboard hides a column named "Done" from
# the board view and uses it for done-stats instead. Blocked comes right
# after Done (closer to the active pipeline, needs attention) and Deferred
# last (parked, lowest urgency).
PHASE_HEADING = {
    "backlog": "Backlog",
    "planning": "Planning",
    "in_progress": "In Progress",
    "review": "Review",
    "validation": "Validation",
    "done": "Done",
    "blocked": "Blocked",
    "deferred": "Deferred",
}


def load_events():
    if not EVENTS_FILE.exists():
        return []
    events = []
    for line in EVENTS_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            events.append(json.loads(line))
    events.sort(key=lambda e: e["ts"])
    return events


def render(tasks):
    columns = list(PIPELINE_PHASES) + ["blocked", "deferred"]
    by_phase = {p: [] for p in columns}
    for task_id, row in tasks.items():
        by_phase[row["phase"]].append((task_id, row))

    lines = []
    for phase in columns:
        lines.append(f"## {PHASE_HEADING[phase]}")
        items = sorted(by_phase.get(phase, []), key=lambda kv: kv[1]["created"])
        for task_id, row in items:
            box = "x" if phase == "done" else " "
            lines.append(f"- [{box}] {task_id} {row['title']}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main():
    events = load_events()
    tasks = project(events)
    VIEW_FILE.write_text(render(tasks), encoding="utf-8")
    print(f"wrote {VIEW_FILE} ({len(tasks)} tasks from {len(events)} events)")


if __name__ == "__main__":
    main()
