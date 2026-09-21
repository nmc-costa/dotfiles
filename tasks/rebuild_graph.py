#!/usr/bin/env python3
"""Project tasks/events.jsonl into tasks/roadmap.md — a Mermaid visual roadmap.

Generated view, never hand-edited (same rule as kanban.md/metrics.md —
D9/D10). Two diagrams, built from the same event log:

1. A `flowchart LR` with one `subgraph` per project (`payload.project`,
   falling back to the legacy PT `payload.projeto` via
   rebuild_view.payload_get — same fallback rebuild_kanban.py/lifecycle.py
   already rely on) containing that project's tasks as nodes, classed by
   phase (tasks/lifecycle.py's PHASES, the single source of truth) via
   `classDef`/`:::`. Phase comes from the same `lifecycle.project()`
   helper rebuild_kanban.py uses, so this always agrees with kanban.md.
2. A `timeline` diagram aggregating tasks that reached `done`, one entry
   per `task.phase_changed` event with `payload.phase == "done"` (grouped
   by that event's `ts` date) — independent of the flowchart above.

See tasks/HANDOFF.md's "Verdict 1" for why this is scoped this way: a
`mindmap` diagram was rejected (tree-only, no cross-links — wrong fit for
a dependency graph); `flowchart LR` + `classDef` per phase + a separate
`timeline` was adopted instead.

Deliberately out of scope here (Wave 2, dotfiles-tsk-graph-dependency-edges,
blocked on `blocked_by` becoming a real list instead of free prose): no
`blocked_by` dependency edges are drawn between nodes.

tasks/roadmap.mmd holds only the flowchart (the "roadmap" proper) as raw
Mermaid source, no markdown fencing around it — the repo's `.mmd`
convention (.agents/instructions/workspace-config/mermaid.instructions.md,
.claude/rules/mermaid.md) is one diagram per `.mmd` file, and a single
Mermaid code fence can't mix two diagram types anyway. The timeline lives
only inside roadmap.md's second ```mermaid block.
"""
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))
from lifecycle import CREATED_TYPES, PHASE_CHANGED_TYPES, PHASES, project, tasks_root  # noqa: E402
from rebuild_view import payload_get  # noqa: E402

TASKS_DIR = tasks_root()
EVENTS_FILE = TASKS_DIR / "events.jsonl"
MD_FILE = TASKS_DIR / "roadmap.md"
MMD_FILE = TASKS_DIR / "roadmap.mmd"

# fill / stroke per phase — distinct colors so the flowchart reads at a
# glance; order follows lifecycle.PHASES (pipeline phases, then the two
# side lanes).
PHASE_COLOR = {
    "backlog":     ("#eceff1", "#607d8b"),
    "planning":    ("#e3f2fd", "#1e88e5"),
    "in_progress": ("#fff8e1", "#f9a825"),
    "review":      ("#ede7f6", "#7b1fa2"),
    "validation":  ("#e8f5e9", "#2e7d32"),
    "done":        ("#c8e6c9", "#1b5e20"),
    "blocked":     ("#ffebee", "#c62828"),
    "deferred":    ("#f5f5f5", "#9e9e9e"),
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


def collect_projects(events):
    """task_id -> project name, from the last task.created (or legacy
    tarefa.criada) event seen for that task_id."""
    task_project = {}
    for ev in events:
        if ev.get("type") not in CREATED_TYPES:
            continue
        task_id = ev.get("task_id")
        if not task_id:
            continue
        payload = ev.get("payload") or {}
        task_project[task_id] = payload_get(payload, "project", "unknown")
    return task_project


def project_node_id(name):
    """A safe Mermaid subgraph id for an arbitrary project name (e.g.
    'Work/notes' has a slash, which isn't a legal bare id character)."""
    slug = re.sub(r"[^A-Za-z0-9_]", "_", name).strip("_")
    return f"proj_{slug or 'unknown'}"


def escape_label(text):
    """Mermaid quoted-label escaping: only double quotes and newlines are
    unsafe inside a `["..."]` label."""
    return str(text).replace('"', "&quot;").replace("\n", " ").replace("\r", "")


def build_flowchart(tasks, task_project):
    lines = ["flowchart LR"]
    for phase in PHASES:
        fill, stroke = PHASE_COLOR[phase]
        lines.append(f"    classDef {phase} fill:{fill},stroke:{stroke},stroke-width:2px,color:#000;")
    lines.append("")

    projects = sorted({task_project.get(tid, "unknown") for tid in tasks})
    for proj_name in projects:
        pid = project_node_id(proj_name)
        lines.append(f'    subgraph {pid}["{escape_label(proj_name)}"]')
        proj_tasks = sorted(
            (
                (tid, row)
                for tid, row in tasks.items()
                if task_project.get(tid, "unknown") == proj_name
            ),
            key=lambda kv: kv[1]["created"],
        )
        for tid, row in proj_tasks:
            label = f"{escape_label(tid)}<br/>{escape_label(row['title'])}"
            lines.append(f'        {tid}["{label}"]:::{row["phase"]}')
        lines.append("    end")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def build_timeline(events):
    by_date = defaultdict(list)
    for ev in events:
        if ev.get("type") not in PHASE_CHANGED_TYPES:
            continue
        payload = ev.get("payload") or {}
        if payload.get("phase") != "done":
            continue
        ts = ev.get("ts") or ""
        date = ts[:10] if ts else "unknown-date"
        by_date[date].append(ev.get("task_id", ""))

    lines = ["timeline", "    title Tasks reaching done, over time"]
    if not by_date:
        lines.append("    %% no task has reached done yet")
    for date in sorted(by_date):
        entries = " : ".join(escape_label(tid) for tid in by_date[date])
        lines.append(f"    {date} : {entries}")
    return "\n".join(lines) + "\n"


def render_md(flowchart_src, timeline_src):
    lines = [
        "# roadmap.md",
        "",
        "**Generated by `rebuild_graph.py` from `events.jsonl` — do not hand-edit.**",
        "One subgraph per project, nodes classed by `tasks/lifecycle.py` phase.",
        "No `blocked_by` dependency edges yet — `blocked_by` is still free prose in",
        "the payload, not a list of task ids (see `dotfiles-tsk-graph-dependency-edges`).",
        "`tasks/roadmap.mmd` carries the flowchart below as raw Mermaid source.",
        "",
        "## Roadmap",
        "",
        "```mermaid",
        flowchart_src.rstrip("\n"),
        "```",
        "",
        "## Done, over time",
        "",
        "```mermaid",
        timeline_src.rstrip("\n"),
        "```",
        "",
    ]
    return "\n".join(lines)


def main():
    events = load_events()
    tasks = project(events)
    task_project = collect_projects(events)

    flowchart_src = build_flowchart(tasks, task_project)
    timeline_src = build_timeline(events)

    MD_FILE.write_text(render_md(flowchart_src, timeline_src), encoding="utf-8")
    MMD_FILE.write_text(flowchart_src, encoding="utf-8")
    print(f"wrote {MD_FILE} and {MMD_FILE} ({len(tasks)} tasks, "
          f"{len({task_project.get(t, 'unknown') for t in tasks})} projects, from {len(events)} events)")


if __name__ == "__main__":
    main()
