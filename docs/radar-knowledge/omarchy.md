# Omarchy — radar knowledge ledger

Durable "last verified" facts for `omarchy-radar`, maintained by a human
merging an approved `radar/omarchy-radar/<date>` branch. **This is a ledger,
not a changelog**: each fact has one entry, dated to when it was last
verified, and gets corrected/overwritten in place when a later radar run
finds it's changed — it never accumulates duplicate history for the same
fact. Check here before spending a fresh research pass re-establishing
something already answered. See
[`../../.agents/skills/researcher-radar/SKILL.md`](../../.agents/skills/researcher-radar/SKILL.md).

## Repo identity

- **Canonical repo:** `omacom/omarchy` (default branch `quattro`).
  Last verified: 2026-09-25. Source: GitHub API + the official
  `omarchy.org/manual` footer link.
- **`basecamp/omarchy` 301-redirects to `omacom/omarchy`** — not a separate
  fork to track. Last verified: 2026-09-25.
- **Plugin marketplace repo:** `omacom/omarchy-plugin-marketplace`.
  Last verified: 2026-09-25. `HANCORE-linux/...` also redirects here — not a
  separate source.
- **GitHub Discussion #9689** is about Google Antigravity support, **not**
  the `--prompt` flag — don't cite it for the launcher CLI. Last verified:
  2026-09-25.
- **GitHub Discussion #11029** is confirmed accurate; also add
  `~/.config/starship.toml` to its tracked-file list. Last verified:
  2026-09-25.

## Launcher surface

- **`omarchy-agent --help` is not a real invocation.** The real launcher
  surface is `omarchy agent prompt "<text>"`, which execs
  `omarchy-agent --prompt "<text>"`. Confirmed from
  `/usr/share/omarchy/bin/omarchy-agent` source and `omarchy.org/manual/ai/`.
  Last verified: 2026-09-25.
- **Its built-in `claude` launch command is `claude --permission-mode
  auto`** — too permissive/unrestricted for an unattended job; `omarchy-radar`
  invokes `claude -p` directly instead of going through `omarchy agent`. Last
  verified: 2026-09-25.
- **`omarchy update` deliberately has no changelog/"what's new" surface** —
  confirmed via the official manual. No duplication risk for `omarchy-radar`
  from this. Last verified: 2026-09-25.

## Aggregators and prior art

- **`mtolhuys/omarchy-news-radar`** (MIT, active,
  github.com/mtolhuys/omarchy-news-radar) is a real Omarchy desktop plugin
  whose Python collector already aggregates Omarchy GitHub releases + the
  official `omarchy.org/news` RSS + marketplace catalog diffs into a
  deduplicated `events.json`, publishing a public feed at
  `mtolhuijs.nl/news-radar/feed.xml`. This is `omarchy-radar`'s **primary**
  source for releases/marketplace/news (direct-GitHub-API is the fallback
  path). Last verified: 2026-09-25. Small/low-star project — treat as
  "exists and useful," not "guaranteed to stay up"; re-check liveness
  periodically.
- **The feed domain `mtolhuijs.nl` genuinely doesn't match the repo owner
  `mtolhuys`** — that's correct, not a typo to "fix" in `sources.md`. Last
  verified: 2026-09-25.
- **Feed format confirmed:** RSS 2.0, `<item><guid isPermaLink="false">evt_…
  </guid><title><link><description><pubDate>` — dedupe on `<guid>`. Last
  verified: 2026-09-25.
- **`last30days-skill` (`mvanhorn/last30days-skill`) is not installed on
  this machine.** `collect.sh` does not hard-depend on it; noted in
  `sources.md` as a future drop-in upgrade path, not a current blocker. Last
  verified: 2026-09-25.
- No tool combines GitHub Discussions + Reddit + HN + a dedup ledger for
  Omarchy in one package — bespoke collection code is genuinely needed for
  those three. `varunyn/git-digest` (state-file dedup pattern) and
  `camilleroux/tech-digest` (zero-dependency RSS parsing, ships as a Claude
  Code plugin) are useful reference implementations, not dependencies (both
  too thin/unmaintained to depend on directly). Last verified: 2026-09-25.

## Delivery-channel candidates (not built, just verified real)

- **`jankeesvw/omarchy-notification-center`** and **`njpatel/omapager`** are
  real, installable Omarchy plugins (`omarchy plugin add <url> --enable`)
  that turn the notification stream into a persistent, re-openable bar
  history — a day-one `omarchy-radar` brief-display candidate to surface in
  `sources.md`, not something to force-install as part of the build. Last
  verified: 2026-09-25.

## Local machine facts (re-verify per machine, not global truth)

- **No Hyprland/Omarchy dotfile is tracked/symlinked from `~/dotfiles` on
  this machine** — `~/.config/hypr/*.lua`, `~/.config/omarchy/shell.json`,
  `~/.config/omarchy/extensions/omarchy-menu.jsonc`, `~/.bashrc`,
  `foot.ini` are all plain, untracked files. A live-config suggestion
  therefore diffs against the real `~/.config` file directly (read-only,
  rendered inline in the brief), never applied and never committed — there
  is nothing tracked to commit a diff against. Last verified: 2026-09-25
  (this machine).
