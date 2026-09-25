---
name: gauntlet-prompting
description: >
  Compile a goal into a Gauntlet Loop prompt (Matt Shumer's method) that
  refines an LLM's output against a real exemplar: pick a fetchable quality
  bar (an existing site, repo, file or command — never a rubric), then emit a
  short harness-specific kickoff prompt where builders produce work and
  fresh-context critics make blind A/B picks against the bar, looping until
  the work wins or the round budget runs out. Use when the user says
  "gauntlet", "gauntlet loop", "gauntlet prompting", "make it as good as <X>",
  or wants an artifact (site, CLI, doc, deck, skill, essay) iterated against a
  concrete reference. Not for planning/research (plan-orchestra), one-shot
  critique (reviewhits), or instruction-file tidying (simplifyhit). Thin shell
  over scripts/render_prompt.py and scripts/gauntlet_ledger.py (D14).
---

# /gauntlet-prompting

Compiles a goal + a real exemplar into a short Gauntlet Loop kickoff prompt.
Method: Matt Shumer, "The Gauntlet Loop" (2026-07-27,
https://somethingbig.ai/gauntlet-loop); prior skill packaging by RoboNuggets
(github.com/robonuggets/gauntlet-loop, CC BY 4.0) — the template here is
written fresh. **Local hardening beyond the source:** the critic's pick is
*blind* (A/B order shuffled by a script, local files staged under neutral
names) and every run has a hard round cap. The source asks for an
independent A/B-style critic and leaves stopping open.

**You COMPILE and HAND OFF. The loop always runs in a fresh session** —
never in this one, whose context is already loaded (owner decision
2026-09-25). Deterministic parts — bar check, rendering, A/B shuffle, stop
rule — live in `scripts/`; never re-derive them by hand.

## Harness split

- **Claude Code** — the rendered prompt uses real subagents (Agent tool) for
  builders and a brand-new subagent for every critic pass.
- **Copilot CLI / Antigravity (`agy`) / Gemini / anything else** — the prompt
  tells the session to play roles sequentially with an explicit context reset
  before each critic pass (same wording as `plan-orchestra`). Blindness is
  weaker here; say so when handing off.
- **`agy`** — the script appends a "cost/plumbing unverified" warning
  (`tasks/harness-provider-model-index.md`).

## What to do

`S=~/.agents/skills/gauntlet-prompting/scripts` (or
`.agents/skills/gauntlet-prompting/scripts` inside `~/dotfiles`).

1. **Goal** — one sentence: the artifact and who it's for. Don't ask for
   implementation detail; the method leaves the "how" to the builder.
2. **Bar** — propose 2-3 candidates as a short table (name, ref, why it
   fits). Each must be **named**, **fetchable** (URL, local path, or
   `cmd:<command>`) and **comparable** side by side with the output.
   **The owner picks — never pick for them.** The bar may be out of reach.
3. **Verify** — `python3 $S/render_prompt.py check-bar --bar <ref>`.
   `FAIL` → back to step 2. "Excellent", "production-ready", a checklist: no
   exemplar, no gauntlet — refuse and propose real ones.
4. **Harness** — where the prompt will run: `claude` (default) | `copilot`
   (small artifacts only) | `agy`.
5. **Budget** — rounds **per piece**, default **3** (owner decision
   2026-09-25). Hitting it is a human gate, not a silent stop. Warn before a
   Claude run you expect to split into more than 3 pieces.
6. **Render** — `python3 $S/render_prompt.py render --goal "..." --bar <ref>
   --harness <h> [--max-rounds N] [--task-id <kanban-id>]`. Exit 1 = over
   250 words: shorten the goal, never the rules.
7. **Hand off** — show the prompt verbatim in a code block, and say it
   belongs in a **fresh session**. With a `--task-id`, also *offer*
   `python3 ~/dotfiles/tasks/dispatch.py --task-id <id> --provider <h> --launch`
   — run it only when the owner says so.

## What the executing session does (enforced by prompt + ledger)

`L init` → per piece, per round: build → `L pair` (prints only `A=… B=…`) →
fresh critic picks `A|B` + the largest gap → `L verdict` → `L status`
prints `WIN` | `CONTINUE` | `STOP_BUDGET` | `STOP_PLATEAU` (3 losses with
near-identical gaps). The ledger lives under
`${XDG_STATE_HOME:-~/.local/state}/gauntlet/<run>/`, outside every repo.

## What NOT to do

- Don't accept a vague adjective or a rubric as the bar.
- Don't run the loop here, and don't reuse a critic across rounds.
- Don't show the critic builder notes, diffs, drafts, or which side is the candidate.
- Don't decide A/B order or when to stop yourself — run `gauntlet_ledger.py`.
- Don't use this for plans (`plan-orchestra`) or one-shot reviews (`reviewhits`).
  If a goal needs a plan before anything can be built, run plan-orchestra
  first and pass its plan in as the goal.

## Tests

`python3 .agents/skills/gauntlet-prompting/scripts/test_gauntlet.py` (stdlib
unittest, no network). Design and behaviour evals:
`tasks/plans/skill-gauntlet-prompting.md`.
