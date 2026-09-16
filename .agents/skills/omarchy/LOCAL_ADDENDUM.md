# Local addendum — NOT part of the vendored bundle

`SKILL.md`, `hyprland.md`, `plugins.md`, `theming.md`, `hooks.md`,
`capture.md`, and `contributing.md` in this directory are **verbatim
copies** of `/usr/share/omarchy/default/agents/skills/omarchy/` — the
Omarchy package's own official AI-agent skill. Never edit those six files
here; edit means diverging silently from upstream, which is exactly what
this addendum exists to avoid. Verify they're still byte-identical any
time you suspect drift (e.g. after `omarchy update`):

```bash
diff -rq ~/dotfiles/.agents/skills/omarchy /usr/share/omarchy/default/agents/skills/omarchy
diff -rq ~/dotfiles/.agents/skills/diagnose-crash /usr/share/omarchy/default/agents/skills/diagnose-crash
```

Both confirmed identical (no output) on 2026-09-16.

This file is additive only — content the official skill doesn't cover yet,
found by reading `omarchy.org/manual/ai/` and `omarchy.org/manual/shell-plugins/`
directly rather than assuming the vendored files are complete. If Omarchy's
own skill ever documents this material, delete the corresponding section
here rather than let it duplicate/drift.

## Gap: the `omarchy agent` launcher subsystem

Confirmed via `omarchy.org/manual/ai/` (2026-09-16) — **not present** in any
of the six vendored files above:

- **Agent launcher**: `omarchy agent` / `omarchy-agent-*` dispatches to 9+
  configured coding agents (Claude Code among them).
- **Default agent**: `omarchy default agent` sets which one launches
  without a further prompt.
- **Global shortcut**: `Super+Shift+Ctrl+A` opens the agent launcher from
  anywhere in the desktop session.
- **Agents Panel**: a usage/limits/tokens dashboard across configured
  agents — surfaces spend and rate-limit state without leaving the shell.
- **Crash-capture integration**: the launcher wires into the same
  crash-capture path `diagnose-crash` covers, so an agent-launched session
  that crashes gets picked up the same way a normal process crash would.

This gap is not a bug in Omarchy's skill packaging — the manual documents
this subsystem, the vendored agent-facing skill just hasn't caught up to it
yet. Recommendation for the workspace owner (not an action taken here,
since reporting upstream is a visible external action): consider filing
this as a documentation gap via the flow in [`contributing.md`](contributing.md)
(Suggestions category, since it's "the skill doesn't mention X" rather than
a bug).

## Plugins

### The official manifest standard (validated online, not inferred)

Confirmed against `omarchy.org/manual/shell-plugins/` and
`plugins.omarchy.org/develop.html` (2026-09-16):

- **6 plugin `kinds`**: `bar-widget`, `panel`, `overlay`, `menu`, `service`
  (a singleton QML component that runs headless *inside* the
  `omarchy-shell` process — not a separate systemd service), `bar`.
- **Dev flow**: `omarchy plugin clone <id> --edit` → edit → `omarchy plugin
  validate <plugin-folder>` + `qmllint` → submit to the marketplace via an
  issue form at `github.com/omacom/omarchy-plugin-marketplace/issues/new?template=submit-plugin.yml`.
- **Sanctioned pattern for anything with real logic**: a thin QML front-end
  (`bar-widget`/`service` kind) in front of a genuine **user-level systemd
  service** doing the actual work — confirmed against a real plugin under
  review, "Omarchy Google Calendar" (marketplace issue #6846: Rust daemon +
  systemd unit + Unix socket + a QML front-end cloned from `omarchy.clock`).
- **Installing a third-party plugin**: `omarchy plugin add <git-url>
  [--enable] [--yes]` (confirmed via `omarchy plugin --help`, 2026-09-16).
  **Do not invent a repo URL for any plugin mentioned below** — only that
  it's listed on `plugins.omarchy.org` is confirmed; find the real
  clone URL there before running `omarchy plugin add`.

`omarchy-voice` (see below) does **not** follow this format — it's a plain
`install.sh` that drops a binary + systemd service + keybinding, with no
`manifest.json`, no `kinds`/`entryPoints`, and no marketplace listing.
Building something "in the Omarchy plugin format" means targeting the
manifest system above, not that shape.

### Voice → agent: two real options, a trade-off, not a recommendation

The owner corrected an earlier framing here: the goal is being able to
**talk to any configured agent**, not only Claude Code — even though
Claude Code is what's used today. Two real projects exist, and they trade
off differently. Which one fits depends on the answer to the open question
below, which is the owner's call, not decided here.

| | **VoxClaude** | **omarchy-voice ("Jarvis")** |
|---|---|---|
| Marketplace status | Official, approved (`omarchy-plugin-marketplace` issue #6050) | Not listed — standalone `install.sh`, no manifest |
| STT engine | `voxtype` native (Whisper, local, offline, free) | OpenAI cloud API |
| Agent target | Claude Code only (≥2.1.260), `voxtype` ≥1.0 required | Launches "coding/analysis" tasks in background — **unconfirmed** whether the backend agent is configurable or fixed |
| Trade-off | Offline/free/private, but locked to one agent | Likely better transcription quality (cloud model), but a recurring cloud dependency + cost, and multi-agent flexibility unverified |

**Open question for the owner to check before choosing**: does
`omarchy-voice` actually dispatch to a configurable agent backend, or is it
hardwired to one? The repo is `wombatoperator/omarchy-voice` (the project
behind the "I BUILT JARVIS IN OMARCHY" video) — read its own docs/source to
confirm before deciding, rather than assuming multi-agent support because
the demo happened to use it that way.

Full landscape-scan context (why these two and not something else) is in
`.agents/instructions/workspace-config/standards/RESEARCH_NOTES.md`,
2026-09-16 entry.

## Out of scope for this addendum

Expanding this file to cover all of `/usr/share/omarchy/bin` (441 scripts)
— the official vendored skill is deliberately curated; only the concrete
gap identified above (the agent launcher subsystem) gets added here.
Reporting the gap upstream is the owner's action, not something done as
part of writing this file.
