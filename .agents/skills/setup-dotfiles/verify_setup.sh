#!/usr/bin/env bash
# Read-only checklist: did a new-machine `./setup.sh` + `./sync.sh` actually
# produce the state those scripts (not the docs) are supposed to produce?
#
# README.md/AGENTS.md and setup.sh's own comments disagree with each other in
# two places (~/.agents & ~/.claude symlink-vs-copy, ~/.vscode &
# ~/.custom_providers symlink-vs-copy) — this script checks against the
# scripts' actual current behavior, and reports (never asserts a "correct"
# answer for) the two places where the docs are stale. See
# setup-dotfiles/SKILL.md.
#
# Never touches secrets: the chezmoi/age step is reported, not automated —
# restoring the private key is a human action (docs/SECRETS.md).
#
# Exit 0 = nothing FAILed. WARN = expected/manual/known-gap, not a bug.
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
cd "$REPO_ROOT"

PASS=0; FAIL=0; WARN=0
ok()   { printf '  OK    %s\n' "$1"; PASS=$((PASS+1)); }
bad()  { printf '  FAIL  %s\n' "$1"; FAIL=$((FAIL+1)); }
warn() { printf '  WARN  %s\n' "$1"; WARN=$((WARN+1)); }
info() { printf '  INFO  %s\n' "$1"; }

echo "=== setup-dotfiles verification (repo: $REPO_ROOT) ==="
echo

echo "-- Repo hygiene (scripts/validate_dotfiles.sh) --"
if [[ -x scripts/validate_dotfiles.sh ]]; then
  if ./scripts/validate_dotfiles.sh; then
    ok "validate_dotfiles.sh passed"
  else
    bad "validate_dotfiles.sh reported failures (see output above)"
  fi
else
  warn "scripts/validate_dotfiles.sh not found or not executable"
fi
echo

# $1 = source path relative to repo root, $2 = destination absolute path
check_file_symlink() {
  local rel_src=$1 dest=$2
  local src="$REPO_ROOT/$rel_src"
  if [[ ! -f "$src" ]]; then
    warn "$dest: source $rel_src does not exist in this repo, skipping"
    return
  fi
  if [[ ! -L "$dest" ]]; then
    bad "$dest is not a symlink (expected -> $rel_src)"
    return
  fi
  if [[ "$(readlink -f "$dest")" == "$(readlink -f "$src")" ]]; then
    ok "$dest -> $rel_src"
  else
    bad "$dest is a symlink but points elsewhere ($(readlink -f "$dest"))"
  fi
}

echo "-- Per-tool file-level symlinks (setup_agent_file_symlink) --"
check_file_symlink ".claude/CLAUDE.md"                "$HOME/.claude/CLAUDE.md"
check_file_symlink ".gemini/GEMINI.md"                "$HOME/.gemini/GEMINI.md"
check_file_symlink ".codex/AGENTS.md"                 "$HOME/.codex/AGENTS.md"
check_file_symlink ".copilot/copilot-instructions.md" "$HOME/.copilot/copilot-instructions.md"
check_file_symlink ".cursor/rules/workspace.mdc"      "$HOME/.cursor/rules/workspace.mdc"
echo

echo "-- Root-level context symlinks (setup_root_symlink) --"
check_file_symlink "global/ROOT.CLAUDE.md"     "$HOME/CLAUDE.md"
check_file_symlink "AGENTS.md"                 "$HOME/AGENTS.md"
check_file_symlink "global/PROJECTS.CLAUDE.md" "$HOME/Projects/CLAUDE.md"
echo

echo "-- ~/.agents and ~/.claude: real directories reconciled by sync.sh, not symlinks --"
echo "   (2026-09-17 design — a symlink here makes source/dest hashes always equal and"
echo "   sync.sh's manifest reconciliation refuses to run; see CLAUDE.md Known Gaps)"
# Mirrors sync.sh's sync_source_paths rule for skills/ (sync.sh:150-152):
# a top-level dir under .agents/skills/ only counts as a real skill, and
# only gets synced, if it has a SKILL.md. _templates/ deliberately has none
# (it's example scaffolding, not a skill) — listing it here would make this
# check permanently FAIL on a correctly-synced machine.
list_real_skills() {
  local skills_dir=$1
  local d
  for d in "$skills_dir"/*/; do
    [[ -f "$d/SKILL.md" ]] && basename "$d"
  done
}

check_real_dir_with_skills() {
  local dest=$1
  if [[ -L "$dest" ]]; then
    bad "$dest is a symlink — sync.sh expects a real, independently-writable directory here"
    return
  fi
  if [[ ! -d "$dest" ]]; then
    bad "$dest does not exist — run ./sync.sh"
    return
  fi
  ok "$dest is a real directory"
  local dest_skills="$dest/skills"
  local src_skills="$REPO_ROOT/.agents/skills"
  if [[ -d "$dest_skills" ]]; then
    local missing
    missing="$(comm -23 <(list_real_skills "$src_skills" | sort) <(list_real_skills "$dest_skills" | sort))"
    if [[ -z "$missing" ]]; then
      ok "$dest_skills has every skill from .agents/skills/"
    else
      bad "$dest_skills is missing: $(echo "$missing" | tr '\n' ' ')"
    fi
  else
    bad "$dest_skills does not exist"
  fi
}
check_real_dir_with_skills "$HOME/.agents"
check_real_dir_with_skills "$HOME/.claude"
echo

echo "-- ~/.vscode and ~/.custom_providers (chezmoi-managed; reported as-is, not asserted) --"
report_state() {
  local dest=$1
  if [[ -L "$dest" ]]; then
    info "$dest is a symlink -> $(readlink -f "$dest")"
  elif [[ -d "$dest" ]]; then
    info "$dest is a real directory"
  else
    info "$dest does not exist"
  fi
}
report_state "$HOME/.vscode"
report_state "$HOME/.custom_providers"
if [[ -d "$HOME/.dtx-providers" ]]; then
  warn "~/.dtx-providers still exists — pre-2026-09-23 name (docs/SECRETS.md, PR #70 renamed it to ~/.custom_providers/dtx_providers.env). Leftover from before the rename, not auto-migrated by setup.sh; safe to remove by hand once ~/.custom_providers/dtx_providers.env has the same value."
fi
echo "  NOTE  README.md/AGENTS.md call these symlinks; setup.sh's undo_legacy_dir_symlink"
echo "        comment says both are now real directories written by 'chezmoi apply'"
echo "        instead (docs/SECRETS.md). This script reports current reality above"
echo "        rather than assert either doc's claim — that contradiction is itself a"
echo "        known gap, not something for this script to resolve."
echo

echo "-- chezmoi + age secrets (human step — never automated here) --"
if command -v chezmoi >/dev/null 2>&1; then
  ok "chezmoi is installed"
  if [[ -f "$HOME/.config/chezmoi/key.txt" ]]; then
    ok "age private key present at ~/.config/chezmoi/key.txt"
    if out="$(chezmoi status 2>&1)"; then
      if [[ -z "$out" ]]; then
        ok "chezmoi status: nothing pending"
      else
        warn "chezmoi status reports pending changes — review with 'chezmoi diff', then 'chezmoi apply' yourself:"
        echo "$out" | sed 's/^/        /'
      fi
    else
      warn "chezmoi status failed: $out"
    fi
  else
    warn "no age key at ~/.config/chezmoi/key.txt — restore it from Bitwarden (see docs/SECRETS.md 'New-machine setup') before 'chezmoi apply' can decrypt secrets. Expected on a brand-new machine, not a failure."
  fi
else
  warn "chezmoi not installed — secrets (.vscode/settings.json API key, ~/.custom_providers/dtx_providers.env) won't be restored until it is (see docs/SECRETS.md)"
fi
echo

echo "-- Branch-naming pre-push hook (documented but not shipped as of 2026-09-23) --"
if [[ -f "$REPO_ROOT/tasks/scripts/setup_git_hooks.sh" ]]; then
  ok "tasks/scripts/setup_git_hooks.sh exists"
else
  warn ".claude/CLAUDE.md references tasks/scripts/setup_git_hooks.sh, tasks/scripts/pre-push.sample, and a './setup.sh --install-hooks' / './sync.sh --install-hooks' flag, but none of these exist in this repo yet — known doc/reality gap, nothing this script can install"
fi
echo

echo "-- git / gh --"
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  ok "$REPO_ROOT is a git checkout (branch: $(git branch --show-current))"
else
  bad "$REPO_ROOT is not a git checkout"
fi
if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then
  ok "gh CLI authenticated"
else
  warn "gh CLI not authenticated — PR automation won't work (run: gh auth login)"
fi
echo

echo "-- Legacy leftovers --"
if [[ -d "$HOME/.agent" ]]; then
  bad "~/.agent (singular, pre-migration dir) still exists — should be removed"
else
  ok "no legacy ~/.agent directory"
fi
echo

echo "=== Summary: $PASS OK, $WARN warnings, $FAIL failures ==="
[[ $FAIL -eq 0 ]]
