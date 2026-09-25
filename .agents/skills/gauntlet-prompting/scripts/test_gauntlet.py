#!/usr/bin/env python3
"""Tests for gauntlet_ledger.py and render_prompt.py.

    python3 .agents/skills/gauntlet-prompting/scripts/test_gauntlet.py
"""
import contextlib
import io
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gauntlet_ledger as L  # noqa: E402
import render_prompt as R  # noqa: E402


def run(mod, *argv):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = mod.main(list(argv))
    return code, out.getvalue().strip(), err.getvalue().strip()


class LedgerTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        patcher = mock.patch.dict(os.environ, {"GAUNTLET_STATE_DIR": self.tmp.name})
        patcher.start()
        self.addCleanup(patcher.stop)
        self.cand = Path(self.tmp.name) / "cand.html"
        self.cand.write_text("candidate")
        self.bar = "https://example.com"

    def play(self, slug, piece, candidate_wins, reason, seed=None):
        _, out, _ = run(L, "pair", slug, piece, "--candidate", str(self.cand), "--bar", self.bar,
                        *(["--seed", str(seed)] if seed is not None else []))
        a_is_bar = out.splitlines()[0] == f"A={self.bar}"
        cand_label = "B" if a_is_bar else "A"
        pick = cand_label if candidate_wins else ("A" if cand_label == "B" else "B")
        code, _, err = run(L, "verdict", slug, piece, pick, "--reason", reason)
        self.assertEqual(code, 0, err)
        return run(L, "status", slug, piece)[1]

    def test_shuffle_is_balanced(self):
        run(L, "init", "s", "--max-rounds", "1000")
        a_count = 0
        for seed in range(200):
            _, out, _ = run(L, "pair", "s", "p", "--candidate", str(self.cand), "--bar", self.bar,
                            "--seed", str(seed))
            a_count += out.splitlines()[0] != f"A={self.bar}"
        self.assertTrue(80 <= a_count <= 120, a_count)

    def test_candidate_staged_under_neutral_name(self):
        run(L, "init", "s")
        _, out, _ = run(L, "pair", "s", "p", "--candidate", str(self.cand), "--bar", self.bar, "--seed", "1")
        self.assertNotIn("cand", out)
        staged = [line.split("=", 1)[1] for line in out.splitlines() if not line.endswith(self.bar)][0]
        self.assertEqual(Path(staged).read_text(), "candidate")

    def test_win(self):
        run(L, "init", "s")
        self.assertEqual(self.play("s", "p", True, "none"), "WIN")

    def test_budget(self):
        run(L, "init", "s", "--max-rounds", "3")
        reasons = ["typography is cramped", "no hero image at all", "footer links broken"]
        statuses = [self.play("s", "p", False, r) for r in reasons]
        self.assertEqual(statuses, ["CONTINUE", "CONTINUE", "STOP_BUDGET"])
        code, _, err = run(L, "pair", "s", "p", "--candidate", str(self.cand), "--bar", self.bar)
        self.assertEqual(code, 2)
        self.assertIn("STOP_BUDGET", err)

    def test_plateau(self):
        run(L, "init", "s", "--max-rounds", "10")
        statuses = [self.play("s", "p", False, "the typography is cramped and hard to read") for _ in range(3)]
        self.assertEqual(statuses[-1], "STOP_PLATEAU")

    def test_varied_losses_continue(self):
        run(L, "init", "s", "--max-rounds", "10")
        reasons = ["typography is cramped", "no hero image at all", "footer links broken"]
        self.assertEqual([self.play("s", "p", False, r) for r in reasons][-1], "CONTINUE")

    def test_pieces_are_independent(self):
        run(L, "init", "s")
        self.play("s", "a", True, "x")
        self.play("s", "b", False, "gap")
        self.assertEqual(run(L, "status", "s")[1].splitlines(), ["a WIN", "b CONTINUE"])

    def test_verdict_without_pair_fails(self):
        run(L, "init", "s")
        code, _, err = run(L, "verdict", "s", "p", "A", "--reason", "x")
        self.assertEqual(code, 2)
        self.assertIn("pair", err)

    def test_init_refuses_overwrite_and_bad_slug(self):
        self.assertEqual(run(L, "init", "s")[0], 0)
        self.assertEqual(run(L, "init", "s")[0], 2)
        self.assertEqual(run(L, "init", "../x")[0], 2)


class RenderTest(unittest.TestCase):
    GOAL = "a landing page for my dotfiles"

    def test_each_harness(self):
        for harness in R.DELEGATION:
            text = R.render(self.GOAL, "https://charm.sh", harness, 3, "slug")
            self.assertLessEqual(R.word_count(text), R.MAX_WORDS, harness)
            self.assertNotIn("{{", text)
            self.assertIn("--max-rounds 3", text)
            if harness == "claude":
                self.assertIn("Agent tool", text)
            else:
                self.assertIn("reset", text)
            self.assertEqual("unverified" in text, harness == "agy")

    def test_task_line(self):
        self.assertIn("Kanban card: dotfiles-x", R.render(self.GOAL, "/", "claude", task_id="dotfiles-x"))

    def test_word_limit_enforced(self):
        code, _, err = run(R, "render", "--goal", "word " * 300, "--bar", "/")
        self.assertEqual(code, 1)
        self.assertIn("words", err)

    def test_check_bar_path_and_command(self):
        self.assertTrue(R.check_bar(__file__)[0])
        self.assertTrue(R.check_bar("cmd:python3 --help")[0])
        self.assertFalse(R.check_bar("/definitely/not/here")[0])
        self.assertFalse(R.check_bar("cmd:no-such-cmd-xyz --flag")[0])

    def test_vague_bar_rejected(self):
        # `make` is on PATH; without the cmd: prefix this must still fail.
        for vague in ("make it great", "excellent", "production-ready"):
            self.assertFalse(R.check_bar(vague)[0], vague)

    def test_check_bar_url(self):
        with mock.patch.object(R, "url_ok", return_value=(True, "HTTP 200")):
            self.assertEqual(R.check_bar("https://charm.sh")[:2], (True, "url"))
        with mock.patch.object(R, "url_ok", return_value=(False, "HTTP 404")):
            self.assertFalse(R.check_bar("https://charm.sh/nope")[0])


if __name__ == "__main__":
    unittest.main()
