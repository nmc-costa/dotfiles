#!/usr/bin/env python3
"""Project tasks/events.jsonl into tasks/tarefas.md — a generated view, never hand-edited.

D9/D10 (Workspace Agil doc): the JSONL log is the source of truth; every
other representation (this table, a future SQLite index) is a disposable,
rebuildable projection. Re-run this script any time events.jsonl changes.
"""
import json
from pathlib import Path

TASKS_DIR = Path(__file__).parent
EVENTS_FILE = TASKS_DIR / "events.jsonl"
VIEW_FILE = TASKS_DIR / "tarefas.md"

COLUMNS = [
    "id", "título", "projeto", "estado", "energia",
    "estimativa", "prazo", "bloqueado_por", "origem", "criado", "tocado",
]


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
    """Last event wins per task_id (D10). Returns dict[task_id] -> row."""
    tasks = {}
    for ev in events:
        task_id = ev.get("task_id")
        if not task_id:
            continue  # events not tied to a task (e.g. session-level) don't appear in the table
        payload = ev.get("payload") or {}
        row = tasks.setdefault(task_id, {col: "" for col in COLUMNS})
        row["id"] = task_id

        if ev["type"] == "tarefa.criada":
            row["título"] = payload.get("titulo", row["título"])
            row["projeto"] = payload.get("projeto", row["projeto"])
            row["energia"] = payload.get("energia", row["energia"])
            row["estimativa"] = payload.get("estimativa", row["estimativa"])
            row["prazo"] = payload.get("prazo", row["prazo"])
            row["bloqueado_por"] = payload.get("bloqueado_por", row["bloqueado_por"])
            row["origem"] = payload.get("origem", row["origem"])
            row["estado"] = ev.get("estado", row["estado"])
            row["criado"] = ev["ts"]
        elif ev["type"] == "tarefa.estado_mudou":
            row["estado"] = payload.get("estado", row["estado"])
            if "bloqueado_por" in payload:
                row["bloqueado_por"] = payload["bloqueado_por"] or ""
        row["tocado"] = ev["ts"]

    return tasks


def render(tasks):
    lines = [
        "# tarefas.md",
        "",
        "**Gerado por `rebuild_view.py` a partir de `events.jsonl` — não editar à mão.**",
        "Para mudar uma tarefa, acrescenta um evento com `append_event.py` e corre este script outra vez.",
        "",
        "| " + " | ".join(COLUMNS) + " |",
        "|" + "|".join(["---"] * len(COLUMNS)) + "|",
    ]
    for task_id in sorted(tasks, key=lambda tid: tasks[tid]["criado"]):
        row = tasks[task_id]
        lines.append("| " + " | ".join(str(row[col]) for col in COLUMNS) + " |")
    lines.append("")
    return "\n".join(lines)


def main():
    events = load_events()
    tasks = project(events)
    VIEW_FILE.write_text(render(tasks), encoding="utf-8")
    print(f"wrote {VIEW_FILE} ({len(tasks)} tasks from {len(events)} events)")


if __name__ == "__main__":
    main()
