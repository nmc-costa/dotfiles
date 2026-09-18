#!/usr/bin/env bash
set -euo pipefail

# Minimal workspace bootstrap: create dirs, clone repos, optional dotfiles
BASE_DIR="$HOME"
DRY_RUN=0
DO_DOTFILES=0

for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=1 ;;
    --dotfiles) DO_DOTFILES=1 ;;
    --*) echo "unknown flag: $arg" >&2; exit 1 ;;
    *) BASE_DIR="$arg" ;;
  esac
done

WORK_DIR="$BASE_DIR/Work"
PROJECTS_DIR="$BASE_DIR/Projects"

# Override on another machine/user via env, e.g.:
#   GITHUB_USER=someone WORK_REPOS="repo1 repo2" PROJECTS_REPOS="repo3" ./setup.sh
GITHUB_USER="${GITHUB_USER:-nmc-costa}"
read -ra WORK_REPOS <<< "${WORK_REPOS:-codebase mobai RAGFusion sp_xai_nos technopage wondercube}"
read -ra PROJECTS_REPOS <<< "${PROJECTS_REPOS:-architect agentic_instructions notes HIcode HITnode HITtwintag ibots roi_lab}"

echo "Base dir: $BASE_DIR"
if [[ $DRY_RUN -eq 1 ]]; then
  echo "DRY RUN: no changes will be made"
else
  mkdir -p "$WORK_DIR" "$PROJECTS_DIR"
fi

clone(){
  local repo=$1 target=$2
  local ssh="git@github.com:$GITHUB_USER/$repo.git"
  local https="https://github.com/$GITHUB_USER/$repo.git"
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
    git clone "https://${GITHUB_TOKEN}@github.com/$GITHUB_USER/$repo.git" "$target" && { echo "cloned via token: $repo"; return; } || true
  fi
  git clone "$https" "$target" && echo "cloned via HTTPS: $repo" || echo "failed: $repo"
}

for r in "${WORK_REPOS[@]}"; do clone "$r" "$WORK_DIR/$r"; done
for r in "${PROJECTS_REPOS[@]}"; do clone "$r" "$PROJECTS_DIR/$r"; done

if [[ $DO_DOTFILES -eq 1 ]]; then
  if [[ $DRY_RUN -eq 1 ]]; then
    echo "(dry) would setup bare dotfiles from https://github.com/nmc-costa/dotfiles"
  else
    git clone --bare "https://github.com/$GITHUB_USER/dotfiles.git" "$HOME/.cfg" || echo "dotfiles clone failed or already present"
    echo "Add: alias config='git --git-dir=$HOME/.cfg/ --work-tree=$HOME' to your shell rc, then run: config checkout"
  fi
fi

# === AGENTS & SKILLS SETUP ===

# Whole-directory symlink — only safe for a directory that is ENTIRELY
# curated/versioned content, where nothing ever writes live runtime state
# into it. `.agents/` (skills/instructions/etc.) and `.vscode/` (its one
# real secret already handled specially via chezmoi+age, see SECRETS.md)
# both qualify.
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
    if [[ "$(readlink -f "$agent_dest")" == "$(readlink -f "$agent_src")" ]]; then
      echo "skip: $agent_dest already symlinked correctly"
    else
      echo "relink: $agent_dest pointed elsewhere, updating"
      ln -sfn "$agent_src" "$agent_dest"
      echo "symlink: .$agent_name -> $agent_dest"
    fi
    return
  fi

  if [[ -d "$agent_dest" ]]; then
    local backup="${agent_dest}.backup.$(date +%Y%m%dT%H%M%S)"
    echo "backup: moving $agent_dest to $backup"
    mv "$agent_dest" "$backup"
  fi

  ln -sf "$agent_src" "$agent_dest"
  echo "symlink: .$agent_name -> $agent_dest"
}

# File-level symlink — required for a directory that MIXES versioned
# config with live runtime state (credentials, sessions, logs, caches).
# `~/.claude/` is exactly that: whole-directory symlinking it would
# redirect Claude Code's live writes (.credentials.json, history.jsonl,
# sessions/, etc. — none of which .gitignore's .claude/{sessions,logs,cache}/
# entries cover) straight into the git working tree. Only the one curated
# file gets linked; the directory itself stays real and untouched.
setup_agent_file_symlink() {
  local agent_name=$1 file=$2
  local file_src="$BASE_DIR/dotfiles/.$agent_name/$file"
  local file_dest="$BASE_DIR/.$agent_name/$file"

  if [[ ! -f "$file_src" ]]; then
    echo "skip: $file_src does not exist"
    return
  fi

  if [[ $DRY_RUN -eq 1 ]]; then
    echo "(dry) would symlink $file_src -> $file_dest"
    return
  fi

  mkdir -p "$BASE_DIR/.$agent_name"

  if [[ -L "$file_dest" ]]; then
    if [[ "$(readlink -f "$file_dest")" == "$(readlink -f "$file_src")" ]]; then
      echo "skip: $file_dest already symlinked correctly"
    else
      echo "relink: $file_dest pointed elsewhere, updating"
      ln -sfT "$file_src" "$file_dest"
      echo "symlink: .$agent_name/$file -> $file_dest"
    fi
    return
  fi

  if [[ -d "$file_dest" ]]; then
    echo "skip: $file_dest is a directory, refusing to symlink over it (fix manually)"
    return
  fi

  if [[ -f "$file_dest" ]]; then
    local backup="${file_dest}.backup.$(date +%Y%m%dT%H%M%S)"
    echo "backup: moving $file_dest to $backup"
    mv "$file_dest" "$backup"
  fi

  ln -sfT "$file_src" "$file_dest"
  echo "symlink: .$agent_name/$file -> $file_dest"
}

# Root-level (~) CLAUDE.md/AGENTS.md coverage — arbitrary src/dest pairs
# (different names, some nested one level, none of them a per-tool "hidden
# dir + same filename" pair), so this doesn't fit setup_agent_symlinks or
# setup_agent_file_symlink's fixed naming conventions. Lets Claude Code
# (and Codex, via AGENTS.md) discover context when a session starts from
# `~`, `~/Projects/...`, or `~/Work/...` — see global/ in this repo.
setup_root_symlink() {
  local src=$1 dest=$2

  if [[ ! -f "$src" ]]; then
    echo "skip: $src does not exist"
    return
  fi

  if [[ $DRY_RUN -eq 1 ]]; then
    echo "(dry) would symlink $src -> $dest"
    return
  fi

  mkdir -p "$(dirname "$dest")"

  if [[ -L "$dest" ]]; then
    if [[ "$(readlink -f "$dest")" == "$(readlink -f "$src")" ]]; then
      echo "skip: $dest already symlinked correctly"
    else
      echo "relink: $dest pointed elsewhere, updating"
      ln -sfT "$src" "$dest"
      echo "symlink: $dest"
    fi
    return
  fi

  if [[ -e "$dest" ]]; then
    local backup="${dest}.backup.$(date +%Y%m%dT%H%M%S)"
    echo "backup: moving $dest to $backup"
    mv "$dest" "$backup"
  fi

  ln -sfT "$src" "$dest"
  echo "symlink: $dest"
}

echo ""
echo "=== Setting up agents and skills ==="

# Setup agent symlinks
setup_agent_symlinks "agents"
setup_agent_symlinks "vscode"

# All four of these mix versioned config with live runtime state
# (credentials/session DBs/logs/caches) the same way ~/.claude/ does —
# confirmed per-tool 2026-09-16 (see CLAUDE.md's Known Gaps). File-level
# only, never the directory.
setup_agent_file_symlink "claude" "CLAUDE.md"
setup_agent_file_symlink "gemini" "GEMINI.md"
setup_agent_file_symlink "codex" "AGENTS.md"
setup_agent_file_symlink "copilot" "copilot-instructions.md"

# Root-level context (~, ~/Projects) — see global/ROOT.CLAUDE.md's own
# note for why ~/Work/CLAUDE.md is NOT included here: it's copied by hand
# from global/WORK.CLAUDE.template.md and never symlinked, since it may
# hold employer-specific content that must never enter this repo.
setup_root_symlink "$BASE_DIR/dotfiles/global/ROOT.CLAUDE.md" "$BASE_DIR/CLAUDE.md"
setup_root_symlink "$BASE_DIR/dotfiles/AGENTS.md" "$BASE_DIR/AGENTS.md"
setup_root_symlink "$BASE_DIR/dotfiles/global/PROJECTS.CLAUDE.md" "$PROJECTS_DIR/CLAUDE.md"

# Sync skills from dotfiles/.agents/skills/ location
if [[ -d "$BASE_DIR/dotfiles/.agents/skills" ]]; then
  echo "info: Syncing skills from dotfiles/.agents/skills..."
  if [[ $DRY_RUN -eq 1 ]]; then
    "$BASE_DIR/dotfiles/sync.sh" --dry-run || true
  else
    "$BASE_DIR/dotfiles/sync.sh" || true
  fi
fi

echo "done" 
