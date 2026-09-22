#!/usr/bin/env python3
"""Cross-provider startup briefing — tasks/plans/human-in-the-loop-
notifications.md §5. The thin, deterministic core behind the future
`/task-brief` skill (`dotfiles-tsk-task-brief-skill`) and its per-provider
triggers (Claude Code `SessionStart` hook, Antigravity's inherited hook,
the `cpx` wrapper for Copilot CLI — `dotfiles-tsk-hook-*`/`-cpx-copilot`,
all still backlog). Logic lives here, not in any hook/skill wrapper (D14:
"script before rule").

Usage:
    python3 tasks/brief.py
        Full briefing: sweep heartbeat check -> pending facts by priority
        -> a director prompt ONLY if nothing is pending. Never picks work
        itself (§5: "nunca escolhe trabalho sozinha").

    python3 tasks/brief.py --prompt-only --task-id dotfiles-my-task
        Just the ready-to-paste dispatch prompt for one task — no
        heartbeat/inbox output. This is the contract
        `dotfiles-tsk-dispatch-launcher` needs to launch a session on
        another provider with a task's brief pre-loaded (tasks/
        handoff.md's cross-provider dispatch verdict).

No separate `tasks/inbox.md` file: the pending list is computed directly
from `tasks/events.jsonl` (the same source `tasks/notify.py` reads), not
from a generated intermediate — fewer moving parts, nothing to keep in
sync with the log that's already the source of truth.
"""
import argparse
import json
import sys
import time
from pathlib import Path

TASKS_DIR = Path(__file__).parent
EVENTS_FILE = TASKS_DIR / "events.jsonl"
HEARTBEAT_FILE = TASKS_DIR / ".sweep-heartbeat"
HEARTBEAT_STALE_SECONDS = 15 * 60

sys.path.insert(0, str(TASKS_DIR))
from lifecycle import CREATED_TYPES, P0_FACT_TYPES, PHASE_CHANGED_TYPES, current_phase  # noqa: E402

RAISED_TYPE = "notification.raised"
ACKED_TYPE = "notification.acked"


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


def heartbeat_status():
    """(is_stale, age_seconds_or_None). age is None when sweep.py has
    never run on this machine (no heartbeat file yet) — still "stale"."""
    if not HEARTBEAT_FILE.exists():
        return True, None
    age = time.time() - HEARTBEAT_FILE.stat().st_mtime
    return age > HEARTBEAT_STALE_SECONDS, age


def pending_facts(events):
    """Un-acked notification.raised facts, one per dedup_key (the freshest
    occurrence wins — a fact can be raised more than once via the
    self-heal retry in tasks/sweep.py), P0 facts first."""
    acked_keys = {e["payload"].get("dedup_key") for e in events if e["type"] == ACKED_TYPE}
    latest_by_key = {}
    for e in events:
        if e["type"] != RAISED_TYPE:
            continue
        key = e["payload"].get("dedup_key")
        if key in acked_keys:
            continue
        latest_by_key[key] = e
    facts = list(latest_by_key.values())
    facts.sort(key=lambda e: e["payload"].get("fact_type") not in P0_FACT_TYPES)
    return facts


def print_full_briefing():
    events = load_events()
    stale, age = heartbeat_status()
    if stale:
        if age is None:
            print("⚠️  tasks/sweep.py has never run on this machine — no heartbeat yet. Facts below may be incomplete.")
        else:
            print(f"⚠️  tasks/.sweep-heartbeat is {int(age / 60)}min old (>15min) — the sweep looks dead. Facts below may be stale.")
        print()

    facts = pending_facts(events)
    if not facts:
        print("Nothing pending. What do you want to work on?")
        return

    print(f"{len(facts)} fact(s) need you:")
    for e in facts:
        tag = " [P0]" if e["payload"].get("fact_type") in P0_FACT_TYPES else ""
        print(f"- {e['task_id']}: {e['payload'].get('fact_type')}{tag} (dedup_key={e['payload'].get('dedup_key')})")


def recommend_harness(phase):
    """Recommends harness and model tier based on the phase and specialization matrix:
    See .agents/instructions/workspace-config/harness-matrix.instructions.md
    """
    if phase in ("backlog", "planning"):
        return "claude (Claude 3.7 Sonnet / Opus — Design & Arquitetura)"
    if phase == "in_progress":
        return "agy (Antigravity/Gemini 2.5 Pro — Implementação & Scaffolding) ou claude (Tier 1 Core/Concorrência)"
    if phase == "review":
        return "copilot (PR review / conflitos) ou claude (Crítica adversária / reviewHITs)"
    if phase == "validation":
        return "claude (CAS gating / verificação formal) + agy (análise massiva de logs/traces)"
    return "copilot (git hygiene / manutenção)"


def prompt_for_task(task_id):
    events = load_events()
    phase = current_phase(events, task_id)
    if phase is None:
        print(f"error: {task_id!r} has no task.created event yet", file=sys.stderr)
        sys.exit(1)

    title = task_id
    handoff = None
    for e in events:
        if e.get("task_id") != task_id:
            continue
        if e["type"] in CREATED_TYPES:
            title = e["payload"].get("title", title)
        elif e["type"] in PHASE_CHANGED_TYPES and e["payload"].get("handoff"):
            handoff = e["payload"]["handoff"]

    recommendation = recommend_harness(phase)
    lines = [
        f"Pega na tarefa {task_id} em tasks/kanban.md e lidera-a.",
        f"Título: {title}",
        f"Fase atual: {phase}.",
        f"Harness recomendado: {recommendation}.",
    ]
    if phase == "backlog":
        lines.append(
            "Move primeiro backlog -> planning -> in_progress "
            "(LEGAL_TRANSITIONS aplica-se, são dois comandos move_task.py)."
        )
    if handoff:
        lines.append(f"Handoff mais recente: {handoff}")
    lines.append("Lê tasks/README.md, tasks/CHEATSHEET.md e .agents/instructions/workspace-config/harness-matrix.instructions.md.")
    print("\n".join(lines))


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--prompt-only", action="store_true", help="print just a dispatch prompt for --task-id")
    parser.add_argument("--task-id")
    args = parser.parse_args()

    if args.prompt_only:
        if not args.task_id:
            parser.error("--prompt-only requires --task-id")
        prompt_for_task(args.task_id)
        return

    print_full_briefing()


if __name__ == "__main__":
    main()
