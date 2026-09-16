#!/usr/bin/env bash
set -euo pipefail

# Sync ALL of dotfiles/.agents/<subdir>/ (skills, instructions, harnesses,
# prompts, workflows, validation, automation — whatever subdirs exist) to
# the locations other harnesses/tools read on this machine.
#
# Kept the name `sync.sh` for backwards compatibility with existing
# docs/muscle memory (this repo's README/CLAUDE.md/AGENTS.md/CHEATSHEET.md
# all reference it by this name) even though it now syncs more than skills —
# 2026-09-15, requested explicitly ("o sync tem de ser global e para tudo").
#
# Usage: ./sync.sh [--dry-run] [--system] [--verbose]
#   --system   also sync skills/ (only) to the Omarchy system-wide location
#              (requires sudo) — other .agents/ subdirs have no established
#              system-wide convention, so --system stays skills-only.

DRY_RUN=0
SYNC_SYSTEM=0
VERBOSE=0
BASE_DIR="${BASE_DIR:-$HOME}"

for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=1 ;;
    --system) SYNC_SYSTEM=1 ;;
    --verbose) VERBOSE=1 ;;
  esac
done

AGENTS_SRC="$BASE_DIR/dotfiles/.agents"
AGENTS_DEST="$BASE_DIR/.agents"
CLAUDE_SKILLS="$BASE_DIR/.claude/skills"
SYSTEM_SKILLS="/usr/share/omarchy/default/agents/skills"

log() {
  if [[ $VERBOSE -eq 1 ]]; then
    echo "[sync] $*"
  fi
}

error() {
  echo "[ERROR] $*" >&2
}

# Sync every item directly under $src into $dest, mirroring (removing dest
# entries that no longer exist in src). Skill folders specifically require
# a SKILL.md to be considered valid (unchanged from the original behavior);
# every other .agents/ subdir syncs its full contents unconditionally.
sync_subdir() {
  local subdir_name=$1 src=$2 dest=$3 location_name=$4

  if [[ ! -d "$src" ]]; then
    log "skip $subdir_name -> $location_name (source does not exist)"
    return 0
  fi

  if [[ $DRY_RUN -eq 1 ]]; then
    echo "(dry-run) would sync: $src -> $dest"
    return 0
  fi

  if [[ "$subdir_name" == "skills" ]]; then
    mkdir -p "$dest"
    for skill_dir in "$src"/*; do
      [[ -d "$skill_dir" ]] || continue
      skill_name=$(basename "$skill_dir")
      if [[ ! -f "$skill_dir/SKILL.md" ]]; then
        log "skip: $skill_name (missing SKILL.md)"
        continue
      fi
      log "syncing skills/$skill_name -> $location_name"
      rm -rf "$dest/$skill_name"
      cp -r "$skill_dir" "$dest/$skill_name"
    done
  else
    log "syncing $subdir_name/ -> $location_name"
    rm -rf "$dest"
    mkdir -p "$(dirname "$dest")"
    cp -r "$src" "$dest"
  fi

  echo "✓ synced $subdir_name -> $location_name"
}

main() {
  if [[ ! -d "$AGENTS_SRC" ]]; then
    error "Agents source not found: $AGENTS_SRC"
    exit 1
  fi

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

  echo ""
  echo "Done!"

  if [[ $DRY_RUN -eq 1 ]]; then
    echo "(dry-run mode - no changes made)"
  fi
}

main "$@"
