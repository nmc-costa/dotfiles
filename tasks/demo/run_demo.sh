#!/usr/bin/env bash
# Self-contained demo: 2 tasks, each worked by 2 different teams across
# phases, with simulated metrics (tokens/cost/duration/cycles) recorded at
# every phase transition. Runs entirely inside this folder — the scripts
# here are copies, so tasks/demo/events.jsonl is its own file, never the
# real tasks/events.jsonl. Safe to re-run: it wipes its own state first.
#
# Usage: ./run_demo.sh   (from anywhere — it cd's into its own directory)
#
# What this proves: two teams working two tasks through the full 6-phase
# lifecycle (backlog -> planning -> in_progress -> review -> validation ->
# done), each phase-close recording who did it and what it cost, ending in
# tasks/demo/kanban.md (both tasks in Done) and tasks/demo/metrics.md (a
# real per-team, per-task cost breakdown built from nothing but move_task.py
# calls — no separate metrics store).
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"

echo "=== reset: wiping this demo's own state (never touches the real tasks/) ==="
: > events.jsonl
rm -f kanban.md metrics.md board.md
echo

move() {
  local task=$1 phase=$2 team=$3 tokens=$4 cost=$5 duration=$6 cycles=$7
  python3 move_task.py --task-id "$task" --to-phase "$phase" --actor-id demo \
    --team "$team" --tokens "$tokens" --cost-usd "$cost" \
    --duration-seconds "$duration" --cycles "$cycles"
}

echo "=== creating 2 tasks ==="
python3 append_event.py --type task.created --actor-kind human --actor-id demo \
  --task-id demo-report --payload '{"title":"Gerar relatorio semanal","project":"demo"}'
python3 append_event.py --type task.created --actor-kind human --actor-id demo \
  --task-id demo-cleanup --payload '{"title":"Limpar dependencias obsoletas","project":"demo"}'
echo

# Two teams, each doing a different slice of the lifecycle on BOTH tasks:
#   team-scout -> does the planning work
#   team-forge -> does in_progress, review, validation
# IMPORTANT: move_task.py attaches metrics to the phase being LEFT, not the
# one being entered — so "team-scout's planning cost" is reported on the
# move OUT of planning (planning -> in_progress), not the move into it.
# Metrics are simulated but distinct per task, so the aggregation in
# metrics.md is actually comparing something, not repeating one number.

echo "=== demo-report: enters planning (no metrics yet, nothing done in backlog) ==="
python3 move_task.py --task-id demo-report --to-phase planning --actor-id demo
echo "=== demo-report: team-scout's planning work closes out ==="
move demo-report in_progress team-scout 8200  0.14 420  1
echo "=== demo-report: team-forge builds, reviews, validates, ships it ==="
move demo-report review      team-forge 15600 0.09 1380 1
move demo-report validation  team-forge 4100  0.06 300  1
move demo-report done        team-forge 1800  0.03 150  1
echo

echo "=== demo-cleanup: enters planning ==="
python3 move_task.py --task-id demo-cleanup --to-phase planning --actor-id demo
echo "=== demo-cleanup: team-scout's planning work closes out ==="
move demo-cleanup in_progress team-scout 5100 0.09 260  1
echo "=== demo-cleanup: team-forge builds, hits one retry in review, ships it ==="
move demo-cleanup review      team-forge 9800 0.06 720  1
move demo-cleanup validation  team-forge 6200 0.08 480  2
move demo-cleanup done        team-forge 1500 0.02 120  1
echo

echo "=== output ==="
echo "kanban.md:"
cat kanban.md
echo
echo "metrics.md:"
cat metrics.md
echo
echo "=== done. Point tuiboard at $(pwd)/kanban.md to watch it, or just read the two .md files above. ==="
