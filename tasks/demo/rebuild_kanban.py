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
on. `deferred` isn't one of the 6 pipeline columns (it's documented as a
parallel lane, not a stage) so it gets its own 7th column, appended after
Done. Move a task with move_task.py — never edit this file directly, it's
overwritten on every rebuild.
"""
import json
import sys
from pathlib import Path

TASKS_DIR = Path(__file__).parent
EVENTS_FILE = TASKS_DIR / "events.jsonl"
VIEW_FILE = TASKS_DIR / "kanban.md"

sys.path.insert(0, str(TASKS_DIR))
from rebuild_view import payload_get  # noqa: E402 — reuse the EN/PT legacy-key fallback

# Order matters — this is the column order tuiboard renders, and the
# lifecycle order decided in tasks/README.md's "Orchestration architecture"
# section. "Done" is named exactly that on purpose: tuiboard hides a column
# named "Done" from the board view and uses it for done-stats instead.
PHASES = ["backlog", "planning", "in_progress", "review", "validation", "done"]
PHASE_HEADING = {
    "backlog": "Backlog",
    "planning": "Planning",
    "in_progress": "In Progress",
    "review": "Review",
    "validation": "Validation",
    "done": "Done",
}
DEFERRED = "deferred"  # not a pipeline stage — a parallel lane, rendered as a 7th column

CREATED_TYPES = ("tarefa.criada", "task.created")
STATUS_CHANGED_TYPES = ("tarefa.estado_mudou", "task.status_changed")
PHASE_CHANGED_TYPES = ("task.phase_changed",)

# Lossless one-time migration for tasks that predate this tool — the exact
# mapping decided in tasks/README.md's "Orchestration architecture" section.
OLD_STATUS_TO_PHASE = {
    "new": "backlog",
    "novo": "backlog",
    "todo": "backlog",
    "in progress": "in_progress",
    "in review": "review",
    "done": "done",
    "feito": "done",
    "deferred": DEFERRED,
    "adiado": DEFERRED,
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


def project(events):
    """Last event wins per task_id. Returns dict[task_id] -> {title, phase, created}.

    `phase` is None until either a real task.phase_changed event or an old
    status_changed event has been seen — resolved to "backlog" at the end
    for anything that never had either.
    """
    tasks = {}
    for ev in events:
        task_id = ev.get("task_id")
        if not task_id:
            continue
        payload = ev.get("payload") or {}
        row = tasks.setdefault(task_id, {"title": task_id, "phase": None, "has_phase_event": False, "created": ev["ts"]})

        if ev["type"] in CREATED_TYPES:
            row["title"] = payload_get(payload, "title", row["title"])
            row["created"] = ev["ts"]
        elif ev["type"] in PHASE_CHANGED_TYPES:
            phase = payload.get("phase")
            if phase in PHASES or phase == DEFERRED:
                row["phase"] = phase
                row["has_phase_event"] = True
        elif ev["type"] in STATUS_CHANGED_TYPES and not row["has_phase_event"]:
            # One-time migration only — a real task.phase_changed event
            # (even a no-op re-affirming the same phase) permanently takes
            # over for that task_id from then on.
            old_status = payload_get(payload, "status", "")
            row["phase"] = OLD_STATUS_TO_PHASE.get(old_status, row["phase"])

    for row in tasks.values():
        if row["phase"] is None:
            row["phase"] = "backlog"

    return tasks


def render(tasks):
    columns = PHASES + [DEFERRED]
    by_phase = {p: [] for p in columns}
    for task_id, row in tasks.items():
        by_phase[row["phase"]].append((task_id, row))

    heading = dict(PHASE_HEADING, **{DEFERRED: "Deferred"})
    lines = []
    for phase in columns:
        lines.append(f"## {heading[phase]}")
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
