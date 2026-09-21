# Claim protocol for `tasks/` — design (2026-09-21)

Produced via a `plan-orchestra` run: 5 parallel researchers (claim schema,
git sync ordering, worktree rule, human escalation, daemon-vs-human
priority) → a verified evidence map → a first decisive plan → one round of
adversarial critique (12 material flaws found, several confirmed as live
bugs in the current code, not style opinions) → this revised plan (v2),
which addresses all 12. Companion cards:
`dotfiles-tsk-tasks-root-resolver` (prerequisite), `dotfiles-tsk-claim-protocol`
(this design), `dotfiles-tsk-jsonl-merge-driver` (a related bug found
independently while verifying the critique, not part of the original
scope but real and urgent).

**Trigger for this work:** during a real multi-session dispatch on
2026-09-21, another live Claude session asked (via a synchronous
cross-session message) whether this session was already working the same
5 backlog tasks — avoiding a real collision. `tasks/` has no built-in claim
mechanism; this design gives it one instead of relying on luck and live
messaging every time.

## A. Where claims and events are written

**A1 (proven).** Coordination never depends on commit/PR/merge — measured
PR merge latency in this repo is 31min–4h09m. Visibility has to come from
the shared filesystem, not git.

**A2.** Claims live outside `events.jsonl`, in their own log
`tasks/claims.jsonl` with its own sidecar lock `tasks/.claims.lock`, both
gitignored (precedent: `tasks/.events.lock`). Why this is load-bearing,
not cosmetic:
- `append_event.last_event_id_for_task()` does not filter by event type —
  a claim written into `events.jsonl` would make the `validation`/`done`
  CAS abort with a misleading `exit 3` ("someone else moved this task
  first") even when nobody moved anything.
- `lifecycle.project()` does `setdefault(task_id, …)` for any event
  carrying `task_id` — a typo'd claim would materialize a phantom card on
  the board.

A separate log removes both by construction and leaves the proven CAS
untouched. Claims are live, machine-local, TTL-bounded state, deliberately
**not durable** — losing `claims.jsonl` just means everyone re-claims; the
audit trail of what actually happened stays where it already lives
(`--team`/`--handoff` on `task.phase_changed`).

**A3.** No `tsk daemon` is required on the critical path — it doesn't
exist yet (README calls it "the actual gap"). History (`events.jsonl`)
gets committed by whoever already commits today: an interactive session,
via the existing PR workflow. If a commit is blocked (e.g. by an
auto-merge classifier), the PR just stays open — nothing on the claim path
depends on it landing.

**A4.** The write-path fix touches every real constant, not just one:
`append_event.EVENTS_FILE`, `append_event.LOCK_FILE`, the new
`CLAIMS_FILE`/`CLAIMS_LOCK`, and the `TASKS_DIR` of every `rebuild_*.py`.
Assert at import that `LOCK_FILE.parent == EVENTS_FILE.parent` (same for
claims) — otherwise two processes can share the events log while flocking
different files, and Layer-A CAS silently stops being atomic while still
looking like it works. `lifecycle.TASKS_DIR` is untouched (it only feeds
`sys.path.insert`, not a write path).

**A5.** No path-substring guard. Resolution order for `tasks_root()`:
1. `$TSK_ROOT` if set (explicit opt-in — how `demo/run_demo.sh` isolates
   itself, and how `tasks/` can be developed inside a worktree against a
   scratch log);
2. otherwise **always** `~/dotfiles/tasks`, regardless of where the `.py`
   file physically lives.
`Path(__file__).parent` is never used for data paths again. A worktree
check, if ever wanted for a warning line, compares `git rev-parse
--git-dir` vs `--git-common-dir` — never a `.claude/worktrees/` substring
(that only catches `EnterWorktree`-made worktrees, not `git worktree add`).

## B. Worktree rule

- Code for a claimed task → one worktree per task, branch `claude/<task-id>`.
  Never a wave-worktree shared by many subagents for independent code work.
- `tasks/` itself → always the canonical root, wherever the process runs
  from — guaranteed by A4/A5, not by discipline.
- **On record:** the 2026-09-21 `wave1-parallel-dispatch` session wrote
  `tasks/handoff.md` and ran `move_task.py` from inside a worktree shared
  by five subagents, violating this same rule already recorded in
  `tasks/README.md:203-208`. Direct, measured consequence: four divergent
  copies of `events.jsonl` existed simultaneously across the main checkout
  and three worktrees, and one real event (`dotfiles-tsk-dispatch-launcher`'s
  `task.created`) was orphaned and later silently dropped by a lossy git
  merge (see `dotfiles-tsk-jsonl-merge-driver`) — recovered by hand on
  2026-09-21. It worked out only because a live cross-session message
  caught the near-miss; it wasn't caught by design. Don't repeat it.

## C. Claim schema

File: `tasks/claims.jsonl`. Three record types (`claim.*`, deliberately
distinct from `task.*` so they're never confused with the task lifecycle):

- `claim.acquired` — `{claim_id, task_id, role, ttl_seconds, expires_at}`
- `claim.released` — `{claim_id, task_id, reason}`
- `claim.preempted` — `{claim_id (new), preempts (old claim_id), task_id, role, ttl_seconds, expires_at, reason}` —
  **one append**, so a task is never ownerless mid-transfer.

`actor`/`session_id`/`ts` reuse the common event envelope, no new fields.

**Closed role vocabulary** — `CLAIM_ROLES = ("implementer", "reviewer",
"validator", "planner")`, out-of-vocabulary → `exit 2`. Free-form roles
filled independently by different LLMs never collide ("implementer" vs
"impl" vs "dev"), which would make the negotiation step in D never fire.

**TTL:** 14400s (4h) for `human`/`agent`; 1800s (30min) for `swarm`.

**Idempotency:** dedup key `(task_id, actor.id, role)`. Inside the lock, a
request matching an existing active key is a **renewal**: reuse the
existing `claim_id`, `expires_at = max(current, requested)` — a renewal
never shortens a claim. This stops a retry/crash-recovery from creating a
rival claim its own owner would then have to negotiate with.

**Every write takes `flock(LOCK_EX)` on `.claims.lock` and re-evaluates
`active_claims(task_id)` *inside* the lock before deciding.** A
check-then-write without the lock lets two sessions both see "no claim"
and both write — two rival claims active forever, exactly the failure
this protocol exists to prevent.

Inside the lock, also: reject a `task_id` with no real `task.created` in
`events.jsonl` (`exit 2`, "unknown task_id") — prevents phantom cards from
a typo.

`claim.released` is authorized only for: the claim's own `actor.id`, any
`human` actor, or an already-expired claim.

**Projection:** `active_claims(task_id, now)` = claims with `expires_at >
now` and no matching `claim.released`/`claim.preempted`. Additive — not
"last event wins" — multiple simultaneous legitimate owners (e.g. a human
reviewer + an agent implementer) are a first-class case, not an edge case.
Expiry is pure read-side logic; no sweeper process.

`lifecycle.py` gains `CLAIM_ROLES`, `SWARM_ACTOR_KINDS = ("swarm",)`,
`ALL_ACTOR_KINDS`. `PIPELINE_PHASES`, `SIDE_LANE_PHASES`,
`LEGAL_TRANSITIONS`, `project()`, `last_event_id_for_task()` are
unchanged.

## D. Escalation flow

1. `active_claims(task_id)`, evaluated **inside the lock**, immediately
   before writing.
2. No active claim → write and proceed.
3. Active claim, **different role** → coexist, write and proceed, no
   question asked.
4. Active claim, **same role**, different actor:
   - **4a. Interactive actor** (a session with a human present): ask the
     owning session directly and synchronously over the cross-session
     channel — *"Are you working on `<task_id>` as `<role>`? I have a
     pending claim for the same role and don't want to duplicate."* No
     reply within 2 minutes → block on the human with exactly these three
     options:
     - **(a)** Let session B proceed anyway, in another worktree
     - **(b)** Session B waits until A releases or confirms
     - **(c)** Session B picks another backlog task
   - **4b. Non-interactive actor** (daemon, a dispatched subagent) —
     **never blocks waiting on a human.** Deterministic policy: expired
     claim → take over via `claim.preempted {reason: "expired"}`; live
     claim → skip this task, take the next backlog item, and emit **one**
     best-effort async notification via the (unbuilt)
     `human-in-the-loop-notifications.md` path. This is the *only*
     sanctioned use of that async/SLA channel for claim conflicts — it
     remains the wrong tool for live conflicts everywhere else, since it's
     built for human-paced delay, not seconds-scale coordination between
     two sessions that are both running right now. Max 3 attempts per
     task per day.
5. `claim.released` authorization as specified in C — checked inside the
   lock, an invariant, not a documentation convention.

## E. Daemon vs. human

`swarm` is the actor-kind for the future `tsk daemon` and other
asynchronous processes. **Accepted, named risk:** `swarm` has zero
occurrences in the real event log today — it's being formalized ahead of
any actual use; whoever builds the daemon should validate it before
relying on it as stable.

**A `swarm` claim is always preemptible by a `human` (or an `agent` acting
on a human's behalf); never the reverse.** Mechanically: **one**
`claim.preempted` (not a separate release + claim — see C, atomicity).

**"Stopping" defined in process terms, not just event terms:** the
preempted actor re-checks its claim before every externally visible action
(file write, git command, event append) and at least every 60s during long
operations. On losing the claim it aborts the current step, does **not**
commit or push work in flight, leaves the task's worktree intact for
human inspection, and exits. Between `agent` and `agent` there is no
preemption — flow D always applies instead.

## F. Backlog cards (created 2026-09-21)

Three cards, in dependency order:

1. **`dotfiles-tsk-tasks-root-resolver`** — the write-path fix (A3–A5) and
   the orphaned-event recovery. Blocks card 2.
2. **`dotfiles-tsk-claim-protocol`** — this design (sections A–F),
   `blocked_by: dotfiles-tsk-tasks-root-resolver`.
3. **`dotfiles-tsk-jsonl-merge-driver`** — not originally in scope; found
   while verifying the critique's data-loss claim. The actual mechanism
   that dropped `dotfiles-tsk-dispatch-launcher`'s event was a git merge
   conflict on `tasks/events.jsonl` resolved "prefer branch" (commit
   `61473f7`) — a different failure mode from write-path misdirection,
   and not fixed by A3–A5 alone. Independent, unblocked.

Full card text is in each card's own payload (`tasks/cards/<id>.md` once
`rebuild_cards.py` runs, or `tasks/events.jsonl`'s `task.created` events).

## Accepted risks (not re-litigated, carried forward deliberately)

- `swarm` canonized with zero real usage (E).
- History commits for `events.jsonl` still go through the existing PR
  workflow, which has measured latency up to ~4h — acceptable because
  nothing on the *live coordination* path depends on it, only the
  permanent record does.
- The non-interactive escalation fallback (D.4b) reuses the async
  notification design from `human-in-the-loop-notifications.md`, which is
  itself still unimplemented — this design only specifies the one narrow
  case where that channel is the right tool, it doesn't build it.
- Recovering a dropped event by hand (as done for `dispatch-launcher`) is
  not a repeatable process — `dotfiles-tsk-jsonl-merge-driver` exists so
  this doesn't have to happen again, but until it lands, a similar merge
  could still lose data.
