# Kickoff: task-tracking system for the workspace

**Status:** not started. This file is the seed — read it, then plan, then build.
**Created:** 2026-09-15, at the end of a long session that built the repo-hygiene
pattern and the `workspace-standards` schema this task must comply with.

This is the prompt to paste into a **new** Claude Code session (fresh
context — cheaper than `--resume`, which reloads everything; see
`sessionHygiene` in `.agents/instructions/workspace-config/standards/workspace-standards.yaml`,
which is the default this file itself is an example of applying).

---

## Copy from here down into the new session

Read `~/dotfiles/CLAUDE.md` and `~/dotfiles/CHEATSHEET.md` first, then this file
(`~/dotfiles/tasks/KICKOFF.md`) — it's your starting point for planning and
implementing a task-tracking system for the whole workspace.

### What's already decided, and what isn't yet

**Decided (don't re-decide):**
- Lives in `~/dotfiles/tasks/` — a folder in this repo, **not a standalone repo**.
  This was the explicit instruction of this session's owner ("it seems clear to
  me that... a tasks/ folder in dotfiles looks like the best place").
- It's the foundation for the ideas in `~/Projects/notes/ideas/architecture/Workspace Agil
  para Agentes Multiplataforma.md` (main doc) and `~/Projects/notes/ideas/agents/
  Agente Orquestrador - Jarvis do Diretor Humano.md` (human-orchestration layer
  on top). **Read both before designing anything** — they already have closed
  decisions (section "Decisões Fechadas"/`D1`-`D14` in the first document) that
  this system has to respect, not reinvent.
- Has to comply with the `workspace-standards.yaml` already created this
  session (`.agents/instructions/workspace-config/standards/`) — clean root,
  README with Directory tree + What's where (index) + Guidelines (For you/For
  agents), validated by `scripts/validate_workspace_standards.py`.

**To be decided in this next session — don't assume, resolve with real investigation:**

1. **Tension to resolve first:** the Jarvis document (§16, "How to Host: the
   Repo is the Agent") explicitly proposes a **dedicated repo** for the
   Architect with `worksheets/tarefas.csv` inside it — the opposite of the
   "folder in dotfiles" decision made now. Don't silently ignore this: read
   §16 in full, and decide explicitly — either (a) the `tasks/` folder in
   dotfiles replaces that dedicated repo and §16 is now outdated (say why,
   and correct that document), or (b) `tasks/` in dotfiles is just the
   *layer* and Jarvis's own repo still makes sense for something else (say
   what). Don't move ahead with implementation without closing this out.
2. **Format:** the Workspace Agil doc already decided (`D9`) on an append-only
   JSONL event log as the source of truth, with SQLite/DuckDB as a disposable
   index — and no knowledge graph. Jarvis proposes `tarefas.md`/`tarefas.csv`
   with fixed columns (`id`, `título`, `projeto`, `estado`, `energia`,
   `estimativa`, `prazo`, `bloqueado_por`, `origem`, `criado`/`tocado` — see
   Jarvis §5.2, its original Portuguese column names). Reconcile the two: this
   repo's `tasks/` is probably the *worksheets* (a readable master table), not
   the event log itself (which already has a home decided in D11 — the
   workspace's central repo, which may or may not be this same `tasks/`,
   confirm).
3. **Real initial scale:** this workspace already has ~11 open branches across
   4 repos waiting for PR/merge from this session (see `CHEATSHEET.md` §4 and
   the branch list at the bottom of this file) — **use these as the first real
   tasks** to enter the system, not invented sample data. It's the most honest
   test of whether the design holds up to real use from day one.
4. **Minimal PoC before building everything:** Jarvis (§14) already explicitly
   argues for starting with the smallest possible PoC (static worksheets, no
   notifications, no live session) before any automation. Follow that advice
   here too — don't build the scheduled job/dispatcher before validating that
   the table itself is reliable and useful.

### How to orchestrate this (parallel agents were explicitly requested)

**Phase 1 — Planning (blocks phase 2, don't skip):**
Launch agents in `Plan` mode (read/investigate only, no file writes) in
parallel, one per question, so you don't lose the whole day reading the
documents by hand:
  - One agent reads the entire Workspace Agil doc (it's large, ~2000 lines)
    and extracts only what's relevant to `tasks/`: D9, D11, §4.5, §5 (if it
    exists; confirm the current section number), §14.3, and the task table
    in §0.6.
  - One agent reads the entire Jarvis doc and extracts: §5 (worksheets,
    `tarefas.md` schema), §14 (minimal PoC), §16 (hosting — the tension in
    point 1 above).
  - One agent reads `workspace-standards.schema.json`+`.yaml` and
    `scripts/validate_workspace_standards.py` (including the already-
    implemented `extends` resolution) to know exactly what rules `tasks/`
    has to comply with.
  - Merge the three reports yourself (the main session, not another agent)
    and write a concrete plan — column schema, file format (a small `.md`
    vs. `.csv` above a few hundred lines, already the Workspace Agil doc's
    own rule), and the explicit resolution of the tension in point 1.
  - **Before implementing, run `EnterPlanMode`/present the plan to the owner
    and wait for approval** — this is a new architecture decision, not a
    mechanical fix like the rest of this session.

**Phase 2 — Implementation (only after phase 1 is approved):**
Parallel agents per component, each on a `claude/tasks-<something>` branch
(never `main` directly, same pattern as this whole session):
  - Base files (`tasks/tarefas.md` or `.csv`, `tasks/README.md` with the
    index/guidelines already established)
  - `tasks/standards.yml` (a workspace-standards instance that `extends`
    the central file)
  - A dedicated validator (`scripts/validate_tasks.py` or similar — follows
    the pattern of `scripts/validate_workspace_standards.py`/
    `validate_dotfiles.sh`)
  - Real seed data: this session's ~11 pending branches, as table entries

After each component passes the validator, merge it all together, run
`./scripts/validate_dotfiles.sh`, push the branch, hand back the compare
link — don't open a PR (`gh` isn't authenticated on this machine, confirm
whether that's changed).

### State at the end of the previous session (2026-09-15) — verify before trusting

Branches awaiting PR, all in `nmc-costa/dotfiles` except where marked:
- `claude/todo-continuation-and-notes-backlog`
- `claude/repo-hygiene-dotfiles`
- `claude/workspace-standards-schema` (the most recent — this file lives there)
- `nmc-costa/architect`: `claude/env-leak-fix`, `claude/repo-hygiene-architect`, `claude/workspace-standards-schema`
- `nmc-costa/notes`: `claude/repo-hygiene-notes`, `claude/ideas-review-fixes`, `claude/workspace-standards-schema` (⚠️ this last one diverges from `repo-hygiene-notes` — see `CHEATSHEET.md`)
- `DTx-DSML/notes`: `claude/repo-hygiene-worknotes`, `claude/workspace-standards-schema`

**Don't assume this is still true** — run `git -C ~/dotfiles branch -a` (and
the equivalent in the other 3 repos) and `gh auth status` to confirm the
real state before acting on this list.

---

## End of what to copy

If the new session reaches its own natural conclusion (e.g. phase 1 done,
phase 2 is large and independent work), apply the same rule
(`sessionHygiene`) to it — suggest a new session, hand back a kickoff
prompt, update this file or `CHEATSHEET.md` with what's done before ending.
