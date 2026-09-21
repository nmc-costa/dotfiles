// Spike script for dotfiles-tsk-spike-workflow-model.
//
// Goal: confirm the Workflow tool's agent(prompt, {model, effort}) actually
// overrides the model per phase (per tasks/README.md's "Orchestration
// architecture" section, L2 row), not just that the script parses/runs.
//
// Minimal 2-phase design, each phase pinning a different model and asking
// the spawned agent to self-report its own model id/name (visible to it via
// its own system prompt) — differentiation is judged by comparing the two
// reported strings, not by trusting that the call merely didn't error.
//
// NOTE: this script was authored following the workflow-authoring skill's
// conventions but was NOT executed — see
// tasks/evaluations/workflow-model/README.md for why (the Workflow tool is
// not present in the toolset of the agent that ran this spike). Kept here,
// unexecuted, as the artifact a re-run from a session that does have the
// tool should use as-is.

export const meta = {
  name: 'spike-model-override',
  description: 'Confirm per-phase model/effort override in Workflow agent() calls',
  phases: [
    { title: 'Phase A (haiku)', detail: 'agent self-reports its own model id', model: 'haiku' },
    { title: 'Phase B (opus)', detail: 'agent self-reports its own model id', model: 'opus' },
  ],
}

phase('Phase A (haiku)')
const a = await agent(
  'You are running inside a Workflow agent() call. State ONLY the exact model name/id you are, exactly as it appears in your own system prompt (e.g. "claude-haiku-4-5" or "Haiku 4.5"). No explanation, just the identifier.',
  { model: 'haiku', effort: 'low', label: 'self-report-haiku' }
)

phase('Phase B (opus)')
const b = await agent(
  'You are running inside a Workflow agent() call. State ONLY the exact model name/id you are, exactly as it appears in your own system prompt (e.g. "claude-opus-4-5" or "Opus 4.5"). No explanation, just the identifier.',
  { model: 'opus', effort: 'high', label: 'self-report-opus' }
)

log(`Phase A reported: ${a}`)
log(`Phase B reported: ${b}`)

return {
  phaseA_model_requested: 'haiku',
  phaseA_self_report: a,
  phaseB_model_requested: 'opus',
  phaseB_self_report: b,
  differentiated: a !== b,
}
