#!/usr/bin/env bash
# Drift check for always-loaded "core blocks": a short instruction block that
# is inlined, byte for byte, into every harness entry file, between
#
#   <!-- NAME:CORE BEGIN -->
#   ...
#   <!-- NAME:CORE END -->
#
# (e.g. OUTPUT-FRAME:CORE, later AUTONOMY:CORE). One script for every such
# block — see tasks/plans/agent-output-tldr-format.md §6 "S4".
#
# Usage: scripts/check_core_blocks.sh [MARKER ...]
#   MARKER   a block name such as OUTPUT-FRAME or AUTONOMY (no ":CORE").
#   no args  auto-discover: every NAME that has a block in a tracked file or
#            a line in the manifest. A new block is covered without editing
#            this script (but see the manifest rule below).
#
# What counts as a block: a BEGIN/END marker line that is exactly the marker
# (trailing whitespace allowed) at the start of a line and NOT inside a
# fenced code block (``` or ~~~). Plans quote the block inside fences, so
# they're ignored by construction; tasks/plans/ and *.instructions.md are
# additionally excluded from discovery as a belt-and-braces measure.
#
# Checks, per marker:
#   - every file listed for it in scripts/core_blocks.manifest exists and has
#     the block (catches a MISSING copy, not just drift);
#   - every file that has the block is listed in the manifest (a copy nobody
#     knows about is a copy nobody will keep in sync);
#   - each file has exactly one BEGIN and one END, BEGIN first;
#   - the extracted blocks (markers included) are byte-identical; files that
#     differ from the majority are named and shown as a diff -u.
#   - explicitly asking for a marker that has neither blocks nor manifest
#     lines is an error (probably a typo); auto-discover mode just can't see it.
#
# Env: CORE_BLOCKS_MANIFEST overrides the manifest path (for tests).
# Exit 0 = every copy is present and identical. Exit 1 = read the FAIL lines.
set -uo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."
REPO_ROOT="$(pwd)"
MANIFEST="${CORE_BLOCKS_MANIFEST:-scripts/core_blocks.manifest}"

PASS=0
FAIL=0
ok()  { echo "  OK   $1"; PASS=$((PASS+1)); }
bad() { echo "  FAIL $1"; FAIL=$((FAIL+1)); }

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

NAME_RE='^[A-Z0-9][A-Z0-9_-]*$'

# Print "LINENO<TAB>BEGIN|END<TAB>NAME" for every unfenced marker line.
# POSIX awk only (mawk on ubuntu-latest): no {n,} intervals, no gawk-isms.
scan_file() {
  awk '
    function fence_len(s,   i, c, n) {
      i = 1
      while (i <= 3 && substr(s, i, 1) == " ") i++
      c = substr(s, i, 1)
      if (c != "`" && c != "~") return 0
      n = 0
      while (substr(s, i + n, 1) == c) n++
      if (n < 3) return 0
      FCH = c; REST = substr(s, i + n)
      return n
    }
    {
      line = $0
      sub(/\r$/, "", line)
      n = fence_len(line)
      if (infence) {
        if (n >= flen && FCH == fch && REST ~ /^[ \t]*$/) infence = 0
        next
      }
      if (n > 0) {
        # a backtick fence whose info string contains a backtick is not a fence
        if (!(FCH == "`" && REST ~ /`/)) { infence = 1; fch = FCH; flen = n }
        next
      }
      if (line ~ /^<!-- [A-Z0-9][A-Z0-9_-]*:CORE (BEGIN|END) -->[ \t]*$/) {
        name = line
        sub(/^<!-- /, "", name)
        sub(/:CORE .*$/, "", name)
        kind = (line ~ /:CORE BEGIN -->/) ? "BEGIN" : "END"
        print FNR "\t" kind "\t" name
      }
    }
  ' "$1"
}

# --- Manifest --------------------------------------------------------------
# MANIFEST_ROWS: "MARKER<TAB>path" in file order.
: > "$TMP/manifest"
if [[ -f "$MANIFEST" ]]; then
  lineno=0
  while IFS= read -r raw || [[ -n "$raw" ]]; do
    lineno=$((lineno+1))
    raw="${raw%%#*}"
    read -r m p extra <<< "$raw"
    [[ -z "${m:-}" ]] && continue
    if [[ -z "${p:-}" || -n "${extra:-}" || ! "$m" =~ $NAME_RE ]]; then
      bad "$MANIFEST:$lineno: malformed line (expected 'MARKER path')"
      continue
    fi
    printf '%s\t%s\n' "$m" "$p" >> "$TMP/manifest"
  done < "$MANIFEST"
else
  bad "manifest $MANIFEST not found — cannot detect missing copies"
fi

# --- Scan: tracked files with a marker, plus every manifest path on disk ----
: > "$TMP/scan"   # "path<TAB>lineno<TAB>kind<TAB>name"
{
  git -C "$REPO_ROOT" grep -l -E ':CORE (BEGIN|END) -->' -- . \
    ':(exclude)tasks/plans/' ':(exclude)*.instructions.md' 2>/dev/null || true
  cut -f2 "$TMP/manifest"
} | sort -u > "$TMP/candidates"

while IFS= read -r f; do
  [[ -z "$f" || ! -f "$f" ]] && continue
  scan_file "$f" | while IFS= read -r row; do printf '%s\t%s\n' "$f" "$row"; done >> "$TMP/scan"
done < "$TMP/candidates"

# --- Which markers to check -------------------------------------------------
EXPLICIT=0
if [[ $# -gt 0 ]]; then
  EXPLICIT=1
  markers=()
  for a in "$@"; do
    a="${a%:CORE}"   # tolerate "OUTPUT-FRAME:CORE"
    if [[ ! "$a" =~ $NAME_RE ]]; then
      bad "invalid marker name '$a' (expected e.g. OUTPUT-FRAME)"
      continue
    fi
    markers+=("$a")
  done
else
  mapfile -t markers < <( { cut -f4 "$TMP/scan"; cut -f1 "$TMP/manifest"; } | sed '/^$/d' | sort -u )
fi

echo "=== core-block drift check (root: $REPO_ROOT) ==="

if [[ ${#markers[@]} -eq 0 && $EXPLICIT -eq 0 ]]; then
  ok "no *:CORE blocks in tracked files and none in the manifest — nothing to check"
fi

for name in "${markers[@]}"; do
  echo "-- $name:CORE --"
  mapfile -t expected < <(awk -F'\t' -v n="$name" '$1 == n { print $2 }' "$TMP/manifest")
  mapfile -t found    < <(awk -F'\t' -v n="$name" '$4 == n { print $1 }' "$TMP/scan" | awk '!seen[$0]++')

  if [[ ${#expected[@]} -eq 0 && ${#found[@]} -eq 0 ]]; then
    bad "$name:CORE: no blocks found in tracked files and no manifest entries (typo, or not rolled out yet?)"
    continue
  fi

  # Order: manifest order first, then unlisted files.
  files=()
  declare -A listed=()
  for f in "${expected[@]}"; do listed["$f"]=1; files+=("$f"); done
  for f in "${found[@]}"; do [[ -z "${listed[$f]:-}" ]] && files+=("$f"); done

  good=()
  for f in "${files[@]}"; do
    if [[ -z "${listed[$f]:-}" ]]; then
      bad "$f has a $name:CORE block but isn't listed in $MANIFEST — add 'MARKER path' there (or remove the stray copy)"
    fi
    if [[ ! -f "$f" ]]; then
      bad "$f: listed for $name:CORE in $MANIFEST but the file doesn't exist"
      continue
    fi
    rows="$(awk -F'\t' -v n="$name" -v p="$f" '$4 == n && $1 == p { print $2 "\t" $3 }' "$TMP/scan")"
    if [[ -z "$rows" ]]; then
      bad "$f: missing its $name:CORE block (no unfenced '<!-- $name:CORE BEGIN -->' line)"
      continue
    fi
    nb="$(grep -c $'\tBEGIN$' <<< "$rows")"
    ne="$(grep -c $'\tEND$' <<< "$rows")"
    if [[ "$nb" -ne 1 || "$ne" -ne 1 ]]; then
      bad "$f: expected exactly one $name:CORE BEGIN and one END, found $nb BEGIN / $ne END"
      continue
    fi
    b="$(awk -F'\t' '$2 == "BEGIN" { print $1 }' <<< "$rows")"
    e="$(awk -F'\t' '$2 == "END"   { print $1 }' <<< "$rows")"
    if [[ "$b" -ge "$e" ]]; then
      bad "$f: $name:CORE END (line $e) comes before BEGIN (line $b)"
      continue
    fi
    out="$TMP/block.$name.${#good[@]}"
    sed -n "${b},${e}p" "$f" > "$out"
    printf '%s\t%s\n' "$(cksum < "$out" | tr ' ' '-')" "$f" >> "$TMP/hashes.$name"
    good+=("$f")
  done
  unset listed

  [[ ${#good[@]} -eq 0 ]] && continue

  # Majority block wins; ties go to the earliest file (manifest order).
  ref_hash="$(cut -f1 "$TMP/hashes.$name" | awk '{ c[$0]++; if (!($0 in o)) o[$0] = NR }
    END { for (h in c) if (c[h] > bc || (c[h] == bc && o[h] < bo)) { bh = h; bc = c[h]; bo = o[h] } print bh }')"
  ref_idx=-1; i=0
  while IFS=$'\t' read -r h f; do
    [[ "$h" == "$ref_hash" && $ref_idx -lt 0 ]] && ref_idx=$i && ref_file="$f"
    i=$((i+1))
  done < "$TMP/hashes.$name"

  ndiff=0; i=0
  while IFS=$'\t' read -r h f; do
    if [[ "$h" != "$ref_hash" ]]; then
      ndiff=$((ndiff+1))
      bad "$f: $name:CORE block differs from the majority copy (reference: $ref_file)"
      diff -u --label "$ref_file" --label "$f" "$TMP/block.$name.$ref_idx" "$TMP/block.$name.$i" | sed 's/^/         /'
    fi
    i=$((i+1))
  done < "$TMP/hashes.$name"

  if [[ $ndiff -eq 0 ]]; then
    ok "$name:CORE identical across ${#good[@]} file(s): ${good[*]}"
  fi
done

echo "=== $PASS passed, $FAIL failed ==="
[[ $FAIL -eq 0 ]] && echo "OK" && exit 0
echo "FAIL — fix the copies (or scripts/core_blocks.manifest) above. Block text: edit the canonical .agents/instructions/workspace-config/<name>.instructions.md first, then every copy identically."
exit 1
