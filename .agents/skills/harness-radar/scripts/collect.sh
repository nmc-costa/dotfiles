#!/bin/bash
# harness-radar/scripts/collect.sh — deterministic, no-LLM data collection.
# Every source below is a plain read-only `curl`/`gh api`/GraphQL fetch —
# nothing here ever executes third-party code. See ../security.md and
# ../sources.md before changing anything.
#
# Output: $STATE_DIR/inbox/<date>.json (new items only, grouped by
# category) and $STATE_DIR/status.json (per-source ok/error tracking).
# Cursors live in $STATE_DIR/seen.json.pending — run.sh promotes that file
# to seen.json only after a successful commit (radar_promote_seen in
# radar-common/lib.sh), so a crash before that point never loses track of
# what was already collected.
#
# House style: bash, [[ ]] / (( )), 2-space indent, matching
# .agents/providers/proxy/ensure-proxy.sh and radar-common/lib.sh.

set -euo pipefail

SCRIPT_DIR="$(cd -P -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd -P -- "$SCRIPT_DIR/.." && pwd)"
REPO_DIR="$(cd -P -- "$SKILL_DIR/../../.." && pwd)"
RADAR_NAME="harness-radar"

# shellcheck source=../../../.agents/automation/radar-common/lib.sh
source "$REPO_DIR/.agents/automation/radar-common/lib.sh"

STATE_DIR="$HOME/.local/state/$RADAR_NAME"
DATE="$(date +%Y-%m-%d)"
SEEN_FILE="$STATE_DIR/seen.json"
PENDING_FILE="$STATE_DIR/seen.json.pending"
STATUS_FILE="$STATE_DIR/status.json"
SNAP_DIR="$STATE_DIR/snapshots"
INBOX_DIR="$STATE_DIR/inbox"
INBOX_FILE="$INBOX_DIR/$DATE.json"
STATUS_FAIL_THRESHOLD=3
USER_AGENT="harness-radar/1.0 (+https://github.com/nmc-costa/dotfiles)"

mkdir -p "$STATE_DIR" "$SNAP_DIR" "$INBOX_DIR"
[[ -f "$SEEN_FILE" ]] || echo '{}' > "$SEEN_FILE"
# PENDING_FILE is the live cursor store for this not-yet-promoted cycle. It
# is seeded from seen.json only when it doesn't already exist (i.e. right
# after a promotion, or on a brand-new machine) — a same-day re-run of this
# script (or of run.sh after a crash, before promotion) reuses whatever
# cursors are already staged here, which is what makes "run collect.sh
# twice back-to-back" produce an empty second inbox instead of duplicates.
[[ -f "$PENDING_FILE" ]] || cp -f "$SEEN_FILE" "$PENDING_FILE"
[[ -f "$STATUS_FILE" ]] || echo '{}' > "$STATUS_FILE"
[[ -f "$INBOX_FILE" ]] || jq -n --arg d "$DATE" '{date: $d, categories: {}}' > "$INBOX_FILE"

now_iso() { date -u +"%Y-%m-%dT%H:%M:%SZ"; }

# ---------------------------------------------------------------------------
# Small local helpers (state/status/inbox bookkeeping specific to this
# radar's collect.sh — per radar-common's own header comment, per-source
# status tracking and inbox shape are collect.sh's job, not lib.sh's).
# ---------------------------------------------------------------------------

get_seen() {
  local key="$1"
  jq -r --arg k "$key" '.[$k] // empty' "$PENDING_FILE" 2>/dev/null
}

set_pending() {
  local key="$1" value="$2"
  local tmp
  tmp="$(mktemp)"
  jq --arg k "$key" --arg v "$value" '.[$k] = $v' "$PENDING_FILE" > "$tmp"
  radar_atomic_install "$tmp" "$PENDING_FILE"
}

get_seen_json() {
  local key="$1" default_json="$2"
  jq -c --arg k "$key" --argjson d "$default_json" '.[$k] // $d' "$PENDING_FILE" 2>/dev/null
}

set_pending_json() {
  local key="$1" value_json="$2"
  local tmp
  tmp="$(mktemp)"
  jq --arg k "$key" --argjson v "$value_json" '.[$k] = $v' "$PENDING_FILE" > "$tmp"
  radar_atomic_install "$tmp" "$PENDING_FILE"
}

mark_ok() {
  local key="$1"
  local tmp
  tmp="$(mktemp)"
  jq --arg k "$key" --arg t "$(now_iso)" \
    '.[$k] = {status: "ok", consecutive_failures: 0, last_checked: $t}' \
    "$STATUS_FILE" > "$tmp"
  radar_atomic_install "$tmp" "$STATUS_FILE"
}

mark_error() {
  local key="$1" msg="$2"
  local prev count tmp
  prev="$(jq -r --arg k "$key" '.[$k].consecutive_failures // 0' "$STATUS_FILE")"
  count=$(( prev + 1 ))
  tmp="$(mktemp)"
  jq --arg k "$key" --arg t "$(now_iso)" --arg m "$msg" --argjson c "$count" \
    '.[$k] = {status: "error", consecutive_failures: $c, last_checked: $t, message: $m}' \
    "$STATUS_FILE" > "$tmp"
  radar_atomic_install "$tmp" "$STATUS_FILE"
  echo "$RADAR_NAME: [$key] error: $msg" >&2
  if (( count == STATUS_FAIL_THRESHOLD )); then
    radar_notify "$RADAR_NAME: source '$key' failing" \
      "'$key' has failed $count runs in a row (latest: $msg). Check status.json." \
      "normal"
  fi
}

add_item() {
  local category="$1" json_item="$2"
  local tmp
  tmp="$(mktemp)"
  jq --arg c "$category" --argjson item "$json_item" \
    '.categories[$c] = ((.categories[$c] // []) + [$item])' \
    "$INBOX_FILE" > "$tmp"
  radar_atomic_install "$tmp" "$INBOX_FILE"
}

# ---------------------------------------------------------------------------
# Generic collectors, reused across several named sources in sources.md.
# ---------------------------------------------------------------------------

# collect_gh_releases <key> <owner/repo> <category>
#   New releases since the last-seen tag. An absent cursor (first run, or
#   right after a promotion with no prior entry for this key) means every
#   release currently on the first API page counts as new -- this radar's
#   inbox is meant to be populated on a first run, per its own README's
#   acceptance criteria, not silently seeded.
collect_gh_releases() {
  local key="$1" repo="$2" category="$3"
  local last_tag json
  last_tag="$(get_seen "$key")"
  if ! json="$(gh api "repos/$repo/releases?per_page=30" 2>/dev/null)"; then
    mark_error "$key" "gh api repos/$repo/releases failed"
    return
  fi
  mark_ok "$key"
  local newest_tag new_items
  newest_tag="$(jq -r '.[0].tag_name // empty' <<< "$json")"
  new_items="$(jq --arg last "$last_tag" '
    . as $all
    | if $last == "" then $all
      else ( ($all | map(.tag_name) | index($last)) as $idx
             | if $idx == null then $all else $all[0:$idx] end )
      end
  ' <<< "$json")"
  jq -c '.[]' <<< "$new_items" | while IFS= read -r item; do
    add_item "$category" "$(jq -c '{repo: $repo, title: .name, tag: .tag_name, url: .html_url, published_at: .published_at}' --arg repo "$repo" <<< "$item")"
  done
  [[ -n "$newest_tag" ]] && set_pending "$key" "$newest_tag"
}

# collect_gh_commits <key> <owner/repo> <category> [sha_ref]
#   <sha_ref> is optional -- omitted (the common case), GitHub uses the
#   repo's actual default branch, which isn't safe to assume (verified
#   during implementation: herdrdev/herdr's default branch is `master`,
#   not `main`) so this never hardcodes one.
collect_gh_commits() {
  local key="$1" repo="$2" category="$3" sha_ref="${4:-}"
  local last_sha json endpoint="repos/$repo/commits?per_page=30"
  [[ -n "$sha_ref" ]] && endpoint="repos/$repo/commits?sha=$sha_ref&per_page=30"
  last_sha="$(get_seen "$key")"
  if ! json="$(gh api "$endpoint" 2>/dev/null)"; then
    mark_error "$key" "gh api $endpoint failed"
    return
  fi
  mark_ok "$key"
  local newest_sha new_items
  newest_sha="$(jq -r '.[0].sha // empty' <<< "$json")"
  new_items="$(jq --arg last "$last_sha" '
    . as $all
    | if $last == "" then $all
      else ( ($all | map(.sha) | index($last)) as $idx
             | if $idx == null then [] else $all[0:$idx] end )
      end
  ' <<< "$json")"
  jq -c '.[]' <<< "$new_items" | while IFS= read -r item; do
    add_item "$category" "$(jq -c '{repo: $repo, sha: .sha[0:7], message: (.commit.message | split("\n")[0]), url: .html_url}' --arg repo "$repo" <<< "$item")"
  done
  [[ -n "$newest_sha" ]] && set_pending "$key" "$newest_sha"
}

# collect_gh_topic_repos <key> <topic> <category>
#   Diffs a GitHub topic listing as a whole (never per-repo content fetches)
#   — used for herdr's plugin marketplace (herdr-plugin topic) and the
#   Copilot CLI plugin topic, per sources.md.
collect_gh_topic_repos() {
  local key="$1" topic="$2" category="$3"
  local last_cursor json
  last_cursor="$(get_seen "$key")"
  if ! json="$(gh api "search/repositories?q=topic:$topic&sort=updated&order=desc&per_page=30" 2>/dev/null)"; then
    mark_error "$key" "gh api search/repositories topic:$topic failed"
    return
  fi
  mark_ok "$key"
  local newest new_items
  newest="$(jq -r '.items[0].updated_at // empty' <<< "$json")"
  new_items="$(jq --arg last "$last_cursor" '
    .items as $all
    | if $last == "" then $all else [ $all[] | select(.updated_at > $last) ] end
  ' <<< "$json")"
  jq -c '.[]' <<< "$new_items" | while IFS= read -r repo; do
    add_item "$category" "$(jq -c '{repo: .full_name, url: .html_url, updated_at: .updated_at, stars: .stargazers_count}' <<< "$repo")"
  done
  [[ -n "$newest" ]] && set_pending "$key" "$newest"
}

# collect_snapshot_diff <key> <url> <category> <label> [content_check]
#   Fetches <url>, verifies it looks like the expected content (when a
#   content_check substring is given -- guards against an HTML error/
#   captive-portal page that happened to return 200, same check
#   omarchy-radar applies to its RSS feed), diffs it against the last
#   snapshot (diffing against /dev/null on a genuinely first run, so day
#   one is still populated instead of silently just seeding), and stores
#   the new snapshot either way.
collect_snapshot_diff() {
  local key="$1" url="$2" category="$3" label="$4" content_check="${5:-}"
  local snap="$SNAP_DIR/$key.snapshot"
  local tmp
  tmp="$(mktemp)"
  if ! curl -fsSL --max-time 20 -A "$USER_AGENT" "$url" -o "$tmp" 2>/dev/null; then
    mark_error "$key" "curl $url failed"
    rm -f "$tmp"
    return
  fi
  if [[ -n "$content_check" ]] && ! grep -qi -- "$content_check" "$tmp"; then
    mark_error "$key" "response from $url didn't contain expected marker '$content_check' -- possible error/captive page, not trusting it"
    rm -f "$tmp"
    return
  fi
  mark_ok "$key"
  local baseline="$snap"
  [[ -f "$baseline" ]] || baseline="/dev/null"
  if ! diff -q "$baseline" "$tmp" >/dev/null 2>&1; then
    local diff_text
    diff_text="$(diff -u "$baseline" "$tmp" 2>/dev/null | head -c 4000)"
    add_item "$category" "$(jq -n --arg label "$label" --arg url "$url" --arg diff "$diff_text" '{label: $label, url: $url, diff: $diff}')"
  fi
  cp -f "$tmp" "$snap"
  rm -f "$tmp"
}

# ---------------------------------------------------------------------------
# Named sources — see ../sources.md for the research backing each one.
# ---------------------------------------------------------------------------

# 1. herdr itself.
collect_herdr() {
  collect_gh_releases herdr_releases herdrdev/herdr herdr
  collect_gh_commits herdr_commits herdrdev/herdr herdr
}

# 2. herdr's plugin marketplace (herdr.dev/plugins == the herdr-plugin topic).
collect_herdr_marketplace() {
  collect_gh_topic_repos herdr_plugin_marketplace herdr-plugin herdr_plugin_marketplace
}

# 3. DeepSeek Harness (dsh) + its plugin ecosystem index.
collect_dsh() {
  collect_gh_releases dsh_releases deepseek-ai/deepseek-harness dsh
  collect_snapshot_diff dsh_ecosystem \
    "https://raw.githubusercontent.com/zoahdev/dsh-ecosystem/main/README.md" \
    dsh "dsh-ecosystem README" ""
}

# 4. Codex CLI plugin ecosystem.
collect_codex() {
  collect_snapshot_diff codex_awesome \
    "https://raw.githubusercontent.com/RoggeOhta/awesome-codex-cli/main/README.md" \
    codex_cli "awesome-codex-cli README" ""

  local key="codex_discussion" category="codex_cli"
  local last_count json total
  last_count="$(get_seen "$key")"
  local query='query($owner:String!,$repo:String!,$num:Int!){repository(owner:$owner,name:$repo){discussion(number:$num){comments(last:20){totalCount nodes{url bodyText createdAt author{login}}}}}}'
  if ! json="$(gh api graphql -f query="$query" -F owner=openai -F repo=codex -F num=16329 2>/dev/null)"; then
    mark_error "$key" "gh api graphql (openai/codex discussion #16329) failed"
    return
  fi
  mark_ok "$key"
  total="$(jq -r '.data.repository.discussion.comments.totalCount // 0' <<< "$json")"
  if [[ -z "$last_count" ]] || (( total > last_count )); then
    jq -c '.data.repository.discussion.comments.nodes[]' <<< "$json" | while IFS= read -r c; do
      add_item "$category" "$(jq -c '{author: .author.login, url: .url, created_at: .createdAt, excerpt: (.bodyText[0:200])}' <<< "$c")"
    done
  fi
  set_pending "$key" "$total"
}

# 5. OpenCode plugin ecosystem.
collect_opencode() {
  collect_snapshot_diff opencode_awesome \
    "https://raw.githubusercontent.com/awesome-opencode/awesome-opencode/main/README.md" \
    opencode "awesome-opencode README" ""
}

# 6. Gemini CLI Extensions Gallery.
collect_gemini_cli() {
  collect_snapshot_diff gemini_cli_gallery \
    "https://geminicli.com/extensions" \
    gemini_cli "Gemini CLI Extensions Gallery" "extension"
}

# 7. Copilot CLI plugin marketplaces.
#    NOTE (under-specified in sources.md, reasonable call made here):
#    sources.md names these only as "copilot-plugins and awesome-copilot"
#    with no owner/org given for either. `github/awesome-copilot` is a real,
#    canonical-looking repo (GitHub's own org); "copilot-plugins" has no
#    equally obvious single canonical repo, so it's tracked here as the
#    `copilot-plugin` GitHub topic (the same topic-diff pattern used for
#    herdr's marketplace) rather than a guessed single repo slug. Revisit
#    and pin a canonical answer in docs/radar-knowledge/harness.md the next
#    time this radar's sources are reviewed.
collect_copilot_cli() {
  collect_snapshot_diff copilot_awesome \
    "https://raw.githubusercontent.com/github/awesome-copilot/main/README.md" \
    copilot_cli "awesome-copilot README" ""
  collect_gh_topic_repos copilot_plugins_topic copilot-plugin copilot_cli
}

# 8. Claude Code's own marketplace -- confirmed via this machine's actual
#    plugin-marketplace config (~/.claude/plugins/known_marketplaces.json,
#    checked 2026-09-25: anthropics/claude-plugins-official) rather than
#    assumed from memory, per sources.md's own instruction. Falls back to
#    that confirmed default if the config file isn't present (e.g. a fresh
#    machine that hasn't launched Claude Code with this marketplace yet).
collect_claude_plugins_official() {
  local repo="anthropics/claude-plugins-official"
  local marketplaces_file="$HOME/.claude/plugins/known_marketplaces.json"
  if [[ -f "$marketplaces_file" ]]; then
    local configured
    configured="$(jq -r '.["claude-plugins-official"].source.repo // empty' "$marketplaces_file" 2>/dev/null)"
    [[ -n "$configured" ]] && repo="$configured"
  fi
  collect_gh_releases claude_plugins_official "$repo" claude_code
}

# 9. Multi-agent / orchestration frameworks -- named repos' releases,
#    never a thin "awesome" list (see sources.md for why).
collect_orchestration_frameworks() {
  collect_gh_releases crewai crewAIInc/crewAI orchestration
  collect_gh_releases langgraph langchain-ai/langgraph orchestration
  collect_gh_releases deer_flow bytedance/deer-flow orchestration
  collect_gh_releases agent_framework microsoft/agent-framework orchestration
  collect_gh_releases openclaw openclaw/openclaw orchestration
  collect_gh_releases hermes_agent NousResearch/hermes-agent orchestration
}

# 10. Benchmark leaderboards.
#     NOTE (under-specified in sources.md, reasonable call made here):
#     sources.md gives exact leaderboard URLs for SWE-bench/Verified and
#     LiveCodeBench, but only names Terminal-Bench's *repo*
#     (harbor-framework/terminal-bench), not a specific leaderboard page URL
#     to diff. Rather than guess a URL, Terminal-Bench is tracked via that
#     repo's GitHub releases (the same reliable, named-endpoint pattern used
#     for every other repo-backed source) as a proxy for leaderboard-moving
#     changes. Pin the real leaderboard endpoint in docs/radar-knowledge/
#     harness.md once confirmed, and switch this to collect_snapshot_diff.
collect_benchmarks() {
  collect_snapshot_diff swebench \
    "https://www.swebench.com/" \
    benchmarks "SWE-bench leaderboard" "swe-bench"
  collect_snapshot_diff swebench_verified \
    "https://www.swebench.com/verified.html" \
    benchmarks "SWE-bench Verified leaderboard" "verified"
  collect_gh_releases terminal_bench harbor-framework/terminal-bench benchmarks
  collect_snapshot_diff livecodebench \
    "https://livecodebench.github.io/leaderboard.html" \
    benchmarks "LiveCodeBench leaderboard" "livecodebench"
}

# 11. Skill/plugin/MCP ecosystem aggregators.
collect_ecosystem_aggregators() {
  collect_snapshot_diff best_skills_csv \
    "https://raw.githubusercontent.com/LinklyAI/best-skills/main/data/latest/rankings/best-100.csv" \
    ecosystem "best-skills CSV" ""

  local key="mcp_registry" category="mcp_registry"
  local seen_ids json filtered new_ids
  seen_ids="$(get_seen_json "$key" '[]')"
  if ! json="$(curl -fsSL --max-time 20 -A "$USER_AGENT" "https://registry.modelcontextprotocol.io/v0/servers" 2>/dev/null)"; then
    mark_error "$key" "curl MCP registry failed"
    return
  fi
  mark_ok "$key"
  # Filtered to rows plausibly relevant to coding harnesses/agents, per
  # sources.md ("filtered query -- skip cleanly if no relevant hits").
  # NOTE: only the current page (the registry paginates via a `nextCursor`,
  # 30 servers/page as verified at implementation time) is checked each
  # run, not the whole registry -- sources.md doesn't ask for full
  # pagination, and this still surfaces newly-published servers as they
  # land near the front of the listing. Dedup key is `.server.name`
  # (the registry's actual identifier field -- verified live, it is NOT a
  # flat `.name`/`.id`, entries are wrapped as `{"server": {...}, "_meta":
  # {...}}`); a version bump of an already-seen server is not treated as
  # a new item.
  filtered="$(jq -c --argjson seen "$seen_ids" '
    ( .servers // [] ) as $list
    | [ $list[]? | .server // empty | select(
        (((.name // "") + " " + (.description // "")) | test("agent|harness|claude|codex|copilot|coding agent|dev ?tool"; "i"))
        and (( (.name // "") as $i | ($seen | index($i)) ) == null)
      ) ]
  ' <<< "$json" 2>/dev/null || echo '[]')"
  [[ -z "$filtered" ]] && filtered='[]'
  jq -c '.[]' <<< "$filtered" | while IFS= read -r srv; do
    add_item "$category" "$(jq -c '{name: .name, description: (.description // ""), version: (.version // "")}' <<< "$srv")"
  done
  new_ids="$(jq -c --argjson seen "$seen_ids" '
    ( .servers // [] ) as $list
    | ( $seen + [ $list[]? | .server.name? // empty ] ) | unique
  ' <<< "$json" 2>/dev/null || echo "$seen_ids")"
  [[ -z "$new_ids" ]] && new_ids="$seen_ids"
  set_pending_json "$key" "$new_ids"
}

main() {
  # Each source is independent and wrapped so that an unexpected failure in
  # one (beyond the network-error handling already inside each collector)
  # never stops the rest from running -- consistent with status.json
  # tracking failures per-source rather than the whole run dying together.
  collect_herdr || true
  collect_herdr_marketplace || true
  collect_dsh || true
  collect_codex || true
  collect_opencode || true
  collect_gemini_cli || true
  collect_copilot_cli || true
  collect_claude_plugins_official || true
  collect_orchestration_frameworks || true
  collect_benchmarks || true
  collect_ecosystem_aggregators || true
}

main

echo "$RADAR_NAME: collect.sh done for $DATE ($INBOX_FILE)"
