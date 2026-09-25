# omarchy-radar sources

Every source `collect.sh` fetches, with the exact endpoint/repo/API. **All of
these are data fetches (`curl`/`gh api`) — none of them execute third-party
code.** See [`security.md`](security.md) for why that distinction is
load-bearing. Repo identities below were confirmed via GitHub API and the
official `omarchy.org/manual` footer during this skill's research pass — see
`docs/radar-knowledge/omarchy.md` for the durable ledger, and check it first
before re-verifying any of these facts from scratch in a future session.

## Primary: releases, marketplace, news

**`https://mtolhuijs.nl/news-radar/feed.xml`** — the public RSS feed published
by [`mtolhuys/omarchy-news-radar`](https://github.com/mtolhuys/omarchy-news-radar)
(MIT, active), an existing Omarchy desktop plugin whose Python collector
already aggregates Omarchy GitHub releases, the official `omarchy.org/news`
RSS, and marketplace catalog diffs into a deduplicated feed. `collect.sh`
consumes this instead of re-scraping releases/marketplace from scratch.

- Format: RSS 2.0, `<item><guid isPermaLink="false">evt_…</guid><title>
  <link><description><pubDate>`. Dedupe on `<guid>`.
- Parse with Python's stdlib `xml.etree.ElementTree` — do not assume `xmllint`
  is installed.
- **Verify the response is well-formed RSS before trusting it** (not an
  HTML error/captive-portal page that happened to return 200). On any parse
  failure or non-200, fall back to `gh api repos/omacom/omarchy/releases`
  directly.
- Note: the feed's domain (`mtolhuijs.nl`) genuinely doesn't match the repo
  owner (`mtolhuys`) — that's correct, not a typo to "fix."

## Direct GitHub sources

- `gh api repos/omacom/omarchy/commits?sha=quattro` — new commits since the
  last-seen SHA (the news-radar feed doesn't cover raw commits).
  `omacom/omarchy`'s default branch is `quattro`; `basecamp/omarchy` now
  301-redirects to it — use `omacom/omarchy` as canonical.
- `gh api graphql` against `omacom/omarchy` for GitHub Discussions (REST has
  no Discussions endpoint, and no off-the-shelf tool covers this). The
  existing `repo`/`read:org` token scopes are sufficient for reading
  Discussions on a public repo — no new scope needed.
- Diff the current `aorumbayev/awesome-omarchy` README against the last
  snapshot in `~/.local/state/omarchy-radar/snapshots/`.
- Diff `omacom/omarchy-plugin-marketplace`'s index against the last snapshot,
  as a **secondary** check only (metrics like views/hearts are explicitly
  excluded from the ranking signal, per `ranking.md`) — mainly a backstop in
  case the news-radar feed misses a listing. The marketplace repo is
  `omacom/omarchy-plugin-marketplace`, not `HANCORE-linux/...` (which also
  redirects there).

## Community discussion

- Reddit: `https://www.reddit.com/r/omarchy/new/.rss` (keyless Atom feed,
  custom `User-Agent` header required; parsed with stdlib ElementTree).
  The `.json` endpoint used originally now 403-blocks this machine's
  UA/IP class (verified live 2026-09-25) while `.rss` still serves 200.
- Hacker News: `https://hn.algolia.com/api/v1/search_by_date?query=omarchy`
  (HN Algolia API, keyless).
- **`last30days-skill` (`mvanhorn/last30days-skill`) is not installed on this
  machine** and `collect.sh` does not hard-depend on it. If the user installs
  it later, it's a drop-in upgrade path for this section, not a blocker now.

## Skill/plugin/MCP ecosystem signal

Filtered to Omarchy/Hyprland/dotfiles-relevant rows only, and data-fetch only:

- `LinklyAI/best-skills` daily CSV:
  `https://raw.githubusercontent.com/LinklyAI/best-skills/main/data/latest/rankings/best-100.csv`
- MCP registry JSON API: `https://registry.modelcontextprotocol.io/v0/servers`
  (filtered query — skip cleanly if no relevant hits, which is expected most
  days).
- **`npx skills find` / `npx tessl search` are explicitly NOT run by
  `collect.sh`.** They execute arbitrary, unpinned npm code unattended, which
  contradicts `security.md`'s own rule. They're documented instead in
  [`ranking.md`](ranking.md) as commands the *human* can run interactively
  when evaluating one specific suggestion a brief surfaces — never scheduled,
  never run by an agent.

## Known-good delivery-surface candidate (not a data source, listed for the ranking step)

`jankeesvw/omarchy-notification-center` or `njpatel/omapager` — real,
installable Omarchy plugins (`omarchy plugin add <url> --enable`) that turn
the notification stream into a persistent, re-openable bar history. This is
exactly the kind of thing this radar's own ranking rubric would surface as a
top-3 candidate for the very first real brief — listed here as a known-good,
already-verified option rather than force-installed as part of this build.
See `README.md`'s Delivery channels section.

## Prior art consulted as design reference (not dependencies)

- `varunyn/git-digest` (MIT, tiny) — state-file dedup pattern, read before
  writing the seen-tracking logic.
- `camilleroux/tech-digest` (MIT, 37 stars, ships as a Claude Code plugin) —
  zero-dependency RSS parsing pattern.

Neither is depended on directly (both too thin/unmaintained); both were
useful to read once, and that's now recorded here so a future session doesn't
have to re-find them.
