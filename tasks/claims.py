#!/usr/bin/env python3
"""Claim engine — tasks/claims.jsonl, a separate log from tasks/events.jsonl.

Design: tasks/plans/claim-protocol.md. Claims exist so concurrent
sessions/teams/a future tsk daemon can signal "I'm working on this task"
without touching the task lifecycle log, for two load-bearing reasons
(not stylistic):

- append_event.last_event_id_for_task() does not filter by event type —
  a claim written into events.jsonl would make the validation/done CAS
  abort with a misleading "someone else moved this task first" exit 3,
  even though nobody moved anything.
- lifecycle.project() does setdefault(task_id, ...) for ANY event
  carrying task_id — a typo'd claim would materialize a phantom card on
  the board.

Claims are live, machine-local, TTL-bounded state, deliberately NOT
durable: tasks/claims.jsonl and its sidecar lock tasks/.claims.lock are
both gitignored. Losing claims.jsonl just means everyone re-claims; the
permanent audit trail of who actually did what stays where it already
lives (--team/--handoff on task.phase_changed in events.jsonl).

Unlike a plain event append, EVERY claim write takes flock(LOCK_EX) on
.claims.lock and re-evaluates active_claims() *inside* the lock before
deciding — a check-then-write without the lock lets two writers both see
"no claim" and both write, leaving two rival claims active forever. Claims
are rare and cheap; there's no lock-free fast path here.
"""
import datetime
import fcntl
import json
import sys
import uuid
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))
from lifecycle import (  # noqa: E402
    AGENT_ACTOR_KINDS,
    CLAIM_ROLES,
    CREATED_TYPES,
    HUMAN_ACTOR_KINDS,
    SWARM_ACTOR_KINDS,
    tasks_root,
)

TASKS_DIR = tasks_root()
CLAIMS_FILE = TASKS_DIR / "claims.jsonl"
CLAIMS_LOCK = TASKS_DIR / ".claims.lock"
EVENTS_FILE = TASKS_DIR / "events.jsonl"
assert CLAIMS_LOCK.parent == CLAIMS_FILE.parent, (
    "CLAIMS_FILE and CLAIMS_LOCK must share a parent directory — same "
    "atomicity hazard as append_event.py's EVENTS_FILE/LOCK_FILE assert"
)

CLAIM_TYPE = "claim.acquired"
RELEASE_TYPE = "claim.released"
PREEMPT_TYPE = "claim.preempted"

# tasks/plans/claim-protocol.md section C: 4h for human/agent, 30min for swarm.
DEFAULT_TTL_SECONDS = {"human": 14400, "agent": 14400, "swarm": 1800}


class UnknownTaskError(Exception):
    """task_id has no real task.created event in events.jsonl. Callers exit(2)."""


class InvalidRoleError(Exception):
    """role isn't in CLAIM_ROLES. Callers exit(2)."""


class UnauthorizedReleaseError(Exception):
    """claim.released attempted by an actor that isn't the claim's owner, a
    human, or releasing an already-expired claim. Callers exit(3) — same
    family as append_event.ConcurrentModificationError, an authorization
    invariant, not a documentation convention (tasks/plans/
    claim-protocol.md section C)."""


class NotPreemptableError(Exception):
    """preempt() attempted on a claim that isn't an active swarm claim, or
    by an actor that isn't human/agent. Callers exit(3)."""


def _now():
    return datetime.datetime.now(datetime.timezone.utc)


def _parse(ts):
    return datetime.datetime.fromisoformat(ts)


def load_claims():
    if not CLAIMS_FILE.exists():
        return []
    claims = []
    for line in CLAIMS_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            claims.append(json.loads(line))
    return claims


def _write_claim_line(record):
    with CLAIMS_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def task_exists(task_id):
    """A real task.created event exists for task_id in events.jsonl —
    checked so a typo'd claim can never materialize a phantom card via
    lifecycle.project()'s setdefault (tasks/plans/claim-protocol.md section C)."""
    if not EVENTS_FILE.exists():
        return False
    for line in EVENTS_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        ev = json.loads(line)
        if ev.get("task_id") == task_id and ev.get("type") in CREATED_TYPES:
            return True
    return False


def project_claims(claims):
    """dict[claim_id] -> {task_id, role, actor, expires_at (iso str), released (bool)}.

    Additive, not "last event wins": a renewal (same claim_id) extends
    expires_at to the max of current/requested — never shortens. A
    claim.preempted marks its `preempts` claim_id released and creates a
    new one, in the same append (tasks/plans/claim-protocol.md section C)."""
    state = {}
    for rec in claims:
        rtype = rec.get("type")
        payload = rec.get("payload") or {}
        cid = payload.get("claim_id")
        if not cid:
            continue
        if rtype == CLAIM_TYPE:
            existing = state.get(cid)
            expires_at = payload["expires_at"]
            if existing and not existing["released"]:
                expires_at = max(existing["expires_at"], expires_at)
            state[cid] = {
                "task_id": rec.get("task_id"),
                "role": payload.get("role"),
                "actor": rec.get("actor"),
                "expires_at": expires_at,
                "released": False,
            }
        elif rtype == RELEASE_TYPE:
            if cid in state:
                state[cid]["released"] = True
        elif rtype == PREEMPT_TYPE:
            old_cid = payload.get("preempts")
            if old_cid in state:
                state[old_cid]["released"] = True
            state[cid] = {
                "task_id": rec.get("task_id"),
                "role": payload.get("role"),
                "actor": rec.get("actor"),
                "expires_at": payload["expires_at"],
                "released": False,
            }
    return state


def active_claims(claims, task_id, now=None):
    """Claims for task_id with expires_at > now and no matching release/
    preemption. Additive — multiple simultaneous legitimate owners (a
    human reviewer + an agent implementer) are a first-class case, not an
    edge case. Expiry is pure read-side logic; no sweeper process."""
    now = now or _now()
    state = project_claims(claims)
    result = []
    for cid, rec in state.items():
        if rec["task_id"] != task_id or rec["released"]:
            continue
        if _parse(rec["expires_at"]) > now:
            result.append({"claim_id": cid, **rec})
    return result


def acquire(task_id, role, actor_kind, actor_id, ttl_seconds=None, session_id=None):
    """Locked conditional append (tasks/plans/claim-protocol.md section C): takes
    flock, re-evaluates active_claims() INSIDE the lock, and either renews
    an existing claim for the same (task_id, actor_id, role) — extending
    expires_at, never shortening it — or creates a new claim_id. Returns
    (this actor's claim record, the OTHER active claims on this task at
    write time, for the caller's escalation-flow decision)."""
    if role not in CLAIM_ROLES:
        raise InvalidRoleError(f"role must be one of {CLAIM_ROLES}, got {role!r}")
    if not task_exists(task_id):
        raise UnknownTaskError(f"unknown task_id: {task_id!r} (no task.created event)")

    ttl = ttl_seconds or DEFAULT_TTL_SECONDS.get(actor_kind, DEFAULT_TTL_SECONDS["agent"])

    CLAIMS_LOCK.touch(exist_ok=True)
    with CLAIMS_LOCK.open("r+", encoding="utf-8") as lock_fh:
        fcntl.flock(lock_fh, fcntl.LOCK_EX)
        try:
            claims = load_claims()
            now = _now()
            active = active_claims(claims, task_id, now)
            others = [c for c in active if not (c["actor"]["id"] == actor_id and c["role"] == role)]
            mine = next((c for c in active if c["actor"]["id"] == actor_id and c["role"] == role), None)

            requested_expires = now + datetime.timedelta(seconds=ttl)
            if mine:
                claim_id = mine["claim_id"]
                expires_at = max(_parse(mine["expires_at"]), requested_expires)
            else:
                claim_id = str(uuid.uuid4())
                expires_at = requested_expires

            record = {
                "type": CLAIM_TYPE,
                "actor": {"kind": actor_kind, "id": actor_id},
                "session_id": session_id,
                "task_id": task_id,
                "ts": now.isoformat(),
                "payload": {
                    "claim_id": claim_id,
                    "role": role,
                    "ttl_seconds": ttl,
                    "expires_at": expires_at.isoformat(),
                },
            }
            _write_claim_line(record)
            return record, others
        finally:
            fcntl.flock(lock_fh, fcntl.LOCK_UN)


def release(claim_id, task_id, actor_kind, actor_id, reason=""):
    """Authorized only for: the claim's own actor.id, any human actor, or
    an already-expired claim (checked inside the lock — an invariant, not
    a documentation convention, tasks/plans/claim-protocol.md sections C/D.5)."""
    CLAIMS_LOCK.touch(exist_ok=True)
    with CLAIMS_LOCK.open("r+", encoding="utf-8") as lock_fh:
        fcntl.flock(lock_fh, fcntl.LOCK_EX)
        try:
            claims = load_claims()
            state = project_claims(claims)
            existing = state.get(claim_id)
            if existing is None or existing["released"]:
                raise ValueError(f"claim_id {claim_id!r} is not an active claim")
            now = _now()
            is_owner = existing["actor"]["id"] == actor_id
            is_human = actor_kind in HUMAN_ACTOR_KINDS
            is_expired = _parse(existing["expires_at"]) <= now
            if not (is_owner or is_human or is_expired):
                raise UnauthorizedReleaseError(
                    f"{actor_id!r} ({actor_kind}) may not release claim {claim_id!r}, "
                    f"owned by {existing['actor']['id']!r}"
                )
            record = {
                "type": RELEASE_TYPE,
                "actor": {"kind": actor_kind, "id": actor_id},
                "task_id": task_id,
                "ts": now.isoformat(),
                "payload": {"claim_id": claim_id, "reason": reason},
            }
            _write_claim_line(record)
            return record
        finally:
            fcntl.flock(lock_fh, fcntl.LOCK_UN)


def preempt(task_id, old_claim_id, role, actor_kind, actor_id, reason, ttl_seconds=None, session_id=None):
    """A swarm claim is always preemptible by a human (or an agent acting
    on a human's behalf); never the reverse. ONE append — the task is
    never ownerless mid-transfer (tasks/plans/claim-protocol.md section E)."""
    if actor_kind not in HUMAN_ACTOR_KINDS and actor_kind not in AGENT_ACTOR_KINDS:
        raise NotPreemptableError("only a human (or an agent acting for one) may preempt a claim")
    if role not in CLAIM_ROLES:
        raise InvalidRoleError(f"role must be one of {CLAIM_ROLES}, got {role!r}")

    ttl = ttl_seconds or DEFAULT_TTL_SECONDS.get(actor_kind, DEFAULT_TTL_SECONDS["agent"])

    CLAIMS_LOCK.touch(exist_ok=True)
    with CLAIMS_LOCK.open("r+", encoding="utf-8") as lock_fh:
        fcntl.flock(lock_fh, fcntl.LOCK_EX)
        try:
            claims = load_claims()
            state = project_claims(claims)
            now = _now()
            old = state.get(old_claim_id)
            if old is None or old["released"] or _parse(old["expires_at"]) <= now:
                raise NotPreemptableError(f"claim_id {old_claim_id!r} is not an active claim, nothing to preempt")
            if old["actor"]["kind"] not in SWARM_ACTOR_KINDS:
                raise NotPreemptableError(
                    f"claim {old_claim_id!r} belongs to a {old['actor']['kind']!r} actor, not swarm — "
                    "preemption only applies to swarm claims"
                )

            new_claim_id = str(uuid.uuid4())
            record = {
                "type": PREEMPT_TYPE,
                "actor": {"kind": actor_kind, "id": actor_id},
                "session_id": session_id,
                "task_id": task_id,
                "ts": now.isoformat(),
                "payload": {
                    "claim_id": new_claim_id,
                    "preempts": old_claim_id,
                    "role": role,
                    "ttl_seconds": ttl,
                    "expires_at": (now + datetime.timedelta(seconds=ttl)).isoformat(),
                    "reason": reason,
                },
            }
            _write_claim_line(record)
            return record
        finally:
            fcntl.flock(lock_fh, fcntl.LOCK_UN)
