# omarchy-radar ranking rubric and brief format

This is what the unattended `claude -p` agent step (see `SKILL.md`'s Decision
Framework) applies to `inbox.json` to pick its top 3 suggestions, and what a
human reviewing a brief can use to sanity-check the agent's scoring.

## 0. Security gate — applied before any scoring

Before an item is even scored, ask: **does surfacing or acting on this
require installing, running, or sourcing anything?** If yes:

- Drop it entirely from the automated top-3, or
- Downgrade it to a footnote pointing at a command the human can run
  interactively (see the "Tips" footer below).

This is the same rule as `security.md`'s: `npx skills find`, `npx tessl
search`, `omarchy pkg add`, `omarchy plugin add`, any `sudo`/`pacman`
invocation — none of these are ever executed by `collect.sh` or the agent
step. A brief may *mention* such a command as something the human can choose
to run themselves; it never runs one.

## 1. Rubric (a) — config/behavior suggestions

Score each surviving candidate on:

- **Impact** — how much it actually improves this machine's setup (a real
  Hyprland/terminal/shell quality-of-life or capability gain), not how
  popular the source post was.
- **Effort/Risk** — how invasive the change is (a one-line config tweak vs. a
  new plugin install vs. a workflow change), and whether it's easily
  reversible.
- **Redundancy** — does this duplicate something already tracked in
  `dotfiles` (an existing skill, an existing config choice) or already
  proposed in a prior, still-open brief? Check
  `docs/radar-knowledge/omarchy.md` before assuming something is new.
- **Fit** — does it match how this machine is actually configured (Hyprland +
  Omarchy shell + the terminals actually installed), not a generic Omarchy
  tip that doesn't apply here.

Marketplace/repo popularity metrics (views, hearts, stars) are **explicitly
excluded** as a ranking signal on their own — they inform "is this real and
maintained," never "is this worth doing."

## 2. Rubric (b) — fit/redundancy vs. what's already tracked

Before trusting any candidate repo/source as authoritative, verify it matches
the canonical identity recorded in `sources.md` /
`docs/radar-knowledge/omarchy.md` (e.g. `omacom/omarchy`, not a redirecting or
unofficial mirror). A source that doesn't match gets flagged in the brief,
not silently trusted on star count or post-engagement alone.

## 3. Prune bias

When in doubt between surfacing a marginal fourth item and stopping at 3,
**stop at 3.** The brief's whole value proposition is "under 2 minutes to
read" — a longer, hedged brief that tries to cover everything defeats that.

## 4. Brief format

`briefs/omarchy-radar-<date>.md`:

```markdown
# omarchy-radar — <date>

## Sources checked
- <source>: ok (<n> new items)
- <source>: error (<consecutive-failure count>, see status.json)
...

## Top 3 suggestions

### 1. <title>
- **What**: one or two sentences
- **Why now**: which source(s) this came from, with a link
- **Impact / Effort / Redundancy / Fit**: one short line each
- **Diff**: a real `diff -u` (tracked-file suggestions, spliced in by
  `run.sh` — never model-written) OR an explicitly labeled
  "AI-drafted, unverified" diff block (live `~/.config` suggestions only)

### 2. ...
### 3. ...

## Tips
<interactive-only commands the human may want to run themselves, e.g.
`npx skills find <query>` or `npx tessl search <query>` — never run by the
radar itself; see security.md>
```

If a source failed 3+ consecutive runs, add a `## Source health` section
calling it out explicitly rather than letting it read as "nothing new."

If every category was empty and nothing errored, no brief is written at all
(see `README.md`'s pipeline) — this format only applies once there's
something to say.

## Full ranking output (for the queryable history, not the brief itself)

Alongside the brief, also write `briefs/omarchy-radar-<date>.ranked.json`: a
JSON array with one entry per inbox item you scored (not just the top 3) —
`{"title", "url", "category", "score" (the numeric score from this rubric),
"rationale" (one line), "picked_top3" (true for exactly the items in the
brief, false otherwise)}`. `run.sh` loads this into a per-radar SQLite file
(`~/.local/state/omarchy-radar/history.db`) after a successful commit, so
the human can query a "top 50 over time" view (`sqlite3
~/.local/state/omarchy-radar/history.db "select * from candidates order by
score desc limit 50"`, or `.agents/automation/radar-common/router.sh top
omarchy-radar 50`) instead of reading one brief at a time. This file is a
nice-to-have record — a missing or malformed one never blocks the brief
itself from being committed.
