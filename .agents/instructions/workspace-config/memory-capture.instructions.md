---
applyTo: "**"
---

# Proactive Memory / Context Capture

Learn from every interaction, not just explicit corrections. When an
approach, workaround, or piece of environment knowledge is confirmed to
work — a command that succeeds, a blocker resolved, a preference stated or
implied — persist it using whatever memory/persistence mechanism the
current agent/harness has, instead of waiting for the user to say "remember
this."

**Why:** stated explicitly by the workspace owner (2026-09-16), after
seeing this kind of fact captured only because it was asked for — the
expectation is that it happens by default from now on.

**How to apply, per harness:**

- **Claude Code:** use the built-in auto-memory system
  (`~/.claude/projects/<project>/memory/`) for facts scoped to one project
  or machine; use this `dotfiles` repo
  (`.agents/instructions/workspace-config/`, or a skill's own local
  addendum such as
  [`omarchy/tuning.md`](../../skills/omarchy/tuning.md)) for facts that
  should apply on every machine, to every agent.
- **Other harnesses (Copilot, Gemini, etc.):** persist durable,
  cross-session facts back into this repo rather than letting them live
  only in a single chat transcript, since these harnesses have no
  per-project memory store of their own here.

Keep entries concise and factual — what was confirmed, why it matters, how
to apply it — not a narrative log of the conversation that produced it.
