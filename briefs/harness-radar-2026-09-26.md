# harness-radar brief — 2026-09-26

## Source status

| Source | Status | Today |
|---|---|---|
| herdr plugin marketplace (`herdr-plugin` topic diff) | ok | 4 new/updated items |
| Copilot CLI plugin marketplaces (`copilot-plugins` / `awesome-copilot`) | ok | 1 new/updated item |
| All other sources (herdr releases, dsh + dsh-ecosystem, Codex CLI, OpenCode, Gemini CLI, Claude Code marketplace, orchestration frameworks, benchmark leaderboards, best-skills CSV, MCP registry) | no items in today's inbox | per-source ok/error lives in `status.json`, which is outside this step's read allowlist — nothing in the data provided indicated a source error, but a sustained quiet streak should be confirmed there, not assumed (see `security.md` rule 11) |

Environment note: reads of `~/.claude/plugins/` and `~/.config/opencode/` were blocked by this run's sandbox, so fit was scored against what the dotfiles repo itself documents (Claude Code primary; herdr present via its agent-state hook referenced in `AGENTS.md`; Copilot/Gemini/Codex CLI configs maintained). Fit lines below reflect that reduced visibility.

## Top suggestions (1 — prune-bias: only one item genuinely cleared the bar)

### 1. Evaluate `ZingerLittleBee/Heeler` — dominant new entry in the herdr-plugin space

- **What changed:** a herdr-plugin-topic repo updated 2026-09-25 with 410 stars — roughly two orders of magnitude above every other item in today's marketplace diff (its nearest peer: 3).
- **Why it clears the rubric:** security gate passes (inert index entry; suggestion is evaluate-only, nothing automated). §2 canonical-org check: it is a third-party plugin, not a `herdr`-project impersonator, so the lookalike table doesn't disqualify it. Trend signal is strong and relative: 410★ against a 0–3★ field. Fit is real: herdr is in use on this machine (its agent-state hook is referenced in `AGENTS.md`), so a popular herdr-plugin entry is relevant in a way it wouldn't be on a herdr-less machine. No benchmark data in today's inbox, so §3 contributes nothing either way.
- **Caveats (honest gaps):** Quality could not be independently verified this run (no live fetch of the repo's CI/maintenance state from this step; the 410★ + fresh update is the whole evidence base), and the plugin's purpose is not stated in the index metadata — review before trusting the star count.
- **Manual step (never automated, per `security.md`):** human reviews `https://github.com/ZingerLittleBee/Heeler`, then — if it earns it — installs it via herdr's own plugin command themselves.
- **Diff:** none — this suggestion touches no file `dotfiles` tracks (herdr plugin state lives outside the repo), so no proposal file and no diff placeholder this run.

## Scored and pruned (all below failed Impact/installs-trend and fit, not just the count)

- `cobanov/herdrchat` (3★) — **§2 flag, not silent trust:** `herdr`-named repo under an unrelated owner, the exact shape the ledger's fork-spam note warns about; identity unverifiable from this step. 3★, no fit evidence.
- `aneym/unblock` (0★) — zero trend signal, unknown purpose, no fit evidence.
- `fuad-daoud/relevo` (1★) — same shape as above.
- `marsilitonga-ifb/claude-shopifyql-workbench` (0★) — single-owner, ShopifyQL-niche; no Shopify context on this machine. Note: a `claude-`-prefixed repo surfaced in the Copilot CLI category — likely a cross-tagged topic entry; flagged as a data-quality observation, not scored up.

## Tips

No interactive-only command applies today: `npx skills find` / `npx tessl search` search the skills ecosystem, and today's single suggestion is a `herdr-plugin`-topic item — neither tool would add signal for it. (Reminder: both remain human-interactive-only, never automated.)
