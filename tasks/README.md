# tasks/

**Quick command reference: `tasks/CHEATSHEET.md`.** This file explains the
model and the decisions; the cheatsheet is the "how do I actually do X"
lookup — start there if you just need a command.

Workspace task-tracking system (PoC). Lives here, not in a separate repo —
decision fixed by D2/D7 of the "Workspace Agil" doc (`Repo-Cerebro` =
`dotfiles/`) and D11 (events go into the workspace repo's central log).
Full decision context: `KICKOFF.md` (the original request) and the plan
that resolved the tensions it left open lives in the session that
implemented it — see `notes/ideas/architecture/Workspace Agil para Agentes
Multiplataforma.md` (D1-D18) and `notes/ideas/agents/Agente Orquestrador -
Jarvis do Diretor Humano.md` (task schema, §5.2) as sources.

## Model: two layers

1. **`events.jsonl`** — append-only event log. It is the **source of
   truth** (D9/D10): every line is a fact that happened, a written line is
   never edited — a correction is always a new event. Never hand-edit.
2. **`board.md`** — table generated from the log (columns per §5.2 of the
   Jarvis doc: id, title, project, status, energy, estimate, deadline,
   blocked_by, origin, created, touched). It's a **disposable, rebuildable
   view**, never hand-edited — the PoC-scale equivalent of the
   SQLite/DuckDB index D9 describes for larger scale.

## How to use

Append an event (the only way to write to the log):

```bash
python3 tasks/append_event.py --type task.created \
  --actor-kind human --actor-id nmc-costa \
  --task-id dotfiles-my-task \
  --payload '{"title":"...", "project":"dotfiles", "energy":"mechanical", "origin":"me"}'

python3 tasks/append_event.py --type task.status_changed \
  --actor-kind human --actor-id nmc-costa \
  --task-id dotfiles-my-task \
  --payload '{"status":"in progress"}'
```

Regenerate the table after any change to the log:

```bash
python3 tasks/rebuild_view.py
```

This is the original PoC flow (free-form `status`, `board.md`). For the
6-phase lifecycle, metrics, and handoff notes (`move_task.py`,
`kanban.md`, `metrics.md`) see `tasks/CHEATSHEET.md` instead — both flows
read the same `events.jsonl` and stay in sync, `move_task.py` is just the
newer, more specific tool.

**Language note (2026-09-16):** English is the default vocabulary for new
events — event types (`task.created`, `task.status_changed`), `actor.kind`
(`human`/`agent`/`swarm`), and payload keys (`title`/`project`/`status`/
`energy`/`estimate`/`deadline`/`blocked_by`/`origin`). Events written
before that date used a Portuguese vocabulary (`tarefa.criada`,
`humano`/`agente`, `titulo`/`projeto`/`estado`/...) — the log is
append-only, so those historical lines are never rewritten.
`rebuild_view.py` reads either vocabulary (falls back to the Portuguese key
when the English one is absent), so old and new events project into the
same `board.md` columns without loss.

## Statuses (D12)

`new -> todo -> in progress -> in review -> done`, plus `deferred` as a
parallel lane (any status can move to `deferred` and back — it's not a
step in the main sequence). `blocked` and `abandoned` (the older enum from
the Jarvis doc) aren't statuses of their own in this PoC: "blocked" is any
status with `blocked_by` filled in; "abandoned" is a task going quiet with
no new events, signaled by `touched` (staleness), with no dedicated status
column.

`deferred` was added 2026-09-16, informed by the `communityFirst` default's
landscape scan (see `RESEARCH_NOTES.md` in
`.agents/instructions/workspace-config/standards/`): `claude-task-master`
(28k stars) has this status in its kanban and ours didn't — it covers
"park without cancelling" (different from `abandoned`, which is
passive/by staleness, and different from `blocked`, which is waiting on
another task). It's documentation + payload convention only —
`append_event.py` already accepts a free-form `status`, there's no enum to
widen in code.

**Considered and not adopted**: `Backlog.md`'s (6.7k stars) `AC:BEGIN`/
`AC:END` convention for delimiting acceptance criteria inside a long
per-task file. Doesn't apply to the current design — `board.md` is a flat
table generated from the log, not one file per task with internal
sections. Revisit only if/when a task needs multi-item acceptance criteria
that justify that structure.

## Provenance decides the entry point (D13)

A task created by a human enters `todo` directly. A proposal from an agent
(`actor.kind: agent`) enters `new`, with a quota of 3 simultaneously open
proposals, a 14-day expiry, and dedup by `payload` fingerprint — all
applied automatically by `append_event.py`, not by human convention (D14:
script before rule).

## Out of scope for this PoC

A SQLite/DuckDB index, `tasks.csv` (only once `board.md` passes "a few
dozen lines" — the Jarvis doc's own §5.4 rule). See the history of the
session that created this for the full reasoning.

**No longer out of scope, superseded 2026-09-18:** automation
(cron/systemd) and the Jarvis/orchestrator persona were ruled out-of-scope
for the original PoC — that's now reversed, see the section below. The
reversal is deliberate, not scope creep: the earlier decision assumed the
orchestrator would have to be *built*; the 2026-09-18 research found most
of the execution/observability engine already exists (adopted, not
built), which is what made automating the remainder tractable.

## Orchestration architecture (decided 2026-09-18, not yet implemented)

This section documents an architecture **decision**, not a shipped
feature — nothing below exists on disk yet except this description.
Implementation is Phase 1+ of the plan; see "Status" at the end of this
section for what's actually done.

### Why this exists

The owner wants multiple AI coding-agent CLIs (Claude Code, GitHub
Copilot CLI, Gemini CLI) to be able to pick up this `tasks/` folder
independently and in parallel — "posso dizer ao Claude Code para pegar na
pasta tasks e voltar ao trabalho, e em paralelo dizer ao Copilot CLI para
se focar noutras tasks" — with a real-time view (a Kanban board) of what
every concurrent agent team is doing, so a human can glance once instead
of babysitting every session. Full requirements, research, and rejected
alternatives are preserved in the session that made this decision
(2026-09-18); this section is the durable summary.

### The decision: 4 layers, adopt 2 of them

| Layer | What it is | Decision |
|---|---|---|
| **L1 — task contract** | The file format any CLI reads/writes to claim and update a task | **Build, thin.** Extends `events.jsonl` (this file's existing log) with file locking and git-ref compare-and-swap claiming (pattern from `tasksmd/tasks.md`), plus one markdown+YAML-frontmatter card per task (format adapted from `Backlog.md`/`antopolskiy/kanban-md`) |
| **L2 — execution engine** | Spawns agents, tiers model capability per stage, isolates concurrent work | **Adopt.** Claude Code's own `Workflow` tool (`phase()`, `agent(prompt, {model, effort})`, `isolation: 'worktree'`, `parallel()`/adversarial-verify/judge-panel patterns) for the Claude side; `asheshgoplani/agent-deck` (Go, MIT, 9 CLI vendors incl. Copilot, worktree isolation w/ sparse checkout, Telegram/Slack/ntfy bridge) for Copilot/Gemini |
| **L3 — observability** | Live view of what every agent is doing | **Adopt.** `herdr` (already installed, v0.8.2 — Rust/Ratatui terminal multiplexer, 18+ CLI integrations, `plugin pane open` for popups, `notification show`, `pane.agent_status_changed` events) + Agent Deck's fleet TUI/web dashboard + Claude Code's `claude agents --json` and `~/.claude/jobs/<id>/{state.json,timeline.jsonl}` for per-session telemetry (`detail`, sub-agent `fan[]`) |
| **L4 — policy & escalation** | Per-phase model tiers, WIP limits, review SLA, human escalation | **Build — this is the actual gap.** A `tsk` CLI + a `tsk daemon` (systemd `--user`, separate from any interactive session so it survives session close/compaction) reading `tasks/policy.yaml`. Estimated ~600 LOC total, not a few thousand — most of the system is adopted, not written |

`tuiboard` (`NazzarenoGiannelli/tuiboard`, MIT, already herdr-native) is
the first thing to evaluate for the Kanban board UI itself before writing
any Rust — see "Decided answers" below.

### Task lifecycle (supersedes "Statuses (D12)" above, once `tsk` ships)

```
backlog -> planning -> in_progress -> review -> validation -> done
                                         \                      ^
                                          \-------- blocked ----/
(deferred stays a parallel lane, unchanged from D12)
```

Migration from the current vocabulary is lossless: `new -> backlog`,
`todo -> backlog (ready)`, `in progress -> in_progress`,
`in review -> review`, `done`/`feito -> done`. `deferred` and
`blocked_by`-driven `blocked` carry over unchanged.

`review` and `validation` are new stages, not a renaming: `review` is an
automated judge-panel pass (per `policy.yaml`'s `review.judges`);
`validation` is the final sign-off, by a human or — only after the SLA
elapses with no human action — the orchestrator model. A card's
percentage-complete is derived from a checkpoints list on its card file,
never from a model self-reporting a number (LLMs are known to drift a
self-estimate toward ~90% and stall there).

### Decided answers (2026-09-18)

These resolve the open questions the architecture research raised. Where
the owner gave a concrete rule beyond a simple yes/no, it's recorded
here verbatim in intent, since it changes `policy.yaml`'s shape once
built:

- **Orchestrator = a separate systemd-user daemon**, never the
  owner's interactive Claude Code session (a session can close or get
  compacted; the SLA below has to survive that).
- **Review SLA: 4 hours.** If no human acts on a card in `validation`
  within 4h, the orchestrator model validates automatically instead.
- **Automode budget cap: 3 sessions/day, 2 loops per agent per task.**
  If a task exceeds 2 loops, it goes straight to `validation` and — unlike
  the normal 4h-then-orchestrator-fallback path — **a human is the only
  valid validator for that card**, no automatic orchestrator fallback.
  This is a harder rule than the general SLA: it exists specifically to
  stop a stuck agent from burning budget in a retry loop unsupervised.
- **The owner is "the director":** whenever the main/orchestrator agent
  is engaged by the owner, it should ask what tasks they want worked on
  rather than silently picking its own priorities — the daemon's
  autonomous dispatch (§L4) is for *already-approved* backlog items, not
  a way to bypass the owner deciding what starts.
- **TUI: evaluate `tuiboard` before writing anything in Rust — done,
  2026-09-18, passed.** Safe (no install scripts, no hidden network calls),
  local (plain markdown + read-only local session files), fast (~165MB
  RSS, near-instant startup), and confirmed to correctly move a task
  through our full 6-stage lifecycle by editing the board file directly
  (tuiboard has no interactive move-column command — it's watch-and-render
  only via `chokidar`, which is exactly the shape `tsk` needs). Full
  writeup, captured states, and example files in
  `tasks/evaluations/tuiboard/README.md`. Still no from-scratch Ratatui
  board planned unless this candidate falls through for a reason found
  later (e.g. multi-vendor agent detection, not yet tested).
- **`tasks/` stays inside `dotfiles/`** (per D2/D7 above) — only the
  `tsk daemon` ever commits changes to `tasks/`, never an individual
  agent session, to avoid the exact concurrent-working-tree collision
  that produced a real bug in this repo's history (`tasks/` and repo code
  are different concurrency domains: code always gets one worktree per
  claimed task; `tasks/` itself never does).

### Still open

- Whether `agent-deck` and `herdr` overlap enough to only need one, or
  are genuinely complementary (herdr = panes/TUI/notifications, Agent
  Deck = worktree engine + notification bridge) — first thing to test.
- `.github/copilot-instructions.md`'s "Known Gaps" claim that Copilot CLI
  has no automatic repo-file-reading mechanism is likely stale (GitHub's
  own docs describe `AGENTS.md`/`CLAUDE.md` support plus hooks since
  v1.0.86, 2026-09-17) — needs re-testing before the Copilot-side adapter
  is designed.

### Status

One de-risking spike is done (tuiboard evaluation, above). A first real
slice of `tsk` also exists now — just the move, none of the
claiming/locking/daemon machinery yet:

- **`move_task.py`** — moves a task to a new phase. Appends a
  `task.phase_changed` event to `events.jsonl` and regenerates `kanban.md`
  in one step. Intended caller is an agent session, not the human directly
  (see "the owner is the director" above — a human tells the agent what to
  do, the agent moves the card):
  ```bash
  python3 tasks/move_task.py --task-id dotfiles-my-task --to-phase in_progress --actor-id claude
  ```
- **`rebuild_kanban.py`** — projects `events.jsonl` into `tasks/kanban.md`,
  a tuiboard-format board (the 6 lifecycle columns plus a 7th `Deferred`
  column for the parallel lane). Tasks that predate this tool get a
  one-time migrated phase from their old `status` value (see the mapping
  in `rebuild_kanban.py`'s docstring); a task's first real
  `task.phase_changed` event takes over from then on. Point tuiboard's
  config at `tasks/kanban.md` to watch it live — same file shape verified
  in `tasks/evaluations/tuiboard/`.
- **`move_task.py`'s metrics flags + `rebuild_metrics.py`** (added
  2026-09-21) — optional `--team`/`--tokens`/`--cost-usd`/
  `--duration-seconds`/`--cycles` on any move, recorded against the phase
  being **left** (report what a team spent on `in_progress` when you call
  `--to-phase review`, not on the call that opened `in_progress`).
  `rebuild_metrics.py` projects these into `tasks/metrics.md`: every
  metered phase-transition, plus totals by team and by task. No analysis
  happens yet — this only makes the data collect, for the
  orchestration-improvement/team-profile use this is meant to eventually
  feed (see "Orchestration architecture" below). **`tasks/demo/`** is a
  runnable, isolated worked example (2 tasks, 2 teams, full lifecycle,
  `./run_demo.sh`) — see its own README for exactly how the isolation
  works.

**Notification/human-in-the-loop layer, planned (2026-09-21):**
`tasks/plans/human-in-the-loop-notifications.md` — full `plan-orchestra`
output (research + evidence map + 2 rounds of decisive-plan/adversarial-
critique) for the "human only needed on exception" system: SLA-then-
orchestrator auto-validation with a compare-and-swap so it can never
silently overwrite a human decision, a deduplicated notification/
escalation path via herdr+notify-send, two watchdogs so a dead sweep
doesn't look like "all clear", and a cross-provider `/task-brief` startup
skill (Claude Code via a real hook, Copilot CLI via a wrapper since its
own `sessionStart` hook is currently broken, Antigravity via its inherited
hook). Its own prerequisite (merging `move_task.py`/`rebuild_kanban.py`,
above) is done, and so is the plan's §0 ("Write path unificado", below).

**`tasks/lifecycle.py`, §0 done (2026-09-21):** single source of truth for
`PHASES` (now 8: the 6 pipeline phases plus the `blocked`/`deferred` side
lanes — previously only defined piecemeal, and `move_task.py` couldn't
actually target `blocked`/`deferred` at all despite the CHEATSHEET
documenting them), `LEGAL_TRANSITIONS`, and the PT/EN actor-kind and event-
type vocabulary, exactly as specified in the plan doc's §0. Consequences:
- `append_event.py::append()` is now the single physical writer to
  `events.jsonl`; `move_task.py` calls it instead of writing `open("a")`
  itself.
- An illegal `task.phase_changed` transition (e.g. `backlog` straight to
  `in_progress`, skipping `planning`) is rejected, `exit 2`.
- `append()` optionally takes `expect_last_event_id` — Layer A of the
  plan's CAS (§2): `flock(LOCK_EX)` on a sidecar `tasks/.events.lock`
  (never on `events.jsonl` itself), re-reads the task's last event inside
  the lock, aborts (`exit 3`) if it no longer matches. `move_task.py`
  requires `--expect-last-event-id` on every move into `validation` or
  `done` — verified with a 10-way concurrent race: exactly 1 winner, 9
  aborts, every time.
- `rebuild_kanban.py` now renders 8 columns (added `Blocked`, next to the
  pre-existing `Deferred`) and delegates phase-projection to
  `lifecycle.project()` instead of its own copy.

Deliberately **not** done in this slice (needs `tasks/policy.yaml` and the
sweep's own event types, neither exists yet): `FACT_TYPES` and
`dedup_key()`'s escalation-period argument, and Layer B of the CAS (the
rule protecting a human's `validation`/`done` decision from a stale
auto-validation — depends on `notify.py`/`sweep.py` existing to matter).

Remaining spikes before the rest of `tsk` gets written: install Agent
Deck, confirm a `Workflow` script with per-phase `model` overrides,
confirm a trivial herdr plugin can open a popup. (Git-ref CAS under
concurrent writers is now confirmed, above, as part of shipping it rather
than as a separate spike.)
