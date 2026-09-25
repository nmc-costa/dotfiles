#!/usr/bin/env python3
"""Generator: one markdown+YAML-frontmatter card per task into generated/cards or tasks/cards by default."""
import json
import sys
import os
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.parent  # generators/.. so imports still work
sys.path.insert(0, str(SCRIPT_DIR))
from lifecycle import CREATED_TYPES, PHASE_CHANGED_TYPES, project as project_phases, tasks_root  # noqa: E402
from rebuild_view import payload_get  # noqa: E402

TASKS_DIR = tasks_root()
EVENTS_FILE = TASKS_DIR / "events.jsonl"
# output dir: TASKS_OUTPUT_DIR env var or TASKS_DIR
OUT_DIR = Path(os.environ.get("TASKS_OUTPUT_DIR", str(TASKS_DIR)))
CARDS_DIR = OUT_DIR / "cards"

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
    # Fixed and path-free on purpose: live worktree state is per-machine and
    # lives in the gitignored tasks/cards/worktrees/ view (tasks/worktree.py),
    # so this tracked file never churns when a worktree is created/removed.
    lines.append("")
    lines.append(f"Worktrees (this machine): [worktrees/{task_id}.md](worktrees/{task_id}.md) — "
                 f"`python3 ~/dotfiles/tasks/worktree.py list --task-id {task_id}`")
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
    CARDS_DIR.mkdir(parents=True, exist_ok=True)
    for task_id, card in cards.items():
        (CARDS_DIR / f"{task_id}.md").write_text(render_card(task_id, card), encoding="utf-8")
    print(f"wrote {len(cards)} card(s) to {CARDS_DIR} (from {len(events)} events)")


if __name__ == "__main__":
    main()
