#!/usr/bin/env python3
"""chronicle.py — mine interaction history into improvement candidates with cited evidence.

Thin deterministic core behind the /chronicle skill (D5, card
dotfiles-tsk-chronicle-d4-d6; reference: Copilot CLI /chronicle, propose-only).

Read-only over three sources:
  1. Claude Code session transcripts (~/.claude/projects/**/*.jsonl)
     - repeated shell commands (candidate: script/skill automation)
     - instruction language from the user (candidate: instructions edit)
  2. tasks/events.jsonl (the one real log, via tasks/paths.tasks_root())
     - cards that bounced review -> in_progress more than once (rework loops)
  3. merged PR churn (gh) - files touched by several merged PRs

Output: a candidates report (markdown or --json). It NEVER writes to the
repo, never opens a PR, never merges - the agent curates the report and
proposes changes on a chronicle/* branch; merges are human-only. Quotes are
truncated and pass a secret-redaction pass, but curate before publishing:
the report is for your eyes, a PR is not.
"""

from __future__ import annotations

import argparse
import collections
import datetime as dt
import glob
import json
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path

TRIVIAL = {"cd", "ls", "cat", "echo", "pwd", "clear", "exit"}
INSTRUCTION_RE = re.compile(
    r"\b(sempre|nunca|não faças|nao facas|don't|do not|never|always|from now on|"
    r"doravante|passa a|replace .+ with|em vez de)\b", re.IGNORECASE)
SECRET_RES = [
    re.compile(r"ghp_[A-Za-z0-9_]+"),
    re.compile(r"github_pat_[A-Za-z0-9_]+"),
    re.compile(r"(?<![A-Za-z0-9_-])sk-[A-Za-z0-9_\-]{8,}"),
    re.compile(r"AGE-SECRET-KEY-[0-9A-Z]+"),
    re.compile(r"(?i)\b(password|passwd|token|secret|api[_-]?key)\b\s*[=:]\s*\S+"),
]
QUOTE_MAX = 160
# user-type lines that are harness/skill boilerplate, not the human typing
BOILERPLATE_PREFIXES = (
    "Another Claude session sent a message",
    "Base directory for this skill",
    "Implement card ",
    "Implement the approved ",
    "Pega na tarefa ",
    "Write a git commit message",
)


def redact(text: str) -> str:
    for rx in SECRET_RES:
        text = rx.sub("[REDACTED]", text)
    return text


def quote(obj_ts: str | None, line: str) -> dict:
    q = redact(" ".join(line.split()))
    return {"ts": obj_ts, "quote": (q[:QUOTE_MAX] + "…") if len(q) > QUOTE_MAX else q}


def ts_of(obj: dict) -> str | None:
    t = obj.get("timestamp") or obj.get("ts")
    return t[:10] if isinstance(t, str) else None


def in_since(obj: dict, since: dt.date | None) -> bool:
    if since is None:
        return True
    t = ts_of(obj)
    if t is None:
        return True  # keep undated lines; better noisy than silently dropped
    try:
        return dt.date.fromisoformat(t) >= since
    except ValueError:
        return True


# --- source 1: Claude Code transcripts --------------------------------------

def iter_transcript_files(max_files: int) -> list[Path]:
    root = Path.home() / ".claude" / "projects"
    files = glob.glob(str(root / "*" / "*.jsonl"))
    files.sort(key=lambda p: os.path.getmtime(p), reverse=True)
    return [Path(p) for p in files[:max_files]]


def mine_transcripts(files: list[Path], since: dt.date | None,
                     min_count: int) -> tuple[list[dict], list[dict]]:
    cmd_counter: collections.Counter[str] = collections.Counter()
    cmd_evidence: dict[str, list[dict]] = collections.defaultdict(list)
    instr_counter: collections.Counter[str] = collections.Counter()
    instr_evidence: dict[str, list[dict]] = collections.defaultdict(list)

    for path in files:
        try:
            with path.open(encoding="utf-8", errors="replace") as fh:
                for raw in fh:
                    if len(raw) > 200_000:
                        continue
                    try:
                        obj = json.loads(raw)
                    except json.JSONDecodeError:
                        continue
                    if not in_since(obj, since):
                        continue
                    msg = obj.get("message") or {}
                    content = msg.get("content")
                    if obj.get("type") == "user":
                        text = None
                        if isinstance(content, str):
                            text = content
                        elif isinstance(content, list):
                            texts = [c.get("text", "") for c in content
                                     if isinstance(c, dict) and c.get("type") == "text"]
                            text = " ".join(t for t in texts if t)
                        if not text or text.startswith("<"):
                            continue
                        if text.startswith(BOILERPLATE_PREFIXES) or "<agent-message" in text:
                            continue
                        for rx in INSTRUCTION_RE.finditer(text):
                            phrase = rx.group(0).lower()
                            instr_counter[phrase] += 1
                            if len(instr_evidence[phrase]) < 3:
                                instr_evidence[phrase].append(
                                    quote(ts_of(obj), f"{path.name}: {text}"))
                    elif obj.get("type") == "assistant" and isinstance(content, list):
                        for block in content:
                            if not (isinstance(block, dict)
                                    and block.get("type") == "tool_use"
                                    and block.get("name") == "Bash"):
                                continue
                            cmd = (block.get("input") or {}).get("command") or ""
                            for seg in re.split(r"&&|;|\|", cmd):
                                try:
                                    tokens = shlex.split(seg, posix=True)
                                except ValueError:
                                    tokens = seg.split()
                                while tokens and tokens[0] == "cd":
                                    tokens = tokens[2:]  # drop 'cd <dir>' prefixes
                                if len(tokens) < 2 or tokens[0] in TRIVIAL:
                                    continue
                                key = " ".join(tokens[:2])
                                cmd_counter[key] += 1
                                if len(cmd_evidence[key]) < 3:
                                    cmd_evidence[key].append(
                                        quote(ts_of(obj), f"{path.name}: {seg.strip()}"))
        except OSError:
            continue  # unreadable transcript — skip the file, keep mining

    commands = [{"kind": "repeated command", "key": k, "count": c,
                 "evidence": cmd_evidence[k]}
                for k, c in cmd_counter.most_common(15) if c >= min_count]
    instructions = [{"kind": "instruction language", "key": k, "count": c,
                     "evidence": instr_evidence[k]}
                    for k, c in instr_counter.most_common(10) if c >= min_count]
    return commands, instructions


# --- source 2: tasks/events.jsonl rework loops -------------------------------

def mine_events(root: Path, since: dt.date | None, min_count: int) -> list[dict]:
    events_file = None
    try:
        sys.path.insert(0, str(root / "tasks"))
        from paths import tasks_root  # type: ignore
        events_file = tasks_root() / "events.jsonl"
    except Exception:
        events_file = root / "tasks" / "events.jsonl"
    if not events_file.is_file():
        return []
    bounces: collections.Counter[str] = collections.Counter()
    evidence: dict[str, list[dict]] = collections.defaultdict(list)
    with events_file.open(encoding="utf-8", errors="replace") as fh:
        for raw in fh:
            try:
                e = json.loads(raw)
            except json.JSONDecodeError:
                continue
            if (e.get("type") != "task.phase_changed"
                    or (e.get("payload") or {}).get("from_phase") != "review"
                    or (e.get("payload") or {}).get("phase") != "in_progress"):
                continue
            ts = ts_of(e)
            if not in_since(e, since):
                continue
            tid = e.get("task_id") or "?"
            bounces[tid] += 1
            if len(evidence[tid]) < 3:
                reason = (e.get("payload") or {}).get("reason") or ""
                evidence[tid].append(quote(ts, f"{ts} {reason}"))
    return [{"kind": "rework loop (review -> in_progress)", "key": k, "count": c,
             "evidence": evidence[k]}
            for k, c in bounces.most_common(10) if c >= min_count]


# --- source 3: merged PR churn ------------------------------------------------

def gh_json(args: list[str]) -> list | dict | None:
    try:
        p = subprocess.run(["gh", *args], capture_output=True, text=True, timeout=30)
        return json.loads(p.stdout) if p.returncode == 0 and p.stdout.strip() else None
    except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError):
        return None


def mine_pr_churn(limit: int, min_count: int) -> list[dict]:
    prs = gh_json(["pr", "list", "--state", "merged", "--limit", str(limit),
                   "--json", "number,title,mergedAt"])
    if not prs:
        return []
    files: collections.Counter[str] = collections.Counter()
    evidence: dict[str, list[dict]] = collections.defaultdict(list)
    for pr in prs:
        n = pr.get("number")
        paths = gh_json(["pr", "view", str(n), "--json", "files", "-q",
                         ".files[].path"])
        if isinstance(paths, list):
            for p in paths:
                files[p] += 1
                evidence[p].append({"ts": (pr.get("mergedAt") or "")[:10],
                                    "quote": f"PR #{n}: {pr.get('title', '')}"})
    return [{"kind": "PR churn file", "key": k, "count": c,
             "evidence": evidence[k]}
            for k, c in files.most_common(10) if c >= min_count]


# --- report -------------------------------------------------------------------

def render(candidates: list[dict], header: dict) -> str:
    lines = [
        "# Chronicle candidates",
        "",
        f"Mined {header['generated']} · since {header['since'] or 'beginning'} · "
        f"min-count {header['min_count']} · transcripts {header['transcript_files']} · "
        f"PRs {header['pr_limit']}",
        "",
        "Propose-only: pick real candidates, draft the change, open a "
        "`chronicle/*` PR with this evidence in the body. Merges are human-only. "
        "Curate quotes before publishing (redaction ran, eyes verify).",
        "",
    ]
    if not candidates:
        lines.append("No candidates above threshold. Nothing to propose.")
        return "\n".join(lines) + "\n"
    by_kind: dict[str, list[dict]] = collections.defaultdict(list)
    for c in candidates:
        by_kind[c["kind"]].append(c)
    for kind in sorted(by_kind):
        lines.append(f"## {kind}")
        lines.append("")
        for c in by_kind[kind]:
            lines.append(f"### `{c['key']}` — {c['count']}×")
            for ev in c["evidence"]:
                ts = f" ({ev['ts']})" if ev.get("ts") else ""
                lines.append(f"- {ts} {ev['quote']}")
            lines.append("")
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("action", nargs="?", default="mine", choices=["mine"])
    ap.add_argument("--since", default=None, help="YYYY-MM-DD lower bound")
    ap.add_argument("--min-count", type=int, default=3)
    ap.add_argument("--max-files", type=int, default=50,
                    help="max transcript files (most recent first)")
    ap.add_argument("--pr-limit", type=int, default=10)
    ap.add_argument("--out", default=None, help="write markdown report here")
    ap.add_argument("--json", action="store_true", help="emit candidates as JSON")
    args = ap.parse_args()

    since = dt.date.fromisoformat(args.since) if args.since else None
    rp = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                        capture_output=True, text=True)
    root = Path(rp.stdout.strip()) if rp.returncode == 0 and rp.stdout.strip() else Path.cwd()

    tfiles = iter_transcript_files(args.max_files)
    commands, instructions = mine_transcripts(tfiles, since, args.min_count)
    loops = mine_events(root, since, args.min_count)
    churn = mine_pr_churn(args.pr_limit, args.min_count)
    candidates = commands + instructions + loops + churn

    header = {"generated": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
              "since": args.since, "min_count": args.min_count,
              "transcript_files": len(tfiles), "pr_limit": args.pr_limit}
    if args.json:
        print(json.dumps({"header": header, "candidates": candidates},
                         indent=2, ensure_ascii=False))
    else:
        report = render(candidates, header)
        if args.out:
            Path(args.out).write_text(report, encoding="utf-8")
            print(f"report written: {args.out} ({len(candidates)} candidates)")
        else:
            print(report)


if __name__ == "__main__":
    main()
