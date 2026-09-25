# Plan: `gauntlet-prompting` skill

Card: `dotfiles-tsk-skill-gauntlet-prompting`. Written by an Opus Plan agent on 2026-09-24; implemented 2026-09-25 in `.agents/skills/gauntlet-prompting/`.

**Owner decisions (2026-09-25), which override the defaults below:**
1. Meaning confirmed: the Gauntlet Loop, which refines LLM outputs (not red-teaming).
2. Round cap: **3 per piece** (not 6).
3. **Always hand off** to a fresh session; the loop never runs in the current one.

**Deviations made during implementation:**
- Command bars must be written `cmd:<command>`. Without the prefix, a vague bar like "make it great" passed `check-bar`, because `make` is on PATH.
- `pair` copies local files to neutral `A.<ext>`/`B.<ext>` names so their paths don't reveal which side is the candidate.
- Shumer's source asks for an independent, A/B-style critic but doesn't mandate blindness. Blind picks are local hardening, and SKILL.md says so.

## (a) Definition and scope

**Decision:** "gauntlet prompting" here means the **Gauntlet Loop**, a prompting method Matt Shumer published on 2026-07-27 (https://somethingbig.ai/gauntlet-loop). It has since been packaged as agent skills by RoboNuggets (https://github.com/robonuggets/gauntlet-loop, CC BY 4.0) and by Nicholas Spisak (https://github.com/NicholasSpisak/gauntlet-loop, MIT). The other "Gauntlet" results are unrelated: a prompt-injection benchmark (zeroleaks.ai/gauntlet) and a red-team tool (redamon "AI Gauntlet").

The method's core rules:
- The goal is ambitious and does not say how to build it.
- The quality bar is a **real, named, fetchable, comparable exemplar**, not a rubric ("A rubric asks the agent to grade itself against words it wrote. A bar makes it compare against something that already exists.").
- The lead agent splits the goal into pieces that can be improved separately.
- Each piece gets a **builder** plus a **separate critic with fresh context**.
- The critic inspects the real artifact, never a summary written by the builder.
- The judgment is a **binary blind pick**, not a score.
- The loop runs until the work wins, the owner stops it, or the budget runs out.
- The output prompt is short (about 150 words).

**What this skill does:** it turns a goal into (1) a chosen, verified quality bar and (2) a short, harness-specific **gauntlet prompt** to paste into a fresh session. It also ships a deterministic **ledger script** that the executing session uses for blind A/B ordering, recording verdicts and deciding when to stop. By default it **compiles** the prompt and hands it off; the loop runs in a fresh session.

**What it is NOT:**
- **Not `plan-orchestra`.** That skill critiques a *plan*. Gauntlet iterates on a *built artifact* against an *external exemplar*. Gauntlet reuses plan-orchestra's harness-split wording. If a goal needs a plan first, run plan-orchestra and pass its plan to gauntlet as the goal.
- **Not `reviewhits`.** That is a one-shot critique of a manuscript.
- **Not `simplifyhit`.** That optimizes an instruction file against a rubric.
- **Not red-teaming.**

**Alternatives considered (not chosen):**
1. Adversarial prompt stress-testing: attacker/critic passes against a prompt or system instruction.
2. A multi-gate code workflow like ohshitgorillas/gauntlet. It overlaps with this repo's `tasks/` kanban phases.

## (b) Frontmatter

```yaml
name: gauntlet-prompting
description: >
  Compile a goal into a Gauntlet Loop prompt (Matt Shumer's method): pick a
  real, fetchable quality bar (an existing exemplar, never a rubric), then emit
  a short harness-specific kickoff prompt where builders produce work and
  fresh-context critics make blind A/B picks against the bar, looping until
  the work wins or budget runs out. Use when the user says "gauntlet",
  "gauntlet loop", "gauntlet prompt", "make it as good as <X>", or wants an
  artifact (site, CLI, doc, deck, skill, essay) iterated against a concrete
  reference. Not for planning/research (plan-orchestra), one-shot critique
  (reviewhits), or instruction-file tidying (simplifyhit). Thin shell over
  scripts/render_prompt.py and scripts/gauntlet_ledger.py (D14).
```

## (c) Procedure

1. **Goal:** one sentence (artifact + audience). Don't ask for implementation detail.
2. **Offer 2-3 bars** (named, fetchable, comparable). The owner picks. Never pick for the owner, and never use a rubric.
3. **Verify the bar:** run `render_prompt.py check-bar --bar <ref>`. It checks for a URL 2xx, a path that exists, or a command on `PATH`. On failure, go back to step 2.
4. **Target harness:** `claude` (default) | `copilot` (small artifacts only) | `agy` (adds a warning that cost and plumbing are unverified).
5. **Budget:** `max_rounds`, default 6. Hitting the cap is a human gate, not a silent stop.
6. **Render:** run `render_prompt.py render --goal ... --bar ... --harness ... --max-rounds N [--task-id ID]`. It enforces 250 words or fewer and prints the ledger init line.
7. **Hand off:** show the prompt verbatim. If there is a task-id, offer `tasks/dispatch.py --task-id <id> --provider <h> --launch` but don't run it unprompted. Run the prompt in a fresh session.
8. **What the executing session does:** for each piece, per round: builder → `gauntlet_ledger.py pair` → a fresh-context critic sees only A and B and picks one with a short reason → `verdict` → `status`.
   - `WIN`: integrate the piece.
   - `CONTINUE`: the builder revises using only the critic's reason.
   - `STOP_BUDGET` or `STOP_PLATEAU`: report to the human.

   Critics never see builder notes or earlier drafts and are never reused. Builders never grade their own work.

## (d) Files

| File | Purpose |
|---|---|
| `.agents/skills/gauntlet-prompting/SKILL.md` | Thin shell (~1,500 tokens or fewer) |
| `.agents/skills/gauntlet-prompting/templates/gauntlet-prompt.md` | Prompt template with `{{goal}}`, `{{bar}}`, `{{bar_access}}`, `{{max_rounds}}`, `{{ledger_init}}` and `{{delegation_block}}` |
| `.agents/skills/gauntlet-prompting/scripts/render_prompt.py` | Stdlib only. `check-bar` and `render`; the per-harness delegation blocks are constants |
| `.agents/skills/gauntlet-prompting/scripts/gauntlet_ledger.py` | Stdlib only; D14 core. `init`, `pair`, `verdict`, `status` |
| `.agents/skills/gauntlet-prompting/scripts/test_gauntlet.py` | unittest tests for both scripts |
| `.claude/skills/gauntlet-prompting`, `.github/skills/gauntlet-prompting` | Symlinks to `../../.agents/skills/gauntlet-prompting` (Antigravity/Gemini read `.agents/skills/` directly) |

`gauntlet_ledger.py` details:
- **Ledger location:** `${XDG_STATE_HOME:-~/.local/state}/gauntlet/<slug>/ledger.jsonl`, outside any repo.
- **`pair`:** shuffles A/B (seedable), stores the hidden mapping, and prints only `A=<ref> B=<ref>`.
- **`verdict`:** maps the pick back to candidate or bar and appends the round, winner and reason.
- **`status`:** prints exactly one of `WIN`, `CONTINUE`, `STOP_BUDGET` or `STOP_PLATEAU`. The exit codes and printed tokens are stable. The rules:
  - `WIN`: the candidate won the latest pick.
  - `STOP_BUDGET`: rounds ≥ max.
  - `STOP_PLATEAU`: 3 consecutive losses whose reasons have a Jaccard similarity of 0.8 or more with the previous reason.
  - Otherwise `CONTINUE`.

No README.md or examples.md, following the task-brief and setup-dotfiles precedent.

## (e) SKILL.md skeleton

```markdown
---
name: gauntlet-prompting
description: >  (see §b)
---

# /gauntlet-prompting

Compiles a goal + a real exemplar into a short Gauntlet Loop kickoff prompt
(Matt Shumer, 2026-07-27; skill lineage: robonuggets/gauntlet-loop CC BY 4.0).
You COMPILE and HAND OFF; the loop runs in a fresh session. Deterministic
parts (bar check, rendering, A/B shuffle, stop rule) live in scripts/ (D14).

## Harness split
- Claude Code: real subagents (Agent tool) for builder and each critic; new critic every round.
- Copilot CLI / Antigravity / Gemini / other: roles played sequentially with an explicit
  context reset before each critic pass (same wording as plan-orchestra).
- agy: render_prompt.py adds the "cost/plumbing unverified" warning.

## What to do
1. Goal: one sentence. 2. Offer 2-3 bars, owner picks. 3. check-bar.
4. Harness. 5. Budget (default 6). 6. render. 7. Show prompt; offer (don't run) dispatch.

## What the executing session does
pair → blind critic picks A|B → verdict → status: WIN | CONTINUE | STOP_BUDGET | STOP_PLATEAU.

## What NOT to do
- Don't accept "make it great" / a checklist as the bar.
- Don't run the loop in this context; don't reuse a critic.
- Don't show the critic builder notes, diffs, or which side is the candidate.
- Don't compute A/B order or the stop decision yourself; run gauntlet_ledger.py.
- Don't use this for plans (plan-orchestra) or one-shot reviews (reviewhits).
```

## (f) Testing

**Script tests** (unittest):
1. `pair` puts the candidate on A about 50% of the time (±10%) over 200 seeded runs, and the mapping persists across processes.
2. `status` covers WIN, STOP_BUDGET, STOP_PLATEAU (3 similar losses) and CONTINUE (3 different losses).
3. `render` for each harness: 250 words or fewer, no leftover `{{`, the Agent-tool line for claude, the context-reset line for the others, and the agy warning.
4. `check-bar`: an existing path passes, a missing path fails, an unknown command fails. URLs are tested with a mock.

**Behaviour evals** (run on Claude Code and Copilot CLI, and on agy once its plumbing is confirmed):
- **E1:** "gauntlet this: a landing page as good as https://charm.sh". Expected: the skill offers bars and does not build.
- **E2:** "gauntlet my README until it's excellent". Expected: it refuses the vague bar and proposes exemplars.
- **E3:** a planning request routes to plan-orchestra, and "review this paper" routes to reviewhits.
- **E4:** `tasks/brief.py --help` as clear as `rg --help`, max 3 rounds. Expected:
  - A/B is shuffled across rounds.
  - No builder notes reach the critic.
  - It ends in WIN or STOP_BUDGET.
  - The repo root stays clean.
- **E5:** with `--task-id`, it offers dispatch and does not launch without confirmation.
- **Static checks:** `scripts/validate_dotfiles.sh` passes. The `simplifyhit` audit is advisory only.

## (g) Open questions for the owner

1. Shumer's Gauntlet Loop, or red-teaming a prompt against attacks? (The plan assumes the Gauntlet Loop.)
2. Is a default cap of 6 rounds right, and should it apply per piece or per run?
3. Should the skill ever run the loop in the current session for small artifacts, or always hand off? (The plan says always hand off.)

## (h) Risks

- **Budget burn.** Mitigations: the required cap, the cap as a human gate, and a warning when there are more than 3 pieces on Claude.
- **Weaker blindness without subagents** (Copilot/agy). The critic only gets the refs from `pair`; the output names this risk.
- **No comparable exemplar.** The bar can be a runnable reference plus the same test command on both sides. Otherwise the skill refuses rather than falling back to a rubric.
- **Crude plateau heuristic.** It is deterministic and tunable in one place.
- **Attribution.** Credit Shumer and RoboNuggets (CC BY 4.0) and write the template fresh.
- **Name drift.** Include both "gauntlet prompting" and "Gauntlet Loop" as triggers.

Sources: somethingbig.ai/gauntlet-loop, github.com/robonuggets/gauntlet-loop, github.com/NicholasSpisak/gauntlet-loop, github.com/ohshitgorillas/gauntlet, zeroleaks.ai/gauntlet, github.com/samugit83/redamon/wiki/AI-Gauntlet.
