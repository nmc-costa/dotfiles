# harness-radar — sources

Every source here was concretely verified during a dedicated web-research
pass (repo identity, star count, activity, canonical org) rather than
guessed from memory; the benchmark-leaderboard source below was re-verified
again on 2026-09-25 specifically because it was added after the rest of this
plan was approved. **Every source is a plain data fetch (`curl`/`gh api`,
or a GraphQL read for Discussions) — nothing here ever executes third-party
code.** See [`security.md`](security.md) for why that line is load-bearing,
not just a style choice.

Shares `radar-common`'s exact state/output/flock shape with `omarchy-radar`
(atomic tmp-then-`mv` writes, `seen.json.pending` → `seen.json` promotion
only after a successful commit, per-source `status.json` ok/error tracking,
`inbox/<date>.json` output) — not re-described here. This radar's own paths:

- `~/.local/state/harness-radar/seen.json`
- `~/.local/state/harness-radar/status.json`
- `~/.local/state/harness-radar/snapshots/`
- `~/.local/state/harness-radar/inbox/<date>.json`

If a source's consecutive-failure count in `status.json` crosses the shared
threshold (matching `omarchy-radar`'s, e.g. 3), it gets its own warning
notification instead of silently looking like "nothing new" — see
`radar-common`.

## Sources

### 1. `herdr` itself

- **Repo**: `herdrdev/herdr` (confirmed canonical — ~40.6k stars, Rust, the
  real terminal/multiplexer-for-agents project). Several identically
  described "agent multiplexer" repos under unrelated owners are copy/template
  spam, not the real thing — see `ranking.md`'s canonical-org note before ever
  substituting one of those in.
- **Fetch**: `gh api repos/herdrdev/herdr/releases` and
  `gh api repos/herdrdev/herdr/commits` — new releases/commits since last
  seen tag/SHA.

### 2. herdr's plugin marketplace

- **Source**: `herdr.dev/plugins`, itself an auto-generated index of the
  `herdr-plugin` GitHub topic (1,324 plugins as of research — far too many to
  diff individually).
- **Fetch**: diff the topic listing as a whole against the last snapshot —
  either `gh api search/repositories?q=topic:herdr-plugin&sort=updated` (new
  repos/updates since last run) or a fetch of the `herdr.dev/plugins` page
  itself if it exposes a lighter listing; verify at implementation time which
  is cheaper/more stable and record the choice in
  `docs/radar-knowledge/harness.md`. Either way, this is a diff of an index,
  never a per-plugin content fetch.

### 3. DeepSeek Harness (`dsh`)

- **Repo**: `deepseek-ai/deepseek-harness` (confirmed real, ~235k stars,
  still labeled "developer preview").
- **Fetch**: `gh api repos/deepseek-ai/deepseek-harness/releases`.
- **Plugin ecosystem source**: `zoahdev/dsh-ecosystem` — a maintained
  "living map" of the `dsh-plugin` ecosystem with quality/verification
  badges, used **instead of** the raw `dsh-plugin` GitHub topic (16,000+
  repos, far too noisy to scrape directly). Fetch: diff its README/index
  against the last snapshot.
- **Portability caveat**: see `ranking.md`'s Cordis-scope note before ever
  suggesting a `dsh` plugin as "portable to other harnesses."

### 4. Codex CLI plugin ecosystem

- **`RoggeOhta/awesome-codex-cli`** — diff its README against the last
  snapshot.
- **`openai/codex` discussion #16329** — the official discussion thread
  covering Codex CLI's plugin/extension surface. REST has no Discussions
  endpoint; fetch via `gh api graphql` (confirmed the current `repo`/`read:org`
  token scopes are sufficient for reading Discussions on a public repo, no
  new scope needed) — diff new comments since last seen comment id.

### 5. OpenCode plugin ecosystem

- **`awesome-opencode/awesome-opencode`** — diff its README against the
  last snapshot.

### 6. Gemini CLI plugin ecosystem

- **Official Gemini CLI Extensions Gallery**, `geminicli.com/extensions`.
  Fetch the page, verify it's actually the gallery (not an HTML error/captive
  page that happened to return 200 — same well-formedness check
  `omarchy-radar` applies to its RSS feed) before diffing against the last
  snapshot.

### 7. Copilot CLI plugin ecosystem

- GitHub's own **Copilot CLI "Agent Plugins" marketplaces**:
  `copilot-plugins` and `awesome-copilot`. Diff each README/index against
  its last snapshot.

### 8. Claude Code's own marketplace

- `claude-plugins-official` — already known/installed on this machine.
  Confirm its exact backing repo/endpoint against this machine's actual
  plugin-marketplace configuration at implementation time (don't assume a
  slug from memory here), and record the confirmed identity in
  `docs/radar-knowledge/harness.md` once pinned.

### 9. Multi-agent / orchestration frameworks

Tracked as named repos' releases directly, not via a thin community
"awesome" list (the one candidate found, `vivy-yi/awesome-agent-orchestration`,
is only 43 stars/8 commits — too weak to depend on):

- `gh api repos/crewAIInc/crewAI/releases`
- `gh api repos/langchain-ai/langgraph/releases`
- `gh api repos/bytedance/deer-flow/releases`
- `gh api repos/microsoft/agent-framework/releases` — the real successor to
  both AutoGen and Semantic Kernel; `microsoft/autogen` itself is in
  maintenance mode and is explicitly **excluded** as a live source.
- `gh api repos/openclaw/openclaw/releases` — **OpenClaw** (~390k stars).
  Canonical org confirmed 2026-09-25 (`github.com/openclaw/openclaw`); like
  `herdr`/`dsh`, this name attracts a large amount of unrelated
  community/fork content (setup wizards, agent-template packs, unofficial
  harnesses built on top of it) that are not this source and must not be
  substituted in.
- `gh api repos/NousResearch/hermes-agent/releases` — **Hermes Agent**
  (Nous Research, ~200k+ stars). Canonical org confirmed 2026-09-25
  (`github.com/NousResearch/hermes-agent`); same fork/community-content
  caution as OpenClaw applies (e.g. independent "awesome-hermes-agent"
  directories exist and are reference material at most, never this source).

### 10. Benchmark leaderboards (required source, added post-approval)

Tracks which harness/model/instruction-set combination currently performs
best on real coding-agent benchmarks — a complement to, never a replacement
for, the security-gate → Impact/Quality → fit → prune-bias rubric in
`ranking.md`. Re-verified live on 2026-09-25 (all three below were active
that day; re-check periodically via `docs/radar-knowledge/harness.md` rather
than assuming this list is frozen):

- **SWE-bench / SWE-bench Verified** (`swebench.com`, `swebench.com/verified.html`)
  — **primary**, required. Verified is preferred for ranking over the raw
  SWE-bench set, since the original set has known label-noise issues that
  make raw rankings less reliable. **Caveat recorded 2026-09-25**: OpenAI
  stopped reporting Verified scores in early 2026 and now points to a newer
  "SWE-bench Pro" instead, and an OpenAI audit found a large fraction of the
  hardest unsolved Verified problems have flawed test cases. Verified stays
  the required source here per the approved plan (it's still live, still the
  most widely reported), but `ranking.md` treats a Verified-only rank claim
  as one input, not gospel — and SWE-bench Pro is worth a follow-up check in
  `docs/radar-knowledge/harness.md` as it matures.
- **Terminal-Bench** — verified active 2026-09-25. Canonical repo is
  `harbor-framework/terminal-bench` (the project migrated from its original
  home at `laude-institute/terminal-bench` to the `harbor-framework` org
  alongside the newer Harbor evaluation framework; `laude-institute` remains
  a legitimate related org, not a fork-spam concern, but the leaderboard and
  active repo now live under `harbor-framework`). Fetch/diff the public
  leaderboard, same "surface a rank change or new top entry" pattern as
  every other source here — not raw scraping of every submission.
- **LiveCodeBench** — verified active 2026-09-25
  (`livecodebench.github.io/leaderboard.html`, repo
  `LiveCodeBench/LiveCodeBench`), a contamination-resistant coding benchmark
  with regular updates. Same diff-the-leaderboard pattern.

Fetch method for all three: diff the public leaderboard page or its backing
JSON/data file against the last snapshot in `snapshots/`; confirm the exact
backing endpoint for each (HTML page vs. a discoverable JSON data file) at
implementation time and record the choice in `docs/radar-knowledge/harness.md`,
the same "verify, then write it down once" treatment `omarchy-radar` gives
its RSS feed.

### 11. Skill/plugin/MCP ecosystem aggregators

Moved here from `omarchy-radar`'s original draft, since this scope fits the
AI-agent-tooling radar much better:

- `LinklyAI/best-skills` daily CSV:
  `https://raw.githubusercontent.com/LinklyAI/best-skills/main/data/latest/rankings/best-100.csv`
- MCP registry JSON API: `https://registry.modelcontextprotocol.io/v0/servers`
  (filtered query — skip cleanly if no relevant hits, expected most days).

**`npx skills find` and `npx tessl search` are explicitly not part of this
list and never run inside `collect.sh`.** They execute arbitrary, unpinned
npm code, which directly contradicts `security.md`'s "never install or run
anything collected" rule even though the *output* would be useful signal.
They're documented in `ranking.md` instead as commands the human can run
interactively when evaluating one specific suggestion the brief surfaces —
see `security.md` for the exact rule.

## Design references (not dependencies)

- `duanyytop/agents-radar` — general AI industry news, different scope; this
  radar was named `harness-radar` (not `agents-radar`) specifically to avoid
  colliding with this real, active, public project.
- `ucsandman/agent-infra-digest` — small, close in spirit; worth reading as a
  design reference, same treatment `omarchy-news-radar` got in
  `omarchy-radar`'s `sources.md`, not adopted as a dependency.
