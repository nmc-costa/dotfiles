# GEMINI.md — global pointer

This file is symlinked to `~/.gemini/GEMINI.md` (see `setup.sh`'s
`setup_agent_file_symlink`), the one versioned piece of Gemini CLI's
otherwise-local `~/.gemini/` state directory (`history/`, `state.json`,
`trustedFolders.json`, etc. stay real and untouched).

Real content lives in `.agents/instructions/workspace-config/` — read
every `*.instructions.md` there; they apply to every agent, not just
Gemini (see `.agents/instructions/README.md`).

`output-frame.instructions.md` is the one exception: it's an on-demand
reference, and its always-loaded part is the `OUTPUT-FRAME:CORE` block
below — don't also read the full file at session start.

<!-- OUTPUT-FRAME:CORE BEGIN -->
## Output frame (every human-facing reply; full text: ~/.agents/instructions/workspace-config/output-frame.instructions.md)
Size the reply: S = <~25 lines, no headings · M = 25–80 lines, ≥3 sections, or a multi-file change report · L = any plan, or >~80 lines.
- S: no frame.
- M: first line `MODE [X] · STATUS: … · Confidence n/10 · Entropy: Stable|High · <date>`; end with `---` + **TL;DR** (≤5 bullets that compact what's above, nothing new) + `Needs you: … | none`.
- L: full header (SYSTEM INSTRUCTION MODE / STATUS / RESONANCE / ANALYSIS / TIMESTAMP); end with TL;DR + Index (headings verbatim, in order) + Flow (`Path:` arrow line + ≤12-node mermaid flowchart: steps, dependencies, owner-decision diamonds; omit if no sequence) + Needs you.
- L+ (only when the harness can write files): triggered by (>~150 lines) OR (likely to be revised/re-referenced/handed off). Body goes to a file (tasks/plans/, docs/, scratchpad; Claude Artifact only if visual or requested) with TL;DR+Index+Flow at its TOP; chat = header + footer + path. Revise it with targeted edits, never by re-emitting the whole body; refer to it by path + heading. Prefer a subagent writing the file itself when the harness supports it. Can't write files: send the body inline regardless of length.
- `Needs you:` uses the autonomy charter's DECISION line format. Escalation BLUFs, agent-to-agent messages, commits, PR bodies and verbatim output are exempt.
- Confidence: 9–10 verified this turn, 6–8 consistent-not-run, 3–5 inferred, ≤2 guess. Never invent a timestamp. Footer in the owner's language; header keys in English.
- This block is static: no dates, counters, or per-machine values in it — it's loaded into every session's cached prefix, and dynamic content here would force a cache rewrite on every request.
<!-- OUTPUT-FRAME:CORE END -->

---

## Branch naming policy & client hook

This workspace enforces harness-prefixed branch names (e.g. `copilot/*`, `claude/*`, `agy/*`). A server-side CI workflow rejects pushes/PRs without one. To help local contributors and harnesses opt in to this policy, a client-side pre-push hook is provided at `tasks/scripts/pre-push.sample` and an installer script at `tasks/scripts/setup_git_hooks.sh`.

To install the hook manually:

  bash tasks/scripts/setup_git_hooks.sh

Or opt-in during initial setup/sync by running `./setup.sh --install-hooks` or `./sync.sh --install-hooks`. This is optional and never forced by the scripts; it requires explicit consent from the machine's user.

When creating branches or worktrees, include your harness name as a prefix so CI and reviewers can trace which harness created the branch (example: `copilot/feature-x`).
