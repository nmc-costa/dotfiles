---
applyTo: "**"
---

# Harness × model routing — see tasks/harness-provider-model-index.md

This workspace's canonical, machine-verified reference for "which CLI
harness + model to use, and for which `tasks/` Kanban phase" lives at
[`tasks/harness-provider-model-index.md`](../../../tasks/harness-provider-model-index.md),
not here. It was previously duplicated as a separate, independently-drafted
matrix in this file (authored by the Antigravity harness on branch
`antigravity/harness-model-matrix`); the two diverged — different model
names, no shared verification against actual machine state. Per the
owner's 2026-09-23 decision, they were folded into one document to stop
that drift. Don't recreate a second copy here.

**One constraint worth restating in this directory, since every harness
reads `.agents/instructions/workspace-config/` on session start:** the
owner already pays for Claude Pro (Claude Code) and GitHub Copilot Pro
(`copilot` CLI). Don't reach for a new metered API key when one of those
two already covers the task. See the linked file for the full ranked
index, the phase-routing table, and open gaps.
