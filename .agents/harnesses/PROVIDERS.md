# 🔌 Provider Harnesses (custom models, not instructions)

**Status:** Active
**Not to be confused with:** the other files in this directory
(`claude-code.md`, `gemini.md`, `openai.md`, ...), which are about how a harness
loads *instructions/skills* (`.agents/skills/`, `CLAUDE.md`, etc). This file is
about the opposite direction: how a harness gets access to a *custom model
provider* — an OpenAI-compatible endpoint you point it at, like
`https://glm53-flash.dtx-colab.com/v1`.

---

## The tool: `dtx-providers-tui`

```bash
dtx-providers-tui                          # interactive menu (gum)
dtx-providers-tui status                   # which provider is wired into which harness
dtx-providers-tui add-provider             # register a new custom model provider
dtx-providers-tui add-harness              # register a new harness (writes a TEMPLATE adapter)
dtx-providers-tui apply  <harness> <provider>
dtx-providers-tui remove <harness> <provider>
```

Also reachable from the Omarchy menu: **AI → Harnesses & Providers**
(`~/.config/omarchy/extensions/omarchy-menu.jsonc`).

Source lives at `.agents/providers/` in this repo and is synced like every
other `.agents/` subdir (`./sync.sh`), which also symlinks the TUI itself to
`~/.local/bin/dtx-providers-tui`.

## Layout

```
.agents/providers/
├── registry/<provider-id>.json   # baseURL, models, apiKeyEnvVar — NO secret. Git-tracked.
├── harnesses/<harness-id>.json   # which adapter handles this harness, and its mode
├── adapters/<harness-id>.sh      # apply/remove for exactly one harness's native format
└── proxy/                        # shared LiteLLM proxy (see "Proxy-mode harnesses" below)
```

The actual secret (API key) is never in `registry/`. It's encrypted with the
same `chezmoi` + `age` setup already used for `.vscode/settings.json` in this
repo — see `docs/SECRETS.md`, same identity/recipient, same
"decrypted output lives inside `~/dotfiles/`, gitignored, symlinked into
`$HOME`" pattern (`~/.dtx-providers` → `~/dotfiles/.dtx-providers`).

## Per-harness reality (verified 2026-09-17, not assumed)

| Harness | Mode | How | Verified against |
|---|---|---|---|
| **opencode** | native | `apiKey` field in `opencode.json` supports `{env:VAR}` interpolation — the literal key is never written | opencode.ai/docs/providers |
| **Crush** | native | `crushrc` DSL (`provider add --type openai-compat`, `model add`); `$VAR` is expanded by Crush itself, config file never holds the literal key | charmbracelet/crush README.md |
| **Codex CLI** | proxy | Its `wire_api` **only** supports `"responses"` today — `"chat"` raises `CHAT_WIRE_API_REMOVED_ERROR` (removed). A plain openai-compat chat/completions server has to go through the shared LiteLLM proxy, which bridges `/v1/responses` → `/v1/chat/completions` | `codex-rs/model-provider-info/src/lib.rs` (source, not docs) |
| **Claude Code** | proxy | No per-provider concept at all — only a global `ANTHROPIC_BASE_URL`/`ANTHROPIC_AUTH_TOKEN`. Rather than mutate `~/.claude/settings.json` globally, the adapter writes an opt-in `~/.local/bin/claude-<provider-id>` launcher | LiteLLM docs (`tutorials/claude_responses_api`) |
| **Gemini CLI** | **unsupported** | No base-URL / custom-provider setting exists at all — checked, not guessed | `google-gemini/gemini-cli` `docs/cli/settings.md`, `docs/cli/model.md` |

Don't trust this table blindly as these projects evolve — it was true as of the
verification date above. If an adapter starts failing in a way that looks like
the upstream tool changed its config format, re-verify against the tool's
current docs/source before assuming the adapter is just buggy.

## Proxy-mode harnesses (Codex CLI, Claude Code today)

One shared local LiteLLM proxy, `dtx-litellm-proxy.service` (systemd --user,
`127.0.0.1:4444`), generated from the *entire* provider registry by
`proxy/render-litellm-config.sh` — never hand-edit
`~/.dtx-providers/litellm-config.yaml`, it's always regenerated.

Requires `litellm[proxy]` on `PATH` (not installed by this tooling —
`pipx install "litellm[proxy]"` yourself first). `proxy/ensure-proxy.sh`
renders the config, installs/refreshes the unit, and restarts it; it's called
automatically by `codex.sh`/`claude-code.sh` on `apply`.

The proxy's own local master key (`~/.dtx-providers/proxy.env`,
machine-generated, never synced) is what Codex/Claude Code present to the
*local* proxy — the real upstream provider key lives only inside
`litellm-config.yaml` server-side, which the proxy needs in order to actually
talk to the provider.

## Adding a new provider

`dtx-providers-tui add-provider` — prompts for baseURL/key/model, writes
`registry/<id>.json`, stores the key in `~/.dtx-providers/secrets.env`, and
reminds you to `chezmoi add --encrypt` it so it survives a fresh machine (see
`docs/SECRETS.md`).

## Adding a new harness

`dtx-providers-tui add-harness` writes `harnesses/<id>.json` with
`"mode": "template"` and a stub `adapters/<id>.sh` that fails loudly until you
implement it. Before writing real logic into that adapter:

1. **Confirm, don't assume**, exactly how that harness accepts a custom
   OpenAI-compatible provider — read its actual docs or source, the same way
   the table above was built. If it doesn't support one at all, make the
   adapter say so explicitly (see `adapters/gemini-cli.sh`) instead of
   silently no-op'ing.
2. Decide `native` (writes the harness's own config format directly) vs
   `proxy` (needs `proxy/ensure-proxy.sh` because the harness's wire format
   isn't OpenAI chat/completions-compatible).
3. Keep the literal secret out of anything adapters write when the harness
   supports referencing an env var by name (`{env:VAR}`, `env_key = "VAR"`,
   `$VAR`) — only the shared LiteLLM proxy config is allowed to hold literal
   upstream keys, because it's the piece that actually calls the provider.
