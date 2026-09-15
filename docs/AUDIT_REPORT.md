# AUDIT REPORT

**Date:** 2026-09-14 (original audit) — **corrected 2026-09-15** after independent re-verification found the original's hardcoded-path and `dtx/`-reference claims to be false.
**Status:** ⚠️ CONDITIONAL — root/docs structure is clean, but hardcoded paths and `dtx/` references **do** exist (see §4/§6 below). This report was rewritten in place rather than left standing, per `README.md`'s "flag, don't silently fix" rule for these two docs — the flag is now resolved by correcting the content.

## Checklist Verification

### 1. Root Structure ✅
- ✅ No unnecessary loose files — root holds only `README.md`, `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `CHEATSHEET.md`, `setup.sh`, `sync-skills.sh`, `test-subagents.sh`, `.gitignore`, plus the directories `.agents/`, `.chezmoisource/`, `.claude/`, `.github/`, `.vscode/`, `docs/`, `scripts/`, `.git/`
- ✅ Scripts organized properly (root + `scripts/` for utilities)
- ✅ MDs well organized — all secondary docs (`SECRETS.md`, `STANDARDS.md`, `AUDIT_REPORT.md`, `SUBAGENTS_VERIFICATION.md`, `VSCODE_MONITOR_QUICKSTART.md`, `directory_tree.md`, `requirements.txt`, `vscode-docs-monitor.yml`) live in `docs/`, not root
- ✅ `.gitignore` present and comprehensive
- Verified by `./scripts/validate_dotfiles.sh` (structural checks), currently passing

### 2. MDs — Content Quality ✅ (mostly)
- ✅ README.md — comprehensive, includes real directory tree + human/agent guideline sections
- ✅ CLAUDE.md — consistent with the rest, keeps an explicit "Lacunas Conhecidas" (Known Gaps) section rather than hiding stale claims
- ✅ GEMINI.md — up to date, dotfiles-focused
- ✅ AGENTS.md — complete guide
- ✅ `docs/SUBAGENTS_VERIFICATION.md` — useful, actionable checklist
- ⚠️ `docs/STANDARDS.md` — was presenting proposed/aspirational structure (`.copilot/`, `.gemini/`, `.cursor/`, `agent-versions.json`) as if already implemented; **corrected this round** to label those sections "proposed — not implemented"
- ⚠️ This file (`AUDIT_REPORT.md`) previously claimed "no hardcoded paths" and "no `dtx/` references" — both false; **corrected this round**, see §4/§6

### 3. Estrutura `.agents/` ✅
- ✅ `.agents/skills/` currently contains 13 entries: `archi`, `calls2database`, `diagnose-crash`, `diagramhits`, `documenthits`, `mockuphits`, `omarchy`, `presenthits`, `project-doc-lifecycle`, `projecthits`, `reviewhits`, `simplifyhit`, `_templates` — more than the "2 skills" an earlier version of this report described, reflecting the `agentic_instructions` merge
- ✅ `.agents/workflows/` present
- ✅ `.claude/skills/` no longer diverges from `.agents/skills/` — the 9 HITs skills now live as real content under `.agents/skills/`, with `.claude/skills/<name>` as symlinks back to them (verified: `archi`, `diagramhits`, `documenthits`, `mockuphits`, `presenthits`, `project-doc-lifecycle`, `projecthits`, `reviewhits`, `simplifyhit`)
- ✅ `.github/{harnesses,instructions,prompts,automation,CONTRIBUTING.md}` are symlinks into `.agents/`, avoiding duplication

### 4. Scripts ⚠️
- ✅ `setup.sh` — syntax valid (`bash -n` OK)
- ✅ `sync-skills.sh` — syntax valid
- ✅ `test-subagents.sh` — syntax valid, executable
- ✅ `scripts/validate_dotfiles.sh` — syntax valid (new this round; also `bash -n`-checks every `*.sh` in the repo, see §9)
- ❌ **`setup.sh` hardcodes `WORK_REPOS`, `PROJECTS_REPOS`, and the GitHub username `nmc-costa`** directly in the `clone()` function's SSH/HTTPS URLs (`git@github.com:nmc-costa/$repo.git`) — not portable to another user without editing the script. **Note:** a fix making these overridable via `GITHUB_USER`/`WORK_REPOS`/`PROJECTS_REPOS` environment variables exists in commit `0304d1d` on branch `claude/todo-continuation-and-notes-backlog`, but that fix is **not present on this branch** (`claude/repo-hygiene-dotfiles`) or on `main` — do not assume it's merged until that branch lands.
- ❌ **Hardcoded personal path in `.vscode/github.code-workspace`**: `"path": "dtx/repos/sp_xai_nos"` — a literal `dtx/`-prefixed relative path, hardcoded for one machine/user layout.

### 5. Versionamento ✅
- ✅ `.gitignore` properly excludes session logs, IDE temp files, Python cache
- ✅ Tracks `.agents/`, `.claude/`, `.vscode/`, `.github/` as intended
- ✅ Git history clean and descriptive

### 6. Consistency ❌ (was falsely reported as ✅)
- ✅ NO references to old `.agent/` (singular) — confirmed via repo-wide grep
- ✅ NO references to old `my/` folder in current config
- ❌ **`dtx/` references DO exist** — found in `.vscode/github.code-workspace` (`"path": "dtx/repos/sp_xai_nos"`). Also present, but out of scope for "no hardcoded paths in live config" since they're dated historical artifacts, not active config: archived project snapshots under `.agents/validation/projecthits/**/old/**` (emails like `@dtx.eu`, `dtx_team` fields) and one illustrative example repo name (`dtx-dashboard`) in `docs/directory_tree.md`.
- ✅ `.github/copilot-instructions.md` — **re-checked and found clean**: no `dtx/`, no hardcoded `/home/...` paths, no hardcoded username. An earlier note (in `CLAUDE.md`'s known-gaps section, dated 2026-09-14) named this file as a source of hardcoded-path/`dtx/` contradictions; that appears to have been fixed by commit `8900ac6` ("fix remaining dangling agentic_instructions/github paths repo-wide") and the older note is now itself stale — corrected in `CLAUDE.md` alongside this report.
- ❌ **Hardcoded paths DO exist**: `.vscode/github.code-workspace` (see above) and `setup.sh`'s hardcoded `nmc-costa`/`WORK_REPOS`/`PROJECTS_REPOS` (see §4). Historical/archival content under `.agents/validation/projecthits/**/old/**` also contains old `/home/user/github/...` paths, but these are dated snapshots documenting past work (some files even document the dead-path bug explicitly), not live config.

### 7. Instruções ✅
- ✅ `setup.sh` and `sync-skills.sh` documented with flags
- ✅ Error messages helpful and descriptive

### 8. Links and References ⚠️
- See §9 — the new automated link checker in `scripts/validate_dotfiles.sh` is the current source of truth for this, not a manual claim in this report.

### 9. Functional Verification (new this round)
`scripts/validate_dotfiles.sh` now includes, in addition to the structural checks:
- `bash -n` syntax check on every `*.sh` file in the repo
- A relative markdown-link checker across all tracked `.md` files
- A dry-run smoke test of `./setup.sh --dry-run` and `./sync-skills.sh --dry-run`

Run `./scripts/validate_dotfiles.sh` for current pass/fail counts — do not rely on this report for that; it is a point-in-time snapshot, the script is live.

## Standards Met

| Standard | Status | Notes |
|----------|--------|-------|
| Naming | ✅ | Consistent case across root docs |
| Documentation | ✅ | Clear, bilingual (EN/PT), actionable, gaps labeled rather than hidden |
| Code Quality | ✅ | `bash -n` validated repo-wide (see §9) |
| Structure | ✅ | Logical organization, docs consolidated under `docs/` |
| Consistency | ❌ | `dtx/` reference and hardcoded paths remain — see §4/§6 |
| Completeness | ✅ | All required files present |
| Verification | ✅ | `test-subagents.sh` and `scripts/validate_dotfiles.sh` both available |

## Issues Fixed (this round, 2026-09-15)

1. ❌→✅ This report falsely claimed "no hardcoded paths" and "no `dtx/` references" → **rewritten to state the actual findings** (hardcoded `dtx/repos/...` path in `.vscode/github.code-workspace`, hardcoded `nmc-costa`/repo lists in `setup.sh`)
2. ❌→✅ `docs/STANDARDS.md` presented unimplemented `.copilot/`/`.gemini/`/`.cursor/`/`agent-versions.json` as current structure → **relabeled "proposed / not yet implemented"**
3. ❌→✅ Final Structure section below (and the general MDs list) was out of date after this session's root→`docs/` file moves → **updated**
4. ⚠️ `setup.sh`'s hardcoded repo-list issue is **still open on this branch** — a fix exists on `claude/todo-continuation-and-notes-backlog` (commit `0304d1d`) but has not been merged here; do not describe it as fixed until that lands

## Issues Still Open (not fixed by this round — tracked, not resolved)

1. `.vscode/github.code-workspace` hardcodes a personal `dtx/repos/sp_xai_nos` path
2. `setup.sh` hardcodes `WORK_REPOS`, `PROJECTS_REPOS`, and the GitHub username `nmc-costa` on this branch (fix exists elsewhere, unmerged — see above)
3. **New finding, from running the functional smoke test added this round:** `setup.sh --dry-run` silently mis-parses its own flag. `BASE_DIR="${1:-$HOME}"` takes positional `$1` unconditionally — when invoked as `./setup.sh --dry-run` (no separate base-dir argument), `$1` **is** the string `--dry-run`, so `BASE_DIR` becomes the literal string `--dry-run` instead of `$HOME`. The script still exits 0 and still detects the `--dry-run` flag correctly via its `for arg in "$@"` loop (so dry-run mode itself works), but every printed path is wrong (`--dry-run/Work/codebase` instead of `$HOME/Work/codebase`), and the agent-symlink step silently no-ops (`skip: --dry-run/dotfiles/.claude does not exist`) instead of reporting against the real `$HOME/dotfiles`. Not fixed in this round — flagged here because `scripts/validate_dotfiles.sh`'s new dry-run smoke test only checks exit code 0, which this bug passes despite being wrong; a stricter check would need to grep the output for `$HOME` or absence of the literal string `--dry-run` in printed paths.

## Final Structure

```
dotfiles/
├── .agents/
│   ├── skills/            # 13 entries incl. calls2database, HITs skills, _templates
│   └── workflows/
├── .claude/skills/         # symlinks into .agents/skills/
├── .vscode/
├── .github/
├── scripts/
│   ├── validate_dotfiles.sh   ✅ structural + functional checks
│   ├── monitor_vscode_docs.py
│   └── setup_vscode_monitor_cron.sh
├── docs/
│   ├── AUDIT_REPORT.md         ← this file
│   ├── STANDARDS.md
│   ├── SUBAGENTS_VERIFICATION.md
│   ├── SECRETS.md
│   ├── VSCODE_MONITOR_QUICKSTART.md
│   ├── directory_tree.md
│   ├── requirements.txt
│   └── vscode-docs-monitor.yml
├── .gitignore
├── AGENTS.md
├── CLAUDE.md
├── CHEATSHEET.md
├── GEMINI.md
├── README.md
├── setup.sh          ⚠️ hardcoded repo lists/username, see §4
├── sync-skills.sh    ✅ verified
└── test-subagents.sh ✅ verified
```

## Verification Commands

```bash
# Run structural + functional validator (recommended, current)
cd ~/dotfiles
./scripts/validate_dotfiles.sh

# Run agent/subagent setup checklist
./test-subagents.sh

# Validate syntax individually
bash -n setup.sh
bash -n sync-skills.sh
bash -n test-subagents.sh
bash -n scripts/validate_dotfiles.sh

# Check for the known-remaining dtx/ reference
grep -rn "dtx/" .vscode/*.code-workspace   # currently 1 hit: github.code-workspace
```

## Sign-Off

⚠️ **Repository is usable, but not fully "clean" by this report's own historical claims.** Structure and docs are organized and honest about gaps; two concrete items remain open (§ "Issues Still Open"). Ready for:
- New machine setup: `./setup.sh --dotfiles && ./sync-skills.sh` (works, but the target user must currently be `nmc-costa` or the script must be edited first)
- Skill management: add to `.agents/skills/` and sync

---

**Audited by:** Claude Sonnet 5 (session `session_016gpeGiVkttz3iy2L8hJcgM`)
**Date:** 2026-09-15 (corrects the 2026-09-14 report, which contained the false claims documented above)
**Next Review:** When major structural changes occur, or when the `setup.sh` env-var fix from `claude/todo-continuation-and-notes-backlog` is merged (update §4/§"Issues Still Open" then)
