# `.agents/opencode/` — opencode integration (chronicle D7)

Source of truth for this machine's opencode-specific glue. Versioned here,
deployed to `~/.config/opencode/` by `sync.sh` (see the `opencode` mirror in
`sync.sh`) — same pattern as `skills/` → `~/.claude/skills` and
`hooks/` → `~/.claude/hooks`.

## What lives here

| Path | Deployed to | What it is |
| ---- | ----------- | ---------- |
| `command/*.md` | `~/.config/opencode/command/` | Global slash commands (`/pr-finish`, `/chronicle`, `/task-brief`, `/handoff`) — thin templates that invoke the workspace skills synced to `~/.agents/skills/` (opencode auto-loads those as external skills). |
| `plugin/chronicle-chain.js` | `~/.config/opencode/plugin/` | Server plugin (auto-discovered, no `opencode.json` entry): stages the D6 chain-suggestion footer (`Next: /skill <args>`) into the TUI prompt input via `tui.prompt.append`, propose-only, error-swallowing. |

`~/.config/opencode/opencode.json`, `node_modules/`, herdr's `plugins/` and
all other machine-local state under `~/.config/opencode/` are **not** touched
by the sync — only these two subdirectories are reconciled.

## Conventions implemented

- **Chain suggestion footer** — `.agents/instructions/workspace-config/
  output-frame.instructions.md` (Footers): at most one `Next: /skill <args>`
  line, only when a chain from the executed skill's `## Chains` section
  applies. The plugin stages exactly that line; it never submits.
- **Skill stacking** — `/a /b` in one message works natively; commands stay
  thin so stacking remains a prompt-language concern, not a config one.

## After deploy

Restart opencode: config-time files (commands, plugins) are loaded once at
startup, never hot-reloaded.

## Upstream tracker

Custom sidebar panels (the "real panel" for a session dashboard) are opencode
FR [#5971](https://github.com/anomalyco/opencode/issues/5971) — still open as
of 2026-09-25. When it lands, add a `sidebar` panel to `chronicle-chain.js`
showing the current card's phase + last brief result.
