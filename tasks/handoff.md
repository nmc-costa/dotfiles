# Session handoff — 2026-09-21 (v2, supersedes the first version of this file)

Snapshot of a session that took the `tasks/` orchestration system from
"metrics PR sitting open" to "write-path unified, LEGAL_TRANSITIONS
enforced, CAS proven under concurrency, and a validated design for both
the visual-roadmap and the cross-provider handoff pieces still to build."
Written because the owner is about to hit a usage-limit reset. Not a
permanent doc — delete/archive once its "Still pending" list is empty.

**Important:** two design decisions below (the mermaid/roadmap verdict and
the cross-provider dispatch verdict) were produced by Opus-model
subagents during this session and only exist in this file and in a local,
unversioned Claude Code plan file (`~/.claude/plans/vast-wishing-glade.md`,
machine-local, not in git, may not survive a reset/new machine) — that's
why they're reproduced here in full rather than just referenced.

## What's done (merged to `main`)

- **PR #28** (`claude/tasks-metrics-and-demo`) — `move_task.py` metrics
  flags, `rebuild_metrics.py`, `tasks/demo/`. Merged, merge commit
  `3f55b79`.
- **PR #31** — 16 backlog cards created in `tasks/events.jsonl` for the
  parallelized work plan below (first real, non-demo use of
  `task.created`/`move_task.py`). Merged, merge commit `2a59c2d`.
- **PR #32** — **write-path unification**, the big one. New
  `tasks/lifecycle.py`: single source of truth for `PHASES` (now 8 — the
  6 pipeline phases plus `blocked`/`deferred`, which previously weren't
  even reachable via `move_task.py` despite being documented),
  `LEGAL_TRANSITIONS` (exactly per
  `tasks/plans/human-in-the-loop-notifications.md` §0), and the PT/EN
  actor-kind/event-type vocabulary. `append_event.py::append()` is now
  the single physical writer; illegal transitions exit 2.
  **CAS Layer A**: `--expect-last-event-id` required on every move into
  `validation`/`done` (`flock` on a sidecar `tasks/.events.lock`, never on
  `events.jsonl` itself) — verified with a 10-way concurrent race:
  exactly 1 winner, 9 `ConcurrentModificationError` aborts, every time.
  Merged, merge commit `265f8b5`.
- **PR #33** — closed the `dotfiles-tsk-spike-cas-concurrency` backlog
  card (verified inside PR #32 itself, no separate session needed) and
  fixed a real oversight from #32: `tasks/.events.lock` was untracked but
  not gitignored, almost got committed by accident. Merged.
- **This file** (v2) also moves `dotfiles-tsk-writepath-unification`
  itself through `validation → done` (it was left sitting in `review`
  after #32 merged — a real gap this session almost handed off with a
  stale card state).

## Open PRs (check `gh pr list --state open` — state changes between sessions)

- **PR #35** (`worktree-tsk-dispatch-launcher-card`) — adds one backlog
  card, `dotfiles-tsk-dispatch-launcher` (see verdict below). **Not yet
  merged** — owner hadn't approved it yet when the session ended. Ask
  before merging, same as every other PR this session.
- **PR #30** (`claude/session-handoff`) — this file. Update it in place
  (don't create a new one) the next time a handoff snapshot is needed:
  same branch, rewrite the content, push.
- **PR #34** (`claude/pr1-chezmoi-migration`) — pre-existing, **unrelated
  to this session's work**, not touched. Don't assume it's connected to
  anything above.

## ⚠️ Behavior change: LEGAL_TRANSITIONS is now enforced

Before this session, `move_task.py --to-phase` accepted any phase from
any phase. **That's no longer true as of PR #32.** Legal transitions
(`tasks/lifecycle.py`):

```
backlog     -> planning, deferred
planning    -> in_progress, backlog, deferred, blocked
in_progress -> review, blocked, deferred
review      -> in_progress, validation, blocked
validation  -> done, in_progress, blocked
blocked     -> in_progress, planning, deferred
deferred    -> backlog, planning
done        -> (terminal)
```

Concretely: **you can no longer move a fresh `backlog` task straight to
`in_progress`** — go through `planning` first (two `move_task.py` calls).
This session's own dispatch prompts (in `tasks/README.md`'s "Still
pending" history and in the local plan file) said "move straight to
in_progress" — that guidance is now wrong; use the two-step path instead.
Moving into `validation` or `done` also requires
`--expect-last-event-id <event_id from the previous move>` — read it from
this command's own printed output, or the last line of `events.jsonl` for
that `task_id`.

## Current `tasks/kanban.md` state (at handoff time)

```
Backlog: dotfiles-tsk-spike-agent-deck, dotfiles-tsk-spike-workflow-model,
  dotfiles-tsk-spike-herdr-popup, dotfiles-tsk-tuiboard-install,
  dotfiles-tsk-roadmap-graph, dotfiles-tsk-notify-sweep, dotfiles-tsk-brief,
  dotfiles-tsk-hook-claude-code, dotfiles-tsk-cpx-copilot,
  dotfiles-tsk-hook-antigravity, dotfiles-tsk-task-brief-skill,
  dotfiles-tsk-systemd-units, dotfiles-tsk-graph-dependency-edges,
  dotfiles-tsk-cards-frontmatter
  (+ dotfiles-tsk-dispatch-launcher once PR #35 merges)
Done: dotfiles-tsk-spike-cas-concurrency, dotfiles-tsk-writepath-unification,
  + the 11 older "Abrir PR: ..." cards from before this session
```

Dependency graph (`blocked_by`, prose today — see `dotfiles-tsk-graph-
dependency-edges` for why it isn't a list yet):

```
Wave 1 (dispatchable now, zero deps — write-path already landed):
  4 spikes (agent-deck/workflow-model/herdr-popup; cas-concurrency done),
  tuiboard-install, roadmap-graph

Wave 2 (blocked_by dotfiles-tsk-writepath-unification, now unblocked):
  notify-sweep, brief, graph-dependency-edges, cards-frontmatter

Wave 3 (blocked_by dotfiles-tsk-brief, still blocked):
  hook-claude-code, cpx-copilot, hook-antigravity, task-brief-skill,
  dispatch-launcher (new, see verdict below)
  systemd-units (blocked_by notify-sweep instead)
```

## Verdict 1 — visual roadmap (mermaid), validated by an Opus subagent

The owner asked about hierarchical metadata headers, big-picture-to-small
Mermaid flowcharts (global roadmap → per-project), and a "mindmap" of
what's been tackled. Full verdict (don't re-derive, it's decided):

1. **Metadata headers** = the already-decided L1 in `tasks/README.md`
   ("card markdown+YAML-frontmatter per task"), not a new idea. Must be a
   **generated view** (`rebuild_cards.py`), never hand-edited — that's
   `dotfiles-tsk-cards-frontmatter`.
2. **Mermaid flowcharts**: adopt. Global multi-project is already in
   scope (`payload.project` already has 4 real values, no other repo has
   its own `tasks/`) — one `subgraph` per project in one file, never
   federate logs across repos. Blocked on `blocked_by` becoming a real
   list of ids (currently free prose) — that's
   `dotfiles-tsk-graph-dependency-edges`, blocked_by write-path (now
   unblocked).
3. **Mindmap**: reject the diagram type (Mermaid `mindmap` is tree-only,
   no cross-links, wrong for a dependency graph), adopt the goal via
   `flowchart LR` + `classDef` per phase, plus a separate `timeline`
   diagram for "done accumulated over time."
4. **Concrete plan**: `tasks/rebuild_graph.py` (same pattern as
   `rebuild_kanban.py`/`rebuild_metrics.py`) → `tasks/roadmap.md` (mermaid
   block) + `tasks/roadmap.mmd` (repo already has a `.mmd` convention in
   `.agents/instructions/workspace-config/mermaid.instructions.md` +
   `.claude/rules/mermaid.md`). Split in two: `dotfiles-tsk-roadmap-graph`
   (Wave 1, phases + project grouping + timeline, no edges) is
   dispatchable now; `dotfiles-tsk-graph-dependency-edges` (Wave 2, needs
   the `blocked_by` schema change) comes after. **Never** put mermaid
   inside `kanban.md` itself — tuiboard would misparse it.

## Verdict 2 — cross-provider task handoff, validated by an Opus subagent

The owner asked how an agent hands off work to teams across Claude Code /
Copilot CLI / Antigravity — daemon? per-team handoff file? global config?
Live-verified finding (real `--help` on the 3 real binaries on this
machine): **all three already accept a launch-time prompt** —
`claude "<prompt>"` (+ `-p`, `--bg`), `copilot -i "<prompt>"` (+ `-p`,
`--fleet`), `agy -i`/`--prompt-interactive` (+ `-p`/`--print`). This makes
a daemon unnecessary for the "push" side.

**Verdict: combine two mechanisms, add one small piece, reject three
ideas:**
- **Pull** (already planned, Wave 3): `/task-brief` + `brief.py` +
  per-provider hook/wrapper (`dotfiles-tsk-brief` +
  `dotfiles-tsk-hook-claude-code`/`-antigravity` + `dotfiles-tsk-cpx-
  copilot`). Covers "a fresh session asks what to do."
- **Push** (missing piece, now tracked): `dotfiles-tsk-dispatch-launcher`
  (PR #35, not yet merged) — a `tsk dispatch --task-id X --provider
  {claude,copilot,agy}` that generates the brief text
  (`brief.py --prompt-only`) and launches the right binary with it. No
  daemon, no IPC — state still only ever flows through `events.jsonl`.
  Follows the existing `.agents/providers/adapters/*.sh` convention.
- **Rejected, explicitly, don't rebuild**: `SendMessage` (Claude-Code-only,
  never cross-vendor); a hand-maintained `tasks/teams.yaml` (same drift
  risk as hand-edited cards — if a team profile is ever needed, it must
  be a **generated** `rebuild_teams.py` → `tasks/teams.md`, read-only);
  an interactive "assemble your team" Q&A flow (unneeded ceremony — the
  system's whole point is natural language → `move_task.py` calls).
- Small follow-on scope once built: `dotfiles-tsk-brief` gains
  `--prompt-only --task-id`; `dotfiles-tsk-cpx-copilot` generalizes from
  "just a Copilot wrapper" to "one instance of the general launcher
  pattern."

## Still pending — in priority-ish order

1. **Decide PR #35** (`gh pr view 35`) — small, mechanical, same pattern
   as #31/#33 already approved this session.
2. **Wave 1, dispatchable now, no more write-path blocker**: the 3
   remaining spikes (agent-deck, workflow-model, herdr-popup),
   tuiboard-install, roadmap-graph. Dispatch prompts for these were
   drafted this session (in the local plan file, not versioned) — the
   short version: move each card `backlog → planning → in_progress`
   (two calls, see the LEGAL_TRANSITIONS warning above), do the spike,
   write findings to `tasks/evaluations/<name>/README.md`, close with
   `move_task.py --to-phase review` then `validation`
   (`--expect-last-event-id` required) then `done`.
3. **Wave 2, now unblocked**: `notify-sweep`, `brief` (with the new
   `--prompt-only` scope from Verdict 2), `graph-dependency-edges`,
   `cards-frontmatter`.
4. **Wave 3, blocked on `brief`**: the 3 hooks/wrapper cards, the
   `/task-brief` skill, `dispatch-launcher`, then `systemd-units`.
5. **Acceptance test** (from the notification plan's own "Próximos
   passos" #4): two different CLI sessions working tasks/ in parallel,
   force an SLA violation, confirm CAS doesn't let auto-validation
   silently overwrite a concurrent human decision. Needs Wave 2 done
   first.

## Quick orientation for a fresh session

- `tasks/CHEATSHEET.md` / `tasks/README.md` — updated this session, now
  accurate (LEGAL_TRANSITIONS, CAS, the 8 phases).
- `tasks/plans/human-in-the-loop-notifications.md` — the notification
  system design; §0 is now DONE (was the whole point of this session).
- `tasks/kanban.md` / `tasks/metrics.md` — current real task state.
- `gh pr list --state open` — check first, state changes between
  sessions.
- The two "Verdict" sections above are NOT reproduced anywhere else in
  the git repo — they only existed in a local plan file. If more design
  discussion happened after this file was written, prefer that over this
  snapshot.

## Kickoff prompt for a new session

```
Lê tasks/handoff.md no dotfiles (~/dotfiles) para retomares o contexto de
onde ficou (é a v2, escrita depois de fundir PRs #28/#31/#32/#33 e com
LEGAL_TRANSITIONS agora aplicado). Depois:
1. Confirma o estado de PR #35 e de qualquer PR aberta desde então
   (gh pr list --state open).
2. Diz-me o que está pendente (secção "Still pending") e pergunta-me em
   qual desses items queres que comece a trabalhar.
Não assumas nada do handoff.md como ainda verdadeiro sem confirmar — pode
ter passado tempo desde que foi escrito.
```
