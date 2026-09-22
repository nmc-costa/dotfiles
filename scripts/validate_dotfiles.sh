#!/usr/bin/env bash
# Evaluator: checks that ~/dotfiles is actually organized the way README.md
# and CLAUDE.md claim — clean root, key guideline docs present, and the
# directory tree in README.md matches the real filesystem. Also runs real
# functional smoke tests (not just structure): every *.sh syntax-checks,
# every relative markdown link resolves, and the two entrypoint scripts
# actually run cleanly in --dry-run mode.
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

# --- 0. No unresolved merge-conflict markers in tracked files -------------
# 2026-09-18: PR #12's merge commit committed literal <<<<<<</=======/>>>>>>>
# markers into README.md and nothing caught it until a human/agent noticed
# by eye. Only tracked files, so _templates/ placeholders and other
# untracked noise can't false-positive here.
echo "-- Conflict markers --"
conflict_hits="$(git grep -n -E '^(<<<<<<<|=======$|>>>>>>>)' -- . 2>/dev/null || true)"
if [[ -z "$conflict_hits" ]]; then
  ok "no unresolved merge-conflict markers in tracked files"
else
  while IFS= read -r line; do
    bad "conflict marker: $line"
  done <<< "$conflict_hits"
fi

# 2026-09-22: the check above only catches the marker lines themselves
# (<<<<<<< / ======= / >>>>>>>). Found in the wild: someone resolves a
# conflict by keeping content from both sides and deletes the ``` marker
# lines, but leaves the trailing ref-name fragment of the <<<<<<< HEAD /
# >>>>>>> origin/main lines behind as its own orphan line (" HEAD",
# " origin/main") — content on both sides intact, just this stray line
# sitting in the middle. README.md and the two _templates/*.md files each
# had 2-3 of these (found 2026-09-22, unrelated to the PR #12 incident
# above). Matches HEAD, origin/<branch>, and this repo's own claude/<topic>
# branch convention (see CLAUDE.md) — deliberately not a bare "^ \w+$" to
# avoid false-positives on legitimate single-word indented lines.
residue_hits="$(git grep -n -E '^ (HEAD|origin/[A-Za-z0-9._/-]+|claude/[A-Za-z0-9._/-]+|main|master)$' -- . 2>/dev/null || true)"
if [[ -z "$residue_hits" ]]; then
  ok "no orphaned merge-marker ref-name lines (' HEAD', ' origin/<branch>', ...)"
else
  while IFS= read -r line; do
    bad "orphaned merge-marker residue: $line"
  done <<< "$residue_hits"
fi

# --- 1. Root only has the allowed files/dirs ------------------------------
echo "-- Root cleanliness --"

ALLOWED_ROOT_FILES=(README.md CLAUDE.md AGENTS.md GEMINI.md CHEATSHEET.md HANDOFF.md \
  setup.sh sync.sh test-subagents.sh .gitignore)
ALLOWED_ROOT_DIRS=(.agents .chezmoisource .claude .github .vscode .gemini .codex .copilot docs scripts tasks .git global)

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

# --- 5. Syntax-check every shell script in the repo -----------------------
echo
echo "-- Shell syntax (bash -n) --"
if command -v git >/dev/null 2>&1 && git -C "$REPO_ROOT" rev-parse --git-dir >/dev/null 2>&1; then
  mapfile -t sh_files < <(git -C "$REPO_ROOT" ls-files '*.sh')
else
  mapfile -t sh_files < <(find "$REPO_ROOT" -name '*.sh' -not -path '*/.git/*' | sed "s#^$REPO_ROOT/##")
fi

if [[ ${#sh_files[@]} -eq 0 ]]; then
  bad "no *.sh files found to syntax-check (unexpected)"
else
  for f in "${sh_files[@]}"; do
    if bash -n "$REPO_ROOT/$f" 2>/tmp/validate_dotfiles_syntax_err; then
      ok "bash -n $f"
    else
      bad "bash -n $f — $(tr '\n' ' ' </tmp/validate_dotfiles_syntax_err)"
    fi
  done
  rm -f /tmp/validate_dotfiles_syntax_err
fi

# --- 6. Broken relative markdown links -------------------------------------
echo
echo "-- Relative markdown links --"
if command -v python3 >/dev/null 2>&1; then
  if command -v git >/dev/null 2>&1 && git -C "$REPO_ROOT" rev-parse --git-dir >/dev/null 2>&1; then
    mapfile -t md_files < <(git -C "$REPO_ROOT" ls-files '*.md')
  else
    mapfile -t md_files < <(find "$REPO_ROOT" -name '*.md' -not -path '*/.git/*' | sed "s#^$REPO_ROOT/##")
  fi

  link_report="$(REPO_ROOT="$REPO_ROOT" python3 - "${md_files[@]}" <<'PYEOF'
import os, re, sys

repo_root = os.environ["REPO_ROOT"]
md_files = sys.argv[1:]
link_re = re.compile(r'\]\(([^)]+)\)')
broken = []
checked = 0

for rel in md_files:
    full = os.path.join(repo_root, rel)
    try:
        with open(full, encoding="utf-8", errors="replace") as fh:
            lines = fh.readlines()
    except OSError:
        continue
    # Resolve symlinks (e.g. .github/CONTRIBUTING.md -> ../.agents/CONTRIBUTING.md)
    # so relative links are checked against the file's real physical directory,
    # not the directory of the symlink that points at it.
    link_dir = os.path.dirname(os.path.realpath(full))
    in_fence = False
    for lineno, line in enumerate(lines, start=1):
        if line.lstrip().startswith('```'):
            in_fence = not in_fence
            continue
        if in_fence:
            # Skip links inside fenced code blocks — these are usually
            # illustrative examples/templates (e.g. "{skill-name}"
            # placeholders), not real links to check.
            continue
        for m in link_re.finditer(line):
            target = m.group(1).strip()
            if not target:
                continue
            # drop an optional "title" after a space, and surrounding <>
            target = target.split(' ', 1)[0].strip('<>')
            if not target:
                continue
            if target.startswith(('http://', 'https://', 'mailto:', '#')):
                continue
            if target.startswith('//'):
                continue
            # strip in-page anchor from a path#anchor link
            path_part = target.split('#', 1)[0]
            if not path_part:
                continue
            checked += 1
            resolved = os.path.normpath(os.path.join(link_dir, path_part))
            if not os.path.exists(resolved):
                broken.append(f"{rel}:{lineno}: broken link '{target}' -> resolves to {os.path.relpath(resolved, repo_root)}")

print(f"CHECKED={checked}")
for b in broken:
    print(f"BROKEN={b}")
PYEOF
)"

  checked_count="$(grep -c '^CHECKED=' <<<"$link_report" | head -1)"
  checked_n="$(grep '^CHECKED=' <<<"$link_report" | cut -d= -f2)"
  broken_lines="$(grep '^BROKEN=' <<<"$link_report" | sed 's/^BROKEN=//')"

  if [[ -z "$broken_lines" ]]; then
    ok "all relative markdown links resolve (${checked_n:-0} links checked across ${#md_files[@]} tracked .md files)"
  else
    while IFS= read -r line; do
      [[ -z "$line" ]] && continue
      bad "markdown link: $line"
    done <<<"$broken_lines"
  fi
else
  bad "python3 not available — cannot run the markdown link checker"
fi

# --- 7. Dry-run smoke test of the entrypoint scripts ------------------------
echo
echo "-- Dry-run smoke test --"
if [[ -x "$REPO_ROOT/setup.sh" || -f "$REPO_ROOT/setup.sh" ]]; then
  setup_out="$(bash "$REPO_ROOT/setup.sh" --dry-run 2>&1)"
  setup_rc=$?
  if [[ $setup_rc -eq 0 ]]; then
    ok "./setup.sh --dry-run exits 0"
  else
    bad "./setup.sh --dry-run exited $setup_rc: $(tr '\n' ' ' <<<"$setup_out")"
  fi
else
  bad "setup.sh not found"
fi

if [[ -x "$REPO_ROOT/sync.sh" || -f "$REPO_ROOT/sync.sh" ]]; then
  sync_out="$(bash "$REPO_ROOT/sync.sh" --dry-run 2>&1)"
  sync_rc=$?
  if [[ $sync_rc -eq 0 ]]; then
    ok "./sync.sh --dry-run exits 0"
  else
    bad "./sync.sh --dry-run exited $sync_rc: $(tr '\n' ' ' <<<"$sync_out")"
  fi
else
  bad "sync.sh not found"
fi

# --- 6. Workspace standards config is itself valid --------------------------
echo
echo "-- Workspace standards config --"
if [[ -f "$REPO_ROOT/.agents/instructions/workspace-config/standards/workspace-standards.yaml" ]]; then
  if python3 "$REPO_ROOT/scripts/validate_workspace_standards.py" \
      "$REPO_ROOT/.agents/instructions/workspace-config/standards/workspace-standards.yaml" --quiet >/tmp/validate_ws_standards.$$ 2>&1; then
    ok ".agents/instructions/workspace-config/standards/workspace-standards.yaml passes its own schema checks"
  else
    bad ".agents/instructions/workspace-config/standards/workspace-standards.yaml: $(tr '\n' ' ' </tmp/validate_ws_standards.$$)"
  fi
  rm -f /tmp/validate_ws_standards.$$
else
  bad ".agents/instructions/workspace-config/standards/workspace-standards.yaml not found"
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
