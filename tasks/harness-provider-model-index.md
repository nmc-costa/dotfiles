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
| 3 | Antigravity CLI (`agy`) / Gemini CLI (`gemini`) | Yes — `agy` 1.2.9 at `~/.local/bin/agy`, `gemini` 0.60.0 via mise. Dispatchable by `tasks/dispatch.py` (`PROVIDER_BINARIES["agy"]`), same as Claude/Copilot. | **Unconfirmed** — no entry under `.agents/providers/registry/`, and `.agents/harnesses/antigravity.md` / `gemini.md` both flag their own plumbing as only partially verified. Confirm your actual Google/Gemini plan before relying on it daily. | Not established from here — `.agents/harnesses/gemini.md` explicitly warns an earlier integration guide invented a fictional Gemini API setup. Don't trust a specific model name until re-verified against the CLI's own config/`--model` output. | Large-context scaffolding or codebase surveys once cost and plumbing are confirmed (see "Phase-routing guidance" below). Wired into this repo's own dispatch tool, unlike rows 7/8 below, but treat as unverified until the Gaps section closes. |
| 4 | OpenCode (`opencode`) | Yes (mise, v1.18.31) | Free if pointed at a local Ollama model; **needs a paid key** if pointed at a cloud model via OpenRouter — don't, per the constraint above, unless a specific cloud model is genuinely required | A local Ollama model, once one is actually pulled (none are pulled on this machine yet — `ollama list` errors, daemon isn't running) | Local/offline coding once Ollama has a model pulled and running. Not yet usable here as shipped — needs setup first (see Gaps). |
| 5 | Pi (`pi`) | Yes (mise, v0.85.1) | Free, 100% local (Ollama/LM Studio) | A local quantized coder model, once pulled | Same local/offline niche as OpenCode above — also blocked on Ollama actually having a model today. |
| 6 | `dtx-glm53-flash` (via LiteLLM proxy, reachable from `claude-code`/`codex`/`crush`/`gemini-cli`/`opencode`/`antigravity-cli` adapters) | Registered (`.agents/providers/registry/dtx-glm53-flash.json`) | **Unconfirmed** — DTx Colab's own hosted endpoint; whether it's metered against the owner personally isn't established here. Confirm before relying on it daily. | `zai-org/GLM-5.3-Flash` (reasoning, 262k context) | Once cost is confirmed: a reasoning-heavy task where Claude Pro's usage limits are a concern. Until confirmed, don't default to it. |
| 7 | `omp` | Yes (`~/.local/bin/omp`) | Depends which backend it's pointed at — not itself a model provider, routes to others | N/A — inherits whichever harness/provider it wraps | Not enough here to place it — no docs found in this repo describing its actual setup. Needs its own verification pass before it earns a ranked slot. |
| 8 | DeepSeek Harness (`dsh`) | Binary installed (mise, `@deepseek-ai/dsh` 0.1.5-rc.1) | N/A — integration unverified | N/A | **Do not use for real work yet.** `.agents/harnesses/deepskee.md` states, verbatim: "Status: template → needs verification." The binary exists; nothing confirms it's wired into this workspace's skills/instructions. |

**Explicitly not installed / not configured on this machine — don't
recommend spending on these:** `aider` (no binary found anywhere), a
standalone DeepSeek API key, an Anthropic API key separate from the Claude
Pro plan, OpenRouter credits. These appeared in an earlier draft (see
Appendix) but aren't real here.

### Real Copilot/agy model lists (live, 2026-09-25 — via `tasks/orchestra.py`)

`tasks/orchestra.py`'s `validate_model` reads these live from the CLI
itself on every run (cached per process, never hardcoded), so this list
is a snapshot for humans, not the source of truth:

- **Copilot CLI** (`copilot help config`): `gpt-5-mini`, `gpt-5.3-codex`,
  `gpt-5.4`, `gpt-5.4-mini`, `gpt-5.5`, `gpt-5.6-luna`, `gpt-5.6-sol`,
  `gpt-5.6-terra`, `gpt-6-astra`. There is no plain `gpt-5`.
- **agy** (`agy models`): `claude-opus-4-6-thinking`,
  `claude-sonnet-4-6`, `gemini-3.1-pro-high`, `gemini-3.1-pro-low`,
  `gemini-3.6-flash-{high,low,medium}`, `gemini-3.7-flash-{high,low,medium}`,
  `gemini-3.8-flash-{high,low,medium}`.

`agent-deck` (row-3-adjacent L2 decision in `tasks/README.md`) is now
used in practice, not just evaluated — `tasks/orchestra.py launch` shells
out to `agent-deck launch` for every harness, including `agy` (unverified
support, see `tasks/plans/cross-harness-orchestra.md` §Risks).

## Phase-routing guidance (folded in from a separate Antigravity-authored draft)

A second document — `.agents/instructions/workspace-config/harness-matrix.instructions.md`
on branch `antigravity/harness-model-matrix` — was drafted independently by
the Antigravity harness to answer a related but distinct question: not
"which harness/model is available and paid-for" (this file's job above),
but "which harness fits which `tasks/` Kanban phase." Per the owner's
2026-09-23 decision, that content is folded in here as one canonical
document instead of being kept as two diverging files. The routing logic
below is preserved from that draft; the specific model names it used
(`Claude 3.7 Sonnet`, `o3-mini`, `GPT-4o-mini`) didn't match verified state
and have been corrected against the Ranked index above or removed where
nothing here confirms them. **Don't merge
`origin/antigravity/harness-model-matrix`'s copy of that instructions file
separately** — that would reintroduce the divergence this section closes;
`.agents/instructions/workspace-config/harness-matrix.instructions.md` now
just points back here.

### Recommended harness by task phase

| Phase | Cognitive profile | Recommended harness | Model (per Ranked index above) | Focus |
|---|---|---|---|---|
| `planning` | Deep multi-step reasoning, architectural decomposition | Claude Code (`claude`) | Sonnet 5 / Opus 5 | Technical design, task breakdown, boundary definition |
| `in_progress` — sensitive | Concurrency logic, CAS protocols, core multi-file refactors | Claude Code (`claude`) | Sonnet 5 | Critical algorithm implementation, core invariants |
| `in_progress` — scaffolding | Boilerplate, broad exploration, large-context ingestion | Antigravity CLI (`agy`) | Unconfirmed — see row 3 above; verify cost/plumbing before dispatching real work here | Rapid implementation once verified |
| `review` | Adversarial review, security/standards audit | Claude Code, clean session (no author context) | Sonnet 5 / Opus 5 | Unbiased critique |
| `validation` | Formal verification, edge-case probing, CAS validation (`--expect-last-event-id`) | Claude Code (`claude`) | Sonnet 5 | Regression testing, CAS gating enforcement |
| Git/maintenance hygiene | Mechanical merge conflicts, branch sync, formatting | Copilot CLI (`copilot`) | GitHub's current default — see row 2 above | Never spend a premium reasoning model on this, see guardrail below |

### Token-conservation guardrails

1. Claude Code is for `planning` and sensitive `in_progress`/`validation` work. If a session is about to do large-scale scaffolding or boilerplate, prefer handing off to Antigravity (`agy`) instead of spending Claude Pro usage on it — once Antigravity's plumbing/cost are confirmed (see Gaps).
2. **Scout & Striker:** use a large-context harness to survey a big codebase or log set and produce a short brief, then hand that brief — not the raw material — to Claude Code to write the actual patch.
3. Never spend a premium reasoning session resolving a mechanical git conflict or running a formatting pass — that's what Copilot CLI or a plain script is for.

### Inter-harness handoff (already built in this repo, not aspirational)

- Push-based handoff: `python3 tasks/dispatch.py --task-id <id> --provider <claude|copilot|agy> --launch` (confirmed in `tasks/dispatch.py`'s `PROVIDER_BINARIES`).
- Context isolation: hand off a synthetic brief via `tasks/brief.py --prompt-only --task-id <task-id>`, never a raw transcript.
- Worktree isolation: each task's implementation runs in its own git worktree, never shared across concurrent sessions — see `dotfiles-tsk-claim-protocol` (done) for the claim mechanism that enforces this.

## Per-machine hardware

- **`omarchy`** (this machine, verified 2026-09-23): Intel Iris Xe
  **integrated** graphics only (`lspci`) — no discrete GPU. 38GB total RAM
  (`free -h`). This is a CPU-only box for local inference: any local model
  (rows 4/5 above) needs to run on CPU via Ollama/LM Studio, favor a small
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
5. Antigravity CLI / Gemini CLI (row 3): actual plan/cost and exact model
   tier are unconfirmed — no `.agents/providers/registry/` entry exists for
   it, and its own harness docs (`.agents/harnesses/antigravity.md`,
   `gemini.md`) flag the integration as only partially verified. Don't
   dispatch real scaffolding work to it via the phase-routing table above
   until this closes.

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
