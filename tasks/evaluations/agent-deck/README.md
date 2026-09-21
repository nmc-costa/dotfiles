# agent-deck evaluation (2026-09-21)

Fase-0 de-risking spike for the orchestration architecture decided in
`tasks/README.md`'s "Orchestration architecture" section — specifically the
"install Agent Deck" item under "Remaining spikes" and the open question
"whether `agent-deck` and `herdr` overlap enough to only need one, or are
genuinely complementary". **Result: agent-deck passes, with one important
caveat on Copilot depth.** It's a real, actively maintained tool that
installs cleanly and does detect Claude Code and Copilot CLI sessions
side by side — but the README's own integration table (verified
empirically below) says Copilot only gets "Organization, launch", not
status detection, so "side by side" means "both visible and running
concurrently", not "equally deep telemetry for both".

## What was tested

[`asheshgoplani/agent-deck`](https://github.com/asheshgoplani/agent-deck)
(MIT, 935★, Go, actively released — `v1.16.16` pushed the same day as this
spike), installed from the official install script into `~/.local/bin`,
then exercised against two throwaway tmux-managed sessions (one `claude`,
one `copilot`) in a scratch git repo (`/tmp/agent-deck-scratch/`, outside
this repo, deleted afterward — nothing under `~/.local/share/agent-deck` or
`~/.config/agent-deck` was left configured beyond the default empty
profile).

## Findings

**1. Repo is real and active.** Confirmed via `gh repo view
asheshgoplani/agent-deck`: MIT license, 935 stars, not archived, last push
2026-09-21 (today). Description: "Terminal session manager for AI coding
agents. One TUI for Claude, Gemini, OpenCode, Codex, and more."

**2. Prebuilt binaries exist — no `go install` / `mise use -g go` needed.**
`gh release list` shows 30 releases; the latest (`v1.16.16`,
2026-09-20) ships `agent-deck_1.16.16_{darwin,linux}_{amd64,arm64}.tar.gz`
plus `checksums.txt` via GitHub Actions. Confirmed a Linux/amd64 asset
exists before touching Go at all (`uname -m` → `x86_64`, `uname -s` →
`Linux`). **The Go toolchain install was skipped entirely** — not needed,
and `which go` still fails on this machine after this spike, confirming
nothing pulled it in as a side effect.

**Safety.** Read the official `install.sh`
(`https://raw.githubusercontent.com/asheshgoplani/agent-deck/main/install.sh`,
881 lines) before piping it to bash: greped every `curl`/`wget`/`http(s)`
occurrence — all network calls are scoped to `api.github.com` (version
lookup) and `github.com/asheshgoplani/agent-deck/releases/...` (binary +
checksums download). The script verifies the downloaded tarball's SHA-256
against `checksums.txt` before installing (`verify_download_checksum`,
fails closed if the tool or the checksum entry is missing) — an explicit
mitigation against a tampered/MITM'd binary in a `curl | bash` flow, per
the script's own comments (references "audit H1"). Installed with
`--non-interactive --skip-tmux-config` to `~/.local/bin/agent-deck`;
checksum verification passed. Telemetry is opt-in and off by default
(`agent-deck telemetry status` → `OFF`, `Consent: undecided`, endpoint
never contacted).

**3. Copilot support exists in the binary, but is shallower than Claude's.**
The GitHub README's "Multi-Tool Support" table (fetched via `gh api
repos/.../contents/README.md`) is explicit:

| Tool | Integration Level |
|---|---|
| Claude Code | Full (status, MCP, fork, resume) |
| Codex | Status detection, MCP, organization, conductor, fork |
| **Copilot** | **Organization, launch** (no status detection listed) |

`strings` on the installed binary confirms Copilot handling is real code
(`copilot_set_env_failed`, a `copilot>` prompt-matching regex, etc.), not
just a README claim — but the table's omission of "status detection" for
Copilot is the operative fact for this spike's question.

**4. Side-by-side detection — confirmed, with the depth caveat borne out
empirically.** Added and started one `claude` and one `copilot` session
against the same scratch repo (`agent-deck add . -c claude`, `agent-deck
add . -c copilot`, then `session start` on both). Both launched as
genuinely separate, concurrent tmux-managed processes
(`tmux list-panes -a` showed `agentdeck_test-claude_*` running `claude`
and `agentdeck_test-copilot_*` running `copilot` at the same time — real
concurrent CLI sessions, not a simulation). `agent-deck status -v` then
showed both in one table:

```
WAITING (2):
  ◐ test-claude      claude     tool default           .../proj1  [awaiting menu choice]
  ◐ test-copilot     copilot    -                      .../proj1
```

This is the direct answer to the spike's core question: **yes, agent-deck
detects Claude Code and Copilot CLI sessions side by side on this
machine** — both rows exist, both are polled, both show as running. But
note the asymmetry predicted by the README table: Claude's status column
carries a live, tool-specific detail string (`[awaiting menu choice]`,
i.e. it parsed Claude's actual turn state); Copilot's status column is a
bare `-` — agent-deck knows the session exists and is alive, but (per the
"Organization, launch" integration level) does not parse Copilot's
internal state the way it does Claude's. "Side by side" is true for
*presence/liveness*; it is not true for *status-detail parity*.

**5. TUI screenshot not obtained — documented, not hidden.** The
interactive TUI refuses to run nested inside tmux by default ("Error: The
agent-deck TUI is designed to run OUTSIDE of tmux... set
AGENT_DECK_ALLOW_OUTER_TMUX=1"). This spike's shell runs inside a
sandboxed tmux session itself, so a true "outside tmux" launch wasn't
available. Retried with `AGENT_DECK_ALLOW_OUTER_TMUX=1` in a nested tmux
pane — the process started (log file showed it entering the alternate
screen buffer, `[?1049h`) but `tmux capture-pane` on that nested pane did
not reliably surface the alt-screen contents in this environment, and the
session exited before a second capture. The **CLI-level evidence above
(`agent-deck status -v`) is the evidence this spike relies on** — it's
non-interactive, scriptable, and directly answers the detection question
without needing the TUI to render. A full TUI screenshot is a reasonable
follow-up for whoever builds the fleet-dashboard integration, not a
blocker for this spike's verdict.

**Cleanup.** Both test sessions stopped and removed
(`agent-deck session stop`, `agent-deck remove`), tmux server for them
exited on its own, `/tmp/agent-deck-scratch/` deleted. `agent-deck` itself
stays installed at `~/.local/bin/agent-deck` (that's the artifact of the
spike, consistent with `herdr` also being a persistent installed tool
referenced by `tasks/README.md`); its profile store
(`~/.local/share/agent-deck`) is empty (no sessions configured after
cleanup).

## Overlap with `herdr` (the open question from `tasks/README.md`)

`tasks/README.md` (line ~212) asks: "Whether `agent-deck` and `herdr`
overlap enough to only need one, or are genuinely complementary (herdr =
panes/TUI/notifications, Agent Deck = worktree engine + notification
bridge) — first thing to test."

Evidence from this spike plus reading both tools' `--help` output
(`herdr --help`, `agent-deck --help`):

- **Real overlap exists at the multiplexer layer.** Both are, at their
  core, tmux-flavored terminal/session managers with agent-status
  awareness and a notification path: `herdr` has `pane`, `tab`,
  `notification`, `workspace`, `agent` subcommands and a socket API;
  `agent-deck` explicitly wraps tmux ("Agent Deck adds AI-specific
  intelligence on top of tmux... Think of it as tmux plus AI awareness")
  and manages its own tmux sessions internally. If the only need were "a
  live pane view with notifications", one tool would likely suffice.
- **They diverge in the direction `tasks/README.md` already
  anticipated.** `agent-deck` goes meaningfully further into execution/
  orchestration territory that `herdr`'s `--help` does not surface at
  all: session **fork with context inheritance** (`session fork`, for
  Claude/OpenCode/Pi/Codex/Oh My Pi), **worktree management** (`worktree,
  wt`), a **conductor** meta-agent subcommand for supervising other
  agents, **MCP server management** per session, cross-machine **remote**
  management, and Telegram/Slack/Discord notification *bridges* (not just
  local notifications). `herdr` is a Rust/Ratatui terminal workspace
  manager focused on panes/tabs/worktree-helpers/notifications over a
  socket API — closer to "TUI + plugin popups + notification events" as
  `tasks/README.md` already characterized it.
- **Verdict on the question: complementary, not redundant — but with
  real surface overlap that will need a policy decision later** (e.g.
  which tool owns "the" live pane view the human actually watches).
  Concretely for this repo's stated L2/L3 split: `agent-deck` is the
  better fit for L2 (execution engine: worktree isolation, forking,
  conductor supervision, and — uniquely among the two — actually
  launching Copilot/Codex/OpenCode/etc. sessions, which `herdr` does not
  do). `herdr` remains the better fit for L3 (the interactive
  observability layer already decided in `tasks/README.md`, with its
  `plugin pane open` popup mechanism — see the sibling spike at
  `tasks/evaluations/herdr-popup/`). Running both is not wasted effort;
  it does mean the eventual `tsk` policy layer needs to pick one as the
  "source of truth" pane view to avoid two multiplexers fighting over
  the same terminal, which this spike did not need to resolve.

## Verdict

**Adopt agent-deck for L2 (Copilot/Codex/multi-vendor execution), as
already decided in `tasks/README.md` — confirmed workable, not
blocked.** Prebuilt Linux binary installs cleanly with checksum
verification and no Go toolchain required; it genuinely runs Claude Code
and Copilot CLI sessions concurrently and lists both in one status view.
The one correction to the existing architecture note: don't expect
Copilot-side status telemetry as rich as Claude's — the upstream project
itself scopes Copilot to "Organization, launch" only, not "status
detection". Any policy logic in `tsk`/L4 that needs to know *what a
Copilot session is currently doing* (not just *that it exists and is
running*) will need a different signal than what agent-deck gives for
free today (e.g. content-based tmux pane scraping, the same
"Codex notify hook"-style pattern agent-deck itself uses elsewhere, or a
Copilot-side hook if/when one exists).

## Files here

- This `README.md` only — no throwaway config/board files were worth
  keeping (unlike the `tuiboard` eval, there's no persistent board state
  to snapshot; the scratch repo and its two test sessions were deleted
  after use, and `agent-deck`'s own profile store is empty).

## Not yet tested

- The web dashboard (`agent-deck web`) and fleet TUI screenshot — blocked
  in this sandbox by the nested-tmux restriction described above, not by
  anything about agent-deck itself. Worth a follow-up from a clean
  (non-nested-tmux) shell before building the L3 dashboard integration.
- Gemini CLI and other vendors from the support table (Codex, OpenCode,
  Crush, Cursor, pi, DeepSeek Harness, Oh My Pi) — out of scope for this
  spike, which targeted specifically the Claude+Copilot pairing named in
  the task.
- Whether `agent-deck`'s conductor/watcher meta-orchestration could
  directly replace the planned `tsk daemon` (L4) rather than just feeding
  it — `tasks/README.md` scopes L4 as "build, this is the actual gap",
  and nothing in this spike contradicts that, but the conductor
  subcommand's existence is worth a closer read before L4 design starts.
