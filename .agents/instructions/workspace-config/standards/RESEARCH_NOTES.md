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
