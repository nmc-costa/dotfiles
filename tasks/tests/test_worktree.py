#!/usr/bin/env python3
"""Tests for tasks/worktree.py and dispatch.py --worktree.

Every test runs against a throwaway git repo with TSK_ROOT pointing at its
tasks/ dir, calling the scripts via subprocess — the live
~/dotfiles/tasks/events.jsonl is never touched (asserted in tearDown).

    python3 -m unittest discover -s tasks/tests -v
"""
import json
import os
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent
LIVE_LOG = Path("~/dotfiles/tasks/events.jsonl").expanduser()
CHAIN = ["planning", "in_progress", "review", "validation", "done"]


def run(*args, env, cwd=None, check=False):
    result = subprocess.run([sys.executable, *map(str, args)], env=env, cwd=cwd, capture_output=True, text=True)
    if check and result.returncode != 0:
        raise AssertionError(f"{args} -> {result.returncode}\n{result.stdout}\n{result.stderr}")
    return result


class WorktreeTest(unittest.TestCase):
    def setUp(self):
        self.live_mtime = LIVE_LOG.stat().st_mtime if LIVE_LOG.exists() else None
        self.tmp = Path(tempfile.mkdtemp(prefix="tsk-wt-")).resolve()
        self.repo = self.tmp / "repo"
        (self.repo / "tasks").mkdir(parents=True)
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.name", "test")
        self.git("config", "user.email", "test@example.invalid")
        (self.repo / "README").write_text("x\n")
        self.git("add", "README")
        self.git("commit", "-q", "-m", "init")
        self.env = {**os.environ, "TSK_ROOT": str(self.repo / "tasks")}
        self.env.pop("TSK_HARNESS", None)
        self.base = self.tmp / "repo.worktrees"
        for task_id in ("t1", "t2"):
            self.event("task.created", task_id, {"title": task_id.upper(), "project": "test"})

    def tearDown(self):
        # remove worktrees first so the tmp dir can go
        subprocess.run(["rm", "-rf", str(self.tmp)])
        now = LIVE_LOG.stat().st_mtime if LIVE_LOG.exists() else None
        self.assertEqual(self.live_mtime, now, "live tasks/events.jsonl was modified by a test")

    def git(self, *args, cwd=None):
        return subprocess.run(["git", *args], cwd=str(cwd or self.repo), capture_output=True, text=True, check=True)

    def event(self, type_, task_id, payload):
        run(SRC / "append_event.py", "--type", type_, "--actor-kind", "agent", "--actor-id", "test",
            "--task-id", task_id, "--payload", json.dumps(payload), env=self.env, check=True)

    def to_done(self, task_id):
        prev = "backlog"
        for phase in CHAIN:
            self.event("task.phase_changed", task_id, {"phase": phase, "from_phase": prev})
            prev = phase

    def wt(self, *args, cwd=None):
        return run(SRC / "worktree.py", *args, env=self.env, cwd=cwd)

    def create(self, task_id="t1", harness="claude", *extra):
        return self.wt("create", "--task-id", task_id, "--harness", harness, *extra)

    # 1 — parser + managed filter
    def test_list_shows_only_managed(self):
        self.git("worktree", "add", "-q", "--detach", str(self.tmp / "detached"))
        self.git("worktree", "add", "-q", "-b", "claude/t2", str(self.tmp / "foreign"))
        self.git("worktree", "add", "-q", "-b", "x/locked", str(self.tmp / "locked"))
        self.git("worktree", "lock", "--reason", "busy", str(self.tmp / "locked"))
        self.assertEqual(self.create().returncode, 0)
        out = self.wt("list")
        self.assertEqual(out.returncode, 0, out.stderr)
        rows = [line.split("\t") for line in out.stdout.splitlines()]
        self.assertEqual(len(rows), 1, out.stdout)
        self.assertEqual(rows[0][:3], ["t1", "claude", "claude/t1"])
        self.assertEqual(rows[0][3], str(self.base / "claude" / "t1"))
        data = json.loads(self.wt("list", "--json").stdout)
        self.assertEqual([d["task_id"] for d in data], ["t1"])

    # 2 — create / path
    def test_create_idempotent_and_path(self):
        first, second = self.create(), self.create()
        self.assertEqual(first.returncode, 0, first.stderr)
        path, branch, status = first.stdout.strip().split("\t")
        self.assertEqual((branch, status), ("claude/t1", "created"))
        self.assertEqual(second.stdout.strip().split("\t"), [path, branch, "existing"])
        self.assertEqual(self.wt("path", "--task-id", "t1", "--harness", "claude").stdout.strip(), path)
        self.assertEqual(self.wt("path", "--task-id", "t1", "--harness", "agy").returncode, 1)

    def test_harness_from_env(self):
        self.env["TSK_HARNESS"] = "copilot"
        out = self.wt("create", "--task-id", "t1")
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn("copilot/t1", out.stdout)

    def test_existing_branch_needs_reuse(self):
        self.git("branch", "claude/t1")
        refused = self.create()
        self.assertEqual(refused.returncode, 1)
        self.assertIn("--reuse-branch", refused.stderr)
        ok = self.create("t1", "claude", "--reuse-branch")
        self.assertEqual(ok.returncode, 0, ok.stderr)
        self.assertTrue(ok.stdout.strip().endswith("created"))

    def test_bad_input_exits_1(self):
        self.assertEqual(self.create("nope").returncode, 1)
        self.assertEqual(self.create("t1", "vim").returncode, 1)
        self.assertEqual(self.create("../t1").returncode, 1)
        self.assertEqual(self.wt("create", "--task-id", "t1").returncode, 1)  # no harness at all

    # 3 — remove / prune guard
    def test_remove_guard_and_branch_kept(self):
        path = Path(self.create().stdout.split("\t")[0])
        (path / "scratch.txt").write_text("wip\n")
        refused = self.wt("remove", "--task-id", "t1", "--harness", "claude")
        self.assertEqual(refused.returncode, 2)
        self.assertTrue(path.exists())
        inside = self.wt("remove", "--task-id", "t1", "--harness", "claude", cwd=path)
        self.assertEqual(inside.returncode, 2)
        (path / "scratch.txt").unlink()
        self.git("worktree", "lock", str(path))
        self.assertEqual(self.wt("remove", "--task-id", "t1", "--harness", "claude").returncode, 2)
        self.git("worktree", "unlock", str(path))
        ok = self.wt("remove", "--task-id", "t1", "--harness", "claude")
        self.assertEqual(ok.returncode, 0, ok.stderr)
        self.assertFalse(path.exists())
        self.assertIn("claude/t1", self.git("branch", "--list", "claude/t1").stdout)

    def test_prune_only_done_and_managed(self):
        p1 = Path(self.create("t1").stdout.split("\t")[0])
        p2 = Path(self.create("t2").stdout.split("\t")[0])
        self.git("worktree", "add", "-q", "--detach", str(self.tmp / "detached"))
        self.to_done("t1")
        dry = self.wt("prune")
        self.assertEqual(dry.returncode, 0, dry.stderr)
        self.assertEqual(dry.stdout.split("\t")[:2], ["would-remove", str(p1)])
        self.assertTrue(p1.exists())
        applied = self.wt("prune", "--apply")
        self.assertEqual(applied.returncode, 0, applied.stderr)
        self.assertFalse(p1.exists())
        self.assertTrue(p2.exists())
        self.assertTrue((self.tmp / "detached").exists())

    # 4 — view + card line
    def test_view_and_card_bytes_stable(self):
        gen = SRC / "generators" / "rebuild_cards.py"
        run(gen, env=self.env, check=True)
        card = self.repo / "tasks" / "cards" / "t1.md"
        before = card.read_bytes()
        self.assertIn(b"Worktrees (this machine): [worktrees/t1.md]", before)
        self.create()
        view = self.repo / "tasks" / "cards" / "worktrees" / "t1.md"
        self.assertTrue(view.exists())
        self.assertIn("claude/t1", view.read_text())
        self.assertIn("t1", (view.parent / "README.md").read_text())
        run(gen, env=self.env, check=True)
        self.assertEqual(card.read_bytes(), before)
        self.wt("remove", "--task-id", "t1", "--harness", "claude")
        self.assertFalse(view.exists())

    # 5 — dispatch --worktree
    def test_dispatch_worktree(self):
        bindir = self.tmp / "bin"
        bindir.mkdir()
        record = self.tmp / "record.json"
        fake = bindir / "claude"
        fake.write_text("#!/usr/bin/env python3\nimport json, os, sys\n"
                        f"json.dump({{'pwd': os.getcwd(), 'harness': os.environ.get('TSK_HARNESS'), 'argv': sys.argv}}, open({str(record)!r}, 'w'))\n")
        fake.chmod(fake.stat().st_mode | stat.S_IEXEC)
        self.env["PATH"] = f"{bindir}{os.pathsep}{self.env['PATH']}"
        expected = self.base / "claude" / "t1"

        dry = run(SRC / "dispatch.py", "--task-id", "t1", "--provider", "claude", "--worktree", env=self.env)
        self.assertEqual(dry.returncode, 0, dry.stderr)
        self.assertTrue(dry.stdout.startswith(f"cd {expected} && "), dry.stdout)
        self.assertFalse(expected.exists())

        live = run(SRC / "dispatch.py", "--task-id", "t1", "--provider", "claude", "--worktree", "--launch", env=self.env)
        self.assertEqual(live.returncode, 0, live.stderr)
        got = json.loads(record.read_text())
        self.assertEqual(got["pwd"], str(expected))
        self.assertEqual(got["harness"], "claude")
        self.assertIn(f"Your worktree for this card: {expected}", got["argv"][1])


if __name__ == "__main__":
    unittest.main()
