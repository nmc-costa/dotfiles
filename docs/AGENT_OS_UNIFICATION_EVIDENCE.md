Phase 3 evidence map for [`docs/AGENT_OS_UNIFICATION_PLAN.md`](AGENT_OS_UNIFICATION_PLAN.md),
built from 6 parallel research subagents (Haiku 4.5), each answering one closed sub-question
with a citation (URL + access date, or an on-machine command + its output) and every finding
line tagged `[fact]` or `[inference]`. Cross-checked for conflicts before being handed to the
planner; no cross-researcher conflict required a tie-breaker round.

---

# Evidence map — dotfiles unification plan (Phase 3 output)

Confidence: HIGH = first-party doc or empirical on-machine verification, cross-checked.
MEDIUM = single credible source, not independently cross-checked. LOW = inference only.

## A — AGENTS.md standard & provider caching

- AGENTS.md is governed by the Agentic AI Foundation (AAIF) under the Linux Foundation;
  Anthropic is a Platinum member. Source: agents.md, linuxfoundation.org press release
  (2026-09-20). Confidence: HIGH.
- Precedence: nearest AGENTS.md wins, parent files are fallback for missing instructions;
  user's in-session prompt overrides all. Confidence: HIGH (two independent sources).
- Harness support, with version/date where found:
  - Claude Code: native since v2.1.277 (2026-09-18). HIGH (release notes, first-party).
  - GitHub Copilot: since 2025-08-28 (coding agent). HIGH (GitHub changelog).
  - Cursor: since v3.1.15 (2026-04-01). MEDIUM (third-party comparison article).
  - Codex, OpenCode: supported, exact version/date NOT found (flagged blocker by
    researcher, not fabricated). MEDIUM/LOW.
  - Gemini CLI, Aider: supported per multiple sources but no version/date pinned.
    LOW — treat as "supported, version unconfirmed."
- CORRECTION to original brief: Claude Code the *product* IS available on Bedrock,
  Vertex AI, and Azure AI Foundry. It is specifically the AGENTS.md-fallback feature
  that is absent on those three platforms, per the v2.1.277 release note itself
  ("not yet on Bedrock, Vertex or Foundry"). The brief's "Claude Code... ausente em
  Bedrock/Vertex/Foundry" is imprecise and should not be carried into the plan as-is.
  Confidence: HIGH.
- Prefix-based prompt caching, exact-prefix-match required, confirmed independently
  from each provider's own docs: Anthropic (cache_control breakpoints, cumulative
  hash), OpenAI (KV-state reuse, full prefix must match), Google Gemini (implicit,
  automatic, recommends common content first), DeepSeek (on-disk cache, prefix unit
  match, partial matches don't count). Confidence: HIGH — this directly justifies
  decision 4 (canonical AGENTS.md section ordering: put content shared across the
  most contexts first/most-stable-first, most-likely-to-change last).

## B — Omarchy Quattro (empirically verified ON THIS MACHINE, not just cited)

- `/usr/share/omarchy` is root:root 0755, owned by pkgs `omarchy 4.0.4-1` /
  `omarchy-settings 4.0.4-1`. `~/.config` is user-owned. Confidence: HIGH (local
  `ls -ld`/`stat`/`pacman -Qo`, cross-checked against the official manual page
  31-dotfiles.md which says the same in prose).
- `omarchy-plugin-validate` (read directly from `/usr/bin/omarchy-plugin-validate`,
  lines 111-116) rejects ANY symlink found anywhere inside a plugin folder
  (`.git` internals excluded). This is a hard CLI-level block, not just a convention.
  Confidence: HIGH (primary source: the actual shipped script).
- Quickshell 0.3.1-1 is the only shell package installed and actively running
  (`quickshell -n -p /usr/share/omarchy/shell`); none of Waybar/Walker/Mako/SwayOSD/
  hyprlock/hypridle/swaybg/polkit-gnome are installed. Matches PR #6231's own
  description verbatim. Confidence: HIGH.
- Hyprland 0.56.2, all config files in `~/.config/hypr/` are `.lua`. Confidence: HIGH.
- Official Omarchy dotfiles manual (omarchy.org/manual/dotfiles/, also mirrored at
  the quattro branch path given in the brief) states outright: don't touch
  `/usr/share/omarchy`; customize via `~/.config`; **theme/plugin trees under
  `~/.config/omarchy/*` should NOT be version-controlled at all** (multi-GB vendored
  source, owned/managed by Omarchy itself) — only files that have actually diverged
  from the shipped default belong in a dotfiles repo. Confidence: HIGH.
- CRITICAL RISK FINDING (from thread C, corroborates B): **Omarchy hashes default
  config files on upgrade and silently replaces any file that still matches a known
  default hash — which destroys a symlink sitting at that path.** Tracking an
  unmodified stock file in the dotfiles repo and symlinking it back in guarantees a
  broken link on the next Omarchy upgrade. Confidence: HIGH (cited from
  omarchy.org/manual/dotfiles/ directly). Practical implication: only ever track
  files that are genuinely customized/diverged from default — never mirror pristine
  Omarchy defaults into the repo, symlinked or not.
- "Dots" proposal (discussion #11029): open, PARTIALLY implemented — `mise dot
  track` and related CLI functionality (autosave history, diff, restore, age
  encryption, no-symlink tracking) already work today with mise 2026.9.9+; only the
  built-in Omarchy-menu UI layer is still pending. Author: "Omarchy would own the
  defaults and UX; I'd maintain the mise machinery." Confidence: HIGH.

## C — Dotfiles manager comparison (chezmoi / Stow / bare git / Nix home-manager)

| Criterion | chezmoi | GNU Stow | bare git | Nix home-manager |
|---|---|---|---|---|
| Per-machine templating | Native (`.tmpl`, `.chezmoi.hostname`, `include`) | None built-in | Branches only (coarse) | Native (per-host module dirs) |
| Secrets | Native age (also GPG/rage); `decrypt()` fn reusable across many template files; `.chezmoitemplates/` for shared snippets | None built-in (needs git-crypt addon) | None built-in (needs git-crypt addon) | `sops-nix` / `agenix` modules |
| Real-files-not-symlinks (the plugin constraint) | YES — default IS real files/copies; `chezmoilinked` marks the *exception* paths as symlinks | NO — symlinking is Stow's entire mechanism, no documented Linux copy mode | YES — checkout always produces real files, no symlink concept | YES — per-path `mode` override forces copy instead of symlink |

Confidence: HIGH for all rows (each backed by the tool's own docs, cross-checked
against 4 community repos' actual usage).

Community repos: 2 of 4 use Stow (wh01s17, Reyozaki) and both explicitly document
symlink-conflict pain requiring manual pre-cleanup; 1 uses bare git
(anmolsharma152); 1 (MayberryDT) is custom scripts, explicitly reference-only /
not turnkey. None of the 4 mention chezmoi. Confidence: HIGH (read directly from
each README).

Additional Stow-specific finding: `--no-folding` is required to avoid Stow
collapsing `~/.config/hypr` into a single symlinked directory (which breaks on
Omarchy upgrades the same way as the hash-replace risk above). Confidence: MEDIUM
(single third-party repo, but consistent with the HIGH-confidence upgrade-hash
finding from B).

## D — Agent-instruction sync tooling landscape

Two families:
- GENERATORS (write fresh files, no symlinks): rulesync (50+ harnesses, treats
  AGENTS.md as a real discovery-order format alongside CONTEXT.md/GEMINI.md),
  aiconfigsync (12 harnesses, canonical source `.claude/rules/`, generates with
  regen-marker headers). Confidence: HIGH (both read from primary repo/PyPI docs).
- SYMLINKERS (symlink `.agents/`/`~/.agents/` outward): agent-sync (9 harnesses,
  calls itself a "behavior compiler," merges into AGENTS.md/GEMINI.md), sync-agents
  (4 harnesses, `.agents/` + `sources.yaml`/`sources.lock`, generates AGENTS.md
  symlinked to CLAUDE.md), skills-sync (4 harnesses, `~/.agents/skills` symlinked
  out per-tool, includes dry-run/backup/stale-symlink cleanup, a launchd job every
  5 min).
- KEY GAP, explicitly verified absent in all 3 symlink-based tools' docs: **none of
  them document how to handle a destination directory a harness itself writes live
  runtime state into** (sessions, credentials, logs) — exactly the problem this
  repo's own `sync.sh` already solved by using real copies for `~/.claude`/
  `~/.agents` instead of directory symlinks. Confidence: HIGH (explicit absence
  confirmed by the researcher reading each tool's docs directly, not just "didn't
  mention it").

## E — mise as machine orchestrator

- `jdx/mise` discussion #12709 ("Idea", open, posted 2026-09-02): proposes turning
  `~/.config/mise/config.toml` into a full machine-state file (packages, services,
  dotfiles, dev tools) reproducible via `mise bootstrap`. Confidence: HIGH.
- Omarchy discussion #11029 ("Dots"): mise's role there is explicitly BEYOND
  version management — full dotfiles orchestration (git-based history, no
  symlinking, `mise dot rollback`, age-encrypted tracking, cross-machine sync).
  Both threads open/active as of 2026-09-20. Confidence: HIGH.
- Shipped today (not proposed): `mise bootstrap` is one of mise's 4 core listed
  features — OS packages (brew/apt/dnf/pacman/apk/mas/winget), dotfiles (symlink,
  copy, OR template), repos, services, macOS defaults. Confidence: HIGH
  (mise.jdx.dev, first-party).

## F — Secrets injection prior art

- chezmoi+age: `decrypt()` template function + `.chezmoitemplates/` mechanically
  supports referencing ONE encrypted source across MANY destination template
  files — the mechanism for "scale to many destinations" exists in the product.
  However, no vendor doc or case study was found explicitly recommending/validating
  this at the scale of "OS config + many separate harness config files" — that's an
  honest documentation gap, not a product limitation. Confidence: MEDIUM (mechanism
  HIGH, "recommended at this scale" UNCONFIRMED).
- sops: encrypts leaf values, preserves key names in cleartext; `sopsFiles`/
  `sopsFile` (via sops-nix) supports sharing one secret set across multiple
  files/configs. "Destination rule object" section is explicitly marked
  "Not yet documented" in SOPS's own reference. Confidence: MEDIUM.
- pass: retrieval-only, zero templating/injection — would need chezmoi/SOPS/custom
  scripting on top to actually distribute into multiple files. Confidence: HIGH.
- 1Password CLI `op inject`: real, documented scaling constraints — all-or-nothing
  failure per invocation, ~1s latency per call, personal tier rate limit 1000
  req/24h (~2 requests per invocation) — multi-file injection means one invocation
  per destination file, so this degrades badly at scale. Confidence: HIGH (numbers
  from a specific field-experience blog post, MEDIUM source reliability, but
  consistent with 1Password's own documented all-or-nothing behavior which is
  HIGH/first-party).
- Plain `.env` + `.gitignore`: well-documented baseline failure modes — gitignore
  doesn't un-track an already-committed file, exposure requires full history
  rewrite + credential rotation, zero encryption at rest, zero audit trail.
  Confidence: HIGH.

## Discarded / downgraded findings
- Thread C's inference "Stow users achieve per-machine variation through modular
  package organization" — kept as LOW confidence context only, not load-bearing
  for any decision (Stow is already ruled out on the harder real-files constraint).
- No claim was found unsupported enough to discard outright; all researcher
  [inference] lines were grounded in cited [fact] lines from the same report.
