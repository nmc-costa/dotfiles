# GEMINI.md

Instructions for Gemini when working in this repository.

## Context

`~/dotfiles` is the central repository for configuration and environment synchronization across machines. It contains:

- **Agents:** Crush, Copilot, Gemini, Cline configurations in `.agents/`
- **Skills:** Agent extensions in `.agents/skills/`
- **Workflows:** Personas and workflows in `.agents/workflows/`
- **Context:** `AGENTS.md`, `CLAUDE.md`, `docs/directory_tree.md`
- **Automation:** `setup.sh`, `sync.sh`

## At the start of a session, also read

- **`CHEATSHEET.md`** — where things go, and §4's persistent cross-session TODO list (survives longer than any single session's own tracking).
- **`tasks/board.md`** and **`tasks/README.md`** — the workspace's task tracker (an append-only event log projected into a table). Check it for open work before starting something new, and append an event with `tasks/append_event.py` when you finish something worth tracking there.

(Added 2026-09-16 — Claude Code gets this automatically via a `SessionStart` hook; Gemini has no equivalent hook yet, so this section is the manual substitute. See `CLAUDE.md`'s "Known Gaps" for the full finding.)

<!-- OUTPUT-FRAME:CORE BEGIN -->
## Output frame (every human-facing reply; full text: ~/.agents/instructions/workspace-config/output-frame.instructions.md)
Size the reply: S = <~25 lines, no headings · M = 25–80 lines, ≥3 sections, or a multi-file change report · L = any plan, or >~80 lines.
- S: no frame.
- M: first line `MODE [X] · STATUS: … · Confidence n/10 · Entropy: Stable|High · <date>`; end with `---` + **TL;DR** (≤5 bullets that compact what's above, nothing new) + `Needs you: … | none`.
- L: full header (SYSTEM INSTRUCTION MODE / STATUS / RESONANCE / ANALYSIS / TIMESTAMP); end with TL;DR + Index (headings verbatim, in order) + Flow (`Path:` arrow line + ≤12-node mermaid flowchart: steps, dependencies, owner-decision diamonds; omit if no sequence) + Needs you.
- L >~150 lines, OR likely to be revised/re-referenced/handed off, and you can write files: body goes to a file (tasks/plans/, docs/, scratchpad; Claude Artifact only if visual or requested) with TL;DR+Index+Flow at its TOP; chat = header + footer + path. Revise it with targeted edits, never by re-emitting the whole body; refer to it by path + heading. Prefer a subagent writing the file itself when the harness supports it.
- `Needs you:` uses the autonomy charter's DECISION line format. Escalation BLUFs, agent-to-agent messages, commits, PR bodies and verbatim output are exempt.
- Confidence: 9–10 verified this turn, 6–8 consistent-not-run, 3–5 inferred, ≤2 guess. Never invent a timestamp. Footer in the owner's language; header keys in English.
- This block is static: no dates, counters, or per-machine values in it — it's loaded into every session's cached prefix, and dynamic content here would force a cache rewrite on every request.
<!-- OUTPUT-FRAME:CORE END -->

## Project Structure

Real projects live in:
- **`~/Projects/`** — Personal repos (agentic_instructions, HIcode, ibots, roi_lab, etc.)
- **`~/Work/`** — Professional repos (mobai, RAGFusion, sp_xai_nos, etc.)

Each project is an independent git repository with its own remote.

## Using This Repo

1. **View structure:** `cat ~/dotfiles/README.md`
2. **View available skills:** `ls -la ~/.agents/skills/`
3. **Add a new skill:** see `AGENTS.md` > "Adding a New Skill"
4. **Set up a new machine:** `cd ~/dotfiles && ./setup.sh --dotfiles`

## Best Practices

- Don't edit skills directly in `~/.agents/skills/` — always edit in `~/dotfiles/.agents/skills/` and sync
- For personal workflows: use `~/.agents/workflows/` (symlink to `~/dotfiles/.agents/workflows/`)
- For new skills: add to `~/dotfiles/.agents/skills/` and do `git commit + ./sync.sh`

## Full Documentation

See `AGENTS.md` for the detailed guide on agents, skills, workflows, and cross-machine synchronization.
