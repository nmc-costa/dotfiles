# Priority levels + recurring cards

Design for two additions to the `tasks/` event-sourced kanban:
per-task priority levels, and cards that spawn a new instance of
themselves on a cadence ("recurring cards"). Written before
implementation, same convention as `tasks/plans/claim-protocol.md` and
`tasks/plans/human-in-the-loop-notifications.md`.

Trigger: reviewing `tasks/brief.py`'s "nothing pending" output surfaced
that `tasks/sweep.py` has never actually run on this machine (no
heartbeat file yet) — closed by adding `dotfiles-tsk-sweep-validate` to
backlog — and prompted two follow-on asks: give cards a priority level,
and support cards that recur on a schedule (optionally, but not
necessarily, driven by the same periodic execution `sweep.py` will
eventually get via `dotfiles-tsk-systemd-units`).

## Part A — Priority levels

Closed vocabulary, reusing the `P0` term the codebase already uses for
urgency (`lifecycle.P0_FACT_TYPES`, currently scoped to notification
facts, not tasks): `PRIORITIES = ("P0", "P1", "P2", "P3")` — P0 =
drop-everything, P1 = high, P2 = normal (default when unset), P3 =
low/someday.

**`tasks/lifecycle.py`**
- Add `PRIORITIES` and `PRIORITY_CHANGED_TYPES = ("task.priority_changed",)`.
- Add `project_priorities(events) -> dict[task_id, priority]`: last-
  event-wins per `task_id` over `task.created`'s initial `priority`
  payload key and any later `task.priority_changed` events. Mirrors
  `current_phase()`'s shape. Not folded into `project()` — that
  function's contract is documented as title/phase/created only.

**`tasks/append_event.py`**
- No structural change needed: `validate_and_enrich()` has no event-type
  whitelist (`REQUIRED_FIELDS = ("type", "actor")` only), so
  `task.priority_changed` needs zero core changes to be writable.
- Add one targeted check: if `payload.get("priority")` is present (on
  `task.created` or `task.priority_changed`), it must be a member of
  `PRIORITIES` or raise `ValueError` (exit 1) — same shape as the
  existing `IllegalTransitionError` check for phase legality.

**`tasks/move_task.py`**
- Add `--set-priority {P0,P1,P2,P3}`.
- Usable standalone, without `--to-phase` (mirror the existing
  `--show-handoff` exemption), or combined with a phase move.
- Always writes its own `task.priority_changed` event, even when
  combined with a phase move — don't overload `task.phase_changed`'s
  payload, keep every event type single-purpose (same spirit as the
  existing `--handoff` vs `--reason` split).

**`tasks/rebuild_cards.py` / `tasks/generators/rebuild_cards.py`**
- Import `project_priorities`, add `priority` to each card's YAML
  frontmatter, right after `phase`.

**`tasks/rebuild_kanban.py`** (the top-level file — see debt note below)
- Import `project_priorities`, merge into each row.
- Sort each column by `(PRIORITIES.index(priority), created)` instead of
  today's plain `key=lambda kv: kv[1]["created"]`.
- Render `- [ ] [P0] task-id Title` — bracketed tag, safe for tuiboard
  (its own docstring: every `- [ ]`/`- [x]` line is opaque task text).

**`tasks/CHEATSHEET.md`**
- Document `--set-priority` and the vocabulary next to the existing
  "Create a task"/"Move a task" recipes.

**Pre-existing debt, flagged not fixed**: `tasks/rebuild_kanban.py` and
`tasks/generators/rebuild_kanban.py` have already drifted apart (`diff`
confirms different `SCRIPT_DIR`, one creates the archive dir, the other
doesn't). `rebuild_cards.py` was migrated to a thin wrapper delegating to
`generators/rebuild_cards.py` during `dotfiles-tsk-archive-and-reorg`,
but `rebuild_kanban.py` wasn't — `move_task.py` imports and runs the
top-level file directly (confirmed), so the `generators/` copy looks
orphaned. This work touches only the top-level file. Worth its own small
follow-up card.

## Part B — Recurring cards

A card is terminal at `done` by design (`LEGAL_TRANSITIONS["done"] =
set()`, no way out — keeps history immutable). So recurrence can't mean
reopening a done card; it means spawning a **new instance** task from a
template on a cadence, the same way a recurring calendar event creates a
new occurrence each time.

**`tasks/recurring.yaml`** (new, human-edited config, not a generated
view) — list of templates: `id`, `title`, `project`, `priority`
(optional, defaults `P2`), `cadence_days` (plain integer — deliberately
not cron/ISO-8601, no new dependency needed for "every N days"), `active`
(bool, so pausing a recurrence doesn't require deleting its template).

**`tasks/recur.py`** (new script, sibling to `sweep.py`, not folded into
it — `sweep.py` is deliberately scoped to notification-fact detection
only; spawning recurring instances is a distinct responsibility). Per
active template:
1. Find existing instances via `lifecycle.project(events)` filtered to
   `task_id` starting with `f"{template_id}-"`.
2. No instance yet → spawn the first one now.
3. Most recent instance not yet `done` → skip (don't pile up duplicates
   while one is in flight — same care `sweep.py` already takes against
   double-raising a fact).
4. Most recent instance `done` and `cadence_days` elapsed since *that
   instance's own* `task.created` timestamp → spawn the next one:
   `task_id = f"{template_id}-{today}"`, `actor.kind=agent,
   actor.id=recur`, payload includes `origin: f"recurring:{template_id}"`.
5. Otherwise skip.
Prints what it did/skipped per template, same operator-facing style as
`sweep.py`.

**Answering "pode usar sweep.py ou não precisar"**: `recur.py` never
calls into `sweep.py`'s fact-detection code and doesn't need it to run —
but it's designed for the same periodic cadence, so once
`dotfiles-tsk-systemd-units` (already in backlog) builds the periodic
wrapper for `sweep.py`, that same wrapper can also invoke `recur.py`. No
separate scheduler needed just for this feature.

**No new frontmatter field for template provenance**: reuse the existing
free-text `origin` board field (`origin: "recurring:<template_id>"`) — it
already means "where did this task come from" per `tasks/README.md`'s
field list, so this is a direct fit, not an overload.

**Overlap flag**: `dotfiles-tsk-agile-workspace-schedule` (already in
backlog) plans a broader `jobs/*.yaml` + systemd-timers manifest for
recurring *agent work* generally (dispatching sessions), not specifically
spawning kanban cards. `tasks/recurring.yaml` here is deliberately
narrower — it only ever writes `task.created` events, no agent dispatch.
`recur.py`'s docstring should call this out explicitly so the two efforts
don't silently duplicate each other; revisit once `jobs/*.yaml` lands to
see whether one subsumes the other.

## Status

Design only. Implementation tracked by `dotfiles-tsk-card-priority` (Part
A) and `dotfiles-tsk-recurring-cards` (Part B, sequenced after Part A so
spawned instances carry a priority from day one).
