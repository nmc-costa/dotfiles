#!/usr/bin/env bash
set -euo pipefail

# Minimal workspace bootstrap: create dirs, clone repos, optional dotfiles
BASE_DIR="${1:-$HOME}"
DRY_RUN=0
DO_DOTFILES=0

for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=1 ;;
    --dotfiles) DO_DOTFILES=1 ;;
  esac
done

WORK_DIR="$BASE_DIR/Work"
PROJECTS_DIR="$BASE_DIR/Projects"

WORK_REPOS=(codebase mobai RAGFusion sp_xai_nos technopage wondercube)
PROJECTS_REPOS=(architect agentic_instructions notes HIcode HITnode HITtwintag ibots roi_lab)

echo "Base dir: $BASE_DIR"
if [[ $DRY_RUN -eq 1 ]]; then
  echo "DRY RUN: no changes will be made"
else
  mkdir -p "$WORK_DIR" "$PROJECTS_DIR"
fi

clone(){
  local repo=$1 target=$2
  local ssh="git@github.com:nmc-costa/$repo.git"
  local https="https://github.com/nmc-costa/$repo.git"
  if [[ $DRY_RUN -eq 1 ]]; then
    echo "(dry) would clone $ssh -> $target"
    return
  fi
  if [[ -d "$target/.git" ]]; then
    echo "skip: $target exists"
    return
  fi
  if git clone "$ssh" "$target" 2>/dev/null; then
    echo "cloned via SSH: $repo"
    return
  fi
  if [[ -n "${GITHUB_TOKEN:-}" ]]; then
    git clone "https://${GITHUB_TOKEN}@github.com/nmc-costa/$repo.git" "$target" && { echo "cloned via token: $repo"; return; } || true
  fi
  git clone "$https" "$target" && echo "cloned via HTTPS: $repo" || echo "failed: $repo"
}

for r in "${WORK_REPOS[@]}"; do clone "$r" "$WORK_DIR/$r"; done
for r in "${PROJECTS_REPOS[@]}"; do clone "$r" "$PROJECTS_DIR/$r"; done

if [[ $DO_DOTFILES -eq 1 ]]; then
  if [[ $DRY_RUN -eq 1 ]]; then
    echo "(dry) would setup bare dotfiles from https://github.com/nmc-costa/dotfiles"
  else
    git clone --bare https://github.com/nmc-costa/dotfiles.git "$HOME/.cfg" || echo "dotfiles clone failed or already present"
    echo "Add: alias config='git --git-dir=$HOME/.cfg/ --work-tree=$HOME' to your shell rc, then run: config checkout"
  fi
fi

# === AGENTS & SKILLS SETUP ===
setup_agent_symlinks() {
  local agent_name=$1
  local agent_src="$BASE_DIR/dotfiles/.$agent_name"
  local agent_dest="$BASE_DIR/.$agent_name"
  
  if [[ ! -d "$agent_src" ]]; then
    echo "skip: $agent_src does not exist"
    return
  fi
  
  if [[ $DRY_RUN -eq 1 ]]; then
    echo "(dry) would symlink $agent_src -> $agent_dest"
    return
  fi
  
  if [[ -L "$agent_dest" ]]; then
    echo "skip: $agent_dest already symlinked"
    return
  fi
  
  if [[ -d "$agent_dest" ]]; then
    echo "backup: moving $agent_dest to ${agent_dest}.backup"
    mv "$agent_dest" "${agent_dest}.backup"
  fi
  
  ln -sf "$agent_src" "$agent_dest"
  echo "symlink: .$agent_name -> $agent_dest"
}

echo ""
echo "=== Setting up agents and skills ==="

# Setup agent symlinks
setup_agent_symlinks "claude"
setup_agent_symlinks "agents"
setup_agent_symlinks "vscode"

# Sync skills from dotfiles/.agents/skills/ location
if [[ -d "$BASE_DIR/dotfiles/.agents/skills" ]]; then
  echo "info: Syncing skills from dotfiles/.agents/skills..."
  if [[ $DRY_RUN -eq 1 ]]; then
    "$BASE_DIR/dotfiles/sync-skills.sh" --dry-run || true
  else
    "$BASE_DIR/dotfiles/sync-skills.sh" || true
  fi
fi

echo "done" 
