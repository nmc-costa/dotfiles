# CLAUDE.md

Guidance for Claude Code when working in this repository.

## Quick summary

```
dotfiles/
├── .agents/           ← Source of truth: skills/, instructions/, harnesses/, prompts/, workflows/, validation/, automation/
├── .claude/            ← Claude Code config; .claude/skills/<name> = symlinks into .agents/skills/
├── .github/            ← GitHub + CI config; several subfolders are symlinks into .agents/
├── .vscode/            ← VS Code config (settings.json = real API key, managed by chezmoi+age)
├── .chezmoisource/     ← chezmoi source dir, scoped only to .vscode/settings.json
├── scripts/            ← Utilities (VS Code docs monitor)
├── docs/               ← Everything not auto-loaded by convention (see index below)
├── AGENTS.md, CLAUDE.md, GEMINI.md   ← Auto-loaded by each respective tool
├── docs/SECRETS.md     ← chezmoi+age secrets doc
├── README.md, CHEATSHEET.md
└── setup.sh, sync.sh, test-subagents.sh
```

**Key docs:** `README.md` (overview + full directory tree + human/agent guidelines) · `CHEATSHEET.md` (where things go + persistent TODO) · `docs/STANDARDS.md` (conventions; proposed/not-implemented sections explicitly marked as such since 2026-09-15) · `docs/SUBAGENTS_VERIFICATION.md` (checklist) · `docs/AUDIT_REPORT.md` (audit; corrected 2026-09-15 to reflect real hardcoded paths/`dtx/`) · `docs/SECRETS.md` (chezmoi+age). **Before any structural change, run `./scripts/validate_dotfiles.sh`** — the evaluator that confirms a clean root, required docs present, and this file's/README's tree matching reality.

## Workspace standards (added 2026-09-15)

`.agents/instructions/workspace-config/standards/workspace-standards.yaml` + `workspace-standards.schema.json` define the defaults **every** repo in this workspace must follow (clean root, required README sections, technical language = English, etc.) — each repo has its own instance in `docs/standards.yml` that inherits from these defaults and only declares deviations. `.agents/instructions/workspace-config/standards/RESEARCH_NOTES.md` documents the SOTA research that informed the design (not everything is externally sourced — the README diagram field is the owner's own preference, not SOTA, and is marked as such).

**Periodic review (implicit, runs in the background):** a `SessionStart` hook (`~/.claude/hooks/workspace-standards-review-check.sh`) checks `review.nextDue` at the start of every new Claude Code session and, if it's overdue, injects a strong reminder into context — it doesn't block the session, but the agent is expected to handle it before substantial further work, unless the session's request is clearly narrow and unrelated. For harnesses without hooks (Copilot, Gemini CLI, etc.), the same protocol is described here in prose — read `review.nextDue` in `.agents/instructions/workspace-config/standards/workspace-standards.yaml` at the start of a session and apply the same rule.

Whenever you edit `workspace-standards.yaml`/`.schema.json`, run `python3 scripts/validate_workspace_standards.py .agents/instructions/workspace-config/standards/workspace-standards.yaml` before committing — LLM-generated YAML is more error-prone on indentation than JSON, so this validation isn't optional.

**Open work** (full detail in `CHEATSHEET.md` §4):

| Item | State |
|---|---|
| Back up the age private key (`~/.config/chezmoi/key.txt`) | Manual, pending |
| Authenticate `gh` CLI | **Done 2026-09-16** via browser login (not a manual PAT) — see `CHEATSHEET.md` §4 |
| Adopt `claude/<topic>` + PR convention instead of direct pushes to `main` | **Done 2026-09-16** — 13 PRs opened and merged across `dotfiles`, `architect`, `notes`, `Work/notes`; see `CHEATSHEET.md` §4 |
| Repo hygiene (clean root, README with tree+index+guidelines) — `dotfiles`, `architect`, `~/Projects/notes`, `~/Work/notes` | Done and merged in all 4 repos |
| Archive `agentic_instructions` on GitHub | No longer blocked by `gh auth` — **but see the "⚠️ Known Gaps" verified-merge-status entry below first**: the merge into `dotfiles/.agents/` is only partial, not complete as earlier claimed here |
| Decide sync direction (repo→system vs. system→repo) | **Resolved 2026-09-16**: repo→system only (via `sync.sh` + `setup.sh` file-level symlinks for per-tool instruction files). `setup_agent_symlinks()` was fixed to create file-level symlinks for `CLAUDE.md` rather than whole-directory symlinks. |
| Non-Claude harnesses (Copilot, Gemini, Antigravity) auto-reading `tasks/`+`CHEATSHEET.md` on startup | **Verified via diagnostics 2026-09-16:** fixed for Copilot Chat and Gemini entrypoints; Antigravity received a manual startup fallback and a new `.agents/rules/session-startup.md` to match its discovery paths but still needs one more verification run. Note: Copilot CLI (distinct from Copilot Chat) has no automatic repository-file-reading mechanism — use the manual kickoff prompt for it. See "⚠️ Known Gaps" below |

## What This Repository Is

`~/dotfiles` is the **central configuration and synchronization repository** for:
- AI agents (Crush, Copilot, Gemini, Cline)
- Agent skills and workflows
- Global context and instructions
- Setup and automation

## Structure

```
dotfiles/
├── .agents/                    ← Agents (skills/, workflows/, + harnesses/, instructions/, prompts/, automation/)
├── .claude/                    ← Claude config, incl. .claude/skills/ (symlinks into .agents/skills/)
├── .vscode/                    ← VS Code config (settings.json holds an API key — chezmoi+age managed)
├── .github/                    ← GitHub config; several subfolders are symlinks into .agents/
├── AGENTS.md                   ← Complete agent guide
├── README.md                   ← Overview
├── setup.sh                    ← One-click machine setup (hardcoded for nmc-costa)
└── sync.sh                     ← Synchronize skills
```

*(Note: this section duplicates the "Quick summary" tree above from an earlier version of this file — kept for now, not yet consolidated; treat "Quick summary" at the top as the current one if they ever disagree.)*

## Real Projects

Projects live **outside** dotfiles:
- **`~/Projects/`** — Personal repos (agentic_instructions, HIcode, ibots, roi_lab, etc.)
- **`~/Work/`** — Professional repos (mobai, RAGFusion, sp_xai_nos, etc.)

Each is an independent git repository. See `docs/directory_tree.md` for a map (partly outdated, see `README.md` for the current directory tree).

## Available Skills

Skills are agent extensions. Location: `~/.agents/skills/`

### diagnose-crash
- **Purpose:** Diagnose program crashes via core dumps
- **Triggers:** segfault, SIGABRT, coredumpctl, "why did X crash"
- **See:** `~/.agents/skills/diagnose-crash/SKILL.md`

### omarchy
- **Purpose:** Hyprland/window manager/desktop customization
- **Triggers:** Hyprland, hyprctl, keybindings, themes, gaps, borders
- **See:** `~/.agents/skills/omarchy/SKILL.md`

## Adding a New Skill

1. Create the folder:
   ```bash
   mkdir -p ~/dotfiles/.agents/skills/new-skill
   ```

2. Add `SKILL.md` (required):
   ```markdown
   # New Skill

   Brief description.

   ## Triggers
   - keyword1
   - keyword2
   ```

3. Add other files (optional)

4. Version and sync:
   ```bash
   cd ~/dotfiles
   git add .agents/skills/new-skill/
   git commit -m "Add new-skill for [purpose]"
   git push
   ./sync.sh
   ```

See `AGENTS.md` for the full guide.

## Global Context

README.md/AGENTS.md describe `~/.context-global.md`, `~/claude.md`, `~/directory_tree.md` (symlink to `~/dotfiles/docs/directory_tree.md`) and `agent-versions.json` as symlinks/files of `~/dotfiles/`. **None of these exist on this machine** — don't assume they're present without checking. The sync direction question is resolved (repo→system, via `sync.sh`'s copy and `setup.sh`'s symlinks; never system→repo automatically) — see the next section and the Open work table above.

## New Machine Setup

```bash
cd ~
git clone https://github.com/nmc-costa/dotfiles.git dotfiles-tmp
cd dotfiles-tmp
./setup.sh --dotfiles
# Follow instructions for config checkout
```

Then:
```bash
./sync.sh
```

## Important

- **Don't edit skills in `~/.agents/skills/`** — always edit in `~/dotfiles/.agents/skills/` and sync
- **Skills are shared** — if you add a new skill, every agent sees it
- **Workflows in `.agents/workflows/`** — personas and initializations
- **See `CHEATSHEET.md` for the full workflow** (where things go, agile-workspace roadmap, open TODOs). **Mandatory rule:** any change to the `.agents/` structure (new skill, new harness, a resolved TODO) must update `CHEATSHEET.md` in the same commit — don't leave it for later, that's how this file avoids rotting the way `STANDARDS.md` rotted.

## ⚠️ Known Gaps (audit 2026-09-14, updated 2026-09-16 after a verified re-check of the agentic_instructions merge and a Copilot/Antigravity harness-startup diagnostic)

Don't treat the following files/claims as current truth without checking first:

- **Sync direction resolved 2026-09-16**: repo→system only (via `sync.sh`'s copy and `setup.sh`'s symlinks); no automatic system→repo path — a global learning enters via `claude/<topic>` + PR, same as any other change. Note `setup.sh`/`sync.sh` still may not reflect the machine's real state (e.g. `~/.claude`, `~/.agents`, `~/.vscode` are not symlinks on this machine yet, despite what README/AGENTS.md describe) — that's a "hasn't been run/applied here" gap, not an open design question anymore. Also fixed this round: `setup_agent_symlinks()` used to whole-directory-symlink `~/.claude`, which mixes versioned config with live runtime state (`.credentials.json`, sessions, logs, caches — none of it covered by `.gitignore`'s narrower entries); it now uses a new `setup_agent_file_symlink()` to link only `CLAUDE.md`, leaving the rest of `~/.claude/` real and untouched.
- **`.vscode/settings.json` contains a real API key** for a custom endpoint. The repo is private/personal use (a risk the owner accepts), but don't propagate this file to other repos, examples, or shared contexts. **TODO:** migrate to chezmoi+age (decided, not yet executed — blocked on `sudo pacman -S chezmoi age`, which needs an interactive password).
- **`setup.sh` has hardcoded repo lists** (`WORK_REPOS`, `PROJECTS_REPOS`) and the `nmc-costa` username hardcoded in `clone()` (SSH/HTTPS URLs) — not portable to another user without editing the script directly. **Note:** a fix exists (env vars `GITHUB_USER`/`WORK_REPOS`/`PROJECTS_REPOS`) in commit `0304d1d` on branch `claude/todo-continuation-and-notes-backlog`, but **isn't merged** into that branch's target or `main` — don't assume it's resolved until that branch lands.
- **`.vscode/github.code-workspace` has a hardcoded path** `"dtx/repos/sp_xai_nos"` — a real reference to `dtx/` still in the repo (verified 2026-09-15, the only hit outside historical/archived content).
- **`agentic_instructions` → `dotfiles` merge is only partial, verified 2026-09-16 (previous claim here was overstated)**: genuinely merged/ported are the 6 HITs persona skills + `archi` (adapted from `architect`), `instructions/{base-personas,task-personas,workspace-config,automation}`, the harness guides, `prompts/chronicle/*`, `memories/CURRENT_SESSION.md` (byte-identical), and `calls2database`/`project-doc-lifecycle`/`simplifyHIT`. **Not merged, and not yet judged obsolete-or-worth-porting**: `.copilot-instructions` (a 13.8KB Copilot enforcement blueprint — but see note below, it turned out to be a CRISP-ML(Q) ML-pipeline coding standard unrelated to this repo's scope, not a dotfiles gap), the `tests/agents/*.py` pytest compliance suite (same CRISP-ML(Q) scope, likely also out of scope for dotfiles), and `docs/_ARCHITECTURE/`, `docs/_INTRO/`, `docs/_REFERENCE/`, `docs/_STATUS/` (confirmed obsolete: these are the old repo's own centralized-vs-distributed architecture debate, referencing a `/home/user/github/my/agentic_instructions/` path that was never real on this machine — dotfiles' current single-control-plane design is the actual, working resolution of that exact debate). `scripts/deploy-agentic-framework.sh`/`heartbeat.py`/`setup/quickstart_optimize.py` are tied to that same old deployment model, superseded by `setup.sh`/`sync.sh`. `REGISTRY.md` and `config/.harnesses/*.json` look like deliberate improvements-over, not losses (the JSON harness configs contained fictional fields like a made-up `api.anthropic.com/v1/claude-code` endpoint). **Bottom line: archiving `agentic_instructions` is safe whenever the owner decides to (archiving doesn't delete — full history stays readable), but don't repeat "it's already fully merged" as fact.**
- **Non-Claude harnesses weren't wired to auto-read `tasks/`+`CHEATSHEET.md` on startup — fixed 2026-09-16, round 1; verified with a real diagnostic prompt 2026-09-16, round 2**: round 1 added a startup pointer to `.github/copilot-instructions.md`, `GEMINI.md`, `AGENTS.md`'s sessionHygiene section, and a new `.agents/harnesses/antigravity.md` (a manual-prompt fallback, since nobody had confirmed Antigravity's real discovery mechanism yet). Round 2 asked Copilot and Antigravity directly, with real answers: (1) **Copilot CLI** (as opposed to Copilot Chat in VS Code) has no automatic repository-file-reading mechanism at all — the `.github/copilot-instructions.md` fix only helps Copilot Chat, and there's nothing a repo file can do for the CLI; use the manual kickoff prompt there. (2) **Antigravity** self-reported a real, specific discovery mechanism: it walks up from the open file to the repo root looking for `GEMINI.md`, `AGENTS.md`, and `.agents/rules/*.md` (never `CLAUDE.md`, `CHEATSHEET.md`, or the Copilot file) — so the fix was extended with a dedicated `.agents/rules/session-startup.md` matching that exact convention. The same diagnostic session, however, reported reading *zero* files automatically despite describing this mechanism, flagging its own uncertainty about whether the session was rooted correctly — **re-verify from inside `~/dotfiles` before trusting this is fully live** (see `.agents/harnesses/antigravity.md`'s checklist). Claude Code alone is confirmed to get this automatically via a real `SessionStart` hook.

**Resolved this round (no longer a gap):**
- `.agents/` and `.github/` no longer have duplicated/orphaned content — `.github/{harnesses,instructions,prompts,automation,CONTRIBUTING.md,skills/project-doc-lifecycle}` are now symlinks into `.agents/`, and every dead path to `/my/agentic_instructions/...` and `/home/user/github/...` was fixed or replaced with a note explicitly documenting the old bug. `.claude/skills/` also stopped diverging from `.agents/skills/`: the 9 HITs skills (`archi`, `diagramhits`, `documenthits`, `mockuphits`, `presenthits`, `projecthits`, `reviewhits`, `simplifyhit`, `project-doc-lifecycle`) now live as real content in `.agents/skills/`, with `.claude/skills/<name>` as a symlink.
- `docs/AUDIT_REPORT.md` and `docs/STANDARDS.md` no longer contain false claims presented as current truth. `AUDIT_REPORT.md` was rewritten (2026-09-15) to accurately report that `dtx/` and hardcoded paths **do** exist (see above) instead of denying it — `.github/copilot-instructions.md`, which the earlier note also flagged as a source of contradiction, was re-verified and is clean (fixed in commit `8900ac6`, before this round). `STANDARDS.md` was rewritten to mark `.copilot/`, `.gemini/`, `.cursor/`, `agent-versions.json`, and the `agent-framework` repo as **`[PROPOSED — not implemented]`** instead of presenting them as current structure. Both files still need a critical read (they document open work by nature), but no longer lie about the repo's current state.
- Skills `omarchy`/`diagnose-crash` verified byte-for-byte against `/usr/share/omarchy/default/agents/skills/{omarchy,diagnose-crash}` on 2026-09-16 (`diff -rq`, no output — still identical). The one real gap found (the `omarchy agent` launcher subsystem, documented only in `omarchy.org/manual/ai/`, not in the vendored files) is covered by `.agents/skills/omarchy/LOCAL_ADDENDUM.md`, which also records the plugin manifest standard and the VoxClaude vs. `omarchy-voice` trade-off for voice-to-agent.

## Documentation

- **`AGENTS.md`** — Complete guide (agents, skills, workflows, troubleshooting)
- **`README.md`** — Overview, directory tree, and structure
- **`docs/SUBAGENTS_VERIFICATION.md`** — Setup and verification checklist

---

**For project-specific work:** see repos in `~/Projects/` or `~/Work/` — each has its own `CLAUDE.md`.
