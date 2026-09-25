"""Tests for ledger.py — run: python3 -m unittest discover -s .agents/skills/research-report/tests"""
import contextlib
import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import ledger  # noqa: E402

SRC_A = """Market report 2025. The regional market grew 12,5% in 2024,
reaching “EUR 1.200 million” in revenue. Revenue did not grow in 2023."""
SRC_B = "Independent survey: the market grew 12.5% in 2024 according to our panel."


class LedgerTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        self.root = str(self.dir / ".research")
        self.a = self.add(SRC_A, "https://www.example.com/report", "primary")
        self.b = self.add(SRC_B, "https://survey.org/panel", "secondary")

    def tearDown(self):
        self.tmp.cleanup()

    def run_cli(self, *argv):
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
            code = ledger.main(["--root", self.root, *argv])
        return code, out.getvalue()

    def add(self, text, origin, tier):
        f = self.dir / f"src{abs(hash(text))}.txt"
        f.write_text(text)
        code, out = self.run_cli("add", str(f), "--origin", origin, "--tier", tier,
                                 "--published", "2025-01-10")
        self.assertEqual(code, 0)
        return json.loads(out)["id"]

    def led(self):
        return ledger.Ledger(Path(self.root))

    def seal(self, draft="Growth was strong [[c1]]."):
        d = self.dir / "draft.md"
        d.write_text(draft)
        return self.run_cli("seal", "--topic", "Mercado regional", "--draft", str(d),
                            "--out", str(self.dir / "reports"))

    # plan §E.1 — fabricated number is caught by layer 1
    def test_fabricated_number_fails_l1(self):
        code, out = self.run_cli("claim", "c1", "--text", "The market grew 15% in 2024",
                                 "--support", self.a, "grew 12,5% in 2024")
        self.assertEqual(code, 1)
        self.assertIn("'15'", out)

    def test_decimal_conventions_and_glyphs_match(self):
        # 12.5 in claim vs 12,5 in source; straight quotes vs curly in source
        code, _ = self.run_cli("claim", "c1", "--text", "Revenue reached EUR 1,200 million after 12.5% growth in 2024",
                               "--support", self.a, 'grew 12,5% in 2024, reaching "EUR 1.200 million"')
        self.assertEqual(code, 0)

    def test_version_token_matches_literally(self):
        vid = self.add("Python 3.13.0 final: Monday, 2024-10-07", "https://python.org/x", "primary")
        code, _ = self.run_cli("claim", "c1", "--text", "Python 3.13 shipped on 2024-10-07",
                               "--support", vid, "3.13.0 final: Monday, 2024-10-07")
        self.assertEqual(code, 0)
        code, _ = self.run_cli("claim", "c2", "--text", "Python 3.14 shipped on 2024-10-07",
                               "--support", vid, "3.13.0 final: Monday, 2024-10-07")
        self.assertEqual(code, 1)

    # plan §E.3 — whitespace/glyph normalisation still locates the quote
    def test_quote_whitespace_normalised(self):
        code, _ = self.run_cli("claim", "c1", "--text", "The market grew in 2024",
                               "--support", self.a, "grew   12,5%\n in 2024")
        self.assertEqual(code, 0)

    def test_missing_quote_fails(self):
        code, out = self.run_cli("claim", "c1", "--text", "Market doubled",
                                 "--support", self.a, "the market doubled")
        self.assertEqual(code, 1)
        self.assertIn("quote not found", out)

    # plan §E.2 — tampered snapshot is detected and blocks nothing silently
    def test_tampered_snapshot(self):
        self.run_cli("claim", "c1", "--text", "Grew 12,5% in 2024",
                     "--support", self.a, "grew 12,5% in 2024")
        self.run_cli("verdict", "c1", "supports", "--reason", "direct statement")
        rec = self.led().evidence()[self.a]
        obj = Path(self.root) / "objects" / rec["hash"]
        obj.write_text(SRC_A.replace("12,5", "13,5"))
        (claim, l1, final), = self.led().evaluate()
        self.assertEqual(final["status"], "tampered")

    # plan §E.4 — amending a claim after its verdict blocks the seal
    def test_drift_blocks_seal(self):
        self.run_cli("claim", "c1", "--text", "Grew 12,5% in 2024",
                     "--support", self.a, "grew 12,5% in 2024")
        self.run_cli("verdict", "c1", "supports", "--reason", "ok")
        self.run_cli("claim", "c1", "--text", "Grew strongly: 12,5% in 2024",
                     "--support", self.a, "grew 12,5% in 2024")
        code, _ = self.seal()
        self.assertEqual(code, 2)

    def test_pending_verdict_blocks_seal(self):
        self.run_cli("claim", "c1", "--text", "Grew 12,5% in 2024",
                     "--support", self.a, "grew 12,5% in 2024")
        self.assertEqual(self.seal()[0], 2)

    def test_key_claim_needs_two_publishers(self):
        self.run_cli("claim", "c1", "--key", "--text", "Grew 12,5% in 2024",
                     "--support", self.a, "grew 12,5% in 2024")
        self.run_cli("verdict", "c1", "supports", "--reason", "ok")
        self.assertEqual(self.led().evaluate()[0][2]["status"], "single-source")
        self.run_cli("claim", "c1", "--key", "--text", "Grew 12,5% in 2024",
                     "--support", self.a, "grew 12,5% in 2024",
                     "--support", self.b, "grew 12.5% in 2024")
        self.run_cli("verdict", "c1", "supports", "--reason", "two sources agree")
        self.assertEqual(self.led().evaluate()[0][2]["status"], "verified")

    def test_negative_knowledge(self):
        # Quote is byte-true but negated in context: layer 2 says contradicts.
        args = ("claim", "c1", "--text", "Revenue grew in 2023",
                "--support", self.a, "grow in 2023")
        self.run_cli(*args)
        self.run_cli("verdict", "c1", "contradicts", "--reason", "source says did NOT grow")
        # Re-registered under a new id with identical text+evidence: still disproven.
        self.run_cli("claim", "c2", *args[2:])
        finals = {c["id"]: f for c, _, f in self.led().evaluate()}
        self.assertEqual(finals["c2"]["status"], "disproven")
        self.assertFalse(finals["c2"]["pending"])

    # plan §E.5 — verify reproduces the seal; tampering after seal is caught
    def test_seal_and_verify(self):
        self.run_cli("claim", "c1", "--key", "--text", "Grew 12,5% in 2024",
                     "--support", self.a, "grew 12,5% in 2024",
                     "--support", self.b, "grew 12.5% in 2024")
        self.run_cli("verdict", "c1", "supports", "--reason", "two sources agree")
        code, out = self.seal()
        self.assertEqual(code, 0, out)
        res = json.loads(out)
        rdir = Path(res["report"]).parent
        report = (rdir / "report.md").read_text()
        self.assertIn("[c1]", report)
        self.assertIn("1 verified", report)
        self.assertEqual(self.run_cli("verify", str(rdir), "--seal", res["seal"])[0], 0)
        ev = next((rdir / "evidence").iterdir())
        os.chmod(ev, 0o644)
        ev.write_text("changed")
        code, out = self.run_cli("verify", str(rdir))
        self.assertEqual(code, 1)
        self.assertIn("c1", out)

    def test_unverified_claim_is_sealed_with_marker(self):
        self.run_cli("claim", "c1", "--text", "Grew 12,5% in 2024",
                     "--support", self.a, "grew 12,5% in 2024")
        self.run_cli("verdict", "c1", "insufficient", "--reason", "regional scope unclear")
        code, out = self.seal()
        self.assertEqual(code, 0, out)
        self.assertIn("[c1 · UNVERIFIED]", Path(json.loads(out)["report"]).read_text())

    def test_dedup_and_publisher(self):
        again = self.add(SRC_A, "https://other.com/x", "primary")
        self.assertEqual(again, self.a)
        self.assertEqual(ledger.publisher_of("https://news.bbc.co.uk/a"), "bbc.co.uk")
        self.assertEqual(ledger.publisher_of("https://www.example.com/a"), "example.com")


if __name__ == "__main__":
    unittest.main()
