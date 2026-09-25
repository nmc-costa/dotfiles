# CHEATSHEET.md

How work happens in this workspace, in one place — so you don't have to remember it. Update this table whenever the `.agents/` structure changes (it's a rule, see `CLAUDE.md`).

## 1. Where everything lives

| You want to... | Go to... |
|---|---|
| Add/edit a skill (Claude Code, Copilot, Gemini) | `.agents/skills/<name>/SKILL.md` — the **single real source**. `.claude/skills/<name>` and `.github/skills/<name>` are symlinks to it, never edit there. |
| Add/edit a persona or instruction | `.agents/instructions/{base-personas,task-personas,workspace-config,automation}/` |
| Add/edit a harness guide (Claude Code, Gemini, OpenAI, LiteLLM, VS Code Copilot) | `.agents/harnesses/<name>.md` — use `.agents/harnesses/TEMPLATE.md` as a starting point |
| Add/edit a reusable prompt | `.agents/prompts/{chronicle,_templates}/` |
| Store a real output (validation, client example, session) | `.agents/validation/<skill>/` — never in `.agents/skills/<skill>/examples/` (that folder is only for generic/anonymized examples) |
| Check the state of the `agentic_instructions` → `dotfiles` merge | `CLAUDE.md` → "⚠️ Known Gaps" section |
| Leave/find a session-continuity handoff | `HANDOFF.md` — uppercase, singular, always at the root of whatever scope it describes: `~/HANDOFF.md` (global cross-repo index), `<repo>/HANDOFF.md` (repo-wide), `<repo>/<subsystem>/HANDOFF.md` for a subsystem that already has its own top-level docs (e.g. `tasks/HANDOFF.md`). Not permanent — update in place, delete/archive once its "still pending" list is empty. |
| Add/edit a harness startup hook (e.g. Claude Code `SessionStart`) | `.agents/hooks/` — see `.agents/hooks/README.md`. `sync.sh` mirrors scripts to `~/.claude/hooks/` and merges `session-start-hooks.json` into the live `~/.claude/settings.json` (add-only, idempotent — that file also holds local runtime state, so it's never a straight symlink). |

**Golden rule:** if you edited something inside `.claude/skills/` or `.github/skills/` directly, you edited a conceptually broken symlink — the real file is in `.agents/skills/`. Confirm with `readlink -f <path>` before editing if unsure.

## 2. Adding a new skill (full flow)

```bash
mkdir -p ~/dotfiles/.agents/skills/new-skill
cat > ~/dotfiles/.agents/skills/new-skill/SKILL.md <<'EOF'
---
name: new-skill
description: <what it does and when to use it>
---
EOF

# symlink so other harnesses can read it too
ln -s ../../.agents/skills/new-skill ~/dotfiles/.claude/skills/new-skill

cd ~/dotfiles
git add .agents/skills/new-skill/ .claude/skills/new-skill
git commit -m "Add new-skill for [purpose]"
git push
```

## 3. The 3 repos and each one's role

| Repo | Role | State |
|---|---|---|
| `~/dotfiles` | Single control-plane repo: system config + `.agents/` (skills/instructions/harnesses/validation) as the source of truth | Active, this is where you work going forward |
| `~/Projects/agentic_instructions` | Original persona/skill library | Content only **partially** merged into `dotfiles/.agents/` — see `CLAUDE.md` → "⚠️ Known Gaps" for the real, verified breakdown (2026-09-16) before archiving; don't edit, history only |
| `~/Projects/architect` | Personal research playground for the "The Architect" persona/memory/self-evaluation | Separate, not merged — has a "red by design" test pattern worth copying to `.agents/validation/` in the future, but the content itself (memory/, evolution/, architect_log/) stays there |

## 4. Persistent TODO list (source of truth across sessions)

The task list Claude Code creates within a session (the internal tracking tool) **doesn't survive a new session** — it only survives with `--resume`/`--continue`, which reloads everything (the opposite of saving tokens). This table is the persistent substitute: any new session reads this, recreates its own internal todo list from it, and **checks it off here** (not just in-session) when an item is done.

- [x] Migrate `.vscode/settings.json` (API key) to chezmoi+age — done 2026-09-14, commit `ef2a52f`. Still missing: back up the private key (`~/.config/chezmoi/key.txt`) to a password manager or physical copy — **this is manual, nobody does it for you**.
- [x] **Authenticate the `gh` CLI** — done 2026-09-16 via browser login, not a manual PAT (a method validated by real community research, not just personal preference — see `.agents/instructions/workspace-config/standards/RESEARCH_NOTES.md`). **This is the step to repeat on any new machine, it's simple and fast:**
  ```bash
  gh auth login
  # GitHub.com → SSH (git protocol; uses your already-configured SSH keys)
  # Authenticate Git with your GitHub credentials? → Yes
  # Upload your SSH public key? → No, if it's already on the account (push already working = it's already there)
  # How would you like to authenticate GitHub CLI? → Login with a web browser
  #   (NEVER "Paste an authentication token" — avoids having a manual PAT to manage/lose/expose)
  gh auth status   # confirm: token gho_..., scopes repo+read:org(+gist)
  ```
  Token managed by `gh`'s own keyring, never hand-written to any file; revocable at `github.com/settings/applications`. If you ever genuinely need a manual PAT (headless/CI use, not this case), the community pattern is a `GH_TOKEN` environment variable, never a plaintext dotfiles file.
- [x] **Adopted the `claude/<topic>` + PR convention** instead of pushing directly to `main` — 13 PRs opened with `gh pr create` (2026-09-16) covering `dotfiles`(6), `architect`(2), `notes`(3), `Work/notes`(2). All were reviewed and merged by the owner (2026-09-16). `tasks/OPEN_PULL_REQUESTS.md`, which tracked the list and merge order, has been removed now that its job is done (its own closing note said to do this).
- [x] All local commits were pushed and had a PR opened — nothing stayed local-only.
- [x] `tasks/` event log synced with reality — the 11 "open a PR" tasks were stale (`todo`) after their PRs merged; closed out via `append_event.py` (see `tasks/board.md`, PR #7).
- [ ] Archive `agentic_instructions` on GitHub (Settings → Archive this repository, or `gh repo archive nmc-costa/agentic_instructions`) — no longer blocked (`gh auth` works), but **do this only after** resolving the still-unmerged content flagged in `CLAUDE.md` → "⚠️ Known Gaps" (2026-09-16 verification found the "already merged" claim here was overstated).
- [x] **Decide sync direction (repo→system vs. system→repo)** — resolved 2026-09-16: repo→system only, no automatic system→repo path; a global learning enters via `claude/<topic>` + PR like any other change. Found and fixed in the same pass: `setup_agent_symlinks()` whole-directory-symlinked `~/.claude` (mixes versioned config with live runtime state — `.credentials.json`, sessions, logs, none of it covered by `.gitignore`'s narrower entries), replaced with a new `setup_agent_file_symlink()` that links only `CLAUDE.md`. Generalized same day to every other tool confirmed (via its own docs) to have a real per-user global file — Gemini CLI, OpenAI Codex CLI, GitHub Copilot CLI — each now a thin pointer in `dotfiles/.<tool>/<file>` to `.agents/instructions/workspace-config/`; fixed `AGENTS.md`'s stale claims (a fictional unified `~/.context-global.md`, and a "Broken Symlinks" section that told readers to `ln -sf` the whole `~/.claude` directory) along the way. See `CLAUDE.md` → Known Gaps for detail.
- [ ] `setup.sh` has hardcoded repo lists (`nmc-costa`) — known, not blocking, only matters if you share the repo.
- [x] **Non-Claude harnesses didn't auto-read `tasks/`+`CHEATSHEET.md` on startup** (found 2026-09-16 via Copilot/Antigravity diagnostics the owner ran directly) — fixed round 1 (startup pointer added to `.github/copilot-instructions.md`, `GEMINI.md`, `AGENTS.md`), then **verified round 2 with a second real diagnostic prompt, same day**: Copilot CLI (not Copilot Chat) has no auto-read mechanism at all, nothing fixes that on the repo side; Antigravity self-reported it actually scans for `GEMINI.md`/`AGENTS.md`/`.agents/rules/*.md` — added a matching `.agents/rules/session-startup.md` — but the same test showed zero files actually auto-loaded in that session, so it's not confirmed live yet.
- [ ] **Re-verify Antigravity's startup wiring from inside `~/dotfiles`** (not a parent/unrelated directory) — round 2's diagnostic described the right mechanism but reported nothing was actually auto-loaded; see `.agents/harnesses/antigravity.md`'s checklist for the exact re-test.
- [x] **New skill `gauntlet-prompting`** (2026-09-25, card `dotfiles-tsk-skill-gauntlet-prompting`) — compiles a goal + a real, fetchable exemplar into a short Gauntlet Loop kickoff prompt (Matt Shumer's builder → blind critic → loop method) for a fresh Claude/Copilot/Antigravity session. Deterministic parts in `scripts/render_prompt.py` + `scripts/gauntlet_ledger.py` (A/B shuffle, verdicts, stop rule; state under `~/.local/state/gauntlet/`), tests in `scripts/test_gauntlet.py`. Owner decisions: 3 rounds per piece, always hand off. Symlinked into `.claude/skills/` and `.github/skills/`. Design: `tasks/plans/skill-gauntlet-prompting.md`.

**Rule:** when starting a new session, explicitly ask it to read this list and build its internal todo list from it (see section 7). When finishing a task, the commit that closes it must check the `[x]` off here.

## 5. "Agile Workspace" roadmap (order validated in your own notes — `~/Projects/notes/ideas/architecture/Workspace Agil para Agentes Multiplataforma.md` §13.7)

Don't skip phases — each one is a prerequisite for the next. The autonomous optimizer ("living OS") is the **last** phase, not the first.

| Phase | What | State in this workspace |
|---|---|---|
| 1. See | `agtop` + Claude Code's Langfuse/OTel | To do |
| 2. Tidy up | chezmoi + shared rules + secrets | **In progress** (TODO #1 above) |
| 3. Limit | Per-machine limit profiles, `RandomizedDelaySec` | To do |
| 4. Schedule | `jobs/*.yaml` manifest + systemd timers | To do |
| 5. Structure | Common task→swarm→agent→model→state schema | To do |
| 6. Judge | Verifiable acceptance criteria | To do |
| 7. Choose | **Model routing by cost/performance** — `LiteLLM Router` (not RouteLLM, unmaintained since 2024). Local: Ollama + Qwen3-Coder-30B (24GB VRAM) or Qwen3-8B (8GB). Cloud: DeepSeek V4 (cheap/high-volume), Claude Sonnet 5 (default), Claude Opus 5 (hard reasoning) | Documented, not yet installed |
| 8. Optimize | GEPA over a real skill, measuring before/after | To do — depends on 4-6 being done; independent evidence says multi-agent gains are unstable, measure before trusting |

## 6. Keeping this alive

This table rots like any static doc if nobody updates it. The rule lives in `CLAUDE.md`: any session that changes the `.agents/` structure (new skill, new harness, a TODO resolved) updates this table in the same commit — not later, not "whenever convenient."

## 7. Jumping to a new session without losing the thread (saving tokens)

1. Close/ignore the current session — you don't need `/compact` or `--resume`. Open a new session (`claude`, without `--resume`/`--continue`, clean context).
2. First message, always:
   > "Read `~/dotfiles/CLAUDE.md` and `~/dotfiles/CHEATSHEET.md`. Build a todo list from section 4 (persistent TODO list) and continue from there."
3. The new session builds its own internal todo list (Claude Code's tracking tool) mirroring section 4 — this keeps it focused and visible to you within that session.
4. When an item is done, it has to be checked `[x]` **here**, in section 4, in the same commit that closes it out — the session's internal todo list dies with it; this table is what survives.
