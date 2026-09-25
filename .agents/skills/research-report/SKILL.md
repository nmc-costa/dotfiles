---
name: research-report
description: "Produce a research report where every factual claim is bound to a captured source, checked verbatim by a script, then judged by a blind verifier that never saw the draft; unsupported claims stay visibly marked, never silently passed. Use when the user asks for a research report, fact-checked write-up, market/literature/technical investigation, due diligence, or says 'valida', 'verify', 'fact-check', 'with sources' — not for quick one-line lookups."
---

# Research Report

Role: you are the MAIN agent. You scope, dispatch, run the ledger, and write the prose. You never grade your own claims.

Script: `python3 ~/.agents/skills/research-report/ledger.py` (below: `L`; inside `~/dotfiles` before `./sync.sh`, use `.agents/skills/research-report/ledger.py`). Stdlib only. State goes in `./.research/`, reports in `./research-reports/`. Run from the directory where the report should live. `L --help` / `L <cmd> --help` for flags.

**Harness labels** (same as `plan-orchestra`; see `.agents/harnesses/<this-harness>.md`):
- **Claude Code**: researcher and verifier roles are real `Agent` subagents. Verifier tier ≥ author tier.
- **Anything else**: play each role yourself, sequentially. Before the verifier role, do an explicit context reset: judge only the `L packet` output, as if you had never seen the draft.

## Non-negotiable rules

1. **No evidence id → no citation.** A source you read but didn't `L add` doesn't exist for this report.
2. **Atomic claims.** One checkable fact per claim. Every number in the claim text must appear in one of its support quotes (L1 enforces this).
3. **Quotes are copied, never retyped from memory.** Use `L show <ev> --grep "<phrase>"` to copy exact text.
4. **Author ≠ verifier.** Verdicts come only from Phase 5.
5. **Never argue with L1.** A FAIL means fix the claim, fix the quote, or drop the claim.
6. **Never hide a marker.** The seal refuses pending/drifted claims, and `UNVERIFIED`/`DISPUTED`/`DISPROVEN` markers stay in the body.

## Phase 1: Scope (you)
One-sentence question, 3–6 closed sub-questions, a "done" criterion, and which conclusions are **key** (they need ≥2 independent publishers to reach `verified`). Ask the human if anything is ambiguous.

## Phase 2: Gather (researchers, parallel per sub-question)
Search, read, and capture every source actually used:
```bash
L add https://example.org/page --title "…" --tier primary --published 2025-03-01
# pages the harness fetched/rendered itself (WebFetch, PDF text, JS sites):
<text> | L add - --origin https://example.org/doc.pdf --title "…" --tier primary
```
Tier: `primary` = the original data/statement owner; `secondary` = reporting on it; `tertiary` = aggregators/wikis. Prefer primary. Researchers return evidence ids + one-line relevance, not prose.

## Phase 3: Draft claims (you)
```bash
L claim c1 --key --text "X grew 12.5% in 2024" \
  --support ev-aaa "grew 12,5% in 2024" --support ev-bbb "12.5% growth last year"
```
Write the prose in `draft.md`, citing claims as `[[c1]]`. A factual sentence without a `[[id]]` is a bug.

## Phase 4: L1, deterministic (script)
`L check`: quotes found verbatim (NFKC/whitespace/quote-glyph normalised), numbers present (1,234.5 ≡ 1.234,5), snapshots re-hashed. Loop Phase 3↔4 until PASS or the claim is dropped.

## Phase 5: L2, blind verifier (fresh context, batches of ~10 claims)
Give the verifier **only** `L packet c1 c2 …` output plus this prompt. Never the draft, the question's framing or your reasoning:

> For each claim, judge only whether the CONTEXT supports the CLAIM as worded. Check negation, scope (region/period/population), hedging lost ("may" → "will"), cherry-picking, and whether the number means what the claim says. Return one of: `supports` | `partial` (true but narrower/weaker than worded) | `contradicts` | `insufficient` (context can't decide). Give a one-line reason quoting the deciding words. For claims marked KEY: also search for counter-evidence. If you find credible counter-evidence, capture it with `L add` and return `disputed` with its ids.

Record every result: `L verdict c1 supports --reason "…" [--counter ev-…]`.
Then run `L status`. Fix `partial` claims by rewording them to what the source actually says; re-registering needs a new verdict. Fix `single-source` with a second independent source, or accept it visibly.

## Phase 6: Seal (script)
`L seal --topic "…" --draft draft.md` writes `report.md` + `manifest.json` + `SEAL` + `evidence/` copies. The report opens with the verdict counts and has appendices for verification, sources (tier, publisher, stale ⚠), and the falsification log.

## Phase 7: Deliver
Give the report path, the verdict-count line, the seal hash, and `L verify <dir>` for anyone to recompute offline. Name every non-`verified` key claim in your message. Never paste the report without its markers.

## Final statuses
`verified` · `single-source` (key claim, 1 publisher) · `partial` · `disputed` · `unverified` (L1 fail or `insufficient`) · `disproven` (`contradicts`; remembered, so the same text against unchanged evidence stays disproven) · `tampered` (snapshot changed/missing).

## Budget
- The verifier re-runs only on claims that changed.
- Stop and report out loud if a key sub-question has zero primary/secondary evidence after one retry. Don't fill the gap with tertiary sources silently.

Credits: core ledger design ported from PerryLink/dsh-research-report (Apache-2.0), see `NOTICE`. Tests: `python3 -m unittest discover -s .agents/skills/research-report/tests`.
