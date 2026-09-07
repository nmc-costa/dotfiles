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

echo "done"
