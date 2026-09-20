---
name: plan-orchestra
description: "Orchestrate a multi-agent research-and-planning workflow: clarify scope with the human, fan out closed sub-questions to research subagents, verify and reconcile their findings into an evidence map, have a single subagent commit to one decisive plan, subject that plan to adversarial critique, then deliver. Use when the user asks for a plan, proposal, or investigation that needs verified evidence gathered by multiple subagents before a decision is made — not for simple single-step questions."
---

# Plan Orchestra

Role: you are the MAIN agent. You clarify, dispatch, verify, and integrate — you never research or write the plan yourself.

Every phase below names a role (researcher / planner / critic), not a specific tool call, so this skill runs on any harness. Match your label below to `.agents/harnesses/<this-harness>.md` before assuming which one applies:

- **Claude Code** — verified delegation primitive: the `Agent`/Task tool. Dispatch real subagents in parallel per each phase's instructions. Pass model tier via its enum values `haiku`/`sonnet`/`opus`/`fable` — never a dated model ID — cheapest tier only for trivial confirmatory lookups, top tier for Phase 4's plan and Phase 5's critique (never below the plan's own tier).
- **Gemini CLI / Copilot / OpenAI / Antigravity / LiteLLM / deepskee / anything else with no delegation primitive documented in `.agents/harnesses/` yet** — play every role yourself, sequentially, in the same conversation: one closed sub-question at a time, same citation/`[fact]`/`[inference]` discipline, an explicit context reset before Phase 5's critique. You lose the parallelism/cost benefit, not the rigor.

If a harness doc is later updated to confirm a real delegation mechanism, give it its own label here instead of leaving it under the second one.

## Phase 1 — Clarify (you, no subagents)

Dispatch nothing until scope is agreed with the human.
Produce: a one-sentence goal, 3-5 closed sub-questions, and a "done" criterion.
Ask about anything ambiguous. Do not assume.
If the work doesn't split into at least three genuinely separable sub-questions, answer directly — fan-out would be pure cost.

## Phase 2 — Research (fan-out)

One researcher role per sub-question, dispatched together in parallel wherever the harness allows it — going one at a time is this workflow's main source of wasted time, whether that's sequential subagent dispatch or you working through sub-questions yourself.
Default every researcher to a mid/high-capability tier: this is decision-grade cited research, not lookup, the same reasoning behind Anthropic's own published multi-agent research system pairing a strong orchestrator with mid-tier (not cheapest-tier) workers. Savings come from the fan-out shape and tight scoping, not a cheaper worker.
Each sub-task is self-contained and states:
- the one closed sub-question, plus starting URLs if any exist
- cite a URL + date for every fact; mark every line `[fact]` or `[inference]`
- report in under ~300 words, no preamble
- do not rewrite the overall plan; report blockers upward instead of working around them

Do not ask a researcher to judge source quality or resolve contradictions; that's your job.

## Phase 3 — Verify (you)

Cross-check the outputs. On a conflict, dispatch ONE tie-breaking researcher (a cheaper/faster tier is fine here — the question is narrow and already framed) with the deciding question.
Discard unsupported `[inference]`s.
Produce an evidence map: claim -> source -> confidence. The map, not the transcripts, is what moves forward.

## Phase 4 — Plan (single subagent or role-switch, top tier)

Receives: goal, evidence map, constraints, deliverables. Never the researchers' raw transcripts.
Name any unresolved tension in the map and order the planner to settle it.
Must CHOOSE, not enumerate. Open decisions = rejection.

## Phase 5 — Critique (single subagent or role-switch, top tier, clean context)

Never the same instance that wrote the plan, and never below the planner's tier — a weaker or non-independent reviewer misses exactly the flaws this phase exists for. Where the harness can't spawn a real second context, force an explicit reset instead: restate the plan cold, without your own drafting rationale, before critiquing it.
Looks for: unvalidated assumptions, non-idempotent steps, what fails first, circular dependencies, decisions the evidence doesn't support.
Material flaw → back to Phase 4 with the findings. Maximum 2 rounds; after round 2, proceed to Phase 6 and list remaining flaws as accepted risks.

## Phase 6 — Deliver

Final plan + evidence map + consciously accepted risks.

## Budget

Never relaunch a fresh subagent with an unrelated prompt to "continue" one that already finished — that produces a second, confused agent instead of an answer. Use whatever the harness provides to resume/message an existing subagent; with nothing available, treat its output as final and scope any follow-up as an explicitly new request.

Hard stop — abandon the run and report what you have, out loud:
- a dispatch fails twice in a row (its one allowed retry also fails)
- Phase 4 comes back with open decisions twice

Not a hard stop: 2 completed critique rounds — that's Phase 5's normal exit; proceed to Phase 6.

Never continue silently.
