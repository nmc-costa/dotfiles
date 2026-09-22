---
applyTo: "**"
---

# Harness and Model Specialization Matrix

This document defines the specialization matrix, token-conservation rules, and phase-routing protocols across all CLI harnesses in this workspace: **Claude Code**, **Antigravity / Gemini CLI**, and **GitHub Copilot CLI** (with support for **OpenAI Codex / Cline**).

## Core Principle: Cognitive Fit & Token Economics

No single harness or model is optimal across the entire development lifecycle. Premium reasoning models (e.g., Claude Opus, Claude 3.7 Sonnet with Extended Thinking) are costly ($15–$75 / 1M tokens) and have tight quota limits. Mechanical tasks (git sync, conflict resolution, formatting, linting, boilerplate) must never consume high-reasoning tokens ("Opus Janitor" anti-pattern).

Instead, work is routed by Kanban/SDLC phase according to cognitive requirements:

| Phase | Cognitive Profile | Recommended Harness | Recommended Models | Primary Focus |
| :--- | :--- | :--- | :--- | :--- |
| **`planning`** | Deep multi-step reasoning, architectural decomposition, constraint discovery. | **Claude Code** (`claude`) | Claude 3.7 Sonnet (Thinking), Claude Opus | Technical design, task breakdown, boundary definition. |
| **`in_progress` (Tier 1)** | Sensitive concurrency logic, CAS protocols, core multi-file refactoring. | **Claude Code** (`claude`) | Claude 3.7 Sonnet | Critical algorithm implementation, core invariants. |
| **`in_progress` (Tier 2)** | Scaffolding, feature implementation, boilerplate, doc generation, broad exploration. | **Antigravity / Gemini CLI** (`agy`) | Gemini 2.5 Pro / Flash | Rapid implementation leveraging 1M–2M context window. |
| **`review`** | Adversarial review, data race detection, security audit, standards compliance. | **Claude Code** (clean session) / `reviewHITs` | Claude 3.7 Sonnet (Thinking) | Unbiased, critical critique without author context pollution. |
| **`validation`** | Formal verification, edge-case probing, CAS validation (`--expect-last-event-id`). | **Claude Code** (`claude`) + **Antigravity** (logs) | Claude 3.7 Sonnet / o3-mini (logic), Gemini Flash (traces) | CAS gating enforcement, regression testing, coredump analysis. |
| **Maintenance / Git** | Mechanical merge conflict resolution, branch sync, git hygiene, PR review workflows. | **GitHub Copilot CLI** (`copilot`) | Copilot Native, Claude Haiku, GPT-4o-mini | Git operations, rebase/merges, linting, format checks. |

---

## Token Conservation Rules (Guardrails)

1. **Restricted Claude Code Scope:**
   - Claude Code sessions should be preferentially utilized during **`planning`** and critical **`validation`**.
   - If Claude Code is about to execute extensive scaffolding, large file conversions, or standard docs, it should proactively advise the user to transition to Antigravity (`agy`), or offer to launch it via `python3 tasks/dispatch.py --task-id <id> --provider agy --launch`.
2. **Scout & Striker Pattern:**
   - Use Antigravity (Gemini 2.5 Pro/Flash with 1M+ token window) as the **Scout** to survey entire codebases, ingest megabytes of logs or research docs, and produce a concise 1–2k token summary.
   - Dispatch Claude Code as the **Striker** with that concise brief to write the surgical patch.
3. **Zero Premium Tokens on Git Hygiene:**
   - Never use Claude 3.7 / Opus to resolve straightforward git merge conflicts or run formatting passes. Use GitHub Copilot CLI or helper scripts.

---

## Inter-Harness Handoff Protocols

1. **Autonomous Dispatch (`tasks/dispatch.py`):**
   - Push-based handoff: Any session completing a phase can hand off to another harness via:
     ```bash
     python3 tasks/dispatch.py --task-id <task-id> --provider <claude|copilot|agy> --launch
     ```
   - State flows strictly through `tasks/events.jsonl` (and leases via `tasks/claims.jsonl`).
2. **Context Isolation (The Synthetic Brief):**
   - Never pipe raw transcripts or full conversation logs across harnesses.
   - Handoff context is always a structured brief produced by `tasks/brief.py --prompt-only --task-id <task-id>`, defining task boundaries, acceptance criteria, and specific target files.
3. **Worktree Isolation per Task:**
   - Every task implementation runs in its own dedicated git worktree (`antigravity/<task-id>`, `claude/<task-id>`, or `copilot/<task-id>`).
   - Never share worktrees across concurrent sessions.
