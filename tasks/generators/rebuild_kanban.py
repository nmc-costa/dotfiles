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

SCRIPT_DIR = Path(__file__).parent.parent
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


def render(tasks, events, done_window_days=30, view_file=VIEW_FILE):
    """Render kanban. Show recent 'done' tasks only (within done_window_days).

    Older done items are archived into tasks/archive.md (generated view).
    """
    import datetime

    columns = list(PIPELINE_PHASES) + ["blocked", "deferred"]
    by_phase = {p: [] for p in columns}
    for task_id, row in tasks.items():
        by_phase[row["phase"]].append((task_id, row))

    # Compute done timestamp per task (when it entered 'done')
    done_ts = {}
    for ev in reversed(events):
        tid = ev.get("task_id")
        if not tid:
            continue
        if tid in done_ts:
            continue
        # phase_changed to 'done'
        if ev.get("type") in ("task.phase_changed",):
            payload = ev.get("payload") or {}
            if payload.get("phase") == "done":
                done_ts[tid] = ev["ts"]
                continue
        # legacy status_changed to 'done'
        if ev.get("type") in ("tarefa.estado_mudou", "task.status_changed"):
            payload = ev.get("payload") or {}
            status = payload.get("status") or payload.get("estado")
            if status and status.lower() in ("done", "feito"):
                done_ts[tid] = ev["ts"]
                continue

    # cutoff
    now = datetime.datetime.now(datetime.timezone.utc)
    cutoff = now - datetime.timedelta(days=done_window_days)

    # Partition done tasks into recent and archived
    recent_done = set()
    archived = {}
    for task_id, row in by_phase.get("done", []):
        ts_str = done_ts.get(task_id) or row.get("created")
        try:
            ts = datetime.datetime.fromisoformat(ts_str)
        except Exception:
            ts = now
        if ts >= cutoff:
            recent_done.add(task_id)
        else:
            # group by YYYY-MM
            key = ts.strftime("%Y-%m")
            archived.setdefault(key, []).append((ts, task_id, row))

    # Render columns, omitting archived done items from the Done column
    lines = []
    for phase in columns:
        lines.append(f"## {PHASE_HEADING[phase]}")
        items = sorted(by_phase.get(phase, []), key=lambda kv: kv[1]["created"])
        for task_id, row in items:
            if phase == "done" and task_id not in recent_done:
                continue
            box = "x" if phase == "done" else " "
            lines.append(f"- [{box}] {task_id} {row['title']}")
        lines.append("")

    # Build archive text (monthly sections) and write it
    archive_lines = ["# Archived Done Tasks", ""]
    if archived:
        for month in sorted(archived.keys(), reverse=True):
            archive_lines.append(f"## {month}")
            for ts, task_id, row in sorted(archived[month], key=lambda t: t[0], reverse=True):
                date = ts.date().isoformat()
                archive_lines.append(f"- [{date}] {task_id} {row['title']}")
            archive_lines.append("")
    else:
        archive_lines.append("_No archived items._")
        archive_lines.append("")

    # write archive file next to view_file
    archive_file = Path(view_file).parent / "archive.md"
    archive_file.parent.mkdir(parents=True, exist_ok=True)
    archive_file.write_text("\n".join(archive_lines).rstrip() + "\n", encoding="utf-8")

    return "\n".join(lines).rstrip() + "\n"


def main():
    import os

    events = load_events()
    tasks = project(events)
    # Allow override of done window via env var (days)
    try:
        done_window_days = int(os.environ.get("TASKS_DONE_WINDOW_DAYS", "30"))
    except Exception:
        done_window_days = 30
    import os

    out_dir = Path(os.environ.get("TASKS_OUTPUT_DIR", str(TASKS_DIR)))
    view_file = out_dir / "kanban.md"
    out_text = render(tasks, events, done_window_days=done_window_days, view_file=view_file)
    # ensure parent exists
    view_file.parent.mkdir(parents=True, exist_ok=True)
    view_file.write_text(out_text, encoding="utf-8")
    print(f"wrote {view_file} ({len(tasks)} tasks from {len(events)} events)")


if __name__ == "__main__":
    main()
