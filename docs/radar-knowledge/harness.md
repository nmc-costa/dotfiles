# Harness ecosystem — radar knowledge ledger

Durable "last verified" facts for `harness-radar`, maintained by a human
merging an approved `radar/harness-radar/<date>` branch. **This is a ledger,
not a changelog**: each fact has one entry, dated to when it was last
verified, and gets corrected/overwritten in place when a later radar run
finds it's changed. Check here before spending a fresh research pass
re-establishing something already answered. See
[`../../.agents/skills/researcher-radar/SKILL.md`](../../.agents/skills/researcher-radar/SKILL.md).

## Repo identities (canonical org matters — fork-spam is real, see below)

- **`herdr` (terminal/multiplexer for running agents):** canonical repo is
  `herdrdev/herdr` — confirmed real, ~40.6k stars, Rust. Last verified:
  2026-09-25. Several identically-described "agent multiplexer" repos under
  unrelated owners are copy/template spam, not the real project — verify the
  owning org before surfacing any `herdr`-named candidate.
- **`herdr`'s plugin marketplace, `herdr.dev/plugins`,** is itself an
  auto-index of the `herdr-plugin` GitHub topic (1,324 plugins as of this
  research pass) — diff that page/topic rather than re-scraping individual
  repos. Last verified: 2026-09-25.
- **DeepSeek Harness (`dsh`):** canonical repo is
  `deepseek-ai/deepseek-harness` — confirmed real, ~235k stars, still
  "developer preview." Last verified: 2026-09-25.
- **`dsh` plugin-ecosystem source of record:** `zoahdev/dsh-ecosystem`, a
  maintained "living map" of the `dsh-plugin` ecosystem with
  quality/verification badges — used instead of the raw `dsh-plugin` topic
  (16,000+ repos, far too noisy to scrape directly). Last verified:
  2026-09-25.
- **`dsh`'s plugin kernel is `cordiverse/cordis`**, a pre-existing,
  independent, generic plugin runtime (also powers the Koishi chatbot
  framework). A "portable to other harnesses" claim for a dsh plugin is real
  only when the plugin is Cordis-generic (touches only Cordis's
  context/event-bus primitives) — **not** automatically portable to Claude
  Code/OpenCode/Codex, which use unrelated plugin formats. Score a
  "make this dsh plugin agnostic" suggestion on Cordis-genericity, not assume
  portability by default. Last verified: 2026-09-25.

## Per-harness plugin-ecosystem sources (all confirmed to exist)

- **Codex CLI:** `RoggeOhta/awesome-codex-cli` + the official `openai/codex`
  discussion #16329. Last verified: 2026-09-25.
- **OpenCode:** `awesome-opencode/awesome-opencode`. Last verified:
  2026-09-25.
- **Gemini CLI:** the official Gemini CLI Extensions Gallery,
  `geminicli.com/extensions`. Last verified: 2026-09-25.
- **Copilot CLI:** GitHub's own "Agent Plugins" marketplaces —
  `copilot-plugins`, `awesome-copilot`. Last verified: 2026-09-25.
- **Claude Code:** its own marketplace, `claude-plugins-official` (already
  known/installed on this machine). Last verified: 2026-09-25.
- **Fork-spam caveat:** several near-identical "awesome-codex-plugins" forks
  all point at the same unofficial `codex-marketplace.com` aggregator — flag
  or drop a candidate that doesn't match the project's documented canonical
  org, don't trust star count alone. Last verified: 2026-09-25.

## Multi-agent / orchestration frameworks

- **Active, worth tracking directly (not via a thin "awesome" list):**
  `crewAIInc/crewAI`, `langchain-ai/langgraph`, `bytedance/deer-flow`,
  `microsoft/agent-framework`. Last verified: 2026-09-25.
- **`microsoft/agent-framework` is the real successor to both AutoGen and
  Semantic Kernel.** Microsoft has put `microsoft/autogen` itself into
  maintenance mode — **exclude `microsoft/autogen` as a live source**. Last
  verified: 2026-09-25.
- **`vivy-yi/awesome-agent-orchestration`** is too weak to depend on as a
  source (43 stars / 8 commits at research time) — excluded. Last verified:
  2026-09-25.
- **Also track two large adjacent harnesses** despite not being in the
  original request: **OpenClaw** (~390k stars) and **Hermes Agent** (Nous
  Research, ~200k+ stars). Last verified: 2026-09-25.
- **Close near-misses, complementary not duplicative:**
  `duanyytop/agents-radar` (general AI-industry news — different scope; this
  is why this radar is named `harness-radar` and not the user's original
  suggestion `agents-radar`, which collides with this real, active, public
  project) and `ucsandman/agent-infra-digest` (small, close in spirit —
  worth reading as a design reference, not a dependency). Last verified:
  2026-09-25.

## Benchmark leaderboards

- **Primary: SWE-bench** (`swebench.com`), both the original and
  **SWE-bench Verified** — Verified is the more trustworthy ranking signal
  since the original set has known label-noise issues. Last verified:
  2026-09-25.
- **Terminal-Bench** (agentic terminal-use benchmark) and **LiveCodeBench**
  (contamination-resistant coding benchmark) — included if genuinely still
  active/maintained; **re-verify each at implementation/run time**, don't
  assume liveness from this entry alone. Last verified: 2026-09-25.
- **A benchmark-rank change is a strong signal, never sufficient alone** —
  `ranking.md` combines it with the security-gate → Impact/Quality → fit →
  prune-bias rubric, not a replacement for it. Last verified: 2026-09-25.

## Skill/plugin/MCP ecosystem aggregators (moved here from `omarchy-radar`'s
## original scope — fit the AI-agent-tooling domain, not Omarchy)

- **`LinklyAI/best-skills`** daily CSV
  (`raw.githubusercontent.com/LinklyAI/best-skills/main/data/latest/rankings/best-100.csv`).
  Last verified: 2026-09-25.
- **MCP registry JSON API** (`registry.modelcontextprotocol.io/v0/servers`).
  Last verified: 2026-09-25.
- **`npx skills find` / `npx tessl search` stay interactive-only** —
  documented in `ranking.md` for a human to run when evaluating one specific
  suggestion; never run unattended (executes arbitrary, unpinned npm code,
  which would contradict `security.md`'s own rule). Last verified:
  2026-09-25.
