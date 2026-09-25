#!/bin/bash
# omarchy-radar/scripts/collect.sh — deterministic, no-LLM data collection.
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
# .agents/providers/proxy/ensure-proxy.sh, radar-common/lib.sh, and
# harness-radar/scripts/collect.sh (same collector-function shapes, kept
# consistent across radars even though each collect.sh is self-contained —
# see radar-common/lib.sh's own header comment on why per-source status
# tracking and inbox shape live here, not in the shared lib).

set -euo pipefail

SCRIPT_DIR="$(cd -P -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd -P -- "$SCRIPT_DIR/.." && pwd)"
REPO_DIR="$(cd -P -- "$SKILL_DIR/../../.." && pwd)"
RADAR_NAME="omarchy-radar"

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
USER_AGENT="omarchy-radar/1.0 (+https://github.com/nmc-costa/dotfiles)"

mkdir -p "$STATE_DIR" "$SNAP_DIR" "$INBOX_DIR"
[[ -f "$SEEN_FILE" ]] || echo '{}' > "$SEEN_FILE"
# PENDING_FILE is the live cursor store for this not-yet-promoted cycle,
# seeded from seen.json only when it doesn't already exist -- what makes
# "run collect.sh twice back-to-back" produce an empty second inbox instead
# of duplicates (the explicit Testing acceptance criterion).
[[ -f "$PENDING_FILE" ]] || cp -f "$SEEN_FILE" "$PENDING_FILE"
[[ -f "$STATUS_FILE" ]] || echo '{}' > "$STATUS_FILE"
[[ -f "$INBOX_FILE" ]] || jq -n --arg d "$DATE" '{date: $d, categories: {}}' > "$INBOX_FILE"

now_iso() { date -u +"%Y-%m-%dT%H:%M:%SZ"; }

# ---------------------------------------------------------------------------
# Small local helpers (state/status/inbox bookkeeping) -- identical shape to
# harness-radar/scripts/collect.sh, kept in sync deliberately for anyone
# reading both radars side by side.
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
# Generic collectors (same shapes as harness-radar's, for consistency).
# ---------------------------------------------------------------------------

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

# collect_gh_commits <key> <owner/repo> <category> <sha_ref>
#   sha_ref is required here (unlike harness-radar's optional version) --
#   omacom/omarchy's default branch is a Quattro-era rename away from
#   "main"/"master" (it's "quattro"), so this never relies on GitHub's
#   default-branch fallback for this specific repo.
collect_gh_commits() {
  local key="$1" repo="$2" category="$3" sha_ref="$4"
  local last_sha json endpoint="repos/$repo/commits?sha=$sha_ref&per_page=30"
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

# collect_snapshot_diff <key> <url> <category> <label> [content_check]
#   Fetches <url>, verifies it looks like the expected content when a
#   content_check substring is given (guards against an HTML error/
#   captive-portal page that returned 200), diffs against the last snapshot
#   (against /dev/null on a genuine first run, so day one is populated
#   instead of silently just seeding), stores the new snapshot either way.
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
# Named sources -- see ../sources.md for the research backing each one.
# ---------------------------------------------------------------------------

# 1. Primary: the news-radar feed (releases + marketplace + news, already
#    aggregated by mtolhuys/omarchy-news-radar). RSS 2.0; parsed with
#    Python's stdlib xml.etree.ElementTree per sources.md (never assume
#    xmllint is installed). Falls back to a direct GitHub releases fetch on
#    any non-200, non-RSS, or parse failure.
collect_news_radar_feed() {
  local key="news_radar_feed" category="omarchy_core"
  local url="https://mtolhuijs.nl/news-radar/feed.xml"
  local tmp items
  tmp="$(mktemp)"
  if ! curl -fsSL --max-time 20 -A "$USER_AGENT" "$url" -o "$tmp" 2>/dev/null; then
    mark_error "$key" "curl $url failed -- falling back to direct GitHub releases"
    rm -f "$tmp"
    collect_gh_releases omarchy_releases_fallback omacom/omarchy "$category"
    return
  fi

  local last_guid seen_guids_json
  last_guid="$(get_seen "${key}_last_guid")"
  seen_guids_json="$(get_seen_json "${key}_seen_guids" '[]')"

  if ! items="$(python3 - "$tmp" <<'PYEOF'
import sys, json
import xml.etree.ElementTree as ET

path = sys.argv[1]
try:
    tree = ET.parse(path)
except ET.ParseError:
    print("PARSE_ERROR")
    sys.exit(0)

root = tree.getroot()
channel = root.find("channel")
if channel is None:
    print("PARSE_ERROR")
    sys.exit(0)

out = []
for item in channel.findall("item"):
    guid_el = item.find("guid")
    out.append({
        "guid": (guid_el.text or "").strip() if guid_el is not None else "",
        "title": (item.findtext("title") or "").strip(),
        "link": (item.findtext("link") or "").strip(),
        "description": (item.findtext("description") or "").strip()[:500],
        "pub_date": (item.findtext("pubDate") or "").strip(),
    })
print(json.dumps(out))
PYEOF
  )" || [[ "$items" == "PARSE_ERROR" ]]; then
    mark_error "$key" "response from $url is not well-formed RSS -- falling back to direct GitHub releases"
    rm -f "$tmp"
    collect_gh_releases omarchy_releases_fallback omacom/omarchy "$category"
    return
  fi
  rm -f "$tmp"
  mark_ok "$key"

  local new_items
  new_items="$(jq -c --argjson seen "$seen_guids_json" '
    [ .[] | select(.guid != "" and ((.guid) as $g | ($seen | index($g)) == null)) ]
  ' <<< "$items")"

  jq -c '.[]' <<< "$new_items" | while IFS= read -r item; do
    add_item "$category" "$item"
  done

  local newest_guid all_guids
  newest_guid="$(jq -r '.[0].guid // empty' <<< "$items")"
  all_guids="$(jq -c --argjson seen "$seen_guids_json" '
    ( $seen + [ .[].guid | select(. != "") ] ) | unique
  ' <<< "$items")"
  [[ -n "$newest_guid" ]] && set_pending "${key}_last_guid" "$newest_guid"
  set_pending_json "${key}_seen_guids" "$all_guids"
}

# 2. Raw commits on the quattro branch (the feed doesn't cover these).
collect_omarchy_commits() {
  collect_gh_commits omarchy_commits omacom/omarchy omarchy_core quattro
}

# 3. GitHub Discussions on omacom/omarchy (REST has no Discussions endpoint;
#    GraphQL, existing repo/read:org token scopes are sufficient).
collect_omarchy_discussions() {
  local key="omarchy_discussions" category="omarchy_core"
  local last_cursor json
  last_cursor="$(get_seen "$key")"
  local query='query($owner:String!,$repo:String!){repository(owner:$owner,name:$repo){discussions(first:20,orderBy:{field:UPDATED_AT,direction:DESC}){nodes{url title updatedAt author{login}}}}}'
  if ! json="$(gh api graphql -f query="$query" -F owner=omacom -F repo=omarchy 2>/dev/null)"; then
    mark_error "$key" "gh api graphql (omacom/omarchy discussions) failed"
    return
  fi
  mark_ok "$key"
  local newest new_items
  newest="$(jq -r '.data.repository.discussions.nodes[0].updatedAt // empty' <<< "$json")"
  new_items="$(jq --arg last "$last_cursor" '
    .data.repository.discussions.nodes as $all
    | if $last == "" then $all else [ $all[] | select(.updatedAt > $last) ] end
  ' <<< "$json")"
  jq -c '.[]' <<< "$new_items" | while IFS= read -r d; do
    add_item "$category" "$(jq -c '{title: .title, author: .author.login, url: .url, updated_at: .updatedAt}' <<< "$d")"
  done
  [[ -n "$newest" ]] && set_pending "$key" "$newest"
}

# 4. awesome-omarchy README diff.
collect_awesome_omarchy() {
  collect_snapshot_diff awesome_omarchy \
    "https://raw.githubusercontent.com/aorumbayev/awesome-omarchy/main/README.md" \
    omarchy_core "awesome-omarchy README" ""
}

# 5. Plugin marketplace index diff -- secondary/backstop only, per
#    sources.md (metrics like views/hearts excluded from ranking signal).
collect_plugin_marketplace() {
  collect_gh_releases omarchy_marketplace omacom/omarchy-plugin-marketplace omarchy_core
}

# 6. Community discussion: Reddit + Hacker News (keyless).
collect_community_discussion() {
  local key="reddit_omarchy" category="community"
  local tmp posts
  # Reddit's .json endpoint 403-blocks this machine's UA/IP class (verified
  # live 2026-09-25) while the Atom .rss endpoint serves 200 -- fetch .rss
  # and parse it with stdlib ElementTree, same approach as the news-radar
  # feed collector above (never assume xmllint is installed).
  tmp="$(mktemp)"
  if ! curl -fsSL --max-time 20 -A "$USER_AGENT" \
      "https://www.reddit.com/r/omarchy/new/.rss" -o "$tmp" 2>/dev/null; then
    mark_error "$key" "curl reddit r/omarchy .rss failed"
    rm -f "$tmp"
  else
    posts="$(python3 - "$tmp" <<'PYEOF'
import sys, json
import xml.etree.ElementTree as ET

NS = {"a": "http://www.w3.org/2005/Atom"}
try:
    root = ET.parse(sys.argv[1]).getroot()
except ET.ParseError:
    print("[]")
    sys.exit(0)

out = []
for entry in root.findall("a:entry", NS):
    link_el = entry.find("a:link", NS)
    author_el = entry.find("a:author/a:name", NS)
    out.append({
        "id": (entry.findtext("a:id", "", NS) or "").strip(),
        "title": (entry.findtext("a:title", "", NS) or "").strip(),
        "url": (link_el.get("href") or "").strip() if link_el is not None else "",
        "author": (author_el.text or "").strip() if author_el is not None else "",
        "updated": (entry.findtext("a:updated", "", NS) or "").strip(),
    })
print(json.dumps(out))
PYEOF
)"
    rm -f "$tmp"
    mark_ok "$key"
    local seen_ids_json new_items
    seen_ids_json="$(get_seen_json "${key}_seen_ids" '[]')"
    new_items="$(jq -c --argjson seen "$seen_ids_json" '
      [ .[] | select((.id) as $i | ($seen | index($i)) == null and $i != "") ]
    ' <<< "$posts")"
    jq -c '.[]' <<< "$new_items" | while IFS= read -r post; do
      add_item "$category" "$post"
    done
    local all_ids
    all_ids="$(jq -c --argjson seen "$seen_ids_json" '
      ( $seen + [ .[].id ] ) | unique
    ' <<< "$posts")"
    set_pending_json "${key}_seen_ids" "$all_ids"
  fi

  key="hn_omarchy"
  if ! json="$(curl -fsSL --max-time 20 -A "$USER_AGENT" \
      "https://hn.algolia.com/api/v1/search_by_date?query=omarchy&tags=story" 2>/dev/null)"; then
    mark_error "$key" "curl HN Algolia failed"
    return
  fi
  mark_ok "$key"
  local last_ts seen_ids_json new_items
  last_ts="$(get_seen "$key")"
  new_items="$(jq --arg last "${last_ts:-0}" '
    [ .hits[] | select((.created_at_i | tostring) > $last) ]
  ' <<< "$json")"
  jq -c '.[]' <<< "$new_items" | while IFS= read -r hit; do
    add_item "community" "$(jq -c '{title: .title, url: (.url // ("https://news.ycombinator.com/item?id=" + (.objectID // ""))), points: .points, author: .author}' <<< "$hit")"
  done
  local newest_ts
  newest_ts="$(jq -r '[.hits[].created_at_i] | max // empty' <<< "$json")"
  [[ -n "$newest_ts" ]] && set_pending "$key" "$newest_ts"
}

# 7. Skill/plugin/MCP ecosystem signal, filtered to Omarchy/Hyprland/
#    dotfiles-relevant rows only (data-fetch only -- npx skills/tessl stay
#    interactive-only for the human, per security.md).
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
  # Filtered to rows plausibly relevant to Omarchy/Hyprland/dotfiles, per
  # sources.md. Dedup key is `.server.name` (verified live shape:
  # {"server": {...}, "_meta": {...}}, not a flat `.name`).
  filtered="$(jq -c --argjson seen "$seen_ids" '
    ( .servers // [] ) as $list
    | [ $list[]? | .server // empty | select(
        (((.name // "") + " " + (.description // "")) | test("omarchy|hyprland|dotfiles|wayland|linux desktop|arch linux"; "i"))
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
  # Each source is independent and wrapped so an unexpected failure in one
  # never stops the rest -- consistent with status.json tracking failures
  # per-source rather than the whole run dying together.
  collect_news_radar_feed || true
  collect_omarchy_commits || true
  collect_omarchy_discussions || true
  collect_awesome_omarchy || true
  collect_plugin_marketplace || true
  collect_community_discussion || true
  collect_ecosystem_aggregators || true
}

main

echo "$RADAR_NAME: collect.sh done for $DATE ($INBOX_FILE)"
