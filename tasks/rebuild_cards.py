#!/usr/bin/env python3
"""Project tasks/events.jsonl into one markdown+YAML-frontmatter card per
task, under tasks/cards/<task_id>.md.

This is L1 from tasks/README.md's "Orchestration architecture" decision
table: "one markdown+YAML-frontmatter card per task (format adapted from
Backlog.md/antopolskiy/kanban-md)". Generated view, never hand-edited —
same D9/D10 rule as board.md/kanban.md/metrics.md. events.jsonl is still
the only source of truth; a card is a per-task lens on it, nothing more.
Deliberately NOT a second place to record state: if you want to change a
task, use append_event.py/move_task.py and re-run this script (or let
move_task.py do it for you, same as it already does for kanban.md).

Each card carries the same fields board.md's flat table has (title,
project, energy, estimate, deadline, blocked_by, origin, created,
touched) plus `phase` (from the 6/8-phase lifecycle, tasks/lifecycle.py)
in YAML frontmatter, and a human-readable body: the phase history and the
latest --handoff note, if any (tasks/CHEATSHEET.md's "leave a handoff
note" feature). `blocked_by` stays free-text prose here too — it becomes
a real list of ids only once dotfiles-tsk-writepath-unification's schema
extends to that (see dotfiles-tsk-graph-dependency-edges), and this file
reads whatever's in the payload either way.
"""
import json
import sys
from pathlib import Path

TASKS_DIR = Path(__file__).parent
EVENTS_FILE = TASKS_DIR / "events.jsonl"
CARDS_DIR = TASKS_DIR / "cards"

sys.path.insert(0, str(TASKS_DIR))
from lifecycle import CREATED_TYPES, PHASE_CHANGED_TYPES, project as project_phases  # noqa: E402
from rebuild_view import payload_get  # noqa: E402

BOARD_FIELDS = ("energy", "estimate", "deadline", "blocked_by", "origin")


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
    """dict[task_id] -> card data: frontmatter fields + history + handoff."""
    phases = project_phases(events)  # title/phase/created, from lifecycle.py
    cards = {}
    for ev in events:
        task_id = ev.get("task_id")
        if not task_id or task_id not in phases:
            continue
        payload = ev.get("payload") or {}
        card = cards.setdefault(
            task_id,
            {
                "title": phases[task_id]["title"],
                "project": "",
                "created": phases[task_id]["created"],
                "touched": ev["ts"],
                "history": [],
                "handoff": None,
                "handoff_phase": None,
                **{f: "" for f in BOARD_FIELDS},
            },
        )
        card["touched"] = ev["ts"]

        if ev["type"] in CREATED_TYPES:
            card["project"] = payload_get(payload, "project", card["project"])
            for field in BOARD_FIELDS:
                card[field] = payload_get(payload, field, card[field])
        elif ev["type"] in PHASE_CHANGED_TYPES:
            actor = ev.get("actor") or {}
            entry = {
                "ts": ev["ts"],
                "from_phase": payload.get("from_phase"),
                "to_phase": payload.get("phase"),
                "actor_kind": actor.get("kind"),
                "actor_id": actor.get("id"),
                "reason": payload.get("reason"),
            }
            card["history"].append(entry)
            blocked_by = payload_get(payload, "blocked_by", None)
            if blocked_by is not None:
                card["blocked_by"] = blocked_by or ""
            if payload.get("handoff"):
                card["handoff"] = payload["handoff"]
                card["handoff_phase"] = payload.get("phase")

    for task_id, card in cards.items():
        card["phase"] = phases[task_id]["phase"]
    return cards


def yaml_escape(value):
    text = str(value)
    if not text:
        return '""'
    needs_quoting = any(ch in text for ch in ':#"\'{}[],&*!|>%@`') or text != text.strip()
    if needs_quoting:
        return '"' + text.replace('"', '\\"') + '"'
    return text


def render_card(task_id, card):
    frontmatter_fields = [
        ("task_id", task_id),
        ("title", card["title"]),
        ("project", card["project"]),
        ("phase", card["phase"]),
        ("created", card["created"]),
        ("touched", card["touched"]),
    ] + [(f, card[f]) for f in BOARD_FIELDS]

    lines = ["---"]
    for key, value in frontmatter_fields:
        lines.append(f"{key}: {yaml_escape(value)}")
    lines.append("---")
    lines.append("")
    lines.append(f"# {task_id}")
    lines.append("")
    lines.append(card["title"])
    lines.append("")
    lines.append("## History")
    if card["history"]:
        for entry in card["history"]:
            who = f"{entry['actor_id']}/{entry['actor_kind']}"
            reason = f" — {entry['reason']}" if entry["reason"] else ""
            lines.append(f"- {entry['ts']}: {entry['from_phase']} -> {entry['to_phase']} (actor: {who}){reason}")
    else:
        lines.append("- (no phase_changed events yet — still in its original created phase)")
    if card["handoff"]:
        lines.append("")
        lines.append("## Latest handoff")
        lines.append(f"_@ {card['handoff_phase']}_")
        lines.append("")
        lines.append(card["handoff"])
    lines.append("")
    return "\n".join(lines)


def main():
    events = load_events()
    cards = project(events)
    CARDS_DIR.mkdir(exist_ok=True)
    for task_id, card in cards.items():
        (CARDS_DIR / f"{task_id}.md").write_text(render_card(task_id, card), encoding="utf-8")
    print(f"wrote {len(cards)} card(s) to {CARDS_DIR} (from {len(events)} events)")


if __name__ == "__main__":
    main()
