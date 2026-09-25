# Plan — `/task-card` + `/task-plan` + `/task-flow` (card `dotfiles-tsk-task-plan`)

> Planned 2026-09-25 by Claude Code (Sonnet 5), following an Opus 5.5 review
> requested by the owner. Owner answered an alignment questionnaire the
> same day (recorded in the card's handoff). **Awaiting owner approval
> before moving the card to `in_progress`** — same gate
> `dotfiles-tsk-cross-harness-orchestra` went through.

## Context

The owner asked to review `/task-brief`: shouldn't it be `/task-orchestration`,
covering (1) brief, (2) task-setup, (3) task-card creation, (4) task-plan
(best agent-team orchestration per card phase, with a diagram per team per
card, saved on the card)?

An Opus 5.5 review (lenses: `task-brief`, `plan-orchestra`, `archi`,
`diagramhits`, `simplifyhit`, `task-worktree`/PR #78, `/harness-orchestra`
plan/PR #81) came back **GO-with-changes**:

- **No rename.** `task-brief` is deliberately read-only (`tasks/brief.py`,
  "never picks work" — see its own SKILL.md). `*-orchestra*` already names
  two other skills (`plan-orchestra`, the planned `/harness-orchestra`); a
  third would make "orchestrate this" ambiguous. `simplifyhit`'s own
  guidance (few critical rules per skill, small token budget) favors a
  family of thin skills over one umbrella.
- **Reordered:** brief → card → plan → setup → execution. A worktree
  (setup) needs a task-id, which only exists after the card step.

The owner's own answers (questionnaire, 2026-09-25) refined this further —
see "Owner decisions" below.

**Since the review, the ground moved:** PR #78 (`tasks/worktree.py`) and
PR #81 (`tasks/plans/cross-harness-orchestra.md`) both merged into `main`
while this card was in `planning`. Verified directly against
`origin/main` before writing this doc (not assumed):

- `tasks/worktree.py` exists and is **merged**, but its own docstring
  declares the layout "fixed, never configurable in v1":
  `<repo>.worktrees/<harness>/<task-id>`, branch `<harness>/<task-id>`.
  The owner's "hybrid" answer (`[-<model>]` suffix, only when a harness has
  >1 agent on the same card) is **not implemented** — it needs a v2 change,
  tracked separately (see "Out of scope" below), not assumed done by this
  plan.
- `tasks/orchestra.py` (the actual `/harness-orchestra` implementation)
  **does not exist yet** — PR #81 merged only the design doc
  (`tasks/plans/cross-harness-orchestra.md`); the card itself is still
  `planning` on `origin/main`. So "hand off to orchestra.py" in what
  follows describes a **future integration point**, not existing code to
  patch today.

## Owner decisions (questionnaire, 2026-09-25)

1. **Naming:** family of small skills (`task-brief`, `task-card`,
   `task-plan`, `task-worktree`) **plus a thin router `/task-flow`** that
   chains brief → card → plan → worktree → dispatch/`harness-orchestra`.
   Not a rename to `*-orchestra*`.
2. **"task-setup"** meant: help orchestrate agents per phase — planning,
   card creation, team-per-phase. That's exactly what `/task-flow` +
   `/task-card` + `/task-plan` cover together; no separate `task-setup`
   skill, no bootstrap-`tasks/`-in-a-new-repo card right now (parked, not
   built).
3. **Worktree layout — hybrid:** `tasks/worktree.py` stays the one engine.
   Path: `<repo>.worktrees/<harness>/<task-id>[-<model>]`; branch matches.
   The `-<model>` segment only appears when the **same harness** has more
   than one agent on the same card. `orchestra.py`, once built, must call
   `worktree.py` for the path rather than letting the agent-deck layer
   pick its own.
4. Card `dotfiles-tsk-card-worktrees` (PR #78, already merged) is now a
   real card in the log — added to this card's `blocked_by` alongside
   `dotfiles-tsk-task-brief-assistant` (PR #74) and
   `dotfiles-tsk-cross-harness-orchestra` (PR #81, design merged).

## What ships in this card

Four small pieces, each independently mergeable, each a thin shell over a
stdlib script (D14):

### 1. `/task-card` (new skill)

Documents the **existing** create path — no new script. `append_event.py
--type task.created` already applies D13 (agent-proposal quota of 3,
14-day expiry, dedup by payload fingerprint) and already accepts every
field `rebuild_cards.py`'s `BOARD_FIELDS` renders. What's missing is a
written contract an agent can follow without re-deriving it:

- Payload schema: `title`, `project`, `energy`, `estimate`, `deadline`,
  `blocked_by` (comma-separated task-ids, free prose today — see
  `tasks/generators/rebuild_graph.py`'s own noted limitation), `origin`.
- Id convention: `<project>-tsk-<slug>` (`dotfiles-tsk-*`, `architect-*`,
  etc. — see existing ids in `tasks/cards/`).
- **Always** `--actor-kind agent --actor-id <own-name>` when the agent is
  the one deciding the write, even if the payload's `origin` describes a
  human's earlier decision (`tasks/README.md`'s actor-attribution rule,
  hard-won 2026-09-24).
- **Never** hand-edit `tasks/cards/*.md` — always
  `append_event.py` + `rebuild_cards.py` (cards are generated, disposable
  views).

### 2. `/task-plan` (new skill) + `tasks/task_plan.py` (new script)

Records, per card and per phase, the team of agents doing the work, and
lets the generated card show it as a diagram.

**Data model — one new event type, `plan.team_assigned`:**

```json
{
  "type": "plan.team_assigned",
  "actor": {"kind": "agent", "id": "claude"},
  "task_id": "dotfiles-tsk-example",
  "payload": {
    "phase": "in_progress",
    "team": [
      {"role": "implementer", "harness": "claude", "model": "opus", "subtask": "core script"},
      {"role": "reviewer", "harness": "copilot", "model": "gpt-5.5"}
    ],
    "rationale": "one-line why this split",
    "index_ref": "tasks/harness-provider-model-index.md@2026-09-23",
    "plan_doc": "tasks/plans/example.md"
  }
}
```

- `role` ∈ `tasks/lifecycle.py`'s `CLAIM_ROLES` (`implementer`, `reviewer`,
  `validator`, `planner`) — reuse, don't invent a second vocabulary.
- `harness` ∈ `tasks/worktree.py`'s `HARNESSES` (`claude`, `copilot`,
  `gemini`, `agy`, `codex`) for the worktree name, but `tasks/task_plan.py
  emit` only prints a `dispatch.py` command when the harness is also in
  `dispatch.py`'s `PROVIDER_BINARIES` (today: `claude`, `copilot`, `agy` —
  `gemini`/`codex` aren't dispatchable yet, `emit` says so and stops).
- `model` checked against `tasks/harness-provider-model-index.md`'s
  ranked table; a row marked **Unconfirmed** there requires
  `--allow-unverified` to use, so an unverified model can't silently look
  chosen-with-confidence.
- `tasks/task_plan.py set` only writes when the card is currently
  `planning` or `in_progress` (exit 2 otherwise) — a team assignment for a
  phase the card isn't in yet is very likely a mistake, not a real plan.
- Long-form reasoning stays in a hand-written `tasks/plans/<slug>.md`
  (unchanged) and is only *referenced* by `plan_doc` — `plan.team_assigned`
  is a structured pointer + team roster, not a place to write prose.

**Diagram — generated, never hand-authored:** `rebuild_cards.py` grows a
`## Team plan` section per card with a Mermaid `flowchart LR`, one
subgraph per phase that has a `plan.team_assigned` event, nodes labeled
`role · harness · model`. Precedent: `rebuild_graph.py` already generates
`tasks/roadmap.mmd` the same way — no new pattern, no second file that can
drift from the log. A card with no team-assignment event renders
byte-identical to today (no empty `## Team plan` heading).

**Hand-off, not duplication:** `tasks/task_plan.py emit --task-id X
--phase P`:
- team of 1 → prints a `dispatch.py --provider <h> [--worktree]` dry-run
  line;
- team of >1 → prints the equivalent multi-agent dry-run once
  `orchestra.py` exists (today: prints a clear "not built yet, see
  `dotfiles-tsk-cross-harness-orchestra`" message instead of guessing at
  a CLI that doesn't exist).
- `emit` **never launches anything itself** — it only prints commands.

### 3. `/task-flow` (new, thin router skill)

A short SKILL.md, no new script: states the sequence (brief → card → plan
→ worktree → dispatch/`harness-orchestra`) and links to each skill's own
SKILL.md for the actual steps. Exists so an agent asking "what's the whole
flow for a `tasks/` card" has one place to read, without turning any of
the four real skills into an umbrella. If usage shows `/task-flow` itself
never gets invoked (agents just chain the individual skills fine on their
own), it's fine to retire later — it carries no logic of its own to strand.

### 4. Move harness-suggestion logic out of `/task-brief`

PR #74 (`dotfiles-tsk-task-brief-assistant`) adds a phase→harness
suggestion to `task-brief`'s SKILL.md. Per the Opus review, that's
`/task-plan`'s job (it's a *decision* about who works the card, not a
*report* of what's pending) — move it there once `/task-plan` exists.
`task-brief` keeps its own "never picks work" contract unchanged. (Not
blocking this card's other three pieces — can land as a small follow-up
edit to PR #74 or right after it merges.)

## Risks called out by the Opus review

1. **CAS collision:** `move_task.py`'s `--expect-last-event-id` compares
   against the *last event for the task_id*, not the last
   *phase-changing* event. A `plan.team_assigned` write in between two
   concurrent `move_task.py` calls would invalidate a stale-but-otherwise-
   valid CAS token. Mitigation: `task_plan.py set` should itself pass
   through the same `--expect-last-event-id` guard `move_task.py` uses for
   `validation`/`done`, so a plan write can't silently race a phase move —
   detail to work out during implementation, not a blocker for this plan.
2. **Worktree layout is still v1-only.** The owner's hybrid `[-<model>]`
   suffix needs an actual code change to `tasks/worktree.py`, which today
   explicitly documents its layout as fixed. Tracked as its own follow-up
   (see "Out of scope"), not silently assumed.
3. **`orchestra.py` doesn't exist.** `task_plan.py emit`'s multi-agent
   branch has nothing to hand off to yet — it degrades to a clear message,
   not a guess.
4. **Generated-vs-authored drift:** the one rule that makes the diagram
   trustworthy is that `## Team plan` is never hand-edited, same as the
   rest of a card. Worth a line in `tasks/README.md`'s existing "cards are
   generated" note once this ships.

## Acceptance criteria

- `tasks/task_plan.py` — stdlib only, `set|show|emit` subcommands.
  - `set` appends `plan.team_assigned` via the same `append_event`
    machinery `append_event.py` uses (not a second writer); refuses
    (exit 2) when the card's current phase isn't `planning`/`in_progress`.
  - Validates `role` against `CLAIM_ROLES`, `harness` against
    `worktree.py`'s `HARNESSES`, `model` against
    `harness-provider-model-index.md` (`--allow-unverified` required for
    a row marked Unconfirmed).
  - `emit` only prints dry-run commands; no subprocess is ever spawned by
    a test.
- `rebuild_cards.py` renders `## Team plan` with valid Mermaid, one
  subgraph per phase that has a team assignment; a card with none is
  byte-identical to its current output.
- `.agents/skills/task-card/SKILL.md`, `.agents/skills/task-plan/SKILL.md`,
  `.agents/skills/task-flow/SKILL.md` are thin shells (D14) — logic lives
  in the scripts, not the prose.
- `task-brief`'s SKILL.md still says, verbatim, that it never picks work;
  the harness-suggestion step (PR #74) is removed from it once `/task-plan`
  exists.
- Tests run with `$TSK_ROOT` pointed at a scratch directory (see this
  plan's own worktree-sync PR, #90, for the pattern) — the real
  `~/dotfiles/tasks/events.jsonl` is never touched by a test run.
- `tasks/CHEATSHEET.md` gets the brief → card → plan → worktree →
  dispatch/`harness-orchestra` sequence added to its command table.

## Out of scope (tracked separately, not silently bundled here)

- **`tasks/worktree.py` v2** (the `[-<model>]` hybrid suffix) — needs its
  own card, since it changes behavior a merged script currently documents
  as fixed. Blocks nothing in this plan's 4 pieces (they only *reference*
  the target layout in `plan.team_assigned` payloads and in `emit`'s
  printed commands; they don't implement worktree-path logic themselves).
- **`tasks/orchestra.py`** (the actual `/harness-orchestra` engine) —
  `dotfiles-tsk-cross-harness-orchestra`'s own card, still `planning` on
  `origin/main` as of this writing.
- **Bootstrapping `tasks/` in a repo other than `~/dotfiles`** — a
  different meaning of "setup" the owner explicitly parked, not part of
  this card.

## Sequencing

1. This plan approved by the owner → card moves `planning -> in_progress`.
2. `/task-card` (trivial, mostly documentation).
3. `tasks/task_plan.py` + `/task-plan` + the `## Team plan` generator
   change.
4. `/task-flow` (thin router, last — it only links to the other three).
5. Follow-up: pull the harness-suggestion step out of PR #74's
   `task-brief` changes into `/task-plan`.
