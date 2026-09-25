#!/bin/bash
# chronicle/scripts/run.sh — daily headless improve (researcher-radar family
# shape, card dotfiles-tsk-chronicle-daily-improve).
#
# Owner-directed policy (2026-09-25, via questionnaire):
#   once a day, mine this machine's interaction history (chronicle.py, local
#   + read-only), feed the latest radar briefs as online-research input, have
#   a headless agent turn the strongest candidate into AT MOST ONE small
#   skill improvement on a disposable branch, open an evidence-cited PR and
#   — only when every gate below holds — auto-merge it:
#
#     gate 1  changed paths ⊆ .agents/skills/** ∪ .agents/opencode/**
#     gate 2  PR is MERGEABLE and mergeStateStatus == CLEAN
#     gate 3  CI green (enforced by `gh pr merge --auto`; GitHub merges
#             only when checks pass)
#     gate 4  max 1 improve PR per day (branch chronicle/improve-<date>,
#             re-checked against open + recently-merged PRs)
#
# Fallback is always git: the PR body carries the revert command; any failed
# gate leaves the PR open for human review (propose-only).
#
# Environment:
#   CHRONICLE_AGENT=opencode|claude   headless engine (default opencode)
#   CHRONICLE_DRY_RUN=1               mine + build prompt, stop before
#                                     agent/push/PR (tests/validate)
#
# This script never writes to tasks/ and never commits to the main checkout.

set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd -- "$SCRIPT_DIR/../../../.." && pwd)"
# Resolve the canonical checkout (works from any worktree or synced copy):
# mine + briefs must always read the real, live repo, not a card worktree.
_git_common="$(git -C "$REPO_DIR" rev-parse --path-format=absolute --git-common-dir 2>/dev/null || true)"
[[ -n "$_git_common" ]] && REPO_DIR="$(dirname "$_git_common")"
CHRONICLE_PY="$REPO_DIR/.agents/skills/chronicle/chronicle.py"
STATE_DIR="${XDG_STATE_HOME:-$HOME/.local/state}/chronicle-improve"
WORKTREE_ROOT="$HOME/dotfiles.worktrees/chronicle"
TODAY="$(date +%F)"
BRANCH="chronicle/improve-$TODAY"
WORKTREE="$WORKTREE_ROOT/improve-$TODAY"
ALLOWLIST_RE='^\.agents/(skills|opencode)/'
REPO="nmc-costa/dotfiles"

log() { echo "[chronicle-improve] $*"; }
die() { echo "[chronicle-improve] ERROR: $*" >&2; exit 0; } # exit 0: a skipped day is not a timer failure

mkdir -p "$STATE_DIR"
DATE_STAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
{ echo "$DATE_STAMP $*"; } >> "$STATE_DIR/run.log" 2>/dev/null || true

command -v gh >/dev/null 2>&1 || die "gh not available"
command -v git >/dev/null 2>&1 || die "git not available"
[[ -f "$CHRONICLE_PY" ]] || die "chronicle.py not found at $CHRONICLE_PY"

# ---- gate 4 (pre-flight): one improve PR per day --------------------------
if [[ -f "$STATE_DIR/last-pr" ]] && [[ "$(cat "$STATE_DIR/last-pr")" == "$TODAY" ]]; then
  log "already ran today ($TODAY), nothing to do"
  exit 0
fi

git -C "$REPO_DIR" fetch origin main --quiet

existing="$(gh pr list --repo "$REPO" --head "$BRANCH" --state all --limit 1 \
  --json number --jq '.[0].number // empty' 2>/dev/null || true)"
if [[ -n "$existing" ]]; then
  log "PR #$existing already exists for $BRANCH, nothing to do"
  echo "$TODAY" > "$STATE_DIR/last-pr"
  exit 0
fi

# ---- disposable worktree off fresh origin/main ----------------------------
mkdir -p "$WORKTREE_ROOT"
BASE="$(git -C "$REPO_DIR" rev-parse origin/main)"

[[ -d "$WORKTREE" ]] && git -C "$REPO_DIR" worktree remove --force "$WORKTREE" 2>/dev/null || true
git -C "$REPO_DIR" worktree add --detach "$WORKTREE" "$BASE" --quiet
# -C: reset-or-create, so a branch left over from an aborted run can't wedge today's run
git -C "$WORKTREE" switch -C "$BRANCH" --quiet

cleanup() { git -C "$REPO_DIR" worktree remove --force "$WORKTREE" 2>/dev/null || true; }
if [[ "${CHRONICLE_DRY_RUN:-0}" != "1" ]]; then trap 'cleanup' EXIT; fi

# ---- deterministic collect: mine local history (read-only) ----------------
# Runs with cwd = canonical checkout so chronicle.py's tasks_root() and
# transcript paths resolve to the real, live data; outputs land in a temp
# dir, the main checkout is never written.
MINE_DIR="$(mktemp -d)"
python3 "$CHRONICLE_PY" mine --json --out "$MINE_DIR/mine.md" \
  > "$MINE_DIR/candidates.json" || die "chronicle.py mine failed"

CANDIDATE_COUNT="$(python3 -c \
  'import json,sys;print(len(json.load(open(sys.argv[1]))))' \
  "$MINE_DIR/candidates.json" 2>/dev/null || echo 0)"
log "mined $CANDIDATE_COUNT candidate groups"

# ---- online-research input: newest brief per radar, if any ----------------
# The radars write briefs/<name>-<date>.md on their disposable worktree
# branches; today they physically live under ~/.local/state/<radar>/
# worktrees/<date>/briefs/. Also accept the documented repo location
# (<repo>/briefs/) for whenever the radars start landing briefs there.
BRIEF_LINES=""
for radar in omarchy-radar harness-radar; do
  latest="$(
    {
      ls -t "$REPO_DIR/briefs/$radar"-*.md 2>/dev/null || true
      ls -t "$HOME/.local/state/$radar"/worktrees/*/briefs/"$radar"-*.md 2>/dev/null || true
    } | head -1
  )"
  if [[ -n "$latest" ]]; then
    cp "$latest" "$MINE_DIR/brief-$radar.md"
    BRIEF_LINES+="- Radar brief: $MINE_DIR/brief-$radar.md"$'\n'
    log "research input: $(basename "$latest")"
  else
    log "research input: no $radar brief present, continuing without"
  fi
done

# ---- agent prompt -----------------------------------------------------------
PROMPT="$(mktemp)"
cat > "$PROMPT" <<PROMPT
You are the unattended chronicle improve agent for the dotfiles workspace.

Mission: pick the SINGLE strongest candidate (or radar-brief-supported idea)
and implement it as one small, mechanical improvement to the workspace's
skill layer. Quality over quantity — most days the right answer is a small
polish; if NO candidate clears the bar, change nothing.

Hard rules:
- Work only inside this worktree ($WORKTREE).
- You may ONLY create or edit files under .agents/skills/ or .agents/opencode/.
- Never touch tasks/, .claude/, opencode.json, or anything else.
- Keep the change minimal: one skill, one behavior. No refactors.
- Every change must cite its evidence (candidate id / brief file + line).
- If the change adds a chain, update the touched skill's ## Chains section;
  keep skill descriptions tight (triggering is description-driven).
- When finished: git add ONLY the files you edited and run
  git commit -m "chronicle improve: <one-line summary>"
- If you changed nothing, commit nothing.
- Do not push; the harness script owns push/PR/merge.

Inputs (read-only):
- Candidates JSON: $MINE_DIR/candidates.json
- Mine report (human-readable, cited): $MINE_DIR/mine.md
$BRIEF_LINES
Respond with exactly one line: either "NO-CHANGE: <reason>" or
"CHANGED: <one-line summary>".
PROMPT

if [[ "${CHRONICLE_DRY_RUN:-0}" == "1" ]]; then
  log "dry-run: mine + prompt ready; agent step would start here"
  log "prompt: $PROMPT | candidates: $MINE_DIR/candidates.json | worktree: $WORKTREE"
  exit 0
fi

# ---- headless agent step ----------------------------------------------------
AGENT_OUT="$(mktemp)"
case "${CHRONICLE_AGENT:-opencode}" in
  opencode)
    (cd "$WORKTREE" && timeout 480 opencode run "$(cat "$PROMPT")") \
      > "$AGENT_OUT" 2>&1 || true
    ;;
  claude)
    # Same unattended wrapper the radars use (radar-common/lib.sh), so the
    # agent-step flags stay in exactly one place across the family.
    # shellcheck source=../../automation/radar-common/lib.sh
    source "$REPO_DIR/.agents/automation/radar-common/lib.sh"
    radar_common_run_agent "$WORKTREE" "$(cat "$PROMPT")" > "$AGENT_OUT" 2>&1 || true
    ;;
  *) die "unknown CHRONICLE_AGENT '$CHRONICLE_AGENT' (use opencode|claude)" ;;
esac

[[ "$(git -C "$WORKTREE" rev-parse HEAD)" == "$BASE" ]] && {
  log "agent made no commit ($(tail -c 200 "$AGENT_OUT" | tr '\n' ' ')), nothing to propose today"
  exit 0
}

# ---- push + PR --------------------------------------------------------------
git -C "$WORKTREE" push -u origin "$BRANCH" --quiet

PR_BODY="$(mktemp)"
{
  echo "Automated chronicle improve for $TODAY (card dotfiles-tsk-chronicle-daily-improve)."
  echo
  echo "## Evidence"
  echo "- Local mining report (chronicle.py, read-only):"
  echo
  echo '```'
  head -c 4000 "$MINE_DIR/mine.md"
  echo
  echo '```'
  for f in "$MINE_DIR"/brief-*.md; do
    [[ -f "$f" ]] && echo "- Radar brief used as research input: \`$(basename "$f")\`"
  done
  echo
  echo "## Self-enforced gates before merge"
  echo "1. changed paths only under \`.agents/skills/**\` or \`.agents/opencode/**\`"
  echo "2. PR MERGEABLE + CLEAN"
  echo "3. CI green (\`gh pr merge --auto --squash\`)"
  echo "4. first improve PR today"
  echo
  echo "## Fallback / revert (after merge)"
  echo '```'
  echo "git revert <squash-commit-sha>          # undo the landed improvement"
  echo "gh pr close <this-pr>                   # or reject before merge"
  echo '```'
} > "$PR_BODY"

PR_URL="$(gh pr create --repo "$REPO" --base main --head "$BRANCH" \
  --title "chronicle improve: $TODAY" --body-file "$PR_BODY")"
PR_NUMBER="${PR_URL##*/}"
echo "$TODAY" > "$STATE_DIR/last-pr"
log "opened $PR_URL (#$PR_NUMBER)"

# ---- gates 1 + 2, then gate 3 via --auto ------------------------------------
sleep 3 # let GitHub compute mergeability
FILES_OK=true
while IFS= read -r f; do
  [[ -z "$f" ]] && continue
  if ! [[ "$f" =~ $ALLOWLIST_RE ]]; then
    log "gate 1 FAILED: $f outside allowlist — leaving PR open for review"
    gh pr comment "$PR_NUMBER" --repo "$REPO" \
      --body "Gate 1 (path allowlist) failed: \`$f\`. Human review required; not auto-merging." \
      || true
    FILES_OK=false
    break
  fi
done < <(gh pr view "$PR_NUMBER" --repo "$REPO" --json files --jq '.files[].path')

STATE="$(gh pr view "$PR_NUMBER" --repo "$REPO" \
  --json mergeable,mergeStateStatus --jq '"\(.mergeable) \(.mergeStateStatus)"')"
if [[ "$FILES_OK" == "true" && "$STATE" == "MERGEABLE CLEAN" ]]; then
  log "gates 1+2 passed — enabling auto-merge (gate 3 = CI green, enforced by GitHub)"
  gh pr merge "$PR_NUMBER" --repo "$REPO" --auto --squash || {
    log "auto-merge not accepted (branch protection/reviews?) — PR left open for review"
  }
else
  log "gates not satisfied (state: $STATE) — PR left open for human review"
fi

log "done"
