# harness-radar — brief for 2026-09-25

**Day-one note:** this is the radar's first-ever run, so every source's first
API page counts as "new" (per README's acceptance criteria). Volume is
baseline flood, not a busy-day signal. Benchmark leaderboards established
their snapshots today — rank-change signal starts with tomorrow's diffs.

## Source status (24/24 ok)

All 24 sources `ok` with zero consecutive failures — see
`~/.local/state/harness-radar/status.json`. No dead-source warnings.

## Top suggestions

### 1. herdr v0.9.1 + native kitty rendering (breaking) — update your herdr

- **What:** `herdrdev/herdr` shipped **v0.9.1** (latest stable), and main
  landed **`feat!: replace the custom graphics api with optimized native
  kitty rendering` (c411883)** — a breaking change replacing the custom
  graphics API. Same window also added per-pane opencode subagent status
  tracking (f639075).
- **Why it clears the rubric:** herdr is this machine's actual agent
  multiplexer (herdr-commander work, `herdr-agent-state.sh` hook) — top
  possible fit. A breaking rendering change is exactly the kind of thing to
  catch *before* an accidental preview-build update, not after.
- **Action for you:** check which herdr build this machine runs and read the
  v0.9.0/v0.9.1 release notes for the kitty-graphics migration notes before
  updating. No automated install (radar never runs anything).

### 2. best-skills #1: `vercel-labs/agent-browser` — skill worth evaluating

- **What:** the best-skills daily CSV ranks **agent-browser** (vercel-labs)
  as the #1 most-installed agent skill; anthropics' `frontend-design` and
  `find-skills` fill out the top 3.
- **Why it clears the rubric:** this machine is skills-heavy (`~/.agents/
  skills` + `~/.claude/skills` sync flow); the #1 installed skill in the
  ecosystem is a strong trend signal, and browser automation fits the
  Chrome/agent workflows in use here.
- **Security gate:** suggestion only — nothing installed or run by the
  radar. Evaluate manually before adopting.

### 3. herdr-plugin marketplace: two notable arrivals

- **What:** the `herdr-plugin` topic listing (the `herdr.dev/plugins` index)
  shows **`openclaw/crabbox`** (★1430, canonical openclaw org — verified
  against `ranking.md`'s canonical-org table, not fork-spam) and
  **`eliasstravik/herdr-projects`** (★460) as the highest-signal new
  entries; `ChmaraX/herdr-nvim` (★209) also re-surfaced.
- **Why it clears the rubric:** marketplace scan is this radar's standing
  plugin-discovery source; these two dominate the day's listing by stars and
  provenance. Fit is plausible (herdr-adjacent tooling) but unproven — hence
  "look", not "adopt".
- **Duplicate-note:** the topic diff contained same-day re-listings
  (crabbox, herdr-nvim, unblock ×2) — deduped in `ranked.json`.

## Pruned (not padded)

Hermes Agent's near-daily cadence (v0.21.5 today), microsoft/agent-framework
shipping Copilot support, and the tracked frameworks' routine releases all
scored mid-table — real signals, but none clears the "worth your attention
today" bar today. Full scoring in the ranked file below.

**Interactive-only commands** (never run by the radar; for you, if you want
more detail on suggestion 2):
- `npx skills find agent-browser`
- `npx tessl search agent-browser`

## Full-ranking record

`briefs/harness-radar-2026-09-25.ranked.json` — one scored entry per inbox
item (326), feeding `~/.local/state/harness-radar/history.db`
(`sqlite3 ~/.local/state/harness-radar/history.db "select * from candidates
order by score desc limit 50"` or `.agents/automation/radar-common/router.sh
top harness-radar 50`).
