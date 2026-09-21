# workflow-model-override evaluation (2026-09-21)

Fase-0 de-risking spike for the orchestration architecture decided in
`tasks/README.md`'s "Orchestration architecture" section — specifically the
"confirm a `Workflow` script with per-phase `model` overrides" item listed
under "Remaining spikes before the rest of `tsk` gets written". **Result:
PASS, confirmed.** The spike was first attempted from a delegated subagent,
where the `Workflow` tool turned out to be unreachable (see "Tool
availability constraint" below) — the orchestrating top-level session then
ran the already-authored script itself and got a clean, differentiated
result: `agent(prompt, {model, effort})` really does select a different
model per phase, not just accept the option and ignore it.

## Confirmed result (run from the top-level session, `wf_1c1da6c5-023`)

```json
{
  "phaseA_model_requested": "haiku",
  "phaseA_self_report": "claude-haiku-4-5-20251001",
  "phaseB_model_requested": "opus",
  "phaseB_self_report": "claude-opus-5",
  "differentiated": true
}
```

Both phases reported back a model id plausibly matching the tier
requested (`haiku` → `claude-haiku-4-5-20251001`, `opus` → `claude-opus-5`),
and the two reports differ — this is real differentiation, not two calls
silently falling back to the same default model.

## What was attempted

1. Loaded the `workflow-authoring` skill first, as instructed, to read the
   real script-API conventions before writing anything (pure-literal
   `meta`, `phase()`/`agent()` usage, `opts.model`/`opts.effort`, the
   `meta.phases[].model` convention for documenting a phase's override).
2. Authored a minimal 2-phase script,
   `spike-model-override.workflow.mjs` (this directory): phase A calls
   `agent(..., {model: 'haiku', effort: 'low'})`, phase B calls
   `agent(..., {model: 'opus', effort: 'high'})`. Each agent is asked to
   self-report the exact model id/name from its own system prompt — the
   differentiation check is "did A and B report different strings", not
   merely "did the script run without error".
3. Attempted to invoke it via the `Workflow` tool.

## Finding: the `Workflow` tool is not in this agent's toolset

This spike ran as a delegated subagent (spawned by an orchestrator via the
Agent/Task mechanism), not as a top-level interactive Claude Code session.
In that context:

- `Workflow` is **not** among the tools listed at the top of the session
  (only `Agent`, `Artifact`, `Bash`, `Edit`, `EnterWorktree`, `Read`,
  `Skill`, `ToolSearch`, `Write`, `SubagentHandback`).
- `Workflow` is **not** among the deferred tools the session's
  system-reminder explicitly enumerated as loadable via `ToolSearch`
  (`ArtifactComments`, `ArtifactData`, `ExitWorktree`, `Monitor`,
  `NotebookEdit`, `SendMessage`, `TaskStop`, `WebFetch`, `WebSearch`, plus
  the Slack/Claude-Docs MCP tools).
- `ToolSearch` was queried four separate ways (`"select:Workflow"`,
  `"workflow orchestration multi-agent script"`,
  `"select:Workflow,workflow,RunWorkflow,workflow_tool"`, and
  `"phase agent parallel pipeline meta subagent script orchestrate"`) —
  every query came back with either "No matching deferred tools found" or a
  list of unrelated tools (Monitor, SendMessage, TaskStop, Slack MCP tools).
  There is no `Workflow` schema to load, so there was no way to construct a
  call to it at all — not a permission block, an outright absence.
- No `.claude/settings*.json` in this worktree or its `.claude/` config
  restricts a `Workflow` tool by name (checked — none exist here that
  mention it), so this isn't a local policy override either; it reads as
  the harness simply not exposing `Workflow` to Task/Agent-spawned
  subagents, only to a main-loop session.

Given this, actually running the script and reading back which model each
phase used was not possible from here. Rather than fabricate a plausible
looking result, this is reported as a blocked spike.

## Why this finding still matters for the architecture decision

`tasks/README.md`'s L2 row assumes `Workflow`'s `agent(prompt, {model,
effort})` is available to whatever process orchestrates `tsk`'s phases. If
that orchestration itself is implemented as (or delegates through) a
subagent layer — which is exactly the shape this very spike task was
dispatched in (a sibling-worktree "team-workflow-model" agent) — then
`Workflow` may be unreachable at the point where it's needed. This spike
did not confirm or refute the model-override behavior itself, but it did
surface a real constraint: **`Workflow` invocation needs to happen from a
main-loop/top-level session, not from inside a delegated subagent.** That
should be re-verified directly (see "Re-run instructions" below) before
`tsk`'s L2 layer is built on the assumption that any agent in the fleet can
call it.

## Re-run instructions (for whoever picks this back up)

Run `spike-model-override.workflow.mjs` (unchanged, or via
`Workflow({scriptPath: "<path to this file>"})`) from a top-level
interactive Claude Code session where the `Workflow` tool is actually
listed as available, and confirm:

- The run completes with two `agent()` results.
- `phaseA_self_report` and `phaseB_self_report` differ, and each plausibly
  names the requested tier (haiku vs. opus) rather than both reporting the
  session's default model.
- Report the literal returned object (or the run's `journal.jsonl`) as the
  evidence — not just "it ran with no errors", since a silent no-op
  fallback to the default model would still exit cleanly.

## Files here

- `spike-model-override.workflow.mjs` — the authored-but-unexecuted script,
  ready to run as-is from a session with `Workflow` access.

## Verdict

**PARCIAL / blocked** — not PASS (the override was never actually
confirmed) and not a clean FAIL of the feature itself (nothing suggests
`Workflow`'s per-phase override is broken; the blocker is tool
availability in this session, a different question). The `Workflow`
per-phase `model`/`effort` override item in `tasks/README.md`'s spike list
should stay open until re-run from a session where the tool is reachable.
