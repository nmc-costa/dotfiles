# `research-report` skill — design (2026-09-24)

**Status: implemented 2026-09-25** — `.agents/skills/research-report/` (see §H for the live-eval result).

**Ask (human, pt):** "era importante ter uma skill de research report que foca
mesmo e valida o que está a ver" — can we use
<https://github.com/PerryLink/dsh-research-report>, or build something better?

**Verdict: don't install it; port its core ideas (Apache-2.0) into a
harness-neutral skill and add the semantic layer it deliberately leaves out.**

## A. What dsh-research-report actually is

Evaluated at HEAD on 2026-09-24 (shallow clone, source read, not just README).

- **A1 [fact].** A **DeepSeek Harness (`dsh`) plugin**, not a SKILL.md: ~4.2k
  lines of TypeScript whose peer deps are `@deepseek-ai/cordis`,
  `@deepseek-ai/dsh-{session,tools,web,jobs,system-prompt}`. Installed with
  `dsh plugin add …`. None of our harnesses (Claude Code, Copilot CLI,
  Antigravity, Gemini CLI) can load it.
- **A2 [fact].** Its core is portable: `src/ledger.ts` imports only
  `node:crypto/fs/path`; `src/verify.ts` imports only a local type. License
  is Apache-2.0, so we can port the logic with attribution.
- **A3 [fact] — what's worth keeping:**
  1. Content-addressed evidence store (`objects/<sha256>` + JSONL index);
     every read re-hashes, so a tampered or missing snapshot is detected rather than trusted.
  2. Claim ↔ evidence binding; nothing can be cited unless it was captured.
  3. Deterministic byte check: every number/quoted span in a claim must be
     found verbatim in the bound snapshot.
  4. Honest verdict vocabulary with inline markers kept in the report
     (`unverified` / `insufficient` / `disproven` / `contradicted`), plus an
     appendix. Nothing is silently passed.
  5. Falsification log + "negative knowledge" (a disproven claim stays
     disproven until its evidence changes).
  6. Sealed, versioned output (`report.md` + `manifest.json`; seal = sha256
     of manifest) and a standalone re-verifier.
- **A4 [fact] — its own stated limits (SUMMARY.md "已知限制"):** byte check is
  **non-semantic**, so any paraphrased claim with no literal comes out
  `unverified`. There's no retrieval loop and no source-quality judgement, and DOI
  checks are syntax-only (no network). Text snapshots only, no PDF.
- **A5 [inference].** The byte check alone proves "the literal exists in the
  source", not "the source supports the claim". A quote taken out of context
  or negated ("revenue did **not** grow 12%") passes byte-level. That gap is
  exactly the "valida o que está a ver" ask.

## B. Design: what "better" means, concretely

Two verification layers, each covering what the other can't:

| Layer | Who | Catches | Can't catch |
|---|---|---|---|
| **L1 deterministic** (`ledger.py check`) | script | fabricated numbers/quotes, tampered/missing snapshots, uncited claims | misread context, negation, cherry-picking |
| **L2 blind semantic** (verifier role) | fresh subagent / reset context | quote doesn't entail claim, out-of-context, overgeneralisation, missing counter-evidence | fabricated source text (L1 does) |

On top of the dsh core, add:

- **B1. Mandatory support span.** Every claim carries ≥1 `(evidence_id,
  quote)` pair. L1 checks that the quote is in the snapshot (after NFKC + whitespace
  normalisation), and that every number in the claim appears in one of the quotes.
  This moves dsh's "paraphrase → unverified" into a checkable form.
- **B2. Blind verifier.** It gets only the claim, the quote and ±N chars of snapshot
  context. It never sees the draft or the author's reasoning. It returns
  `supports | partial | contradicts | insufficient` + one-line reason.
  Author ≠ verifier, same rule as `plan-orchestra` Phase 5.
- **B3. Falsification search** for claims flagged `key: true`: the verifier
  actively searches for counter-evidence and captures whatever it finds into
  the ledger. A hit → `disputed`, both sides shown.
- **B4. Corroboration.** A key claim reaches `verified` only with ≥2
  independent sources (different registrable domain / publisher). With one
  source it stays `single-source`, visibly.
- **B5. Source metadata.** Each evidence has `tier` (primary/secondary/tertiary),
  `published` date and `captured_at`. Stale ones (> configurable age) are flagged in
  the report.
- **B6. Online reference check (optional).** DOI/URL resolves and the title
  matches, when network is available. Otherwise syntax-only, stated explicitly.

**Final verdict vocabulary** (inline marker + appendix row):
`verified` · `single-source` · `partial` · `disputed` · `unverified` ·
`disproven` · `tampered`. The seal is refused while any claim lacks an L2 verdict
or its L1 result drifted since the verdict was recorded.

## C. Deliverables

```
.agents/skills/research-report/
  SKILL.md          # workflow + roles, ≤ ~150 lines, simplifyhit-clean
  ledger.py         # stdlib-only Python 3 (D14: script before rule)
  NOTICE            # Apache-2.0 attribution to PerryLink/dsh-research-report
  tests/test_ledger.py  # unittest, fixtures incl. the adversarial cases in E
```

`ledger.py` subcommands (state lives in `./.research/` of the cwd, reports in
`./research-reports/<slug>/<YYYYMMDD-HHMMSS>/`):

| cmd | does |
|---|---|
| `add <url\|path\|->  [--title --tier --published]` | fetch/read → sha256 object + index row → prints `ev-<hash12>` |
| `claim <id> --text … --support ev:"quote" [--key]` | register binding |
| `check [--claim id]` | L1; exit≠0 on any failure, JSON out |
| `verdict <id> <status> --reason …` | record L2 result (binds to current L1 hash) |
| `seal --topic … --draft draft.md` | render markers + appendices (verification table, sources, falsification log, gaps) + `manifest.json`; refuses on drift/missing verdicts |
| `verify <report-dir>` | standalone recompute of seal + L1, zero network |

## D. Workflow (SKILL.md)

Harness labels are the same as `plan-orchestra`: **Claude Code** uses real `Agent`
subagents. The others play each role sequentially, with an explicit context
reset before the verifier role.

1. **Scope**: one-sentence question, 3–6 sub-questions, "done" criterion,
   which claims will be `key`. Ask the human if ambiguous.
2. **Gather** (researcher, parallel per sub-question): search → `ledger.py
   add` every source actually used. **Rule: no evidence id, no citation.**
3. **Draft** (author): atomic claims, each with `claim … --support`; prose
   references claim ids only.
4. **L1**: `ledger.py check`. Failures go back to the author (fix or drop). The author
   doesn't argue with the script.
5. **L2** (verifier, fresh context, batches of ~10 claims): B2 + B3 for key
   claims → `ledger.py verdict`.
6. **Seal**: `ledger.py seal`; the report opens with a verdict summary line
   (e.g. `14 verified · 3 single-source · 1 disputed · 2 unverified`).
7. **Deliver**: report path + seal hash + `verify` command. Never paste a
   report without its marker counts.

Relation to `plan-orchestra`: independent in v1. v2 can make
plan-orchestra's Phase 2/3 evidence map use this ledger. Out of scope here.

## E. Acceptance (tests + one live run)

Unit tests (`tests/test_ledger.py`) must show that:
1. A claim with a fabricated number → L1 fail.
2. Editing one byte of an object file → `tampered`, seal refused.
3. A quote with different whitespace/quote glyphs → still located (normalisation).
4. Changing a claim after its verdict → drift → seal refused.
5. `verify` on a sealed dir reproduces the seal hash.

Live eval (manual, once): a 5-claim report on a real topic that includes a
planted **negated quote** and a **single-source key claim**. The first must end
`disproven`/`partial` (L2 caught it), the second `single-source`. Tests pass +
live eval matches → done.

## F. Accepted risks

- L2 is still a model judgement. Mitigated by blindness + author≠verifier + the
  quote being byte-checked first, not eliminated.
- HTML→text extraction in stdlib is crude. v1 stores the fetched text the
  harness already produced (e.g. WebFetch output piped via `add -`) and
  accepts that the snapshot is "what the agent saw", not the raw page.
- PDFs: only via text the harness already extracted. No parser dependency in v1.

## G. Effort

One session: ledger.py + tests (~400 lines), SKILL.md, symlink via `sync.sh`,
one live eval. Proposed card: `dotfiles-tsk-research-report-skill`.

## H. Live eval result (2026-09-25)

Real sources captured with `ledger.py add` over the network (docs.python.org
What's New 3.13, PEP 719, PEP 703). Five claims, two of them planted:

| claim | planted flaw | L1 | L2 (blind Opus verifier, packet only) | final |
|---|---|---|---|---|
| c1 3.13.0 final on 2024-10-07 (key) | only one publisher (python.org) | PASS | supports | **single-source** |
| c2 GIL disabled by default | quote byte-true, negated in context | PASS | contradicts ("not enabled by default") | **disproven** |
| c3 separate `python3.13t` executable | — | PASS | supports | verified |
| c4 JIT "speeds up Python programs" | hedge dropped ("may speed up some") | PASS | partial | **partial** |
| c5 security updates to ~Oct 2029 | — | PASS | supports | verified |

L1 alone passed all five: the dsh-research-report gap reproduced. L2 caught
both planted flaws without being told they existed. `seal` → `verify` reproduced
the seal hash. One L1 fix came out of the eval: version tokens (`3.13` vs
`3.13.0`) now also match literally, with a regression test.
