# tasks/

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

Automation (cron/systemd/GitHub Actions), a SQLite/DuckDB index,
`tasks.csv` (only once `board.md` passes "a few dozen lines" — the Jarvis
doc's own §5.4 rule), the Jarvis/orchestrator persona itself. See the
history of the session that created this for the full reasoning.
