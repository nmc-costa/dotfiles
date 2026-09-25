# Output frame

Always-loaded copy of the Output Frame core block for tools that discover
instructions via `.agents/rules/*.md` (Antigravity). Canonical, on-demand
full text: `.agents/instructions/workspace-config/output-frame.instructions.md`.
The block below is byte-identical in every entry file —
`scripts/check_core_blocks.sh OUTPUT-FRAME` fails on drift; edit all copies
together.

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
