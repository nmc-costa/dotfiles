# Harness × provider × model index

A ranked reference for which CLI harness + model to reach for on a given
machine, kept as a living doc (not a one-time design record like
`tasks/plans/*.md`) — `tasks/task-brief` (once
`dotfiles-tsk-task-brief-assistant` lands) reads this to suggest an
approach for a task. Verified against real machine state, not assumed —
see "Method" below before trusting a row you haven't re-checked yourself.

**Hard constraint, always apply first:** the owner already pays for
**Claude Pro** (used via Claude Code) and **GitHub Copilot Pro** (used via
the `copilot` CLI). Don't recommend a new metered API key (a separate
Anthropic API key, a DeepSeek API key, OpenRouter credits, ...) when one of
these two already covers the job — only reach past them when the task
genuinely needs something they don't do (fully offline, a specific model
neither plan offers, etc).

## Method

Each row was checked directly on the machine named, not copied from
elsewhere: `mise ls` / `which <bin>` for what's installed, `.agents/
providers/registry/*.json` + `.agents/providers/harnesses/*.json` for
which custom model providers are actually wired up, `.agents/harnesses/
*.md` for each harness's documented integration status,
`tasks/dispatch.py`'s `PROVIDER_BINARIES` for which harnesses this repo's
own task-dispatch tool can launch. Re-run the same checks before trusting
a row on a machine not listed here, or after enough time has passed that
installs may have changed.

## Ranked index (machine: `omarchy`, verified 2026-09-23)

| # | Harness (command) | Installed here? | Cost | Model | When to use |
|---|---|---|---|---|---|
| 1 | Claude Code (`claude`) | Yes (this session) | **Already paid** — Claude Pro subscription | Sonnet 5 / Opus 5 per `/config` | Default for anything non-trivial: multi-file changes, planning, this repo's own `tasks/` orchestration. Dispatchable by `tasks/dispatch.py`. |
| 2 | Copilot CLI (`copilot`) | Yes | **Already paid** — Copilot Pro subscription | GitHub's current default (check `copilot` itself, not `gh copilot` — no `gh copilot` extension is installed here, this is the standalone CLI) | Quick terminal lookups: syntax, regex, one-off commands — the "google of the terminal" case from the owner's own framing, without touching a metered key. Dispatchable by `tasks/dispatch.py`. |
| 3 | OpenCode (`opencode`) | Yes (mise, v1.18.31) | Free if pointed at a local Ollama model; **needs a paid key** if pointed at a cloud model via OpenRouter — don't, per the constraint above, unless a specific cloud model is genuinely required | A local Ollama model, once one is actually pulled (none are pulled on this machine yet — `ollama list` errors, daemon isn't running) | Local/offline coding once Ollama has a model pulled and running. Not yet usable here as shipped — needs setup first (see Gaps). |
| 4 | Pi (`pi`) | Yes (mise, v0.85.1) | Free, 100% local (Ollama/LM Studio) | A local quantized coder model, once pulled | Same local/offline niche as OpenCode above — also blocked on Ollama actually having a model today. |
| 5 | `dtx-glm53-flash` (via LiteLLM proxy, reachable from `claude-code`/`codex`/`crush`/`gemini-cli`/`opencode`/`antigravity-cli` adapters) | Registered (`.agents/providers/registry/dtx-glm53-flash.json`) | **Unconfirmed** — DTx Colab's own hosted endpoint; whether it's metered against the owner personally isn't established here. Confirm before relying on it daily. | `zai-org/GLM-5.3-Flash` (reasoning, 262k context) | Once cost is confirmed: a reasoning-heavy task where Claude Pro's usage limits are a concern. Until confirmed, don't default to it. |
| 6 | `omp` | Yes (`~/.local/bin/omp`) | Depends which backend it's pointed at — not itself a model provider, routes to others | N/A — inherits whichever harness/provider it wraps | Not enough here to place it — no docs found in this repo describing its actual setup. Needs its own verification pass before it earns a ranked slot. |
| 7 | DeepSeek Harness (`dsh`) | Binary installed (mise, `@deepseek-ai/dsh` 0.1.5-rc.1) | N/A — integration unverified | N/A | **Do not use for real work yet.** `.agents/harnesses/deepskee.md` states, verbatim: "Status: template → needs verification." The binary exists; nothing confirms it's wired into this workspace's skills/instructions. |

**Explicitly not installed / not configured on this machine — don't
recommend spending on these:** `aider` (no binary found anywhere), a
standalone DeepSeek API key, an Anthropic API key separate from the Claude
Pro plan, OpenRouter credits. These appeared in an earlier draft (see
Appendix) but aren't real here.

## Per-machine hardware

- **`omarchy`** (this machine, verified 2026-09-23): Intel Iris Xe
  **integrated** graphics only (`lspci`) — no discrete GPU. 38GB total RAM
  (`free -h`). This is a CPU-only box for local inference: any local model
  (rows 3/4 above) needs to run on CPU via Ollama/LM Studio, favor a small
  quantized model (7B class, Q4) over anything larger, and expect it to be
  slower than a GPU box. This matches the profile an earlier draft (see
  Appendix) called "Lenovo E14" — **not** the "RTX 3070 Ti 8GB" desktop
  from that same draft, which is a different, unverified machine.
- **RTX 3070 Ti desktop** (referenced in the owner's draft, unverified
  from here): before trusting the 8GB VRAM figure or any GPU-accelerated
  local-model recommendation for it, run this same Method section's checks
  (`nvidia-smi --query-gpu=name,memory.total --format=csv,noheader`,
  `mise ls`, `ollama list`) directly on that machine and update this
  section with a real row.

## Gaps to close before this index is fully actionable

1. No Ollama model is pulled on `omarchy` yet — rows 3/4 above are
   currently theoretical here. Pulling one (e.g. a 7B Q4 coder model) is a
   separate, explicit action, not assumed done by this doc.
2. `omp`'s actual setup/backend isn't documented anywhere in this repo —
   needs a short verification pass (what does it wrap, what does it cost)
   before it can be ranked with confidence.
3. The `dtx-glm53-flash` endpoint's real cost to the owner is unconfirmed
   — resolve this before treating it as a safe default for anything.
4. The RTX 3070 Ti machine's row is unverified from here (see above).

## Appendix: owner's original draft (unverified / wrong-machine, kept for reference only)

The owner pasted a "Tabela Mestre Unificada" ranking `opencode`,
`gh copilot`, `pi`, `dsh web`, `aider`, `omp`, and `claude` for a machine
described as having an "RTX 3070 Ti 8GB" desktop and a "Lenovo E14 (40GB
RAM, sem GPU)" laptop, recommending model choices including DeepSeek-V3
via cloud API, GPT-5 mini, Qwen 2.5 Coder variants, Claude 3.5 Sonnet via
a raw Anthropic API key (for `aider`), GLM 5.3 Flash, and "Anthropic Fable
5.1" described as "muito alto" cost via native API. Kept here verbatim in
spirit for traceability, but **not used as this index's source of truth**:
it assumes hardware not present on `omarchy` (no discrete GPU here), and
several of its provider/API choices (a separate DeepSeek API key, an
Anthropic API key outside the Claude Pro plan, OpenRouter) directly
conflict with the owner's own stated constraint of not spending beyond the
Claude Pro / Copilot Pro subscriptions already in place. Any future update
to this index should re-derive from the Method section above, not from
this appendix.
