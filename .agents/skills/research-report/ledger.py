#!/usr/bin/env python3
"""Evidence ledger for the research-report skill (stdlib only).

Layer 1 (deterministic) of the skill's two-layer verification: every claim
must carry verbatim support quotes from captured evidence snapshots; this
script proves the quotes and the claim's numbers exist in those snapshots,
detects tampered/missing snapshots, binds layer-2 (semantic) verdicts to the
exact claim+evidence state they judged, and seals a report whose manifest
hash anyone can recompute.

Core ideas (content-addressed store, claim<->evidence binding, byte-level
literal checks, honest verdict markers, falsification log, sealed manifest)
are ported from PerryLink/dsh-research-report (Apache-2.0) — see NOTICE.

State lives in ./.research/ (override with --root or $RESEARCH_LEDGER):
  objects/<sha256>   immutable snapshots
  evidence.jsonl     evidence index (first row per id wins)
  claims.jsonl       claim registrations (latest row per id wins)
  verdicts.jsonl     layer-2 verdicts (latest row per claim wins)
  disproofs.jsonl    negative knowledge: disproven claim-text+evidence hashes
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import html
import json
import os
import re
import shutil
import sys
import unicodedata
import urllib.request
from pathlib import Path

SCHEMA = "research-report/v1"
MAX_BYTES = 5 * 1024 * 1024
L2_STATUSES = ("supports", "partial", "disputed", "contradicts", "insufficient")
FINAL_ORDER = ("verified", "single-source", "partial", "disputed",
               "unverified", "disproven", "tampered")
TIERS = ("primary", "secondary", "tertiary")
# Second-level public suffixes common enough to matter for publisher grouping.
SLD = {"co.uk", "ac.uk", "gov.uk", "org.uk", "com.pt", "gov.pt", "org.pt",
       "com.br", "gov.br", "com.au", "co.jp", "europa.eu"}


class LedgerError(Exception):
    pass


# ── helpers ────────────────────────────────────────────────────────────────

def now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canon(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":")).encode()


_GLYPHS = str.maketrans({
    "\u201c": '"', "\u201d": '"', "\u201e": '"', "\u00ab": '"', "\u00bb": '"',
    "\u300c": '"', "\u300d": '"', "\u2018": "'", "\u2019": "'", "\u201a": "'",
    "\u2013": "-", "\u2014": "-", "\u2212": "-", "\u00ad": None,
})


def norm(text: str) -> str:
    """NFKC + quote/dash glyph folding + whitespace collapse. Case is kept."""
    text = unicodedata.normalize("NFKC", text).translate(_GLYPHS)
    return re.sub(r"\s+", " ", text).strip()


_NUM = re.compile(r"\d+(?:[.,\u202f\u00a0 ]\d+)*")


def numbers(text: str) -> list[str]:
    return [m.group(0) for m in _NUM.finditer(norm(text))]


def num_values(tok: str) -> set[float]:
    """Both decimal conventions: 1,234.5 (en) and 1.234,5 (pt/eu)."""
    tok = re.sub(r"[\u202f\u00a0 ]", "", tok)
    out = set()
    for thousands, decimal in ((",", "."), (".", ",")):
        t = tok.replace(thousands, "")
        if t.count(decimal) <= 1:
            try:
                out.add(float(t.replace(decimal, ".")))
            except ValueError:
                pass
    return out


def publisher_of(origin: str) -> str:
    m = re.match(r"https?://([^/:]+)", origin)
    if not m:
        return "local:" + origin
    host = m.group(1).lower().removeprefix("www.")
    labels = host.split(".")
    if len(labels) >= 3 and ".".join(labels[-2:]) in SLD:
        return ".".join(labels[-3:])
    return ".".join(labels[-2:])


def html_to_text(raw: str) -> str:
    raw = re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>", " ", raw)
    raw = re.sub(r"(?i)<br\s*/?>|</(p|div|li|h\d|tr)>", "\n", raw)
    return html.unescape(re.sub(r"<[^>]+>", " ", raw))


# ── ledger ─────────────────────────────────────────────────────────────────

class Ledger:
    def __init__(self, root: Path):
        self.root = root
        self.objects = root / "objects"

    def _path(self, name: str) -> Path:
        return self.root / f"{name}.jsonl"

    def _rows(self, name: str) -> list[dict]:
        p = self._path(name)
        if not p.exists():
            return []
        rows = []
        for n, line in enumerate(p.read_text().splitlines(), 1):
            if line.strip():
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError as e:
                    raise LedgerError(f"{p}:{n}: corrupt JSONL ({e})")
        return rows

    def _append(self, name: str, row: dict) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        with self._path(name).open("a") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    # evidence
    def evidence(self) -> dict[str, dict]:
        out: dict[str, dict] = {}
        for r in self._rows("evidence"):
            out.setdefault(r["id"], r)
        return out

    def add(self, data: bytes, origin: str, title: str = "", tier: str = "",
            published: str = "", publisher: str = "") -> tuple[dict, bool]:
        if not data.strip():
            raise LedgerError("empty evidence")
        if len(data) > MAX_BYTES:
            raise LedgerError(f"evidence over {MAX_BYTES} bytes")
        h = sha256(data)
        for rec in self.evidence().values():
            if rec["hash"] == h:
                return rec, True
        self.objects.mkdir(parents=True, exist_ok=True)
        tmp = self.objects / f".{h}.tmp"
        tmp.write_bytes(data)
        tmp.replace(self.objects / h)
        rec = {"id": f"ev-{h[:12]}", "hash": h, "origin": origin,
               "title": title, "tier": tier, "published": published,
               "publisher": publisher or publisher_of(origin),
               "captured_at": now(), "bytes": len(data)}
        self._append("evidence", rec)
        return rec, False

    def snapshot(self, ev_id: str, objects: Path | None = None
                 ) -> tuple[str, str | None]:
        """Return (integrity, text): ok | tampered | missing | unknown."""
        rec = self.evidence().get(ev_id)
        if rec is None:
            return "unknown", None
        p = (objects or self.objects) / rec["hash"]
        if not p.exists():
            return "missing", None
        data = p.read_bytes()
        if sha256(data) != rec["hash"]:
            return "tampered", None
        return "ok", data.decode("utf-8", errors="replace")

    # claims
    def claims(self) -> dict[str, dict]:
        return {r["id"]: r for r in self._rows("claims")}

    def add_claim(self, cid: str, text: str, support: list[list[str]],
                  key: bool) -> dict:
        if not re.fullmatch(r"[A-Za-z0-9_.-]+", cid):
            raise LedgerError(f"bad claim id {cid!r}")
        known = self.evidence()
        for ev, _ in support:
            if ev not in known:
                raise LedgerError(f"claim {cid}: unknown evidence {ev}")
        row = {"id": cid, "text": text, "key": key,
               "support": [{"ev": e, "quote": q} for e, q in support],
               "registered_at": now()}
        self._append("claims", row)
        return row

    def verdicts(self) -> dict[str, dict]:
        return {r["claim"]: r for r in self._rows("verdicts")}

    def disproofs(self) -> set[str]:
        return {r["key"] for r in self._rows("disproofs")}

    # layer 1
    def check(self, claim: dict, objects: Path | None = None) -> dict:
        problems, integrity, ev_hashes = [], "ok", {}
        texts: dict[str, str] = {}
        if not claim["support"]:
            problems.append("no support quote")
        for s in claim["support"]:
            state, text = self.snapshot(s["ev"], objects)
            if state != "ok":
                integrity = "tampered"
                problems.append(f"{s['ev']}: snapshot {state}")
                continue
            ev_hashes[s["ev"]] = self.evidence()[s["ev"]]["hash"]
            texts[s["ev"]] = norm(text)
            if norm(s["quote"]) not in texts[s["ev"]]:
                problems.append(f"{s['ev']}: quote not found verbatim")
        quote_vals = set()
        quotes = " | ".join(norm(s["quote"]) for s in claim["support"])
        for tok in numbers(quotes):
            quote_vals |= num_values(tok)
        for tok in numbers(claim["text"]):
            # Value match (12.5 == 12,5) or literal token match (3.13 in 3.13.0).
            literal = re.search(rf"(?<!\d){re.escape(tok)}(?!\d)", quotes)
            if not (num_values(tok) & quote_vals or literal):
                problems.append(f"number {tok!r} not in any support quote")
        l1_hash = sha256(canon({"text": norm(claim["text"]),
                                "support": claim["support"],
                                "evidence": ev_hashes}))
        return {"ok": not problems, "integrity": integrity,
                "problems": problems, "l1_hash": l1_hash,
                "neg_key": sha256(canon([norm(claim["text"]),
                                         sorted(ev_hashes.values())]))}

    def final(self, claim: dict, l1: dict, verdict: dict | None) -> dict:
        """Combine L1, L2 and corroboration into the reported status."""
        ev = self.evidence()
        pubs = {ev[s["ev"]]["publisher"] for s in claim["support"]
                if s["ev"] in ev}
        base = {"sources": len(pubs), "reason": "", "pending": False,
                "drift": False}
        if l1["integrity"] != "ok":
            return {**base, "status": "tampered",
                    "reason": "; ".join(l1["problems"])}
        if not l1["ok"]:
            return {**base, "status": "unverified",
                    "reason": "; ".join(l1["problems"])}
        if verdict is None:
            if l1["neg_key"] in self.disproofs():
                return {**base, "status": "disproven",
                        "reason": "previously disproven against unchanged evidence"}
            return {**base, "status": "unverified", "pending": True,
                    "reason": "awaiting layer-2 verdict"}
        if verdict["l1_hash"] != l1["l1_hash"]:
            return {**base, "status": "unverified", "pending": True,
                    "drift": True,
                    "reason": "claim or evidence changed since verdict"}
        v, why = verdict["status"], verdict.get("reason", "")
        status = {"contradicts": "disproven", "insufficient": "unverified",
                  "partial": "partial", "disputed": "disputed"}.get(v)
        if status is None:  # supports
            status = ("single-source" if claim["key"] and len(pubs) < 2
                      else "verified")
        return {**base, "status": status, "reason": why}

    def record_verdict(self, cid: str, status: str, reason: str,
                       counter: list[str]) -> dict:
        claim = self.claims().get(cid)
        if claim is None:
            raise LedgerError(f"unknown claim {cid}")
        if status not in L2_STATUSES:
            raise LedgerError(f"status must be one of {L2_STATUSES}")
        if not reason.strip():
            raise LedgerError("--reason is required")
        known = self.evidence()
        for ev in counter:
            if ev not in known:
                raise LedgerError(f"unknown counter-evidence {ev}")
        l1 = self.check(claim)
        if not l1["ok"]:
            raise LedgerError(f"{cid} fails layer 1, fix it first: "
                              + "; ".join(l1["problems"]))
        row = {"claim": cid, "status": status, "reason": reason,
               "counter": counter, "l1_hash": l1["l1_hash"], "at": now()}
        self._append("verdicts", row)
        if status == "contradicts":
            self._append("disproofs", {"key": l1["neg_key"], "claim": cid,
                                       "at": row["at"]})
        return row

    def evaluate(self) -> list[tuple[dict, dict, dict]]:
        verdicts = self.verdicts()
        out = []
        for cid, claim in self.claims().items():
            l1 = self.check(claim)
            out.append((claim, l1, self.final(claim, l1, verdicts.get(cid))))
        return out


# ── seal / verify ──────────────────────────────────────────────────────────

def slug(text: str) -> str:
    s = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:60] or "report"


def counts_line(finals: list[dict]) -> str:
    c = {k: 0 for k in FINAL_ORDER}
    for f in finals:
        c[f["status"]] += 1
    return " · ".join(f"{n} {k}" for k, n in c.items() if n)


def marker(cid: str, status: str) -> str:
    return f"[{cid}]" if status == "verified" else f"[{cid} · {status.upper()}]"


def cell(s: str) -> str:
    return str(s).replace("|", "\\|").replace("\n", " ")


def seal(led: Ledger, topic: str, draft: str, out_root: Path,
         max_age_days: int) -> tuple[Path, str]:
    refs = re.findall(r"\[\[([A-Za-z0-9_.-]+)\]\]", draft)
    rows = {c["id"]: (c, l1, f) for c, l1, f in led.evaluate()}
    unknown = sorted(set(refs) - rows.keys())
    if unknown:
        raise LedgerError(f"draft cites unregistered claims: {unknown}")
    if not refs:
        raise LedgerError("draft cites no claims ([[claim-id]] markers)")
    blocked = [f"{cid}: {f['reason']}" for cid, (_, _, f) in rows.items()
               if f["pending"]]
    if blocked:
        raise LedgerError("seal refused, claims without a current layer-2 "
                          "verdict:\n  " + "\n  ".join(blocked))
    verdicts, ev = led.verdicts(), led.evidence()
    body = re.sub(r"\[\[([A-Za-z0-9_.-]+)\]\]",
                  lambda m: marker(m.group(1), rows[m.group(1)][2]["status"]),
                  draft)
    used = sorted({s["ev"] for c, _, _ in rows.values() for s in c["support"]}
                  | {e for v in verdicts.values() if v["claim"] in rows
                     for e in v.get("counter", [])})
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    out = out_root / slug(topic) / stamp
    n = 1
    while out.exists():
        n += 1
        out = out_root / slug(topic) / f"{stamp}-{n}"
    (out / "evidence").mkdir(parents=True)
    for e in used:
        shutil.copy2(led.objects / ev[e]["hash"], out / "evidence" / ev[e]["hash"])

    today = dt.date.today()

    def stale(rec: dict) -> bool:
        try:
            return (today - dt.date.fromisoformat(rec["published"][:10])).days > max_age_days
        except (ValueError, TypeError):
            return False

    finals = [f for _, _, f in rows.values()]
    lines = [f"# {topic}", "",
             f"> **Verdicts:** {counts_line(finals)} · evidence {len(used)} · "
             f"generated {now()}", "", body.strip(), "",
             "## Appendix A — Verification", "",
             "| claim | status | key | independent sources | reason |",
             "|---|---|---|---|---|"]
    for cid, (c, _, f) in rows.items():
        lines.append(f"| {cid} | {f['status']} | {'yes' if c['key'] else ''} "
                     f"| {f['sources']} | {cell(f['reason'])} |")
    unref = sorted(rows.keys() - set(refs))
    if unref:
        lines += ["", f"Registered but not cited in the body: {', '.join(unref)}"]
    lines += ["", "## Appendix B — Sources", "",
              "| id | tier | publisher | published | captured | sha256 | origin |",
              "|---|---|---|---|---|---|---|"]
    for e in used:
        r = ev[e]
        pub = r["published"] + (" ⚠ stale" if stale(r) else "")
        lines.append(f"| {e} | {r['tier']} | {r['publisher']} | {pub} | "
                     f"{r['captured_at'][:10]} | {r['hash'][:12]} | "
                     f"{cell(r['origin'])} |")
    falsified = [(cid, verdicts[cid]) for cid in rows
                 if cid in verdicts and verdicts[cid]["status"] in
                 ("contradicts", "disputed")]
    lines += ["", "## Appendix C — Falsification log", ""]
    lines += [f"- **{cid}** ({v['status']}): {v['reason']}"
              + (f" — counter-evidence: {', '.join(v['counter'])}"
                 if v.get("counter") else "")
              for cid, v in falsified] or ["None recorded."]
    lines += ["", "## Appendix D — Seal", "",
              "The seal is the sha256 of `manifest.json` (see `SEAL`). "
              "Recompute offline with `ledger.py verify <this dir>`.", ""]
    report = "\n".join(lines).encode()
    (out / "report.md").write_bytes(report)
    manifest = {
        "schema": SCHEMA, "topic": topic, "generated_at": now(),
        "report_sha256": sha256(report),
        "evidence": [ev[e] for e in used],
        "claims": [{**c, "l1_hash": l1["l1_hash"],
                    "verdict": verdicts.get(cid), "final": f}
                   for cid, (c, l1, f) in rows.items()],
    }
    mbytes = json.dumps(manifest, indent=2, sort_keys=True,
                        ensure_ascii=False).encode() + b"\n"
    (out / "manifest.json").write_bytes(mbytes)
    seal_hash = sha256(mbytes)
    (out / "SEAL").write_text(seal_hash + "\n")
    return out, seal_hash


def verify_sealed(report_dir: Path, expected: str | None) -> list[str]:
    errs = []
    mbytes = (report_dir / "manifest.json").read_bytes()
    actual = sha256(mbytes)
    sealed = expected or (report_dir / "SEAL").read_text().strip()
    if actual != sealed:
        errs.append(f"seal mismatch: manifest {actual[:12]} != {sealed[:12]}")
    m = json.loads(mbytes)
    if sha256((report_dir / "report.md").read_bytes()) != m["report_sha256"]:
        errs.append("report.md changed after sealing")
    # Replay layer 1 against the sealed evidence copies only.
    tmp = Ledger(report_dir / ".verify-ledger")
    tmp.evidence = lambda: {r["id"]: r for r in m["evidence"]}  # type: ignore
    for c in m["claims"]:
        l1 = tmp.check(c, objects=report_dir / "evidence")
        if l1["l1_hash"] != c["l1_hash"]:
            errs.append(f"{c['id']}: layer-1 state differs from sealed "
                        f"({'; '.join(l1['problems']) or 'hash drift'})")
    return errs


# ── CLI ────────────────────────────────────────────────────────────────────

def read_source(src: str) -> tuple[bytes, str]:
    if src == "-":
        return sys.stdin.buffer.read(), "stdin"
    if re.match(r"https?://", src):
        req = urllib.request.Request(src, headers={
            "User-Agent": "research-report-ledger/1 (+stdlib urllib)"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read(MAX_BYTES + 1)
            ctype = resp.headers.get("Content-Type", "")
            charset = resp.headers.get_content_charset() or "utf-8"
        if "pdf" in ctype:
            raise LedgerError("PDF: extract text with the harness, then "
                              "`add - --origin URL`")
        text = raw.decode(charset, errors="replace")
        if "html" in ctype:
            text = html_to_text(text)
        return text.encode(), src
    p = Path(src)
    if not p.is_file():
        raise LedgerError(f"no such file {src}")
    return p.read_bytes(), str(p)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="ledger.py", description=__doc__.split("\n")[0])
    ap.add_argument("--root", default=os.environ.get("RESEARCH_LEDGER", ".research"))
    sub = ap.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("add", help="capture a source (URL, file, or - for stdin)")
    a.add_argument("source")
    a.add_argument("--origin", help="real origin when source is - or a local copy")
    a.add_argument("--title", default="")
    a.add_argument("--tier", choices=TIERS, default="")
    a.add_argument("--published", default="", help="YYYY-MM-DD")
    a.add_argument("--publisher", default="", help="override domain-derived publisher")

    s = sub.add_parser("show", help="print a snapshot, or context around a phrase")
    s.add_argument("ev")
    s.add_argument("--grep")
    s.add_argument("--context", type=int, default=400)

    c = sub.add_parser("claim", help="register/amend an atomic claim")
    c.add_argument("id")
    c.add_argument("--text", required=True)
    c.add_argument("--support", nargs=2, action="append", default=[],
                   metavar=("EV", "QUOTE"), required=True)
    c.add_argument("--key", action="store_true")

    k = sub.add_parser("check", help="layer 1 on all (or one) claims")
    k.add_argument("--claim")
    k.add_argument("--json", action="store_true")

    p = sub.add_parser("packet", help="blind verifier input for claims")
    p.add_argument("claims", nargs="*")
    p.add_argument("--context", type=int, default=600)

    v = sub.add_parser("verdict", help="record a layer-2 verdict")
    v.add_argument("id")
    v.add_argument("status", choices=L2_STATUSES)
    v.add_argument("--reason", required=True)
    v.add_argument("--counter", nargs="*", default=[])

    sub.add_parser("status", help="final status of every claim")

    z = sub.add_parser("seal", help="render + seal the report")
    z.add_argument("--topic", required=True)
    z.add_argument("--draft", required=True)
    z.add_argument("--out", default="research-reports")
    z.add_argument("--max-age-days", type=int, default=730)

    y = sub.add_parser("verify", help="recompute a sealed report offline")
    y.add_argument("dir")
    y.add_argument("--seal")

    args = ap.parse_args(argv)
    led = Ledger(Path(args.root))
    try:
        if args.cmd == "add":
            data, origin = read_source(args.source)
            rec, dup = led.add(data, args.origin or origin, args.title,
                               args.tier, args.published, args.publisher)
            print(json.dumps({**rec, "deduplicated": dup}, ensure_ascii=False))
        elif args.cmd == "show":
            state, text = led.snapshot(args.ev)
            if text is None:
                raise LedgerError(f"{args.ev}: {state}")
            if not args.grep:
                print(text)
            else:
                t, q, n = norm(text), norm(args.grep), args.context
                hits = [m.start() for m in re.finditer(re.escape(q), t)]
                if not hits:
                    raise LedgerError("phrase not found (after normalisation)")
                for h in hits:
                    print(f"…{t[max(0, h - n):h + len(q) + n]}…\n---")
        elif args.cmd == "claim":
            led.add_claim(args.id, args.text, args.support, args.key)
            l1 = led.check(led.claims()[args.id])
            print(json.dumps({"id": args.id, "l1_ok": l1["ok"],
                              "problems": l1["problems"]}, ensure_ascii=False))
            return 0 if l1["ok"] else 1
        elif args.cmd == "check":
            rows = [(c, l1) for c, l1, _ in led.evaluate()
                    if not args.claim or c["id"] == args.claim]
            if args.claim and not rows:
                raise LedgerError(f"unknown claim {args.claim}")
            if args.json:
                print(json.dumps([{"id": c["id"], **l1} for c, l1 in rows],
                                 ensure_ascii=False, indent=2))
            else:
                for c, l1 in rows:
                    print(f"{'PASS' if l1['ok'] else 'FAIL'}  {c['id']}"
                          + "".join(f"\n      - {p}" for p in l1["problems"]))
            return 0 if all(l1["ok"] for _, l1 in rows) else 1
        elif args.cmd == "packet":
            claims = led.claims()
            ids = args.claims or list(claims)
            n = args.context
            for cid in ids:
                cl = claims.get(cid)
                if cl is None:
                    raise LedgerError(f"unknown claim {cid}")
                print(f"## {cid}{' (KEY)' if cl['key'] else ''}\nCLAIM: {cl['text']}")
                for s in cl["support"]:
                    _, text = led.snapshot(s["ev"])
                    t, q = norm(text or ""), norm(s["quote"])
                    i = t.find(q)
                    ctx = t[max(0, i - n):i + len(q) + n] if i >= 0 else "(quote not found)"
                    print(f"SOURCE {s['ev']}\nQUOTE: {s['quote']}\nCONTEXT: …{ctx}…")
                print()
        elif args.cmd == "verdict":
            row = led.record_verdict(args.id, args.status, args.reason, args.counter)
            print(json.dumps(row, ensure_ascii=False))
        elif args.cmd == "status":
            rows = led.evaluate()
            for c, _, f in rows:
                flag = " (PENDING)" if f["pending"] else ""
                print(f"{f['status']:<14}{c['id']}{flag}  {f['reason']}")
            print(counts_line([f for _, _, f in rows]) or "no claims")
        elif args.cmd == "seal":
            draft = Path(args.draft).read_text()
            out, h = seal(led, args.topic, draft, Path(args.out), args.max_age_days)
            print(json.dumps({"report": str(out / "report.md"), "seal": h}))
        elif args.cmd == "verify":
            errs = verify_sealed(Path(args.dir), args.seal)
            print("OK: seal, report and every claim re-check match"
                  if not errs else "FAIL\n  " + "\n  ".join(errs))
            return 0 if not errs else 1
    except (LedgerError, OSError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
