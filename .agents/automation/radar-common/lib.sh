#!/bin/bash
# radar-common/lib.sh — shared, security-critical plumbing for the
# researcher-radar family (omarchy-radar, harness-radar). Sourced by each
# radar's scripts/collect.sh and scripts/run.sh — never executed directly.
#
# NOTE (2026-09-25): this file was found missing when the harness-radar
# scripts+systemd build pass started, even though the plan's Phase 0 was
# supposed to have already written it. It was authored here, from the same
# approved plan section that would have driven Phase 0
# (~/.claude/plans/inherited-dancing-lampson.md — "researcher-radar
# (meta-skill) and radar-common (shared library)", "The agent step", and
# "Delivery channels" item 0), so the harness-radar scripts below have real
# functions to call instead of guessed ones. If a genuine Phase-0 output
# lands separately, reconcile function names/signatures against this file
# rather than assuming a silent conflict.
#
# House style: bash, [[ ]] / (( )), 2-space indent — matching
# .agents/providers/proxy/ensure-proxy.sh and tasks/*.sh in this repo.
# JSON handling uses `jq` (already a hard dependency of this repo, see
# tasks/validate_herdr_contract.sh) rather than embedding Python here.
#
# Every function below is prefixed `radar_` to avoid colliding with
# anything in a sourcing script.

# ---------------------------------------------------------------------------
# State helpers: atomic tmp-then-mv writes, seen.json.pending -> seen.json
# ---------------------------------------------------------------------------

# radar_atomic_write_stdin <target_file>
#   Reads content from stdin, writes it to <target_file> via a tmp file in
#   the same directory followed by `mv -f`, so a crash mid-write never
#   leaves a partial/corrupt target — the reader only ever sees the old
#   file or the fully-written new one, never a half-written one.
radar_atomic_write_stdin() {
  local target="$1"
  local dir tmp
  dir="$(dirname -- "$target")"
  mkdir -p "$dir"
  tmp="$(mktemp "$dir/.radar-tmp.XXXXXX")"
  cat > "$tmp"
  mv -f -- "$tmp" "$target"
}

# radar_atomic_install <tmp_file> <target_file>
#   Same guarantee as radar_atomic_write_stdin, for a caller that already
#   built the new content in its own tmp file (e.g. `jq ... > "$tmp"`).
radar_atomic_install() {
  local tmp="$1" target="$2"
  local dir
  dir="$(dirname -- "$target")"
  mkdir -p "$dir"
  mv -f -- "$tmp" "$target"
}

# radar_promote_seen <state_dir>
#   Promotes <state_dir>/seen.json.pending to <state_dir>/seen.json, but
#   ONLY when called — i.e. only after run.sh's commit step has actually
#   succeeded. A crashed/failed run leaves seen.json.pending in place and
#   seen.json untouched, so the next run retries the same items instead of
#   losing them. No-op (not an error) if there is no pending file.
radar_promote_seen() {
  local state_dir="$1"
  local pending="$state_dir/seen.json.pending"
  local final="$state_dir/seen.json"
  [[ -f "$pending" ]] || return 0
  mv -f -- "$pending" "$final"
}

# ---------------------------------------------------------------------------
# flock guard
# ---------------------------------------------------------------------------

# radar_acquire_lock <lock_file>
#   Blocking flock on <lock_file>, held for the lifetime of the *current*
#   shell (this must be called from the top-level script via `source`, not
#   from inside a subshell/pipeline, or the fd disappears with the
#   subshell). A manual run.sh invocation that overlaps the systemd timer
#   serializes behind this instead of racing on seen.json/the inbox file.
radar_acquire_lock() {
  local lock_file="$1"
  mkdir -p "$(dirname -- "$lock_file")"
  # `{fd}>` lets bash (>=4.1) pick a free descriptor and export it as
  # RADAR_LOCK_FD, so nested calls / other locks in the same script don't
  # collide with a hardcoded fd number.
  exec {RADAR_LOCK_FD}>"$lock_file"
  flock "$RADAR_LOCK_FD"
}

# ---------------------------------------------------------------------------
# git-worktree helpers — the agent step NEVER runs git itself; every git
# operation lives here, in deterministic bash, bracketing the single
# `claude -p` call. The caller's actual checkout (main) is never switched,
# read-locked, or touched by any of these.
# ---------------------------------------------------------------------------

# radar_branch_exists <repo_dir> <branch>
#   0 (true) if <branch> already exists in <repo_dir> — run.sh uses this to
#   skip a day that already ran, rather than clobbering it.
radar_branch_exists() {
  local repo_dir="$1" branch="$2"
  git -C "$repo_dir" show-ref --verify --quiet "refs/heads/$branch"
}

# radar_worktree_add <repo_dir> <worktree_dir> <branch>
#   `git worktree add <worktree_dir> -b <branch>` against <repo_dir>.
#   Never switches/touches <repo_dir>'s own currently-checked-out branch.
radar_worktree_add() {
  local repo_dir="$1" worktree_dir="$2" branch="$3"
  mkdir -p "$(dirname -- "$worktree_dir")"
  git -C "$repo_dir" worktree add "$worktree_dir" -b "$branch" >/dev/null
}

# radar_worktree_commit <worktree_dir> <message>
#   Stages everything currently in the worktree and commits it there —
#   never `-a`, never `--amend`, never touches anything outside the
#   worktree. Returns non-zero (without erroring the caller's `set -e`
#   unless checked) if there is nothing to commit.
radar_worktree_commit() {
  local worktree_dir="$1" message="$2"
  git -C "$worktree_dir" add -A -- .
  if git -C "$worktree_dir" diff --cached --quiet; then
    return 1
  fi
  git -C "$worktree_dir" commit -m "$message" >/dev/null
}

# radar_worktree_remove <repo_dir> <worktree_dir>
#   Removes the disposable worktree directory; the branch and its commit
#   (if any) persist in <repo_dir> for the human to review/merge.
radar_worktree_remove() {
  local repo_dir="$1" worktree_dir="$2"
  git -C "$repo_dir" worktree remove --force "$worktree_dir" 2>/dev/null \
    || rm -rf -- "$worktree_dir"
}

# ---------------------------------------------------------------------------
# claude -p invocation wrapper — the ONLY place the agent step's flags are
# defined, so every radar's run.sh gets the identical restricted shape.
# ---------------------------------------------------------------------------

# radar_run_claude_agent <worktree_dir> <allowed_tools> <disallowed_tools> <prompt_file>
#   Runs `claude -p` with cwd = <worktree_dir> (so a bare `briefs/*` pattern
#   is unambiguous), fixed to --permission-mode dontAsk and
#   --output-format json, and the caller-supplied allow/deny tool lists —
#   never Bash, never any git subcommand, no --dangerously-skip-permissions.
#   The prompt is piped via stdin from <prompt_file>. Prints claude's raw
#   JSON stdout to this function's own stdout; returns claude's exit code.
radar_run_claude_agent() {
  local worktree_dir="$1" allowed_tools="$2" disallowed_tools="$3" prompt_file="$4"
  # RADAR_CLAUDE_BIN lets a machine route the agent step through an opt-in
  # provider launcher (e.g. ~/.local/bin/claude-dtx-glm53-flash, the claude
  # CLI pointed at the local dtx LiteLLM proxy) without touching this
  # function's flag contract. Defaults to plain `claude`.
  local claude_bin="${RADAR_CLAUDE_BIN:-claude}"
  (
    cd "$worktree_dir" || exit 1
    "$claude_bin" -p \
      --output-format json \
      --permission-mode dontAsk \
      --allowedTools "$allowed_tools" \
      --disallowedTools "$disallowed_tools" \
      < "$prompt_file"
  )
}

# radar_run_opencode_agent <worktree_dir> <prompt_file>
#   Runs `opencode run` with cwd = <worktree_dir> — the opencode twin of
#   radar_run_claude_agent, enforcing the identical security contract via a
#   throwaway OPENCODE_CONFIG (loaded as the final local-scope merge, never
#   written into the worktree or committed):
#     - a dedicated primary agent whose permission ruleset denies Bash,
#       webfetch/websearch, subagents (task), skills, and ALL reads outside
#       the worktree (external_directory) — stronger than claude's
#       deny-list, which blocked only named secret paths;
#     - writes allowed ONLY under briefs/** (permission patterns evaluate
#       last-match-wins, so the "*" deny must precede the briefs/** allow).
#   The prompt is piped via STDIN (a 100KB+ radar prompt overflows the
#   argv size limit — E2BIG). Model comes from the user's global opencode
#   config (their custom provider) unless RADAR_OPENCODE_MODEL overrides
#   it; --pure skips external plugins so a headless run stays
#   deterministic. Prints opencode's stdout; returns opencode's exit code.
radar_run_opencode_agent() {
  local worktree_dir="$1" prompt_file="$2"
  local cfg model_args=()
  cfg="$(mktemp "${TMPDIR:-/tmp}/radar-opencode-config.XXXXXX")"
  cat > "$cfg" <<'JSON'
{
  "$schema": "https://opencode.ai/config.json",
  "default_agent": "radar",
  "agent": {
    "radar": {
      "mode": "primary",
      "steps": 60,
      "permission": {
        "edit": { "*": "deny", "briefs/**": "allow" },
        "bash": "deny",
        "webfetch": "deny",
        "websearch": "deny",
        "task": "deny",
        "skill": "deny",
        "external_directory": "deny"
      }
    }
  }
}
JSON
  [[ -n "${RADAR_OPENCODE_MODEL:-}" ]] && model_args=(--model "$RADAR_OPENCODE_MODEL")
  local rc=0
  (
    cd "$worktree_dir" || exit 1
    export OPENCODE_CONFIG="$cfg" OPENCODE_DISABLE_EXTERNAL_SKILLS=1
    cat "$prompt_file" | opencode run --pure --agent radar "${model_args[@]}"
  ) || rc=$?
  rm -f "$cfg"
  return "$rc"
}

# ---------------------------------------------------------------------------
# Secret-scan safety net — runs on the finished brief before any commit, on
# top of (never instead of) the read-path allow/deny lists in security.md.
# ---------------------------------------------------------------------------

# radar_secret_scan <file>
#   Returns NON-ZERO if <file> matches any deny pattern (a hit — abort the
#   commit), 0 if it's clean. Deliberately inverted from grep's own exit
#   code so a caller can write `if ! radar_secret_scan "$f"; then abort; fi`
#   the same way it would check any other "did this fail" helper.
radar_secret_scan() {
  local file="$1"
  local pattern='AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{36,}|gho_[A-Za-z0-9]{36,}|xox[baprs]-[A-Za-z0-9-]+|-----BEGIN[A-Z ]*PRIVATE KEY-----|AIza[0-9A-Za-z_-]{35}'
  if grep -EIq "$pattern" -- "$file"; then
    return 1
  fi
  return 0
}

# ---------------------------------------------------------------------------
# Full-ranking history — added post-approval, per the user's explicit
# request for a queryable "top 50" view rather than only the top-3 brief.
# A per-radar SQLite file, not a new source of truth (the brief + git
# history remain that) — purely a queryable accumulation of every scored
# candidate, across days, for `sqlite3 ... "select ... order by score desc
# limit 50"` or radar-common/router.sh's `top` subcommand.
# ---------------------------------------------------------------------------

# radar_sqlite_ensure_schema <db_path>
#   Idempotent — safe to call every run.
radar_sqlite_ensure_schema() {
  local db_path="$1"
  mkdir -p "$(dirname -- "$db_path")"
  sqlite3 "$db_path" <<'SQL'
CREATE TABLE IF NOT EXISTS candidates (
  radar        TEXT NOT NULL,
  date         TEXT NOT NULL,
  title        TEXT NOT NULL,
  url          TEXT,
  category     TEXT,
  score        REAL,
  rationale    TEXT,
  picked_top3  INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_candidates_score ON candidates(score DESC);
CREATE INDEX IF NOT EXISTS idx_candidates_radar_date ON candidates(radar, date);
SQL
}

# radar_sqlite_load_ranked <db_path> <radar_name> <date> <ranked_json_file>
#   <ranked_json_file> is a JSON array of {title, url, category, score,
#   rationale, picked_top3}, written by the claude -p agent step alongside
#   the brief (see each radar's ranking.md "Full ranking output" section).
#   Missing/unreadable file is a silent no-op, not an error — the SQLite
#   history is a nice-to-have query surface, never a reason to fail a run
#   that already produced a valid brief.
radar_sqlite_load_ranked() {
  local db_path="$1" radar_name="$2" date="$3" ranked_json_file="$4"
  [[ -f "$ranked_json_file" ]] || return 0
  radar_sqlite_ensure_schema "$db_path"
  jq -c '.[]' "$ranked_json_file" 2>/dev/null | while IFS= read -r row; do
    local title url category score rationale picked
    title="$(jq -r '.title // ""' <<< "$row")"
    url="$(jq -r '.url // ""' <<< "$row")"
    category="$(jq -r '.category // ""' <<< "$row")"
    score="$(jq -r '.score // 0' <<< "$row")"
    rationale="$(jq -r '.rationale // ""' <<< "$row")"
    picked="$(jq -r 'if (.picked_top3 // false) then 1 else 0 end' <<< "$row")"
    local q_radar q_date q_title q_url q_category q_rationale
    q_radar="$(printf '%s' "$radar_name" | sed "s/'/''/g")"
    q_date="$(printf '%s' "$date" | sed "s/'/''/g")"
    q_title="$(printf '%s' "$title" | sed "s/'/''/g")"
    q_url="$(printf '%s' "$url" | sed "s/'/''/g")"
    q_category="$(printf '%s' "$category" | sed "s/'/''/g")"
    q_rationale="$(printf '%s' "$rationale" | sed "s/'/''/g")"
    sqlite3 "$db_path" \
      "INSERT INTO candidates (radar, date, title, url, category, score, rationale, picked_top3) VALUES ('$q_radar', '$q_date', '$q_title', '$q_url', '$q_category', $score, '$q_rationale', $picked);"
  done
}

# ---------------------------------------------------------------------------
# Notification — adapted from tasks/notify.py's herdr_show()/notify_send()
# pattern (herdr's own in-UI toast API, `.result.shown` read from its JSON,
# unconditional notify-send fallback), not written fresh.
# ---------------------------------------------------------------------------

# radar_notify <title> <body> [urgency]
#   Tries `herdr notification show <title> --body <body>` first, and only
#   falls back to notify-send when herdr is absent or its own JSON doesn't
#   report `.result.shown == true` — matching tasks/notify.py's
#   herdr_show()/notify_send() contract exactly (success is read from
#   herdr's JSON, never its exit code).
radar_notify() {
  local title="$1" body="$2" urgency="${3:-}"
  local shown="false"

  if command -v herdr >/dev/null 2>&1; then
    local result
    if result="$(herdr notification show "$title" --body "$body" 2>/dev/null)"; then
      if command -v jq >/dev/null 2>&1; then
        shown="$(printf '%s' "$result" | jq -r '.result.shown // false' 2>/dev/null || echo false)"
      fi
    fi
  fi

  if [[ "$shown" != "true" ]] && command -v notify-send >/dev/null 2>&1; then
    if [[ -n "$urgency" ]]; then
      notify-send -u "$urgency" "$title" "$body"
    else
      notify-send "$title" "$body"
    fi
  fi
}
