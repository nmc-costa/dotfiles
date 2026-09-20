---
name: plan-orchestra
description: "Orchestrate a multi-agent research-and-planning workflow: clarify scope with the human, fan out closed sub-questions to research subagents, verify and reconcile their findings into an evidence map, have a single subagent commit to one decisive plan, subject that plan to adversarial critique, then deliver. Use when the user asks for a plan, proposal, or investigation that needs verified evidence gathered by multiple subagents before a decision is made — not for simple single-step questions."
---

# Plan Orchestra

Role: you are the MAIN agent. You do not investigate or write the plan yourself. You clarify, dispatch, verify, and integrate.

## Phase 1 — Clarify (you, no subagents)

Do not dispatch anything until scope is agreed with the human.
Produce: a one-sentence goal, 3-7 sub-questions, and a "done" criterion.
If anything is ambiguous, ask. Do not assume.

## Phase 2 — Research (fan-out, haiku-4.5)

Maximum 6 concurrent subagents.
Each one receives ONE closed, verifiable sub-question, with:
- a starting list of URLs, if any exist
- the obligation to cite a URL + date for every fact
- the obligation to mark every line `[fact]` or `[inference]`
- a prohibition on rewriting the overall plan
- the obligation to report blockers upward, not work around them

Do not ask a researcher to judge source quality or resolve contradictions — that's your job.

## Phase 3 — Verify (you)

Cross-check the outputs. Where there's a conflict, dispatch ONE extra researcher with the tie-breaking question.
Discard unsupported `[inference]`s.
Produce an evidence map: claim -> source -> confidence.

## Phase 4 — Plan (single subagent, opus)

Receives: goal, evidence map, constraints, deliverables.
Does NOT receive the researchers' raw transcripts.
Must CHOOSE, not enumerate options. Open decisions = rejection.

## Phase 5 — Critique (subagent, opus or sonnet, clean context)

Does not treat the plan as a friend. Looks for: unvalidated assumptions, non-idempotent steps, what fails first, circular dependencies.
If it finds a material flaw, go back to Phase 4 with the findings. Maximum 2 rounds.

## Phase 6 — Deliver

Final plan + evidence map + list of consciously accepted risks.

## Budget

Abort and report if: research takes more than 20 minutes, or critique goes past 2 rounds, or cost exceeds the defined limit. Do not continue silently.
