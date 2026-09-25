#!/bin/bash
# radar-common/validate_pipeline.sh — end-to-end validation of a radar's
# run.sh pipeline in a disposable sandbox. NO network, NO LLM, NO real
# state, NO real repo: builds a throwaway git repo + state dir, replaces
# collect.sh with a fixture writer and the nested backend with a stub
# `opencode`, then asserts the OUTPUT contract of each failure/success
# mode. Exit 0 = every assertion passed.
#
#   validate_pipeline.sh <radar-name>     e.g. omarchy-radar
#
# Covered scenarios (each in a fresh sandbox):
#   1. happy full-auto        — stub backend writes a valid brief+ranked
#   2. secret-scan abort      — brief contains a fake AWS key
#   3. agent-step failure     — stub exits 1 (discard-failed-attempt)
#   4. empty inbox            — "nothing new", no branch, exit 0
#   5. interactive prepare/finalize — the calling-harness-as-agent path
#
# The RADAR_STATE_DIR / RADAR_DATE env hooks in run.sh are what make this
# possible; they must stay backward-compatible defaults.

set -uo pipefail

SCRIPT_DIR="$(cd -P -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
LIB_SRC="$SCRIPT_DIR/lib.sh"
FIXTURE_DATE="2026-01-15"
INBOX_ITEMS=3

RADAR="${1:-}"
[[ -n "$RADAR" ]] || { echo "usage: validate_pipeline.sh <radar-name>" >&2; exit 2; }

SKILL_SRC="$(cd -P -- "$SCRIPT_DIR/../../skills/$RADAR" 2>/dev/null && pwd)"
[[ -d "$SKILL_SRC" ]] || { echo "validate_pipeline.sh: no skill dir for '$RADAR' under .agents/skills/" >&2; exit 2; }
[[ -f "$SKILL_SRC/scripts/run.sh" ]] || { echo "validate_pipeline.sh: $RADAR has no scripts/run.sh" >&2; exit 2; }

PASS=0
FAIL=0
if [[ -n "${RADAR_VALIDATE_KEEP:-}" ]]; then
  # Debug mode: keep the sandbox for post-mortem (run.out lives in each
  # scenario dir). RADAR_VALIDATE_KEEP=/some/dir ./validate_pipeline.sh ...
  SANDBOX="$RADAR_VALIDATE_KEEP"
  rm -rf -- "$SANDBOX"; mkdir -p "$SANDBOX"
else
  SANDBOX="$(mktemp -d /tmp/radar-validate.XXXXXX)"
  trap 'rm -rf -- "$SANDBOX"' EXIT
fi

ok()   { echo "  ok: $1"; PASS=$((PASS + 1)); }
bad()  { echo "  FAIL: $1"; FAIL=$((FAIL + 1)); }
check() { # check <label> <cmd...>
  local label="$1"; shift
  if "$@" >/dev/null 2>&1; then ok "$label"; else bad "$label"; fi
}
check_neg() { # check_neg <label> <cmd...>  — the command MUST fail
  local label="$1"; shift
  if "$@" >/dev/null 2>&1; then bad "$label"; else ok "$label"; fi
}
expect_eq() { # expect_eq <label> <want> <got>
  if [[ "$2" == "$3" ]]; then ok "$1"; else bad "$1 (want '$2', got '$3')"; fi
}

fixture_inbox() { # fixture_inbox <collect-script-path> <empty:0|1>
  local collect="$1" empty="$2"
  if [[ "$empty" == "1" ]]; then
    cat > "$collect" <<'SH'
#!/bin/bash
mkdir -p "${RADAR_STATE_DIR:?}/inbox/${RADAR_DATE:?}"
printf '{"categories":{}}' > "${RADAR_STATE_DIR:?}/inbox/${RADAR_DATE:?}.json"
printf '{"news":{"cursor":"test"}}' > "${RADAR_STATE_DIR:?}/seen.json.pending"
SH
  else
    cat > "$collect" <<SH
#!/bin/bash
mkdir -p "\${RADAR_STATE_DIR:?}/inbox/\${RADAR_DATE:?}"
cat > "\${RADAR_STATE_DIR:?}/inbox/\${RADAR_DATE:?}.json" <<'JSON'
{"generated_at":"${FIXTURE_DATE}T00:00:00Z","categories":{"news":[
 {"title":"Item one","url":"https://example.com/1"},
 {"title":"Item two","url":"https://example.com/2"},
 {"title":"Item three","url":"https://example.com/3"}]}}
JSON
cat > "\${RADAR_STATE_DIR:?}/seen.json.pending" <<'JSON'
{"news":{"cursor":"test"}}
JSON
SH
  fi
  chmod +x "$collect"
}

write_opencode_stub() { # write_opencode_stub <bin-dir> <mode: happy|secret|fail>
  local bin="$1" mode="$2"
  mkdir -p "$bin"
  # Suppress notifications during tests (herdr reports "shown" so
  # radar_notify never reaches notify-send).
  printf '#!/bin/bash\necho '"'"'{"result":{"shown":true}}'"'"'\n' > "$bin/herdr"
  chmod +x "$bin/herdr"
  cat > "$bin/opencode" <<STUB
#!/bin/bash
cat > /dev/null   # consume the piped prompt
BR="briefs/$RADAR-$FIXTURE_DATE"
case "$mode" in
  fail) exit 1 ;;
  happy|secret)
    mkdir -p briefs
    {
      echo "# $RADAR brief (stub)"
      echo
      if [[ "$mode" == "secret" ]]; then
        echo "leak test: AKIAIOSFODNN7EXAMPLE"
      else
        echo "scored all three items; two picked"
      fi
    } > "\$BR.md"
    cat > "\$BR.ranked.json" <<'JSON'
[{"title":"Item one","url":"https://example.com/1","category":"news","score":5,"rationale":"r","picked_top3":true},
 {"title":"Item two","url":"https://example.com/2","category":"news","score":4,"rationale":"r","picked_top3":true},
 {"title":"Item three","url":"https://example.com/3","category":"news","score":1,"rationale":"r","picked_top3":false}]
JSON
    ;;
esac
STUB
  chmod +x "$bin/opencode"
}

build_sandbox() { # build_sandbox <scenario-dir> <empty-inbox:0|1>
  local dir="$1" empty="$2"
  local repo="$dir/repo"
  local skill="$repo/.agents/skills/$RADAR"
  mkdir -p "$repo/.agents/automation/radar-common" "$skill/scripts" "$dir/state" "$dir/bin"
  cp "$LIB_SRC" "$repo/.agents/automation/radar-common/lib.sh"
  cp "$SKILL_SRC/scripts/run.sh" "$skill/scripts/run.sh"
  echo "fake skill doc" > "$skill/SKILL.md"
  echo "fake rubric" > "$skill/ranking.md"
  echo "fake security doc" > "$skill/security.md"
  fixture_inbox "$skill/scripts/collect.sh" "$empty"
  ( cd "$repo" && git init -q -b main && git config user.email t@t && git config user.name t \
    && git add -A && git commit -qm init )
  echo "$repo"
}

run_pipeline() { # run_pipeline <repo> <scenario-dir> <mode> [args...]
  local repo="$1" dir="$2" mode="$3"; shift 3
  write_opencode_stub "$dir/bin" "$mode"
  ( cd "$repo" \
    && PATH="$dir/bin:$PATH" \
       RADAR_STATE_DIR="$dir/state" \
       RADAR_DATE="$FIXTURE_DATE" \
       "$repo/.agents/skills/$RADAR/scripts/run.sh" "$@" ) > "$dir/run.out" 2>&1
}

echo "radar pipeline validation: $RADAR (fixtures @ $FIXTURE_DATE, sandbox $SANDBOX)"

# --- Scenario 1: happy full-auto -------------------------------------------
S="$SANDBOX/s1"; mkdir -p "$S"
REPO=$(build_sandbox "$S" 0)
run_pipeline "$REPO" "$S" happy full; RC=$?
BRANCH="radar/$RADAR/$FIXTURE_DATE"
expect_eq "s1 full-auto exit code" 0 "$RC"
check  "s1 branch $BRANCH exists"       git -C "$REPO" show-ref --verify --quiet "refs/heads/$BRANCH"
expect_eq "s1 exactly one commit on branch" 1 "$(git -C "$REPO" rev-list --count "main..$BRANCH" 2>/dev/null)"
expect_eq "s1 commit touches only its own brief files" \
  "briefs/$RADAR-$FIXTURE_DATE.md briefs/$RADAR-$FIXTURE_DATE.ranked.json" \
  "$(git -C "$REPO" diff --name-only "main" "$BRANCH" | sort | tr '\n' ' ' | sed 's/ $//')"
check  "s1 worktree removed after success" test ! -e "$S/state/worktrees/$FIXTURE_DATE"
check  "s1 seen.json promoted"          test -f "$S/state/seen.json"
check  "s1 no pending left"             test ! -e "$S/state/seen.json.pending"
# cross-check: every inbox title appears in the committed ranked.json
# (the worktree is gone after success, so read it from the branch commit)
IN_TITLES=$(jq -r '[.categories.news[].title] | sort | join("|")' "$S/state/inbox/$FIXTURE_DATE.json")
RANK_TITLES=$(git -C "$REPO" show "$BRANCH:briefs/$RADAR-$FIXTURE_DATE.ranked.json" | jq -r '[.[].title] | sort | join("|")')
expect_eq "s1 ranked titles == inbox titles" "$IN_TITLES" "$RANK_TITLES"
expect_eq "s1 ranked.json entry count == inbox count" "$INBOX_ITEMS" \
  "$(git -C "$REPO" show "$BRANCH:briefs/$RADAR-$FIXTURE_DATE.ranked.json" | jq 'length')"
check  "s1 brief non-empty"             test -n "$(git -C "$REPO" show "$BRANCH:briefs/$RADAR-$FIXTURE_DATE.md")"

# --- Scenario 2: secret-scan aborts the commit -----------------------------
S="$SANDBOX/s2"; mkdir -p "$S"
REPO=$(build_sandbox "$S" 0)
run_pipeline "$REPO" "$S" secret full; RC=$?
check  "s2 run exits non-zero on secret hit" test "$RC" -ne 0
# Deliberate contract: on a secret hit BOTH worktree and branch stay put —
# the day stays blocked until a human inspects and cleans up (the alert
# notification is what makes this visible, never a silent skip). Verified
# live: `git branch -D` cannot delete a branch checked out in the kept
# worktree, so the block is structural, not best-effort.
check  "s2 branch KEPT (day blocked until human inspection)" \
       git -C "$REPO" show-ref --verify --quiet "refs/heads/$BRANCH"
check  "s2 worktree KEPT for inspection" test -d "$S/state/worktrees/$FIXTURE_DATE"
check_neg "s2 seen.json NOT promoted"   test -e "$S/state/seen.json"

# --- Scenario 3: agent-step failure discards the attempt --------------------
S="$SANDBOX/s3"; mkdir -p "$S"
REPO=$(build_sandbox "$S" 0)
run_pipeline "$REPO" "$S" fail full; RC=$?
check  "s3 run exits non-zero when backend fails" test "$RC" -ne 0
check_neg "s3 branch discarded"         git -C "$REPO" show-ref --verify --quiet "refs/heads/$BRANCH"
check  "s3 worktree discarded"          test ! -e "$S/state/worktrees/$FIXTURE_DATE"
check  "s3 agent output kept in state"  test -f "$S/state/last-agent-output.json"

# --- Scenario 4: empty inbox skips everything -------------------------------
S="$SANDBOX/s4"; mkdir -p "$S"
REPO=$(build_sandbox "$S" 1)
run_pipeline "$REPO" "$S" happy full; RC=$?
expect_eq "s4 empty-inbox exit code" 0 "$RC"
check_neg "s4 no branch created"        git -C "$REPO" show-ref --verify --quiet "refs/heads/$BRANCH"
grep -q "nothing new today" "$S/run.out" \
  && ok "s4 output says nothing new" || bad "s4 output says nothing new"

# --- Scenario 5: interactive --prepare / --finalize -------------------------
S="$SANDBOX/s5"; mkdir -p "$S"
REPO=$(build_sandbox "$S" 0)
run_pipeline "$REPO" "$S" happy --prepare; RC=$?
expect_eq "s5 --prepare exit code" 0 "$RC"
check  "s5 prompt file written"         test -s "$S/state/prompt-$FIXTURE_DATE.md"
check  "s5 worktree present"            test -d "$S/state/worktrees/$FIXTURE_DATE"
expect_eq "s5 branch has zero commits after prepare" 0 \
  "$(git -C "$REPO" rev-list --count "main..$BRANCH" 2>/dev/null)"
# The calling harness IS the agent step: write the brief like it would.
WT="$S/state/worktrees/$FIXTURE_DATE"
mkdir -p "$WT/briefs"
printf '# brief by the calling harness\n' > "$WT/briefs/$RADAR-$FIXTURE_DATE.md"
printf '[{"title":"Item one","url":"https://example.com/1","category":"news","score":5,"rationale":"r","picked_top3":true},{"title":"Item two","url":"https://example.com/2","category":"news","score":4,"rationale":"r","picked_top3":true},{"title":"Item three","url":"https://example.com/3","category":"news","score":1,"rationale":"r","picked_top3":false}]' > "$WT/briefs/$RADAR-$FIXTURE_DATE.ranked.json"
run_pipeline "$REPO" "$S" happy --finalize; RC=$?
expect_eq "s5 --finalize exit code" 0 "$RC"
expect_eq "s5 exactly one commit after finalize" 1 "$(git -C "$REPO" rev-list --count "main..$BRANCH" 2>/dev/null)"
check  "s5 worktree removed after finalize" test ! -e "$WT"
check  "s5 seen.json promoted"          test -f "$S/state/seen.json"

echo
echo "results: $PASS passed, $FAIL failed"
if (( FAIL > 0 )); then
  echo "VALIDATION FAILED for $RADAR"
  exit 1
fi
echo "VALIDATION PASSED for $RADAR"
