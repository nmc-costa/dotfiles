# Session handoff — 2026-09-23 (v5, supersedes v4 for current session state)

Written because the owner is hitting usage limits and will continue in a
new session. v4 below (2026-09-21) is now stale for its own Wave 1-3
content (`tasks/kanban.md` shows far more done than v4 describes) — kept
for historical detail only, don't treat its "Still pending" list as
current. This v5 section only covers what changed in *this* session.

## What this session did

Owner asked (in Portuguese) why no card looked open, then requested a
series of new backlog cards + a design pass, ending in real execution on
a branch:

- **`dotfiles-tsk-sweep-validate`** (Backlog) — `sweep.py` has never run
  on this machine (no heartbeat file), needs a real validation pass.
- **`dotfiles-tsk-card-priority`** / **`dotfiles-tsk-recurring-cards`**
  (Backlog, second `blocked_by` the first) — design doc at
  `tasks/plans/priority-and-recurring-cards.md`: P0-P3 priority via a new
  `task.priority_changed` event + `lifecycle.project_priorities()`, and
  recurring cards via `tasks/recurring.yaml` + a new `tasks/recur.py`
  (sibling to `sweep.py`, doesn't require it). Neither implemented yet —
  design only.
- **`dotfiles-tsk-harness-provider-model-index`** (**Review**) —
  **executed**, not just designed. `tasks/harness-provider-model-index.md`
  written on branch `claude/harness-provider-model-index`, **PR #72 open,
  not merged**: https://github.com/nmc-costa/dotfiles/pull/72. Built from
  directly verifying this machine (hostname `omarchy`: Intel iGPU only, no
  discrete GPU, 38GB RAM, mise-installed CLIs, the real
  `.agents/providers/registry/`), not from the owner's pasted draft table,
  which assumed a different (unverified from here) RTX 3070 Ti machine and
  invented provider options (separate DeepSeek/Anthropic API keys,
  OpenRouter) that aren't configured in this repo and conflict with the
  owner's stated constraint: **already pays for Claude Pro + Copilot Pro,
  wants no new metered spend.**
- **`dotfiles-tsk-task-brief-assistant`** (Planning, `blocked_by` the
  index card above) — design recorded on its handoff, not executed:
  extend `.agents/skills/task-brief/SKILL.md` to add a board-shape
  summary + harness/model suggestions read from the index file once it
  exists.

## ⚠️ Conflict risk — check before merging PR #72 or touching the index

**`origin/antigravity/harness-model-matrix`** (a *different* harness —
Antigravity, not Claude Code — pushed this branch, currently unmerged)
independently added its own competing file:
`.agents/instructions/workspace-config/harness-matrix.instructions.md`,
solving what looks like the same problem as PR #72's
`tasks/harness-provider-model-index.md`. That branch is based on an old
point in history (its diff against `main` shows it's missing
`tasks/generators/`, `tasks/rebuild_*.py`'s current shape, etc. — it
predates the archive-and-reorg work), so it isn't an active git conflict
today, but it **is** a real duplicate-effort risk: two harnesses each
wrote their own "which model for which task" reference without seeing the
other. **Before merging PR #72 (or doing more work on the index), diff the
two documents and reconcile — don't let both become the source of truth.**

## Reliability finding: shared-checkout concurrency actually bit this session

This machine runs `tasks/` orchestration with **no per-session isolation**
for the shared `events.jsonl`/`kanban.md` (by design — `tasks_root()`
always resolves to the one canonical `~/dotfiles/tasks`, deliberately, so
a worktree's copy of the scripts never diverges). But that only protects
the *data path*, not the *shared checkout's HEAD*. During this session:

1. At least **2 `move_task.py` writes were silently dropped** — the
   command printed success and an `event_id`, but a fresh read of
   `events.jsonl` moments later showed the line missing. Both were caught
   by re-reading immediately after every write and retried successfully.
   Root cause not fully diagnosed — `append_event.py`'s `flock` protects a
   single append, but nothing serializes "read current state → decide →
   append" across two concurrent processes, and something (very likely
   another live session doing its own `tasks/` writes at the same moment)
   won the race.
2. **The shared checkout's checked-out branch changed out from under this
   session mid-work** — HEAD flipped to a branch this session never
   checked out (`claude/recreate-lost-task-cards`, seemingly another
   session's own work — its name suggests it may already be addressing
   this exact class of bug) and back to `main` again, without this session
   running `git checkout`. A commit meant for `main` landed on the wrong
   branch as a result; recovered via `git update-ref refs/heads/main
   <sha>` (moves the ref without touching the then-checked-out branch's
   working tree — safe, but only because the commit's content happened to
   be redundant with what the other session would commit anyway).
3. Multiple other branches/worktrees were active in this same checkout
   during this session (informational, not further verified):
   `claude/investigate-gh-path-duplication`,
   `claude/recreate-lost-task-cards`, `claude/herdr-commander-eval`,
   `copilot/allow-dtx-providers`, plus `claude/fix-provider-secret-perms`
   (already merged as PR #71).

**Lesson for the next session**: always re-read an event immediately after
writing it before trusting `move_task.py`/`append_event.py`'s own success
message, and check `git branch --show-current` before any commit if
you suspect concurrent activity in this checkout — don't assume the
directory you `cd`'d into is still on the branch you last left it on.
This is itself worth a `tasks/` card (reliability gap, not yet filed as
one) — see the verification prompt below.

## Kickoff / conflict-check prompt for the next session

```
Lê tasks/HANDOFF.md, secção "Session handoff — 2026-09-23 (v5)", para
retomares o contexto de onde ficou a sessão anterior. Antes de continuares
qualquer trabalho novo, verifica conflitos -- não assumas nada abaixo como
ainda verdadeiro sem confirmar, há múltiplas sessões a mexer neste
repositório em paralelo:

1. `gh pr view 72` -- confirma se claude/harness-provider-model-index
   ainda está aberto/mergeable, e lê tasks/harness-provider-model-index.md
   atual (pode ter recebido mais commits).
2. Compara esse ficheiro contra
   .agents/instructions/workspace-config/harness-matrix.instructions.md na
   branch origin/antigravity/harness-model-matrix (`git show
   origin/antigravity/harness-model-matrix:.agents/instructions/workspace-config/harness-matrix.instructions.md`)
   -- dois documentos escritos por harnesses diferentes (Claude Code vs
   Antigravity) a tentar resolver o mesmo problema sem se verem um ao
   outro. Pergunta ao owner qual reconciliar antes de mergear qualquer um.
3. `cat tasks/kanban.md` -- confirma o estado atual de
   dotfiles-tsk-harness-provider-model-index (devia estar em Review) e
   dotfiles-tsk-task-brief-assistant (devia estar em Planning, blocked_by
   o anterior) -- outra sessão pode tê-los movido entretanto.
4. `git branch -vv` -- confirma quais das branches concorrentes listadas
   acima (claude/investigate-gh-path-duplication,
   claude/recreate-lost-task-cards, claude/herdr-commander-eval,
   copilot/allow-dtx-providers) ainda têm trabalho por integrar.
5. Depois de confirmares o acima, diz ao owner o que encontraste e
   pergunta o que quer fazer a seguir -- não decidas sozinho mergear a PR
   #72 nem avançar dotfiles-tsk-task-brief-assistant sem essa reconciliação.
```

---

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
Lê tasks/HANDOFF.md no dotfiles (~/dotfiles) para retomares o contexto de
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
