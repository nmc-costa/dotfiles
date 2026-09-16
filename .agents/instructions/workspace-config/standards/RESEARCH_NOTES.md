# Research notes — workspace-standards schema

Baseline research pass behind `workspace-standards.schema.json` and
`workspace-standards.yaml`. Each future review cycle (see `review:` in the
YAML) should re-check these findings and append a dated update below rather
than silently rewriting history — this file is itself an append-only-ish
record of what was checked and when, same principle as the workspace's
chronicle/event-log convention elsewhere.

## 2026-09-15 — baseline

**AGENTS.md**: deliberately unstructured Markdown, no required fields, no
formal schema — that's explicit in the spec itself, not an omission. Governed
by the Agentic AI Foundation (Linux Foundation), donated Dec 2025 alongside
MCP and goose, read by 30+ tools. **Conclusion: don't schematize AGENTS.md's
content. This schema governs structure/policy metadata around it, never
its prose.**

**llms.txt**: real but explicitly website-scoped (its own spec text never
mentions repos/source trees), community convention with no standards-body
backing, thin vendor adoption as of early 2026. **Not a fit — not adopted,
not referenced.**

**Agent context-efficiency patterns**: the one mature real precedent is
Aider's repo map (tree-sitter + PageRank-ranked symbol map, ~98% token
reduction vs. full source) — but that's a *generated* artifact, a different
mechanism from a hand-authored README. **No evidence found of an established
"README diagram for agents" convention anywhere** — kept in the schema as
optional/low-priority per the owner's own request, explicitly flagged as
not-SOTA-backed rather than silently presented as best practice.

**Existing "AI agent workspace config" standards**: none found that solve
this specific problem (repo-structure conventions + self-review cadence for
a personal multi-repo workspace). Adjacent things (JSON Agents Standard,
A2A Agent Card, ai-agent.json, agents.json) all describe *agent* identity/
capability for external discovery — a different problem. **Genuine gap,
confirmed rather than assumed** before building this schema from scratch.

**Structural analogs borrowed from** (patterns, not schemas):
- GitHub org-wide `.github` community-health files — central defaults +
  per-repo override, silent inheritance. → this schema's `extends` field.
- EditorConfig — declarative, schema-free-but-structured, root-anchored,
  "closer file wins." → the shape of `repoRoot`/`agentEntrypoints`.
- Renovate — `$schema` self-reference for validation, layered schema tiers,
  cron-like `schedule`, and critically: **schema validates shape, external
  logic validates semantics and drives a PR** rather than auto-committing.
  → this schema's `review` block and the `onDrift: open-pr` policy.

**JSON Schema + YAML instance**: confirmed the right pairing (comments,
diffability, human-editable). One real risk: LLMs generating YAML are more
error-prone on indentation than generating JSON. Mitigation: any agent-authored
edit to a `.yml` instance file must be validated against the schema
(`scripts/validate_workspace_standards.py`) before it's committed — not
optional, not just at review time.

Full agent transcript / sources available on request; not reproduced here to
keep this file short enough to actually get re-read next cycle.

## 2026-09-16 — communityFirst landscape scan (first real application)

First real use of the `communityFirst` default just added to this schema:
before/after comparing 3 subsystems this workspace built or is about to
build against what the community already maintains. Surface scan used the
public GitHub Search API (unauthenticated, confirmed accessible — 60
req/hour); see `community-index/snapshots/*.json` and `SUMMARY.md` for the
raw automated data behind this, and `community-index/topics.yaml` for the
exact queries. Three follow-up deep dives (real READMEs/docs, not just
star-count metadata) were done after the owner asked not to stop at
surface metrics.

**Task tracking (`tasks/` event-log PoC, 2026-09-15)**: closest matches are
`Backlog.md` (~6.7k★, flat-file git-native kanban) and `claude-task-master`
(~28k★). Neither does append-only JSONL + generated view — both keep
mutable state in files, which the log was designed to avoid. Two concrete
patterns worth borrowing though:
- `claude-task-master`'s **`deferred` state** — our kanban (D12) has no
  "parked without cancelling" state; added to `tasks/README.md` this round.
- `Backlog.md`'s **`AC:BEGIN`/`AC:END` anchor convention** for acceptance
  criteria inside a long per-task file — **does not apply yet** to our
  desenho (a flat table, not one long file per task with multi-item
  acceptance criteria). Registered as "considered, not adopted" in
  `tasks/README.md` rather than silently ignored.
Verdict: building the PoC was reasonable given the specific append-only
design; revisit when it matures further.

**Repo-hygiene schema (`workspace-standards.schema.json` + `.yaml`)**:
`AGENTS.md` (~24k★) standardizes content, `Repolinter` (~465★, github
todogroup) standardizes file presence via rules (`file-existence`,
`json-schema-passes`) with real `extends` support — genuinely overlaps the
"chata" (boring) half of `validate_workspace_standards.py`. But nothing
found combines JSON-Schema + `extends` + a drift-vs-SOTA review cycle that
opens a PR — the half that's actually interesting here. Verdict: not worth
the dependency just to swap the easy half; keep the custom script, and
register the comparison here instead of silently skipping it (per
`communityFirst.principle`'s "compare, don't skip" requirement).

**Personal orchestrator ("Jarvis", not yet built)**: `khoj` (~37k★,
self-hostable) is the closest existing project — real scheduled personal
automations. Deep-dive confirmed it solves a genuinely different problem:
RAG over personal notes + automation *summaries delivered by email*, no
git-as-datastore, no structured write-back to a task file. Verdict:
building Jarvis separately remains the right call; `khoj` is filed as a
candidate for a *different*, not-yet-planned project (a conversational
assistant over notes), not a substitute for Jarvis.

**Omarchy voice-to-agent (surfaced while auditing the Omarchy gap, not
originally a `communityFirst` topic, but the same discipline applies)**:
`wombatoperator/omarchy-voice` (~166★, active — the project behind the
owner's own "I BUILT JARVIS IN OMARCHY" video) is a general desktop
assistant dependent on OpenAI's cloud for STT; not in the official Omarchy
plugin marketplace, no `manifest.json`. **VoxClaude**, by contrast, is
already an *approved, official* Omarchy Shell Plugin Marketplace entry
(issue #6050) built specifically to voice-launch Claude Code sessions using
the native offline `voxtype` (Whisper local) — no cloud dependency, but
**no multi-agent flexibility** (Claude Code only). This is `communityFirst`
working as intended: something already exists, is official, and fits the
"talk to an agent" need — recommend installing VoxClaude over building
anything, with the multi-agent-vs-Claude-only trade-off left to the owner
(see `.agents/skills/omarchy/LOCAL_ADDENDUM.md`).

**Omarchy plugin standard, validated online (not just inferred from local
vendored files)**: `omarchy.org/manual/shell-plugins/` and
`plugins.omarchy.org/develop.html` confirm 6 official plugin `kinds`
(`bar-widget`, `panel`, `overlay`, `menu`, `service`, `bar`), a
`clone --edit` → `validate` + `qmllint` → marketplace-issue-form workflow,
and the sanctioned heavy-logic pattern (thin QML front-end + real user
systemd service backend) — confirmed against a real plugin under review
("Omarchy Google Calendar", issue #6846). `omarchy-voice` does not follow
this format (plain `install.sh`, no manifest) — noted so future work
targets the real manifest system, not that shape.
