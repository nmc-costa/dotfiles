# Session handoff — 2026-09-21

Snapshot of a long session that took the multi-agent task orchestration
idea from zero to a working first slice + a fully-researched, adversarially
critiqued plan for the rest. Written so a fresh session (any CLI) can
resume without re-deriving context. Not versioned as a permanent doc the
way `tasks/README.md`/`CHEATSHEET.md` are — this is a point-in-time
snapshot; delete or archive it once its "still pending" list is empty.

## What's done (merged to `main`, or in an open PR — see below)

- **Root-level CLAUDE.md/AGENTS.md coverage**: `~/CLAUDE.md`, `~/AGENTS.md`,
  `~/Projects/CLAUDE.md` symlinked to `dotfiles/global/*`;
  `~/Work/CLAUDE.md` a real local file (never symlinked/committed —
  employer content). `setup.sh` wires these on a fresh machine.
- **Repo hygiene fixes**: an orphan git submodule link, a missing
  `.gitignore` entry for `.claude/worktrees/`, a conflict-marker check
  added to `scripts/validate_dotfiles.sh` (would have caught a real
  incident where literal `<<<<<<<` markers got merged into `README.md` —
  fixed too).
- **`tuiboard` evaluated and chosen** as the kanban UI (safe, local, fast
  — full writeup in `tasks/evaluations/tuiboard/`). **Not installed for
  real use yet** — the evaluation ran from a scratch Bun install; `which
  bun`/`which tuiboard` on this machine return nothing right now.
- **`tasks/plans/human-in-the-loop-notifications.md`** — a full
  `plan-orchestra` run (6 parallel researchers + 1 tie-breaker, a verified
  evidence map, 2 rounds of decisive-plan/adversarial-critique) for the
  "human only needed on exception" notification/escalation system. Final
  verdict: **ship it**, with an 8-point addendum already folded into the
  doc. **Nothing in this plan is implemented** — it's a design doc for
  future work.
- **First real slice of `tsk`** (`move_task.py` + `rebuild_kanban.py`,
  merged): move a task through the 6-phase lifecycle
  (`backlog→planning→in_progress→review→validation→done`, plus
  `deferred`), generates `tasks/kanban.md` in tuiboard format.
- **Metrics + handoff notes** (PR #28, **still open, not merged**):
  `--team`/`--tokens`/`--cost-usd`/`--duration-seconds`/`--cycles` on any
  move (attached to the phase being *left*), aggregated into
  `tasks/metrics.md`. Plus `--handoff`/`--show-handoff` — free-text notes
  for whoever picks up a task next.
- **`tasks/demo/`** — a self-contained, runnable, isolated worked example
  (2 tasks, 2 teams, full lifecycle, metrics, a handoff note). Run with
  `tasks/demo/run_demo.sh`.
- **`tasks/CHEATSHEET.md`** — the quick command reference for all of the
  above (create/move/metrics/handoff/observe/demo), plus a comparison of
  every session-observability surface currently available (herdr, `claude
  agents --json`, plain `kanban.md`/`metrics.md`, the planned
  `/task-brief`, Agent Deck) and how to ask an agent to "lead a team" on a
  task today, including its real cross-vendor limits.

## Still pending — in priority-ish order

1. **Merge PR #28** (`claude/tasks-metrics-and-demo`) —
   https://github.com/nmc-costa/dotfiles/pull/28. Clean, mergeable, tested.
   Nothing else below strictly depends on it, but it's the natural next
   step.
2. **Fase 0 de-risking spikes** (from `tasks/README.md`'s "Orchestration
   architecture" → Status), none started:
   - Install Agent Deck and confirm it actually detects Claude Code +
     Copilot CLI sessions side by side.
   - Confirm git-ref compare-and-swap claiming survives concurrent
     writers (the plan doc's Layer A).
   - Confirm a `Workflow` script with a real per-phase `model` override
     runs as expected.
   - Confirm a trivial herdr plugin can open a popup (`herdr plugin pane
     open`) — herdr itself is installed (v0.8.2, confirmed), the plugin
     path hasn't been tried yet.
3. **Install `tuiboard` for real** (not just in a scratch dir) if you want
   to actually watch `tasks/kanban.md` live day-to-day. `bun install -g
   tuiboard`, point its config at `tasks/kanban.md`.
4. **Build the notification/escalation system** per
   `tasks/plans/human-in-the-loop-notifications.md` — nothing in that
   ~300-line plan is implemented. Suggested build order is in the plan's
   own "Próximos passos" section (§0 write-path unification →
   `lifecycle.py` → CAS → `notify.py`/`brief.py`/`sweep.py` → the Claude
   Code hook → the `cpx` Copilot wrapper → the Antigravity hook → systemd
   units following the existing `ensure-*.sh` convention).
5. **`/task-brief` skill** — doesn't exist. Part of the plan above, but
   callable on its own once `brief.py` exists: reads the inbox/kanban,
   briefs whichever session opens next, asks "what do you want to work on"
   if nothing's pending. Needed before "ask an agent to lead a team" stops
   requiring you to type the context by hand every time.
6. **Add `LEGAL_TRANSITIONS` enforcement to `move_task.py`** — right now
   any phase can jump to any other phase, nothing validates the sequence.
   The table is already specified in the plan doc (§0).

## Quick orientation for a fresh session

- `tasks/CHEATSHEET.md` — how to do anything (commands only).
- `tasks/README.md` — the model and every decision, with reasoning.
- `tasks/plans/human-in-the-loop-notifications.md` — the notification
  system design, fully researched and critiqued, nothing built.
- `tasks/kanban.md` / `tasks/metrics.md` — current real task state (once
  PR #28 lands, metrics.md will exist; until then only `kanban.md` does).
- `gh pr list --state open` — check this first, state changes between
  sessions.

## Kickoff prompt for a new session

```
Lê tasks/handoff.md no dotfiles (~/dotfiles) para retomares o contexto de
onde ficou. Depois:
1. Confirma se a PR #28 já foi fundida (gh pr list --state open) — se não,
   pergunta-me se posso fazer merge.
2. Diz-me o que está pendente (secção "Still pending" do handoff.md) e
   pergunta-me em qual desses items queres que eu comece a trabalhar.
Não assumas nada do handoff.md como ainda verdadeiro sem confirmar — pode
ter passado tempo desde que foi escrito.
```
