#!/usr/bin/env python3
"""Migration helper: create tasks/generated/ and run all generators into it.

Usage:
    python3 migrate_to_generated.py

This is safe and reversible: it only writes generated/ and does not change
events.jsonl or other data files. After running, review generated/ and
optionally replace top-level views with symlinks to generated/.
"""
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent
GENERATORS = [
    ROOT / "generators" / "rebuild_kanban.py",
    ROOT / "generators" / "rebuild_cards.py",
    ROOT / "generators" / "rebuild_graph.py",
]
OUT = ROOT / "generated"
OUT.mkdir(parents=True, exist_ok=True)
env = os.environ.copy()
env["TASKS_OUTPUT_DIR"] = str(OUT)

for g in GENERATORS:
    print(f"Running {g} -> {OUT}")
    subprocess.check_call(["python3", str(g)], env=env)

print("Migration complete. Generated views are in tasks/generated/")
print("If you want to make top-level views point to generated/, create symlinks manually:")
print("  ln -sfn generated/kanban.md kanban.md")
print("  ln -sfn generated/cards cards")
