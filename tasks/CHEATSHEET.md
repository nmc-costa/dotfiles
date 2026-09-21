# tasks/ cheatsheet

Quick reference for the commands you actually run. For the *why*, see
`tasks/README.md` (the model/decisions) and
`tasks/plans/human-in-the-loop-notifications.md` (the notification/
orchestration layer — partially built, see below). This file is only the
*how*.

## The tools, in one line each

| Tool | Does |
|---|---|
| `append_event.py` | Create a task, or write a raw event. The only way in. |
| `move_task.py` | Move a task to a new phase — optionally with metrics and/or a handoff note. |
| `rebuild_kanban.py` | Regenerate `kanban.md` from `events.jsonl` (tuiboard format). Run automatically by `move_task.py`. |
| `rebuild_cards.py` | Regenerate one YAML-frontmatter card per task under `tasks/cards/`. Run automatically by `move_task.py`. |
| `rebuild_metrics.py` | Regenerate `metrics.md`. Run automatically by `move_task.py` when metrics are given. |
| `rebuild_view.py` | Regenerate `board.md` (older flat-table view, pre-dates the 6-phase model). |
| `sweep.py` | Detect `sla_expired`/`blocked_too_long` facts, raise `notification.raised` events. Run it periodically yourself — no systemd timer yet. |
| `notify.py` | Deliver pending raised facts (herdr digest + notify-send fallback), or `--ack --dedup-key` to close one out. |

None of these need arguments beyond what's shown below — no config file, no
setup. Run them from anywhere with `python3 tasks/<tool>.py ...` or `cd
tasks && python3 <tool>.py ...`.

## Create a task

```bash
python3 tasks/append_event.py --type task.created \
  --actor-kind human --actor-id nmc-costa \
  --task-id dotfiles-my-task \
  --payload '{"title":"...", "project":"dotfiles"}'
```

New tasks start in `backlog`.

## Move a task through phases

```bash
python3 tasks/move_task.py --task-id dotfiles-my-task --to-phase in_progress --actor-id claude
```

Phases, in order: `backlog → planning → in_progress → review → validation
→ done`, plus `deferred`/`blocked` as side lanes. Only the transitions in
`tasks/lifecycle.py`'s `LEGAL_TRANSITIONS` are accepted (added
2026-09-21) — e.g. `backlog` can only go to `planning` or `deferred`,
never straight to `in_progress`. An illegal move exits 2. Move into
`validation` or `done` and you also need `--expect-last-event-id` (below).

**`--actor-kind`** defaults to `agent` — set `--actor-kind human` when a
human, not an agent, is the one deciding the move (this matters once the
auto-validation/CAS logic in the plan gets built; human-authored moves are
meant to always win).

## Protect a validation/done move (required, not optional)

```bash
python3 tasks/move_task.py --task-id dotfiles-my-task --to-phase validation \
  --expect-last-event-id <event_id printed by the previous move>
```

`--to-phase validation`/`done` **require** `--expect-last-event-id` — the
event_id this command (or `append_event.py`) printed on the task's
previous move, or the `event_id` of the last line in `events.jsonl` for
this `task_id`. If someone else moved the task in the meantime, the id
you have is stale and the command aborts with `exit 3` instead of
silently overwriting them (Layer A of the CAS in
`tasks/plans/human-in-the-loop-notifications.md` §2 — confirmed to hold
under a 10-way concurrent race, exactly 1 winner every time). Every other
phase transition stays lock-free — this only applies to the two phases
where overwriting a decision would actually matter.

## Record what a team spent (optional, on every move)

```bash
python3 tasks/move_task.py --task-id dotfiles-my-task --to-phase review \
  --team team-forge --tokens 12000 --cost-usd 0.18 \
  --duration-seconds 900 --cycles 1
```

**The one gotcha:** metrics describe the phase you're **leaving**, not the
one you're entering. Calling `--to-phase review` closes out `in_progress`
— so `--tokens`/etc. here report what was spent *during* `in_progress`,
not during `review`. If you're not sure, look at `from_phase` in the
event, or just check `metrics.md` after — it'll be obviously wrong if
you got it backwards (numbers show up under the wrong phase).

Regenerates `tasks/metrics.md` automatically (three tables: every metered
transition, totals by team, totals by task).

## Leave a handoff note (optional, on any move)

```bash
python3 tasks/move_task.py --task-id dotfiles-my-task --to-phase in_progress \
  --handoff "Plano em docs/plan.md. Falta a secção 3 — API ainda não escolhida."
```

Read the latest one back (no move happens):

```bash
python3 tasks/move_task.py --task-id dotfiles-my-task --show-handoff
```

`--handoff` is for **state to resume from** (what's done, what's left,
where the work lives); `--reason` is a one-line **why this move happened**.
Different fields, use both if useful. Write a handoff note whenever a
different team/session might pick the task up next — including "future
you" reopening it in a week.

## Notifications (SLA / blocked-too-long facts)

```bash
python3 tasks/sweep.py    # detect facts, raise notification.raised
python3 tasks/notify.py   # deliver pending facts (herdr toast, or notify-send fallback)
python3 tasks/notify.py --ack --dedup-key "dotfiles-my-task:sla_expired:6"
```

Run `sweep.py` periodically yourself (no systemd timer yet —
`dotfiles-tsk-systemd-units` is still backlog). Two facts today: a task
stuck in `validation` past 4h (`sla_expired`), or stuck in `blocked` past
24h (`blocked_too_long`, delivered individually with an unconditional
`notify-send`, not folded into the digest). Neither fact auto-resolves
anything — `sweep.py` only raises, it never moves a task. See
`tasks/README.md`'s "notify.py/sweep.py" status note for exactly what's
deliberately not built yet (auto-validation, `loop_cap_exceeded`,
`agent_session_stalled`).

## See what's going on

```bash
cat tasks/kanban.md      # tuiboard-format board — point tuiboard's config at this file to watch it live
cat tasks/metrics.md      # team/task cost breakdown
cat tasks/board.md        # older flat table (still generated, not the primary view anymore)
cat tasks/cards/dotfiles-my-task.md   # one task's full history + latest handoff, YAML frontmatter + phase log
python3 tasks/move_task.py --task-id X --show-handoff
```

## Which interface for which question

`kanban.md`/`metrics.md` show task **phase** state; these show live
**session** state (what an agent is doing right now) — different
questions, use whichever answers what you're actually asking:

- **`herdr`** (the multiplexer itself, independent of tuiboard) — native
  sidebar with per-session state (`idle`/`working`/`blocked`), already
  installed, works with zero extra config.
- **`claude agents --json`** — Claude Code's native Agent View: lists
  sessions with state, a 1-line summary, and what's blocking each one.
- **`tasks/kanban.md` and `tasks/metrics.md`** — plain text, read in any
  editor or terminal, nothing to run.
- **`/task-brief`** (planned, not built) — fastest for "does anything need
  me": plain text straight in the CLI session, no TUI at all.
- **Agent Deck** (evaluated, not installed) — multi-vendor fleet dashboard
  (TUI+web), specifically useful once Copilot/Gemini sessions are running
  alongside Claude Code.

**For a quick check without opening anything:** `claude agents --json` or
reading `kanban.md`/`metrics.md` directly is faster than opening tuiboard.

## Try it without touching real data

```bash
cd tasks/demo && ./run_demo.sh
```

Self-contained, isolated copy of all the tools — 2 tasks, 2 teams, full
lifecycle, metrics, a handoff note. Safe to re-run any time. See
`tasks/demo/README.md`.

## Asking Claude Code to "lead a team" on a task

There's no dedicated skill for this yet (`/task-brief` from the plan doc
isn't built) — today you just say it directly, e.g.:

> "Pega na tarefa `dotfiles-my-task` em `tasks/kanban.md` e lidera-a —
> spawna a equipa que precisares."

What the agent needs, to actually do this:
- Read/write on `tasks/events.jsonl` (via `move_task.py`) — that's the
  state it coordinates through.
- The `Agent` tool (to spawn sub-agents = "the team") or `Workflow` tool
  for anything with structured phases/model tiers.
- `Bash` for the real work (git, tests, etc).

**Limits, as of now:**
- The agent can only directly coordinate other **Claude Code** sessions
  (same machine, via `SendMessage`). It cannot give live orders to a
  Copilot CLI or Antigravity session — cross-vendor coordination only
  happens through the shared `tasks/events.jsonl` file, not live process
  communication.
- The agent "leads" for as long as **that session** stays open. Close it,
  and a fresh session (or that one resumed) has to pick up purely from
  what's in `events.jsonl` — this is exactly why handoff notes matter.

**Planned, not built:** a `/task-brief` skill that reads the inbox/kanban
and hands a fresh session the right prompt automatically on startup — via
a real hook on Claude Code, a wrapper (`cpx`) on Copilot CLI (its own
startup hook is confirmed broken), and Antigravity's inherited hook. Full
design in `tasks/plans/human-in-the-loop-notifications.md`.
