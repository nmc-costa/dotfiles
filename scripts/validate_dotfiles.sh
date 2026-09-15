#!/usr/bin/env bash
# Evaluator: checks that ~/dotfiles is actually organized the way README.md
# and CLAUDE.md claim — clean root, key guideline docs present, and the
# directory tree in README.md matches the real filesystem.
#
# Exit 0 = repo is in the state a human or an agent can rely on.
# Exit 1 = something in here is lying; read the FAIL lines above the summary.
set -uo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."
REPO_ROOT="$(pwd)"

PASS=0
FAIL=0

ok()   { echo "  OK   $1"; PASS=$((PASS+1)); }
bad()  { echo "  FAIL $1"; FAIL=$((FAIL+1)); }

echo "=== dotfiles validator (root: $REPO_ROOT) ==="
echo

# --- 1. Root only has the allowed files/dirs ------------------------------
echo "-- Root cleanliness --"

ALLOWED_ROOT_FILES=(README.md CLAUDE.md AGENTS.md GEMINI.md CHEATSHEET.md \
  setup.sh sync-skills.sh test-subagents.sh .gitignore)
ALLOWED_ROOT_DIRS=(.agents .chezmoisource .claude .github .vscode docs scripts .git)

unexpected=0
while IFS= read -r entry; do
  name="$(basename "$entry")"
  if [[ -d "$entry" ]]; then
    match=0
    for d in "${ALLOWED_ROOT_DIRS[@]}"; do [[ "$name" == "$d" ]] && match=1; done
    if [[ $match -eq 0 ]]; then
      bad "unexpected root directory: $name (move contents into docs/ or an existing dir, or add it to ALLOWED_ROOT_DIRS in this script if it's a deliberate new top-level area)"
      unexpected=1
    fi
  else
    match=0
    for f in "${ALLOWED_ROOT_FILES[@]}"; do [[ "$name" == "$f" ]] && match=1; done
    if [[ $match -eq 0 ]]; then
      bad "unexpected root file: $name (belongs in docs/, or add it to ALLOWED_ROOT_FILES in this script if it's genuinely meant to live at root)"
      unexpected=1
    fi
  fi
done < <(find . -maxdepth 1 -mindepth 1 -not -name '.git')

[[ $unexpected -eq 0 ]] && ok "root has no unexpected files or directories"

# --- 2. Required guideline docs exist and are non-empty -------------------
echo
echo "-- Required docs --"
for f in README.md CLAUDE.md AGENTS.md CHEATSHEET.md; do
  if [[ -s "$f" ]]; then
    ok "$f exists and is non-empty"
  else
    bad "$f missing or empty"
  fi
done

if [[ -d docs ]] && [[ -n "$(ls -A docs 2>/dev/null)" ]]; then
  ok "docs/ exists and is non-empty"
else
  bad "docs/ missing or empty"
fi

# --- 3. README.md documents guidelines for both audiences -----------------
echo
echo "-- Guidelines for both audiences --"
if grep -q '### For you (human)' README.md 2>/dev/null; then
  ok "README.md has a human-facing guidelines section"
else
  bad "README.md is missing a '### For you (human)' guidelines section"
fi
if grep -qE '### For agents' README.md 2>/dev/null; then
  ok "README.md has an agent-facing guidelines section"
else
  bad "README.md is missing a '### For agents' guidelines section"
fi

# --- 4. README.md's declared directory tree matches the real filesystem ---
echo
echo "-- Directory tree accuracy (README.md vs. disk) --"
if [[ ! -f README.md ]]; then
  bad "no README.md to check a tree against"
else
  # Pull top-level entries out of the fenced tree block (lines like
  # "├── name/  # comment" or "└── name" with NO leading "│", i.e. depth 0).
  declared="$(awk '
    /^```/ { in_block = !in_block; next }
    in_block && /^(├── |└── )/ {
      line=$0
      sub(/^(├── |└── )/, "", line)
      sub(/[[:space:]]+#.*$/, "", line)
      sub(/\/$/, "", line)
      print line
    }
  ' README.md)"

  if [[ -z "$declared" ]]; then
    bad "could not find a top-level directory tree block in README.md (expected a fenced \`\`\` block with ├──/└── lines)"
  else
    tree_bad=0
    while IFS= read -r name; do
      [[ -z "$name" ]] && continue
      if [[ ! -e "$name" ]]; then
        bad "README.md tree claims '$name' exists at root, but it doesn't"
        tree_bad=1
      fi
    done <<< "$declared"
    [[ $tree_bad -eq 0 ]] && ok "every top-level path declared in README.md's tree exists on disk"

    # Reverse check: every allowed root entry should be mentioned somewhere in the tree.
    missing_from_tree=0
    while IFS= read -r entry; do
      name="$(basename "$entry")"
      if ! grep -q "$name" <<< "$declared"; then
        bad "'$name' exists at root but isn't in README.md's declared tree"
        missing_from_tree=1
      fi
    done < <(find . -maxdepth 1 -mindepth 1 -not -name '.git')
    [[ $missing_from_tree -eq 0 ]] && ok "every root entry on disk is mentioned in README.md's tree"
  fi
fi

# --- Summary ----------------------------------------------------------------
echo
echo "=== $PASS passed, $FAIL failed ==="
if [[ $FAIL -eq 0 ]]; then
  echo "dotfiles is organized and ready to use."
  exit 0
else
  echo "Fix the FAIL lines above, then re-run."
  exit 1
fi
