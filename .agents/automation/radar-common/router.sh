#!/bin/bash
# radar-common/router.sh — single entry point across every radar in the
# researcher-radar family. Auto-discovers radars by directory shape (any
# .agents/skills/<name>/ that has both scripts/run.sh and security.md —
# excludes researcher-radar itself, which has neither), so a future radar
# added per researcher-radar/SKILL.md's "Adding a new radar" section shows
# up here with zero changes to this file.
#
# Usage:
#   router.sh list                    # every discovered radar + timer state
#   router.sh status [name]           # one radar's (or every radar's) state
#   router.sh run <name>              # invoke that radar's run.sh directly
#   router.sh top [name] [N]          # top N (default 50) from history.db,
#                                      #   across all radars if name omitted
#
# This is a convenience layer only — it never bypasses a radar's own
# security model (run.sh is invoked exactly as systemd would invoke it, and
# `top`/`status` are read-only queries against each radar's own state dir).

set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd -- "$SCRIPT_DIR/../../.." && pwd)"
SKILLS_DIR="$REPO_DIR/.agents/skills"

# shellcheck source=./lib.sh
source "$SCRIPT_DIR/lib.sh"

# discover_radars — prints one radar name per line, sorted, auto-detected by
# directory shape rather than a hardcoded list.
discover_radars() {
  local dir name
  for dir in "$SKILLS_DIR"/*/; do
    name="$(basename -- "$dir")"
    [[ -f "$dir/scripts/run.sh" && -f "$dir/security.md" ]] || continue
    printf '%s\n' "$name"
  done | sort
}

timer_state() {
  local name="$1"
  if ! command -v systemctl >/dev/null 2>&1; then
    echo "systemctl-unavailable"
    return
  fi
  if systemctl --user is-enabled "$name.timer" >/dev/null 2>&1; then
    if systemctl --user is-active "$name.timer" >/dev/null 2>&1; then
      echo "enabled+active"
    else
      echo "enabled, inactive"
    fi
  else
    echo "not installed/enabled"
  fi
}

cmd_list() {
  local name
  printf '%-16s %-20s\n' "RADAR" "TIMER"
  while IFS= read -r name; do
    printf '%-16s %-20s\n' "$name" "$(timer_state "$name")"
  done < <(discover_radars)
}

cmd_status() {
  local filter="${1:-}"
  local name
  while IFS= read -r name; do
    [[ -z "$filter" || "$name" == "$filter" ]] || continue
    local state_dir="$HOME/.local/state/$name"
    echo "=== $name ==="
    echo "timer: $(timer_state "$name")"
    if [[ -f "$state_dir/status.json" ]]; then
      echo "sources:"
      jq -r 'to_entries[] | "  \(.key): \(.value.status) (last: \(.value.last_checked // "?"))"' \
        "$state_dir/status.json" 2>/dev/null || echo "  (status.json unreadable)"
    else
      echo "sources: (no status.json yet -- collect.sh hasn't run)"
    fi
    local last_branch
    last_branch="$(git -C "$REPO_DIR" for-each-ref --sort=-creatordate --format='%(refname:short)' "refs/heads/radar/$name/" 2>/dev/null | head -1)"
    echo "last branch: ${last_branch:-none yet}"
    if [[ -f "$state_dir/history.db" ]]; then
      local count
      count="$(sqlite3 "$state_dir/history.db" "SELECT count(*) FROM candidates WHERE radar='$name';" 2>/dev/null || echo "?")"
      echo "history.db: $count scored candidates on record"
    else
      echo "history.db: not created yet"
    fi
    echo
  done < <(discover_radars)
}

cmd_run() {
  local name="${1:?usage: router.sh run <radar-name>}"
  local run_sh="$SKILLS_DIR/$name/scripts/run.sh"
  [[ -f "$run_sh" ]] || { echo "router.sh: no such radar '$name' (no $run_sh)" >&2; exit 1; }
  exec "$run_sh"
}

cmd_top() {
  local arg1="${1:-}" arg2="${2:-}"
  local filter="" limit=50
  if [[ "$arg1" =~ ^[0-9]+$ ]]; then
    limit="$arg1"
  else
    filter="$arg1"
    [[ -n "$arg2" ]] && limit="$arg2"
  fi

  local name found_any=0
  while IFS= read -r name; do
    [[ -z "$filter" || "$name" == "$filter" ]] || continue
    local db="$HOME/.local/state/$name/history.db"
    [[ -f "$db" ]] || continue
    found_any=1
    echo "=== $name (top $limit by score) ==="
    sqlite3 -header -column "$db" \
      "SELECT date, title, score, picked_top3, url FROM candidates ORDER BY score DESC LIMIT $limit;"
    echo
  done < <(discover_radars)

  if [[ "$found_any" -eq 0 ]]; then
    echo "router.sh: no history.db found yet for ${filter:-any radar} -- run.sh needs to have completed at least one full agent-step cycle first" >&2
  fi
}

main() {
  local sub="${1:-}"
  shift || true
  case "$sub" in
    list) cmd_list ;;
    status) cmd_status "$@" ;;
    run) cmd_run "$@" ;;
    top) cmd_top "$@" ;;
    *)
      cat <<USAGE
router.sh — single entry point across the researcher-radar family.

  router.sh list                  list every discovered radar + timer state
  router.sh status [name]         one radar's (or every radar's) state
  router.sh run <name>            invoke that radar's run.sh directly
  router.sh top [name] [N]        top N (default 50) scored candidates,
                                   across all radars if name is omitted
USAGE
      exit 1
      ;;
  esac
}

main "$@"
