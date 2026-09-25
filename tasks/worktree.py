#!/usr/bin/env python3
"""tsk worktree: one git worktree per (harness, card) — the same command for
every harness (Claude Code, Copilot CLI, Gemini CLI, Antigravity, Codex).

Turns tasks/plans/claim-protocol.md section B ("code for a claimed task ->
one worktree per task") into code instead of prose. Each harness's own
native worktree feature (`claude -w`, `gemini -w`, `codex --worktree`,
EnterWorktree) picks its own location and naming, and Copilot CLI / agy
have none at all — so this is the single, uniform layer, and the only
cross-harness mechanism it relies on is "run the CLI with its cwd inside
the worktree" (see tasks/plans/card-worktrees.md).

Layout (fixed, never configurable in v1):
    <repo-parent>/<repo-name>.worktrees/<harness>/<task-id>   (worktree)
    <harness>/<task-id>                                       (branch)
where <repo> is always the main checkout that holds tasks_root() — so the
command and the card view can never point at different repos.

Only worktrees at exactly that path are "managed": a branch that merely
looks like `claude/<task-id>` (another workflow, a `.claude/worktrees/`
entry, a hand-made `git worktree add`) is never listed, touched or pruned.

Stdout contract mirrors coderabbitai/git-worktree-runner's `new
--porcelain` record (tab-separated fields, progress on stderr) rather than
inventing a format; `list` reads git's own `worktree list --porcelain`.

Usage:
    python3 ~/dotfiles/tasks/worktree.py create --task-id <id> --harness claude
        -> "<path>\\t<branch>\\tcreated|existing"
    wt=$(python3 ~/dotfiles/tasks/worktree.py create --task-id <id> --harness claude) \
        && cd "$(printf %s "$wt" | cut -f1)" || echo "STOP: worktree create failed"
        (shell one-liner for humans — an agent session should instead be
        started with its cwd already in the worktree: dispatch.py --worktree)
    python3 ~/dotfiles/tasks/worktree.py path   --task-id <id> --harness claude
    python3 ~/dotfiles/tasks/worktree.py list   [--task-id <id>] [--json]
    python3 ~/dotfiles/tasks/worktree.py remove --task-id <id> --harness claude
    python3 ~/dotfiles/tasks/worktree.py prune  [--apply]     # done cards only, dry-run by default
    python3 ~/dotfiles/tasks/worktree.py view                 # regenerate tasks/cards/worktrees/

--harness defaults to $TSK_HARNESS (dispatch.py --worktree sets it).

Exit codes: 0 ok; 1 bad input (unknown task/harness, branch already exists
without a managed worktree and no --reuse-branch, worktree absent); 2
refused by the safety guard (dirty, locked, or you are standing in it);
3 git error.

Never deletes a branch and never passes --force: removal is `git worktree
remove`, whose own dirty check is a second guard behind ours. Live state
goes to tasks/cards/worktrees/ — gitignored and per-machine, because the
tracked cards must not churn with machine-local paths (every card links
to its file there with one fixed, path-free line instead).
"""
import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

TASKS_DIR = Path(__file__).parent
sys.path.insert(0, str(TASKS_DIR))
from lifecycle import project as project_phases, tasks_root  # noqa: E402

HARNESSES = ("claude", "copilot", "gemini", "agy", "codex")
TASK_ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")


class WorktreeError(Exception):
    def __init__(self, message, code=1):
        super().__init__(message)
        self.code = code


def git(*args, cwd, check=True):
    result = subprocess.run(["git", *args], cwd=str(cwd), capture_output=True, text=True)
    if check and result.returncode != 0:
        raise WorktreeError(f"git {' '.join(args)}: {result.stderr.strip()}", code=3)
    return result


def main_repo():
    """The main checkout (not a worktree) that holds tasks_root()."""
    root = tasks_root()
    common = git("rev-parse", "--path-format=absolute", "--git-common-dir", cwd=root).stdout.strip()
    return Path(common).parent


def base_dir(repo):
    return repo.parent / f"{repo.name}.worktrees"


def managed_path(repo, harness, task_id):
    return base_dir(repo) / harness / task_id


def load_events():
    events_file = tasks_root() / "events.jsonl"
    if not events_file.exists():
        return []
    events = [json.loads(line) for line in events_file.read_text(encoding="utf-8").splitlines() if line.strip()]
    events.sort(key=lambda e: e["ts"])
    return events


def parse_porcelain(text):
    """`git worktree list --porcelain` -> list of dicts. Records are
    blank-line separated; `branch` is absent for detached/bare entries and
    `locked`/`prunable` may carry a reason."""
    records, current = [], {}
    for line in text.splitlines():
        if not line.strip():
            if current:
                records.append(current)
            current = {}
            continue
        key, _, value = line.partition(" ")
        if key == "worktree":
            current = {"path": value, "head": None, "branch": None, "detached": False,
                       "bare": False, "locked": None, "prunable": None}
        elif key == "HEAD":
            current["head"] = value
        elif key == "branch":
            current["branch"] = value.removeprefix("refs/heads/")
        elif key in ("detached", "bare"):
            current[key] = True
        elif key in ("locked", "prunable"):
            current[key] = value or "yes"
    if current:
        records.append(current)
    return records


def managed(repo, phases=None):
    """Worktrees whose resolved path is exactly base_dir/<harness>/<task-id>
    for a harness in HARNESSES and a task_id that exists. Path equality —
    never branch-name matching — is what makes a worktree ours."""
    phases = phases if phases is not None else project_phases(load_events())
    out = git("worktree", "list", "--porcelain", cwd=repo).stdout
    base = base_dir(repo).resolve()
    result = []
    for rec in parse_porcelain(out):
        path = Path(rec["path"]).resolve()
        if path.parent.parent != base:
            continue
        harness, task_id = path.parent.name, path.name
        if harness not in HARNESSES or task_id not in phases:
            continue
        result.append({**rec, "path": str(path), "harness": harness, "task_id": task_id,
                       "phase": phases[task_id]["phase"]})
    return sorted(result, key=lambda r: (r["task_id"], r["harness"]))


def is_clean(path):
    status = git("status", "--porcelain", "--untracked-files=all", cwd=path, check=False)
    return status.returncode == 0 and not status.stdout.strip()


def validate(task_id, harness, phases):
    if harness not in HARNESSES:
        raise WorktreeError(f"unknown harness {harness!r} (one of {', '.join(HARNESSES)}; or set $TSK_HARNESS)")
    if not TASK_ID_RE.match(task_id or ""):
        raise WorktreeError(f"invalid task id {task_id!r} (must match {TASK_ID_RE.pattern})")
    if task_id not in phases:
        raise WorktreeError(f"unknown task_id: {task_id!r} (no event for it in {tasks_root() / 'events.jsonl'})")


def find(repo, task_id, harness, phases=None):
    return next((w for w in managed(repo, phases) if w["task_id"] == task_id and w["harness"] == harness), None)


def create(task_id, harness, base="HEAD", reuse_branch=False):
    repo = main_repo()
    phases = project_phases(load_events())
    validate(task_id, harness, phases)
    branch = f"{harness}/{task_id}"
    existing = find(repo, task_id, harness, phases)
    if existing:
        return existing["path"], existing["branch"] or branch, "existing"

    path = managed_path(repo, harness, task_id)
    if path.exists():
        raise WorktreeError(f"{path} exists but is not a registered worktree — move it aside first")
    branch_exists = git("show-ref", "--verify", "--quiet", f"refs/heads/{branch}", cwd=repo, check=False).returncode == 0
    path.parent.mkdir(parents=True, exist_ok=True)
    if branch_exists:
        if not reuse_branch:
            raise WorktreeError(
                f"branch {branch!r} already exists with no managed worktree — it may belong to other work; "
                f"pass --reuse-branch to check it out at {path} anyway")
        git("worktree", "add", str(path), branch, cwd=repo)
    else:
        git("worktree", "add", "-b", branch, str(path), base, cwd=repo)
    return str(path), branch, "created"


def guard(wt):
    """Reasons removal must be refused (empty list = safe)."""
    reasons = []
    if wt["locked"]:
        reasons.append(f"locked ({wt['locked']})")
    if not is_clean(wt["path"]):
        reasons.append("uncommitted or untracked changes")
    cwd = Path.cwd().resolve()
    if cwd == Path(wt["path"]) or Path(wt["path"]) in cwd.parents:
        reasons.append("your cwd is inside it")
    return reasons


def remove_one(repo, wt):
    reasons = guard(wt)
    if reasons:
        raise WorktreeError(f"refused: {wt['path']}: {'; '.join(reasons)}", code=2)
    git("worktree", "remove", wt["path"], cwd=repo)


def remove(task_id, harness):
    repo = main_repo()
    wt = find(repo, task_id, harness)
    if not wt:
        raise WorktreeError(f"no managed worktree for {harness}/{task_id}")
    remove_one(repo, wt)
    return wt


def prune(apply):
    """(action, path, reason) for every managed worktree of a done card."""
    repo = main_repo()
    rows = []
    for wt in managed(repo):
        if wt["phase"] != "done":
            continue
        reasons = guard(wt)
        if reasons:
            rows.append(("refused", wt["path"], "; ".join(reasons)))
        elif not apply:
            rows.append(("would-remove", wt["path"], "card is done"))
        else:
            git("worktree", "remove", wt["path"], cwd=repo)
            rows.append(("removed", wt["path"], "card is done"))
    return rows


def tilde(path):
    home = str(Path.home())
    return "~" + path[len(home):] if path.startswith(home + os.sep) else path


def write_view():
    """Regenerate tasks/cards/worktrees/ (gitignored, per-machine): one
    <task-id>.md per card with managed worktrees + a README.md index.
    Stale files are removed so the folder always mirrors `git worktree list`."""
    view_dir = tasks_root() / "cards" / "worktrees"
    view_dir.mkdir(parents=True, exist_ok=True)
    try:
        rows = managed(main_repo())
    except WorktreeError as exc:
        print(f"warning: worktree view not refreshed: {exc}", file=sys.stderr)
        return view_dir
    by_task = {}
    for wt in rows:
        wt["clean"] = is_clean(wt["path"])
        by_task.setdefault(wt["task_id"], []).append(wt)

    for stale in view_dir.glob("*.md"):
        if stale.name != "README.md" and stale.stem not in by_task:
            stale.unlink()
    for task_id, wts in by_task.items():
        lines = [f"# Worktrees — {task_id}", "",
                 f"Card: [../{task_id}.md](../{task_id}.md) · generated by `tasks/worktree.py`, per-machine, gitignored.", "",
                 "| harness | branch | path | head | state |", "|---|---|---|---|---|"]
        for wt in wts:
            state = "clean" if wt["clean"] else "dirty"
            if wt["locked"]:
                state += ", locked"
            lines.append(f"| {wt['harness']} | `{wt['branch'] or '(detached)'}` | `{tilde(wt['path'])}` "
                         f"| `{(wt['head'] or '')[:8]}` | {state} |")
        lines += ["", f"Enter it: `cd \"$(python3 ~/dotfiles/tasks/worktree.py path --task-id {task_id} --harness <harness>)\"`", ""]
        (view_dir / f"{task_id}.md").write_text("\n".join(lines), encoding="utf-8")

    index = ["# Worktrees on this machine", "",
             "Generated by `tasks/worktree.py` — gitignored, never committed. One file per card with a managed",
             "worktree at `<repo>.worktrees/<harness>/<task-id>`.", ""]
    if by_task:
        index += ["| card | phase | harnesses |", "|---|---|---|"]
        for task_id, wts in sorted(by_task.items()):
            index.append(f"| [{task_id}]({task_id}.md) | {wts[0]['phase']} | {', '.join(w['harness'] for w in wts)} |")
    else:
        index.append("_No managed worktrees right now._")
    index.append("")
    (view_dir / "README.md").write_text("\n".join(index), encoding="utf-8")
    return view_dir


def resolve_harness(args):
    harness = getattr(args, "harness", None) or os.environ.get("TSK_HARNESS")
    if not harness:
        raise WorktreeError("no harness: pass --harness or set $TSK_HARNESS")
    return harness


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)

    def with_task(p, harness=True):
        p.add_argument("--task-id", required=True)
        if harness:
            p.add_argument("--harness", help=f"one of {', '.join(HARNESSES)} (default: $TSK_HARNESS)")
        return p

    p_create = with_task(sub.add_parser("create", help="create (or return) the worktree for a card"))
    p_create.add_argument("--base", default="HEAD", help="start point for a new branch (default: HEAD of the main checkout)")
    p_create.add_argument("--reuse-branch", action="store_true", help="check out an already-existing <harness>/<task-id> branch")
    with_task(sub.add_parser("path", help="print the worktree path"))
    p_list = sub.add_parser("list", help="list managed worktrees")
    p_list.add_argument("--task-id")
    p_list.add_argument("--json", action="store_true")
    with_task(sub.add_parser("remove", help="remove a clean worktree (branch is kept)"))
    p_prune = sub.add_parser("prune", help="remove clean worktrees of done cards (dry-run unless --apply)")
    p_prune.add_argument("--apply", action="store_true")
    sub.add_parser("view", help="regenerate tasks/cards/worktrees/")
    args = parser.parse_args()

    try:
        if args.cmd == "create":
            path, branch, status = create(args.task_id, resolve_harness(args), args.base, args.reuse_branch)
            write_view()
            print(f"{path}\t{branch}\t{status}")
        elif args.cmd == "path":
            harness = resolve_harness(args)
            validate(args.task_id, harness, project_phases(load_events()))
            wt = find(main_repo(), args.task_id, harness)
            if not wt:
                raise WorktreeError(f"no managed worktree for {harness}/{args.task_id}")
            print(wt["path"])
        elif args.cmd == "list":
            rows = [w for w in managed(main_repo()) if not args.task_id or w["task_id"] == args.task_id]
            for w in rows:
                w["clean"] = is_clean(w["path"])
            if args.json:
                print(json.dumps(rows, indent=2))
            else:
                for w in rows:
                    print("\t".join([w["task_id"], w["harness"], w["branch"] or "-", w["path"],
                                     "clean" if w["clean"] else "dirty", "locked" if w["locked"] else "-"]))
        elif args.cmd == "remove":
            wt = remove(args.task_id, resolve_harness(args))
            write_view()
            print(f"removed\t{wt['path']}\tbranch-kept")
        elif args.cmd == "prune":
            rows = prune(args.apply)
            if args.apply:
                write_view()
            for row in rows:
                print("\t".join(row))
            if any(r[0] == "refused" for r in rows):
                sys.exit(2)
        elif args.cmd == "view":
            print(write_view())
    except WorktreeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(exc.code)


if __name__ == "__main__":
    main()
