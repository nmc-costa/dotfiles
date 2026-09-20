---
name: plan-orchestra
description: "Orchestrate a multi-agent research-and-planning workflow: clarify scope with the human, fan out closed sub-questions to research subagents, verify and reconcile their findings into an evidence map, have a single subagent commit to one decisive plan, subject that plan to adversarial critique, then deliver. Use when the user asks for a plan, proposal, or investigation that needs verified evidence gathered by multiple subagents before a decision is made — not for simple single-step questions."
---

# Plan Orchestra

Role: you are the MAIN agent. You clarify, dispatch, verify, and integrate — you never research or write the plan yourself.

Model names are the Agent tool's enum values only — `haiku`, `sonnet`, `opus`, `fable` — never a raw model ID.

## Phase 1 — Clarify (you, no subagents)

Dispatch nothing until scope is agreed with the human.
Produce: a one-sentence goal, 3-5 closed sub-questions, and a "done" criterion.
Ask about anything ambiguous. Do not assume.
If the work doesn't split into at least three genuinely separable sub-questions, answer directly — fan-out would be pure cost.

## Phase 2 — Research (fan-out, `sonnet`)

One researcher per sub-question, dispatched together in a SINGLE message as parallel tool calls — sequential dispatch is this workflow's main latency source.
`sonnet` for every researcher: this is decision-grade cited research, not lookup. Savings come from the fan-out shape, not a cheaper worker.
Each prompt is self-contained and states:
- the one closed sub-question, plus starting URLs if any exist
- cite a URL + date for every fact; mark every line `[fact]` or `[inference]`
- report in under ~300 words, no preamble
- do not rewrite the overall plan; report blockers upward instead of working around them

Do not ask a researcher to judge source quality or resolve contradictions; that's your job.

## Phase 3 — Verify (you)

Cross-check the outputs. On a conflict, dispatch ONE tie-breaking researcher (`haiku` — the question is narrow and already framed) with the deciding question.
Discard unsupported `[inference]`s.
Produce an evidence map: claim -> source -> confidence. The map, not the transcripts, is what moves forward.

## Phase 4 — Plan (single subagent, `opus`)

Receives: goal, evidence map, constraints, deliverables. Never the researchers' raw transcripts.
Name any unresolved tension in the map and order the planner to settle it.
Must CHOOSE, not enumerate. Open decisions = rejection.

## Phase 5 — Critique (single subagent, `opus`, clean context)

Never the agent that wrote the plan, and never below the planner's tier — a weaker reviewer misses exactly the flaws this phase exists for.
Looks for: unvalidated assumptions, non-idempotent steps, what fails first, circular dependencies, decisions the evidence doesn't support.
Material flaw → back to Phase 4 with the findings. Maximum 2 rounds; after round 2, proceed to Phase 6 and list remaining flaws as accepted risks.

## Phase 6 — Deliver

Final plan + evidence map + consciously accepted risks.

## Budget

Never re-invoke the Agent tool to "continue" a finished subagent — that spawns a confused duplicate. Message the existing agent, or dispatch a fresh, self-contained one.

Hard stop — abandon the run and report what you have, out loud:
- a dispatch fails twice in a row (its one allowed retry also fails)
- Phase 4 comes back with open decisions twice

Not a hard stop: 2 completed critique rounds — that's Phase 5's normal exit; proceed to Phase 6.

Never continue silently.
