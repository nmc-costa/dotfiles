#!/usr/bin/env python3
"""Single source of truth for the task lifecycle: phases, legal
transitions, and the vocabulary needed to read/enforce them.

This centralizes constants and a `project()` helper that used to live only
inside rebuild_kanban.py (and were partially re-derived in append_event.py
and move_task.py) — see tasks/plans/human-in-the-loop-notifications.md §0
("Write path unificado") for why: `append_event.py::append()` needs to know
a task's current phase to reject illegal transitions, and it can't import
rebuild_kanban.py for that without inverting the dependency (rebuild_kanban
is a *view* of the log, append() is the *writer* into it).

Not yet implemented here (deliberately deferred to the notification/sweep
layer in the plan doc, Wave 2 — their inputs don't exist yet): `FACT_TYPES`
(depends on event types only `sweep.py` will ever produce, e.g.
`agent.session_stalled`) and `dedup_key()`'s escalation-period argument
(depends on `tasks/policy.yaml`, not written yet). Adding them now would be
unused, speculative code with no real caller.
"""
import sys
from pathlib import Path

TASKS_DIR = Path(__file__).parent
sys.path.insert(0, str(TASKS_DIR))
from rebuild_view import payload_get  # noqa: E402 — reuse the EN/PT legacy-key fallback

# The full phase set, including the two side lanes (D12/CHEATSHEET.md:
# "plus deferred/blocked as side lanes" — not steps in the main sequence,
# reachable from most pipeline phases and reachable back out of).
PIPELINE_PHASES = ("backlog", "planning", "in_progress", "review", "validation", "done")
SIDE_LANE_PHASES = ("blocked", "deferred")
PHASES = PIPELINE_PHASES + SIDE_LANE_PHASES

# tasks/plans/human-in-the-loop-notifications.md §0, verbatim.
LEGAL_TRANSITIONS = {
    "backlog":     {"planning", "deferred"},
    "planning":    {"in_progress", "backlog", "deferred", "blocked"},
    "in_progress": {"review", "blocked", "deferred"},
    "review":      {"in_progress", "validation", "blocked"},
    "validation":  {"done", "in_progress", "blocked"},
    "blocked":     {"in_progress", "planning", "deferred"},
    "deferred":    {"backlog", "planning"},
    "done":        set(),
}

CREATED_TYPES = ("tarefa.criada", "task.created")
STATUS_CHANGED_TYPES = ("tarefa.estado_mudou", "task.status_changed")
PHASE_CHANGED_TYPES = ("task.phase_changed",)

# Correction from Fase 5 ronda 2 of the notification plan: the real log
# uses "humano"/"agente" (PT), not "human"/"agent" — every event written
# before 2026-09-16 uses the PT spelling, and it's append-only so those
# lines are never rewritten.
HUMAN_ACTOR_KINDS = ("humano", "human")
AGENT_ACTOR_KINDS = ("agente", "agent")

# Lossless one-time migration for tasks that predate task.phase_changed —
# the exact mapping decided in tasks/README.md's "Orchestration
# architecture" section. Moved here from rebuild_kanban.py so it isn't
# duplicated once append_event.py also needs to know a task's phase.
OLD_STATUS_TO_PHASE = {
    "new": "backlog",
    "novo": "backlog",
    "todo": "backlog",
    "in progress": "in_progress",
    "in review": "review",
    "done": "done",
    "feito": "done",
    "deferred": "deferred",
    "adiado": "deferred",
}


class IllegalTransitionError(Exception):
    """A task.phase_changed event's phase isn't reachable from the task's
    current phase per LEGAL_TRANSITIONS. Callers exit(2) — distinct from
    ValueError's exit(1) for a merely malformed event."""


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
            if phase in PHASES:
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


def current_phase(events, task_id):
    """The phase a task_id is in right now, or None if it has no
    task.created event yet (doesn't exist)."""
    tasks = project(events)
    if task_id not in tasks:
        return None
    return tasks[task_id]["phase"]
