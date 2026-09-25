#!/usr/bin/env python3
"""Deterministic bookkeeping for a Gauntlet Loop run (D14: script before rule).

The executing agent never decides A/B order or when to stop — it runs this
script and branches on the one token it prints.

    gauntlet_ledger.py init    <slug> [--max-rounds N]
    gauntlet_ledger.py pair    <slug> <piece> --candidate REF --bar REF [--seed S]
    gauntlet_ledger.py verdict <slug> <piece> A|B --reason "largest gap"
    gauntlet_ledger.py status  <slug> [<piece>]

`status` prints exactly one of WIN, CONTINUE, STOP_BUDGET, STOP_PLATEAU per
piece (exit 0). Usage errors and bad state exit 2.

State lives outside any repo: $GAUNTLET_STATE_DIR, else
${XDG_STATE_HOME:-~/.local/state}/gauntlet/<slug>/ — meta.json, ledger.jsonl
(one line per verdict, append-only) and <piece>/pending.json (the hidden
A/B mapping of the round awaiting a verdict).
"""
import argparse
import json
import os
import random
import re
import shutil
import sys
from pathlib import Path

DEFAULT_MAX_ROUNDS = 3
PLATEAU_LOSSES = 3
PLATEAU_JACCARD = 0.8
STATUSES = ("WIN", "CONTINUE", "STOP_BUDGET", "STOP_PLATEAU")


class LedgerError(Exception):
    pass


def state_root():
    env = os.environ.get("GAUNTLET_STATE_DIR")
    if env:
        return Path(env).expanduser()
    xdg = os.environ.get("XDG_STATE_HOME") or "~/.local/state"
    return Path(xdg).expanduser() / "gauntlet"


def _safe_name(name, what):
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", name):
        raise LedgerError(f"invalid {what} {name!r}: use letters, digits, . _ -")
    return name


def run_dir(slug):
    d = state_root() / _safe_name(slug, "slug")
    if not (d / "meta.json").exists():
        raise LedgerError(f"no run {slug!r} — run `init {slug}` first")
    return d


def load_meta(slug):
    return json.loads((run_dir(slug) / "meta.json").read_text())


def load_verdicts(slug, piece=None):
    path = run_dir(slug) / "ledger.jsonl"
    if not path.exists():
        return []
    rows = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    return [r for r in rows if piece is None or r["piece"] == piece]


def _tokens(text):
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def jaccard(a, b):
    ta, tb = _tokens(a), _tokens(b)
    if not ta and not tb:
        return 1.0
    return len(ta & tb) / len(ta | tb)


def piece_status(verdicts, max_rounds):
    if verdicts and verdicts[-1]["winner"] == "candidate":
        return "WIN"
    tail = verdicts[-PLATEAU_LOSSES:]
    if len(tail) == PLATEAU_LOSSES and all(
        jaccard(tail[i]["reason"], tail[i - 1]["reason"]) >= PLATEAU_JACCARD
        for i in range(1, len(tail))
    ):
        return "STOP_PLATEAU"
    if len(verdicts) >= max_rounds:
        return "STOP_BUDGET"
    return "CONTINUE"


def _stage(ref, dest_stem):
    """Copy a local file/dir to a neutral name so its path can't reveal
    which side is the candidate. URLs and commands pass through unchanged."""
    src = Path(ref).expanduser()
    if not src.exists():
        return ref
    if src.is_dir():
        dest = dest_stem
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(src, dest)
    else:
        dest = dest_stem.with_suffix(src.suffix)
        shutil.copyfile(src, dest)
    return str(dest)


def cmd_init(args):
    d = state_root() / _safe_name(args.slug, "slug")
    if (d / "meta.json").exists() and not args.force:
        raise LedgerError(f"run {args.slug!r} already exists at {d} (use --force to restart it)")
    if d.exists() and args.force:
        shutil.rmtree(d)
    if args.max_rounds < 1:
        raise LedgerError("--max-rounds must be >= 1")
    d.mkdir(parents=True, exist_ok=True)
    (d / "meta.json").write_text(json.dumps({"slug": args.slug, "max_rounds": args.max_rounds}))
    print(f"initialized {d} (max {args.max_rounds} rounds per piece)")


def cmd_pair(args):
    meta = load_meta(args.slug)
    piece = _safe_name(args.piece, "piece")
    done = load_verdicts(args.slug, piece)
    status = piece_status(done, meta["max_rounds"])
    if done and status != "CONTINUE":
        raise LedgerError(f"piece {piece!r} is already {status}; no more rounds")
    rnd = len(done) + 1
    rng = random.Random(args.seed) if args.seed is not None else random.SystemRandom()
    candidate_is_a = rng.random() < 0.5
    refs = {"A": args.candidate, "B": args.bar} if candidate_is_a else {"A": args.bar, "B": args.candidate}
    round_dir = run_dir(args.slug) / piece / f"round-{rnd}"
    round_dir.mkdir(parents=True, exist_ok=True)
    shown = {label: _stage(ref, round_dir / label) for label, ref in refs.items()}
    pending = {"round": rnd, "candidate": "A" if candidate_is_a else "B", "shown": shown}
    (run_dir(args.slug) / piece / "pending.json").write_text(json.dumps(pending))
    print(f"A={shown['A']}")
    print(f"B={shown['B']}")


def cmd_verdict(args):
    load_meta(args.slug)
    piece = _safe_name(args.piece, "piece")
    pending_path = run_dir(args.slug) / piece / "pending.json"
    if not pending_path.exists():
        raise LedgerError(f"no pending pair for piece {piece!r} — run `pair` first")
    if not args.reason.strip():
        raise LedgerError("--reason must name the largest gap")
    pending = json.loads(pending_path.read_text())
    winner = "candidate" if args.pick == pending["candidate"] else "bar"
    row = {"piece": piece, "round": pending["round"], "pick": args.pick,
           "winner": winner, "reason": args.reason.strip()}
    with open(run_dir(args.slug) / "ledger.jsonl", "a") as f:
        f.write(json.dumps(row) + "\n")
    pending_path.unlink()
    print(f"round {row['round']}: {winner} won")


def cmd_status(args):
    meta = load_meta(args.slug)
    if args.piece:
        print(piece_status(load_verdicts(args.slug, _safe_name(args.piece, "piece")), meta["max_rounds"]))
        return
    pieces = sorted({r["piece"] for r in load_verdicts(args.slug)})
    if not pieces:
        print("no verdicts yet")
    for p in pieces:
        print(f"{p} {piece_status(load_verdicts(args.slug, p), meta['max_rounds'])}")


def build_parser():
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("init")
    s.add_argument("slug")
    s.add_argument("--max-rounds", type=int, default=DEFAULT_MAX_ROUNDS)
    s.add_argument("--force", action="store_true")
    s.set_defaults(fn=cmd_init)
    s = sub.add_parser("pair")
    s.add_argument("slug")
    s.add_argument("piece")
    s.add_argument("--candidate", required=True)
    s.add_argument("--bar", required=True)
    s.add_argument("--seed", type=int)
    s.set_defaults(fn=cmd_pair)
    s = sub.add_parser("verdict")
    s.add_argument("slug")
    s.add_argument("piece")
    s.add_argument("pick", choices=["A", "B"])
    s.add_argument("--reason", required=True)
    s.set_defaults(fn=cmd_verdict)
    s = sub.add_parser("status")
    s.add_argument("slug")
    s.add_argument("piece", nargs="?")
    s.set_defaults(fn=cmd_status)
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        args.fn(args)
    except LedgerError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
