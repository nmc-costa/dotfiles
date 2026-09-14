#!/usr/bin/env bash
set -euo pipefail

# Sync skills from dotfiles/.agents/skills/ to all locations
# Usage: ./sync-skills.sh [--dry-run] [--system] [--verbose]

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

SKILLS_SRC="$BASE_DIR/dotfiles/.agents/skills"
AGENTS_SKILLS="$BASE_DIR/.agents/skills"
CLAUDE_SKILLS="$BASE_DIR/.claude/skills"
SYSTEM_SKILLS="/usr/share/omarchy/default/agents/skills"

log() {
  if [[ $VERBOSE -eq 1 ]]; then
    echo "[sync-skills] $*"
  fi
}

error() {
  echo "[ERROR] $*" >&2
}

sync_to_location() {
  local src=$1
  local dest=$2
  local location_name=$3
  
  if [[ ! -d "$src" ]]; then
    error "$src does not exist"
    return 1
  fi
  
  if [[ $DRY_RUN -eq 1 ]]; then
    echo "(dry-run) would sync: $src -> $dest"
    return 0
  fi
  
  if [[ ! -d "$dest" ]]; then
    mkdir -p "$dest"
    log "created $dest"
  fi
  
  # Sync each skill folder
  for skill_dir in "$src"/*; do
    if [[ -d "$skill_dir" ]]; then
      skill_name=$(basename "$skill_dir")
      
      # Check if SKILL.md exists (required)
      if [[ ! -f "$skill_dir/SKILL.md" ]]; then
        log "skip: $skill_name (missing SKILL.md)"
        continue
      fi
      
      log "syncing $skill_name -> $location_name"
      rm -rf "$dest/$skill_name"
      cp -r "$skill_dir" "$dest/$skill_name"
    fi
  done
  
  echo "✓ synced to $location_name"
  return 0
}

main() {
  if [[ ! -d "$SKILLS_SRC" ]]; then
    error "Skills source not found: $SKILLS_SRC"
    exit 1
  fi
  
  echo "Syncing skills from: $SKILLS_SRC"
  echo ""
  
  # Sync to ~/.agents/skills (always - this is the reference)
  log "syncing to ~/.agents/skills"
  sync_to_location "$SKILLS_SRC" "$AGENTS_SKILLS" "~/.agents/skills" || true
  
  # Sync to ~/.claude/skills (if exists and different)
  if [[ "$AGENTS_SKILLS" != "$CLAUDE_SKILLS" ]]; then
    if [[ -d "$CLAUDE_SKILLS" ]] || [[ -L "$(dirname "$CLAUDE_SKILLS")" ]]; then
      log "syncing to ~/.claude/skills"
      sync_to_location "$SKILLS_SRC" "$CLAUDE_SKILLS" "~/.claude/skills" || true
    fi
  fi
  
  # Sync to system defaults (optional, requires sudo)
  if [[ $SYNC_SYSTEM -eq 1 ]]; then
    if [[ ! -d "$SYSTEM_SKILLS" ]]; then
      error "System skills path not found: $SYSTEM_SKILLS"
      echo "  (omarchy system skills not installed, skipping)"
      return 1
    fi
    
    if [[ ! -w "$SYSTEM_SKILLS" ]]; then
      echo "Note: $SYSTEM_SKILLS is not writable, attempting sudo..."
      echo "This will sync skills to system-wide location (requires password)"
      echo ""
      
      if sudo -v &>/dev/null; then
        sync_to_location "$SKILLS_SRC" "$SYSTEM_SKILLS" "/usr/share/omarchy/default/agents/skills (sudo)" || true
      else
        error "sudo failed or not available, skipping system sync"
        return 1
      fi
    else
      sync_to_location "$SKILLS_SRC" "$SYSTEM_SKILLS" "/usr/share/omarchy/default/agents/skills" || true
    fi
  fi
  
  echo ""
  echo "Done!"
  
  if [[ $DRY_RUN -eq 1 ]]; then
    echo "(dry-run mode - no changes made)"
  fi
}

main "$@"
