# Session handoff — 2026-09-21 (v4, supersedes v3)

Snapshot of a session that took the `tasks/` orchestration system from
"metrics PR sitting open" to "write-path unified, LEGAL_TRANSITIONS
enforced, CAS proven under concurrency, Wave 1 fully closed by 5 parallel
subagents, and a validated design for both the visual-roadmap and the
cross-provider handoff pieces still to build." Written because the owner
is about to hit a usage-limit reset. Not a permanent doc — delete/archive
once its "Still pending" list is empty.

## ✅ Onda 1 — fechada (2026-09-21)

As 5 tarefas da Onda 1 foram despachadas em paralelo (5 subagentes, um
único worktree isolado partilhado, testando concorrência real de escrita
em `tasks/events.jsonl` — não sintética) e estão todas em `Done`:

- `dotfiles-tsk-spike-agent-deck` — **PASS**. Instalação real (binário
  pré-compilado, sem Go), deteção lado a lado confirmada via
  `agent-deck status -v` com sessões tmux reais Claude Code + Copilot CLI.
  Achado: deteção de estado é completa para Claude Code, superficial para
  Copilot (consistente com o README oficial do projeto). Veredito sobre
  `herdr`: complementares, não redundantes.
- `dotfiles-tsk-spike-workflow-model` — **PASS**. O subagente delegado não
  teve acesso à ferramenta `Workflow` (ausente do toolset de subagentes —
  achado arquitetural relevante para o design do L2: `Workflow` só é
  invocável a partir de uma sessão de topo). A sessão orquestradora correu
  o script já escrito e confirmou diferenciação real por fase:
  `phaseA→claude-haiku-4-5-20251001`, `phaseB→claude-opus-5`.
- `dotfiles-tsk-spike-herdr-popup` — **PARCIAL**. `--placement popup` não
  existe no herdr 0.8.2 instalado (falha silenciosa, processo órfão);
  `--placement overlay` é o equivalente real e funcional, confirmado
  visível/focado. Cleanup (`unlink`) confirmado.
- `dotfiles-tsk-tuiboard-install` — **PASS**. `bun`+`tuiboard` instalados a
  sério (via `mise`+`bun install -g`), config real a apontar para
  `tasks/kanban.md` do checkout principal, render confirmado via captura
  tmux.
- `dotfiles-tsk-roadmap-graph` — **PASS**. `tasks/rebuild_graph.py` novo,
  gera `tasks/roadmap.md`/`.mmd` (flowchart por projeto + timeline de
  `done`), validado com `mermaid-cli` real.

Detalhe completo de cada spike em `tasks/evaluations/<nome>/README.md`.
Ver `tasks/metrics.md` para os custos reais (tokens/duração) por
transição. **Achado de coordenação a reter**: durante o dispatch, outra
sessão Claude pediu coordenação em tempo real sobre estas mesmas 5
tarefas (via `cross-session-message`) — confirmou-se o âmbito e ela
recuou para `dotfiles-tsk-cards-frontmatter` (Wave 2) em vez de duplicar
trabalho. O sistema `tasks/` continua sem mecanismo de claim automático;
este ficheiro + a troca de mensagens ao vivo foi o que evitou a colisão.

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

- **PR #35** and **PR #30** — both merged since v2 was written (confirmed
  2026-09-21, merge commits visible in `git log main`). The
  `dotfiles-tsk-dispatch-launcher` card from #35 is now in `tasks/kanban.md`'s
  Backlog.
- **PR #34** (`claude/pr1-chezmoi-migration`) — still open, pre-existing,
  **unrelated to this session's work**, not touched. Don't assume it's
  connected to anything above.
- This file itself: still update in place on the same branch pattern used
  before (a new `claude/<topic>` branch per handoff rewrite is fine too —
  there's no single fixed branch name to reuse anymore since #30 merged).

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

1. **Wave 1 — DONE**, see section above. Nothing left here.
2. **Wave 2, unblocked**: `notify-sweep`, `brief` (with the new
   `--prompt-only` scope from Verdict 2), `graph-dependency-edges`,
   `cards-frontmatter`. **Check `tasks/kanban.md` before claiming
   `cards-frontmatter`** — another Claude session said (live,
   cross-session-message, 2026-09-21) it was picking that one up while
   Wave 1 was in flight; may already be in progress or done by the time
   you read this.
3. **Wave 3, blocked on `brief`**: the 3 hooks/wrapper cards, the
   `/task-brief` skill, `dispatch-launcher`, then `systemd-units`.
4. **Acceptance test** (from the notification plan's own "Próximos
   passos" #4): two different CLI sessions working tasks/ in parallel,
   force an SLA violation, confirm CAS doesn't let auto-validation
   silently overwrite a concurrent human decision. Needs Wave 2 done
   first. Note: Wave 1's dispatch was itself a real (if informal) version
   of this test for the lock-free transitions — 5 agents wrote
   `planning`/`in_progress` events concurrently into the same
   `events.jsonl` with no corruption; the CAS-specific SLA/auto-validation
   scenario is still untested.

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
onde ficou (é a v4 — Onda 1 fechada, PRs #28/#30/#31/#32/#33/#35 já
fundidas, LEGAL_TRANSITIONS aplicado). Depois:
1. Corre `cat tasks/kanban.md` — confirma que `cards-frontmatter` (Wave 2)
   não foi já reivindicada por outra sessão antes de a tocares.
2. Confirma `gh pr list --state open` — estado muda entre sessões.
3. Diz-me o que está pendente (secção "Still pending") e pergunta-me em
   qual desses items queres que comece a trabalhar.
Não assumas nada do handoff.md como ainda verdadeiro sem confirmar — pode
ter passado tempo desde que foi escrito, e há múltiplas sessões a mexer
neste repositório em paralelo.
```
