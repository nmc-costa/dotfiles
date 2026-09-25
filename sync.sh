#!/usr/bin/env bash
set -euo pipefail

# Sync ALL of dotfiles/.agents/<subdir>/ (skills, instructions, harnesses,
# prompts, workflows, validation, automation, providers — whatever subdirs
# exist) to the locations other harnesses/tools read on this machine.
#
# Kept the name `sync.sh` for backwards compatibility with existing
# docs/muscle memory (this repo's README/CLAUDE.md/AGENTS.md/CHEATSHEET.md
# all reference it by this name) even though it now syncs more than skills —
# 2026-09-15, requested explicitly ("o sync tem de ser global e para tudo").
#
# 2026-09-17: rewritten from a destructive `rm -rf dest; cp -r src dest`
# mirror to a per-file, manifest-based reconciliation (source vs. a
# last-known-synced baseline vs. the destination now) so a file created
# LOCALLY at the destination (e.g. dtx-providers-tui's `add-provider`
# writing into the installed ~/.agents/providers/registry/) is never
# silently deleted, and a file that diverged on BOTH sides is flagged as a
# conflict instead of one side winning blindly. See
# .agents/harnesses/PROVIDERS.md and the design discussion in this repo's
# PR history for the decision table this implements.
#
# Usage: ./sync.sh [--dry-run] [--system] [--verbose] [--non-interactive]
#                   [--resolve=source|dest|both|skip] [--force-source]
#                   [--strict] [--adopt=source] [--respect-deletes] [--pull]
#   --system            also sync skills/ (only) to the Omarchy system-wide
#                        location (requires sudo) — other .agents/ subdirs
#                        have no established system-wide convention.
#   --non-interactive    never prompt (used by the systemd timer); conflicts
#                        are left untouched and reported, exit code 3.
#   --resolve=X          auto-resolve every conflict this run the same way:
#                        source (take incoming), dest (keep local), both
#                        (keep local, drop incoming as .incoming-<sha>),
#                        skip (same as leaving it untouched).
#   --force-source       old behavior: source always wins, but the dest is
#                        backed up first (~/.local/state/dtx-sync/backups/).
#   --strict             a first-run/no-baseline divergence (see table)
#                        becomes a hard failure instead of a warning.
#   --adopt=source       first-run/no-baseline divergences take the source
#                        instead of keeping the destination.
#   --respect-deletes    a file removed at the destination since the last
#                        sync is NOT re-copied from source.
#   --pull               copy local-only / locally-edited destination files
#                        back into the dotfiles source, ready to `git add`.

DRY_RUN=0
SYNC_SYSTEM=0
VERBOSE=0
NON_INTERACTIVE=0
RESOLVE=""
FORCE_SOURCE=0
STRICT=0
ADOPT_SOURCE=0
RESPECT_DELETES=0
PULL=0
BASE_DIR="${BASE_DIR:-$HOME}"

for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=1 ;;
    --system) SYNC_SYSTEM=1 ;;
    --verbose) VERBOSE=1 ;;
    --non-interactive) NON_INTERACTIVE=1 ;;
    --resolve=*) RESOLVE="${arg#--resolve=}" ;;
    --force-source) FORCE_SOURCE=1 ;;
    --strict) STRICT=1 ;;
    --adopt=source) ADOPT_SOURCE=1 ;;
    --respect-deletes) RESPECT_DELETES=1 ;;
    --pull) PULL=1 ;;
  esac
done

AGENTS_SRC="$BASE_DIR/dotfiles/.agents"
AGENTS_DEST="$BASE_DIR/.agents"
CLAUDE_SKILLS="$BASE_DIR/.claude/skills"
CLAUDE_HOOKS="$BASE_DIR/.claude/hooks"
SYSTEM_SKILLS="/usr/share/omarchy/default/agents/skills"
LOCAL_BIN="$BASE_DIR/.local/bin"

STATE_DIR="${XDG_STATE_HOME:-$BASE_DIR/.local/state}/dtx-sync"
MANIFEST_PATH="$STATE_DIR/manifest.json"
BACKUP_DIR="$STATE_DIR/backups/$(date -u +%Y%m%dT%H%M%SZ)"

MANIFEST_JSON='{"version":1,"targets":{}}'
CONFLICT_COUNT=0
CONFLICT_SUMMARY=()

log() {
  if [[ $VERBOSE -eq 1 ]]; then
    echo "[sync] $*"
  fi
}

error() {
  echo "[ERROR] $*" >&2
}

sync_is_interactive() {
  (( NON_INTERACTIVE == 0 )) && [[ -t 0 && -t 1 && -z ${INVOCATION_ID:-} && -z ${CI:-} ]]
}

sync_load_manifest() {
  if [[ -f $MANIFEST_PATH ]] && MANIFEST_JSON=$(jq -c '.' "$MANIFEST_PATH" 2>/dev/null); then
    return 0
  fi
  MANIFEST_JSON='{"version":1,"targets":{}}'
}

sync_save_manifest() {
  (( DRY_RUN )) && return 0
  mkdir -p "$STATE_DIR"
  local tmp
  tmp=$(mktemp "$STATE_DIR/manifest.json.XXXXXX")
  printf '%s' "$MANIFEST_JSON" | jq '.' >"$tmp"
  mv "$tmp" "$MANIFEST_PATH"
}

sync_hash() {
  sha256sum "$1" | cut -d' ' -f1
}

sync_mode() {
  stat -c '%a' "$1"
}

# Reads target.files[path].hash / .mode from the in-memory manifest.
sync_manifest_hash() {
  jq -r --arg t "$1" --arg p "$2" '.targets[$t].files[$p].hash // empty' <<<"$MANIFEST_JSON"
}

sync_manifest_set() {
  local target="$1" path="$2" hash="$3" mode="$4"
  MANIFEST_JSON=$(jq --arg t "$target" --arg p "$path" --arg h "$hash" --arg m "$mode" \
    '.targets[$t].files[$p] = {hash: $h, mode: $m}' <<<"$MANIFEST_JSON")
}

sync_manifest_unset() {
  local target="$1" path="$2"
  MANIFEST_JSON=$(jq --arg t "$target" --arg p "$path" 'del(.targets[$t].files[$p])' <<<"$MANIFEST_JSON")
}

sync_backup() {
  local dfile="$1" target_name="$2" relpath="$3"
  (( DRY_RUN )) && return 0
  local out="$BACKUP_DIR/$target_name/$relpath"
  mkdir -p "$(dirname "$out")"
  cp "$dfile" "$out"
}

# List of relative paths under $src that count as "the source" for this
# subdir. skills/ additionally requires SKILL.md in each top-level folder
# (unchanged rule from before this rewrite) — everything else is unfiltered.
sync_source_paths() {
  local subdir_name="$1" src="$2"
  if [[ $subdir_name == skills ]]; then
    local skill_dir
    while IFS= read -r -d '' skill_dir; do
      if [[ -f "$skill_dir/SKILL.md" ]]; then
        find "$skill_dir" -type f -printf '%P\n' | sed "s#^#$(basename "$skill_dir")/#"
      else
        log "skip: $(basename "$skill_dir") (missing SKILL.md)"
      fi
    done < <(find "$src" -mindepth 1 -maxdepth 1 -type d -print0)
  else
    find "$src" -type f -printf '%P\n'
  fi
}

sync_dest_paths() {
  local dest="$1"
  [[ -d $dest ]] && find "$dest" -type f -printf '%P\n' || true
}

# Applies the actual file operation for one relpath, given the decided
# outcome. Never called for CONFLICT outcomes directly -- those go through
# sync_handle_conflict first.
sync_write_from_source() {
  local sfile="$1" dfile="$2" target="$3" relpath="$4"
  (( DRY_RUN )) && { log "(dry-run) would write $dfile from $sfile"; return 0; }
  mkdir -p "$(dirname "$dfile")"
  cp "$sfile" "$dfile"
  sync_manifest_set "$target" "$relpath" "$(sync_hash "$sfile")" "$(sync_mode "$sfile")"
}

sync_delete_dest() {
  local dfile="$1" target="$2" relpath="$3"
  (( DRY_RUN )) && { log "(dry-run) would remove $dfile"; return 0; }
  rm -f "$dfile"
  sync_manifest_unset "$target" "$relpath"
}

sync_pull_to_source() {
  local sfile="$1" dfile="$2" target="$3" relpath="$4"
  (( DRY_RUN )) && { log "(dry-run) would pull $dfile -> $sfile"; return 0; }
  mkdir -p "$(dirname "$sfile")"
  cp "$dfile" "$sfile"
  sync_manifest_set "$target" "$relpath" "$(sync_hash "$dfile")" "$(sync_mode "$dfile")"
  echo "  pulled: $relpath -> $sfile"
}

sync_handle_conflict() {
  local sfile="$1" dfile="$2" target="$3" relpath="$4" location_name="$5"
  CONFLICT_COUNT=$((CONFLICT_COUNT + 1))

  if (( DRY_RUN )); then
    CONFLICT_SUMMARY+=("$location_name: $relpath (would conflict -- changed both in dotfiles and at the destination)")
    return 0
  fi

  local resolve="$RESOLVE"

  if [[ -z $resolve ]]; then
    if sync_is_interactive; then
      echo ""
      echo "CONFLICT in $location_name: $relpath (changed both in dotfiles and at the destination)"
      resolve=$(printf 'source\ndest\nboth\nview diff\nskip\n' | gum choose --header "Resolve $relpath") || resolve="skip"
      if [[ $resolve == "view diff" ]]; then
        diff -u "$dfile" "$sfile" || true
        resolve=$(printf 'source\ndest\nboth\nskip\n' | gum choose --header "Resolve $relpath") || resolve="skip"
      fi
    else
      # Non-interactive with no --resolve=: never touch the conflicting
      # file, drop the incoming version beside it instead of silently
      # picking a side.
      resolve="both"
    fi
  fi

  case "$resolve" in
  source)
    sync_backup "$dfile" "$(basename "$target")" "$relpath"
    sync_write_from_source "$sfile" "$dfile" "$target" "$relpath"
    ;;
  dest)
    sync_manifest_set "$target" "$relpath" "$(sync_hash "$dfile")" "$(sync_mode "$dfile")"
    ;;
  both)
    (( DRY_RUN )) || cp "$sfile" "$dfile.incoming-$(sync_hash "$sfile" | cut -c1-8)"
    CONFLICT_SUMMARY+=("$location_name: $relpath (kept local, incoming dropped beside it as .incoming-*)")
    ;;
  *)
    CONFLICT_SUMMARY+=("$location_name: $relpath")
    ;;
  esac
}

# The core per-file decision table. See .agents/harnesses/PROVIDERS.md /
# the PR description for the full table this implements.
sync_reconcile_file() {
  local subdir_name="$1" src="$2" dest="$3" target="$4" relpath="$5" location_name="$6"
  local sfile="$src/$relpath" dfile="$dest/$relpath"
  local s_hash="" d_hash="" m_hash=""
  [[ -f $sfile ]] && s_hash=$(sync_hash "$sfile")
  [[ -f $dfile ]] && d_hash=$(sync_hash "$dfile")
  m_hash=$(sync_manifest_hash "$target" "$relpath")

  if (( FORCE_SOURCE )); then
    if [[ -n $s_hash ]]; then
      [[ -n $d_hash && $d_hash != "$s_hash" ]] && sync_backup "$dfile" "$(basename "$target")" "$relpath"
      sync_write_from_source "$sfile" "$dfile" "$target" "$relpath"
    else
      sync_delete_dest "$dfile" "$target" "$relpath"
    fi
    return 0
  fi

  if [[ -n $s_hash && -z $d_hash ]]; then
    if [[ -z $m_hash ]]; then
      sync_write_from_source "$sfile" "$dfile" "$target" "$relpath"       # new
    elif (( RESPECT_DELETES )); then
      sync_manifest_unset "$target" "$relpath"                            # deleted at dest, respected
    else
      sync_write_from_source "$sfile" "$dfile" "$target" "$relpath"       # deleted at dest, re-add
      log "$location_name: $relpath was deleted at the destination, re-added from source (--respect-deletes to keep it gone)"
    fi
    return 0
  fi

  if [[ -n $s_hash && -n $d_hash ]]; then
    if [[ $s_hash == "$d_hash" ]]; then
      sync_manifest_set "$target" "$relpath" "$s_hash" "$(sync_mode "$dfile")"  # unchanged / adopted / converged
      return 0
    fi
    if [[ -z $m_hash ]]; then
      if (( ADOPT_SOURCE )); then
        sync_write_from_source "$sfile" "$dfile" "$target" "$relpath"
      elif (( STRICT )); then
        error "$location_name: $relpath differs from source with no known baseline -- refusing (run with --adopt=source or --strict is set)"
        CONFLICT_COUNT=$((CONFLICT_COUNT + 1))
      else
        CONFLICT_SUMMARY+=("$location_name: $relpath (differs from source, no baseline yet -- kept destination and recorded its hash as the baseline; a future sync auto-adopts source once dest stops changing, use --adopt=source now to take it immediately)")
        log "$location_name: $relpath differs from source with no baseline -- keeping destination, recording its hash as the new baseline"
        # Without this, a file that reaches this branch once reaches it on
        # EVERY future sync too -- s_hash/d_hash never converge and m_hash
        # stays empty forever, so it's flagged as "unresolved" indefinitely
        # even though nothing about it is actually still undecided. Setting
        # d_hash as the baseline here mirrors what sync_handle_conflict's
        # "dest" resolution already does for a real (known-baseline)
        # conflict: the kept destination becomes the new known-good state,
        # so next run either sees it unchanged (dest == baseline -> safe
        # update, source flows in) or changed again (a real new conflict).
        # Found 2026-09-20: workspace-standards.yaml never got a baseline
        # recorded across every sync since the 2026-09-17 manifest rewrite.
        (( DRY_RUN )) || sync_manifest_set "$target" "$relpath" "$d_hash" "$(sync_mode "$dfile")"
      fi
      return 0
    fi
    if [[ $d_hash == "$m_hash" ]]; then
      sync_write_from_source "$sfile" "$dfile" "$target" "$relpath"        # safe update
      return 0
    fi
    if [[ $s_hash == "$m_hash" ]]; then
      log "$location_name: $relpath has local edits, source unchanged -- keeping destination"
      return 0                                                             # local edit, not a conflict
    fi
    sync_handle_conflict "$sfile" "$dfile" "$target" "$relpath" "$location_name"
    return 0
  fi

  if [[ -z $s_hash && -n $d_hash ]]; then
    if [[ -z $m_hash ]]; then
      log "$location_name: $relpath is local-only (never synced from source) -- keeping it"
      return 0                                                             # local-only, e.g. a live-added provider
    fi
    if [[ $d_hash == "$m_hash" ]]; then
      sync_delete_dest "$dfile" "$target" "$relpath"                       # deleted at source, follow it
      return 0
    fi
    CONFLICT_SUMMARY+=("$location_name: $relpath (deleted at source, but edited at destination -- kept destination)")
    log "$location_name: $relpath was deleted at source but edited at destination -- keeping destination"
    return 0
  fi
}

# Sync one subdir/target. Kept the historical name `sync_subdir` so call
# sites in main() don't need to change.
sync_subdir() {
  local subdir_name=$1 src=$2 dest=$3 location_name=$4

  if [[ ! -d "$src" ]]; then
    log "skip $subdir_name -> $location_name (source does not exist)"
    return 0
  fi

  local real_src real_dest
  real_src=$(realpath -m "$src")
  real_dest=$(realpath -m "$dest")
  if [[ $real_dest == "$real_src" || $real_dest == "$real_src"/* ]]; then
    error "$location_name resolves inside its own source ($src) -- skipping rather than risk deleting the source. (Is $dest already a symlink into the repo, e.g. from setup.sh?)"
    return 0
  fi

  (( DRY_RUN )) || mkdir -p "$dest"

  local target="$real_dest"
  MANIFEST_JSON=$(jq --arg t "$target" --arg s "$real_src" --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
    '.targets[$t] //= {files:{}} | .targets[$t].src = $s | .targets[$t].last_sync = $ts' <<<"$MANIFEST_JSON")

  local -A seen=()
  local -a all_paths=()
  local p
  while IFS= read -r p; do
    [[ -n $p && -z ${seen[$p]:-} ]] || continue
    seen[$p]=1
    all_paths+=("$p")
  done < <(sync_source_paths "$subdir_name" "$src"; sync_dest_paths "$dest")

  for p in "${all_paths[@]}"; do
    if (( PULL )); then
      local sfile="$src/$p" dfile="$dest/$p"
      local s_hash="" d_hash="" m_hash=""
      [[ -f $sfile ]] && s_hash=$(sync_hash "$sfile")
      [[ -f $dfile ]] && d_hash=$(sync_hash "$dfile")
      m_hash=$(sync_manifest_hash "$target" "$p")
      if [[ -n $d_hash && ( -z $s_hash || ( -n $m_hash && $d_hash != "$m_hash" && $s_hash == "$m_hash" ) ) ]]; then
        sync_pull_to_source "$sfile" "$dfile" "$target" "$p"
      fi
      continue
    fi
    sync_reconcile_file "$subdir_name" "$src" "$dest" "$target" "$p" "$location_name"
  done

  echo "✓ reconciled $subdir_name -> $location_name"
}

main() {
  if [[ ! -d "$AGENTS_SRC" ]]; then
    error "Agents source not found: $AGENTS_SRC"
    exit 1
  fi

  sync_load_manifest

  echo "Syncing .agents/ subdirs from: $AGENTS_SRC"
  echo ""

  for subdir in "$AGENTS_SRC"/*/; do
    [[ -d "$subdir" ]] || continue
    subdir_name=$(basename "$subdir")

    # Always: reference copy at ~/.agents/<subdir> (the location every
    # harness/tool on this machine is expected to point its config at).
    sync_subdir "$subdir_name" "$subdir" "$AGENTS_DEST/$subdir_name" "~/.agents/$subdir_name" || true

    # skills/ additionally mirrors to ~/.claude/skills (Claude Code's own
    # plugin-style skill discovery location) — no other subdir has an
    # equivalent tool-specific mirror target.
    if [[ "$subdir_name" == "skills" ]]; then
      if [[ -d "$CLAUDE_SKILLS" ]] || [[ -L "$(dirname "$CLAUDE_SKILLS")" ]] || [[ -d "$(dirname "$CLAUDE_SKILLS")" ]]; then
        sync_subdir "skills" "$subdir" "$CLAUDE_SKILLS" "~/.claude/skills" || true
      fi
    fi

    # opencode/ additionally mirrors command/ + plugin/ into
    # ~/.config/opencode/ (opencode's global command and plugin
    # auto-discovery dirs — see .agents/opencode/README.md). Only these two
    # subdirs are reconciled; the rest of ~/.config/opencode (opencode.json
    # with machine-local keys, node_modules, herdr's plugins/) is never
    # touched. Skipped entirely when opencode isn't installed.
    if [[ "$subdir_name" == "opencode" ]]; then
      if [[ -d "$HOME/.config/opencode" ]]; then
        sync_subdir "opencode/command" "$subdir/command" "$HOME/.config/opencode/command" "~/.config/opencode/command" || true
        sync_subdir "opencode/plugin" "$subdir/plugin" "$HOME/.config/opencode/plugin" "~/.config/opencode/plugin" || true
      fi
    fi

    # hooks/ additionally mirrors to ~/.claude/hooks (Claude Code's own
    # hook-script location, same idea as the skills mirror above), then
    # reconciles ~/.claude/settings.json's hooks.SessionStart against
    # hooks/session-start-hooks.json -- add-only, idempotent, never
    # touches hooks this workspace doesn't own. See .agents/hooks/README.md.
    if [[ "$subdir_name" == "hooks" ]]; then
      sync_subdir "hooks" "$subdir" "$CLAUDE_HOOKS" "~/.claude/hooks" || true
      if [[ -f "$BASE_DIR/.claude/settings.json" ]]; then
        # Per-event fragment (SessionStart + PreCompact, dotfiles-tsk-
        # chronicle-skill-layer); older checkouts may only have the
        # pre-rename SessionStart-only file — installer accepts both.
        hook_fragment="$AGENTS_DEST/hooks/session-and-compact-hooks.json"
        [[ -f "$hook_fragment" ]] || hook_fragment="$AGENTS_DEST/hooks/session-start-hooks.json"
        install_args=(--fragment "$hook_fragment" --settings "$BASE_DIR/.claude/settings.json")
        [[ $DRY_RUN -eq 1 ]] && install_args+=(--dry-run)
        python3 "$AGENTS_DEST/hooks/install_session_start_hooks.py" "${install_args[@]}" || true
      fi
    fi

    # providers/ additionally puts its TUI entry point on PATH, same idea as
    # the skills -> ~/.claude/skills mirror above.
    if [[ "$subdir_name" == "providers" ]]; then
      if [[ $DRY_RUN -eq 1 ]]; then
        echo "(dry-run) would symlink: $AGENTS_DEST/providers/dtx-providers-tui -> $LOCAL_BIN/dtx-providers-tui"
      else
        mkdir -p "$LOCAL_BIN"
        ln -sf "$AGENTS_DEST/providers/dtx-providers-tui" "$LOCAL_BIN/dtx-providers-tui"
        echo "✓ symlinked dtx-providers-tui -> ~/.local/bin/dtx-providers-tui"
      fi
    fi
  done

  # Sync to Omarchy system defaults (optional, requires sudo) — skills only.
  if [[ $SYNC_SYSTEM -eq 1 ]]; then
    skills_src="$AGENTS_SRC/skills"
    if [[ ! -d "$SYSTEM_SKILLS" ]]; then
      error "System skills path not found: $SYSTEM_SKILLS"
      echo "  (omarchy system skills not installed, skipping)"
    elif [[ ! -w "$SYSTEM_SKILLS" ]]; then
      echo "Note: $SYSTEM_SKILLS is not writable, attempting sudo..."
      echo "This will sync skills to system-wide location (requires password)"
      echo ""
      if sudo -v &>/dev/null; then
        sync_subdir "skills" "$skills_src" "$SYSTEM_SKILLS" "/usr/share/omarchy/default/agents/skills (sudo)" || true
      else
        error "sudo failed or not available, skipping system sync"
      fi
    else
      sync_subdir "skills" "$skills_src" "$SYSTEM_SKILLS" "/usr/share/omarchy/default/agents/skills" || true
    fi
  fi

  sync_save_manifest

  echo ""
  if (( ${#CONFLICT_SUMMARY[@]} > 0 )); then
    echo "Unresolved (no baseline / deleted+edited):"
    printf '  - %s\n' "${CONFLICT_SUMMARY[@]}"
  fi
  echo "Done!"

  if [[ $DRY_RUN -eq 1 ]]; then
    echo "(dry-run mode - no changes made)"
  fi

  # --dry-run always exits 0 -- it's a report, not an action, and
  # scripts/validate_dotfiles.sh asserts this.
  if (( ! DRY_RUN )) && (( CONFLICT_COUNT > 0 )); then
    exit 3
  fi
  return 0
}

main "$@"
