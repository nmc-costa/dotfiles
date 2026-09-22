#!/usr/bin/env python3
"""Custom git merge driver for append-only tasks/*.jsonl logs.

Root cause this exists to close: on 2026-09-21, a real conflict on
tasks/events.jsonl (merging PR #30 into main, commit 61473f7) was
resolved "prefer PR branch" — a plain textual/ours-theirs resolution
wholesale discarded a real, already-merged event
(dotfiles-tsk-dispatch-launcher's task.created) instead of reconciling
both diverging tails. A standard 3-way text merge is unsafe for this
format: there is no correct way to line-merge two divergent append-only
tails without a semantic union, and letting git fall back to its default
conflict markers just moves the same risk onto whoever resolves them next
(human or agent) — the exact failure that already happened once.

This driver always succeeds (exit 0): the merged result is every record
from the merge-base, "ours", and "theirs", deduplicated by a stable key
and sorted by `ts`. Nothing is ever silently dropped — worst case, a
duplicate line from a genuinely malformed/reordered input survives, which
is far safer than losing a real event. Registered via git's merge-driver
mechanism (see setup.sh's `git config merge.jsonl-union.*` calls and
.gitattributes' `merge=jsonl-union` for tasks/events.jsonl).

Git invokes a merge driver as: <driver> %O %A %B — %O the common
ancestor's temp copy, %A "ours" (this is ALSO the output file: the
driver's result gets written back here), %B "theirs". Exit 0 means
resolved cleanly (no conflict markers, no user prompt); non-zero would
leave %A as a real conflict for git to report — this driver never does
that, by design.
"""
import json
import sys


def read_records(path):
    """Best-effort JSONL read — a merge-base temp file may not exist yet
    (e.g. the very first commit that created the file), and a malformed
    line (from an unrelated corruption elsewhere) is skipped rather than
    aborting the whole merge, since dropping the merge entirely would be
    worse than skipping one bad line."""
    records = []
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    except FileNotFoundError:
        pass
    return records


def record_key(record):
    """Stable dedup key. event_id is the real identity for tasks/events.jsonl
    records; claim_id (inside payload) covers tasks/claims.jsonl if this
    driver is ever applied there too. Falls back to the record's full
    canonical content for anything without either — two records with
    identical content really are the same record."""
    if "event_id" in record:
        return ("event_id", record["event_id"])
    payload = record.get("payload") or {}
    if "claim_id" in payload:
        return ("claim_id", payload["claim_id"], record.get("type"), record.get("ts"))
    return ("raw", json.dumps(record, sort_keys=True, ensure_ascii=False))


def union_merge(ancestor_path, ours_path, theirs_path):
    ancestor = read_records(ancestor_path)
    ours = read_records(ours_path)
    theirs = read_records(theirs_path)

    merged = {}
    for record in ancestor + ours + theirs:
        key = record_key(record)
        merged.setdefault(key, record)

    ordered_keys = sorted(merged.keys(), key=lambda k: merged[k].get("ts", ""))
    return [merged[k] for k in ordered_keys]


def main():
    if len(sys.argv) != 4:
        print("usage: git-merge-jsonl-union.py <ancestor> <ours> <theirs>", file=sys.stderr)
        sys.exit(1)
    ancestor_path, ours_path, theirs_path = sys.argv[1], sys.argv[2], sys.argv[3]

    merged_records = union_merge(ancestor_path, ours_path, theirs_path)

    with open(ours_path, "w", encoding="utf-8") as f:
        for record in merged_records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"jsonl-union: merged {len(merged_records)} record(s) (union of ancestor/ours/theirs, "
          f"deduped, sorted by ts)", file=sys.stderr)
    sys.exit(0)


if __name__ == "__main__":
    main()
