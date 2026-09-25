# harness-radar

A headless, once-a-day digest of the AI coding-agent/harness ecosystem —
`herdr` and its plugin marketplace, per-harness plugin ecosystems (Claude
Code, Codex CLI, OpenCode, Gemini CLI, Copilot CLI, DeepSeek Harness/`dsh`),
multi-agent orchestration frameworks, the skill/plugin/MCP aggregator
ecosystem, and benchmark leaderboards (SWE-bench, SWE-bench Verified,
Terminal-Bench, LiveCodeBench) — compared against what's actually installed
on this machine, with the top 3 worthwhile changes proposed on a disposable
branch for a human to review and merge by hand.

It is one member of the `researcher-radar` family (see
`.agents/skills/researcher-radar/`, the meta-skill documenting the shared
architecture) and its sibling `omarchy-radar` (same pattern, Omarchy Linux
community instead of the harness ecosystem). Both share
`.agents/automation/radar-common/lib.sh` for the security-critical plumbing —
state handling, git-worktree isolation, the `claude -p` invocation wrapper,
secret-scanning, `flock`, and notifications — so that code is written and
reviewed once, not duplicated per radar.

## Why this exists

Verifying "is `zoahdev/dsh-ecosystem` still the right index," "is
`omacom/omarchy` still the canonical repo," "is Terminal-Bench still active,"
or "which harness currently tops SWE-bench Verified" from scratch is real,
repeated research cost — for a human and for every future agent session that
touches this ecosystem. `harness-radar` pays that cost once a day instead of
once per question, and its approved output also updates
`docs/radar-knowledge/harness.md`, a durable "last verified" ledger any
future session should check before re-researching a fact it might already
answer.

## This radar's identity

| | |
|---|---|
| State directory | `~/.local/state/harness-radar/` |
| Systemd timer | `harness-radar.timer`, `OnCalendar=08:20`, `Persistent=true`, `RandomizedDelaySec=600` |
| Systemd service | `harness-radar.service` (`Type=oneshot`) |
| Branch prefix | `radar/harness-radar/<date>` |
| Brief filename | `briefs/harness-radar-<date>.md` (plus optional `briefs/harness-radar-<date>.proposals/` for suggestions touching files `dotfiles` tracks) |
| Knowledge ledger | `docs/radar-knowledge/harness.md` |

**Why `08:20`, not `08:00`:** `omarchy-radar`'s timer fires at `08:00` with
the same `RandomizedDelaySec=600` (up to a 10-minute jitter), so it can land
anywhere in `08:00`–`08:10`. Both radars run `git worktree add`/`remove`
against the same `~/dotfiles` repository from `radar-common`'s shared
helpers; offsetting `harness-radar` to `08:20` leaves a comfortable gap past
that jitter window so the two timers' cold starts don't compete for the same
moment, while both still land well within "briefed before the day starts."
`harness-radar`'s own `RandomizedDelaySec=600` gives it the same
resume-from-suspend-friendly jitter `omarchy-radar` has.

`~/.local/state/harness-radar/` mirrors `omarchy-radar`'s layout exactly
(see that radar's `sources.md`/`README.md` for the shared shape, not
repeated here):

- `seen.json` (promoted from `seen.json.pending` only after a successful
  commit) — last-seen id/sha/guid per source.
- `status.json` — per-source `ok`/`error` + consecutive-failure count, so a
  dead source is visibly different from "genuinely nothing new."
- `snapshots/` — previous copies of diffable listings (README files, index
  pages, the herdr-plugin/dsh-plugin topic listings, benchmark leaderboard
  pages) used to compute real diffs, not just timestamp cutoffs.
- `inbox/<date>.json` — today's new items only, grouped by category; the
  agent step is skipped entirely (no `claude -p` call, no brief, no
  notification) when every category is empty and no source errored.
- `worktrees/<date>/` — the disposable git worktree the agent step runs in;
  removed once its commit lands on `radar/harness-radar/<date>`.
- `harness-radar.lock` — the `flock` guard preventing a manual `run.sh`
  from overlapping the timer.

## Acceptance criteria

Same testing bar as `omarchy-radar` (see the family plan's Testing section);
before either radar's timer is enabled, for `harness-radar` specifically:

1. `collect.sh` run twice back-to-back: the second run's inbox is empty (no
   duplicate items surface) and `status.json` shows every source `ok`.
2. A full `run.sh` pass reads in under ~2 minutes, creates and then removes
   its worktree, never switches `~/dotfiles`'s actual checked-out branch, and
   leaves exactly one new commit on `radar/harness-radar/<date>` touching
   only its own brief (and proposal diffs, if any).
3. The secret-scan step visibly ran (checked via its log line, not just the
   absence of an alert) before that commit.
4. A second same-day `run.sh` detects the existing `radar/harness-radar/<date>`
   branch and skips cleanly; two concurrent `run.sh` invocations serialize via
   `flock` rather than racing on `seen.json`.
5. Running `omarchy-radar` and `harness-radar` concurrently doesn't cross
   state — separate state dirs, separate branches, separate worktrees.

## Folder layout

```
.agents/skills/harness-radar/
├── SKILL.md              # frontmatter + when-to-use + pointers (this family's entry point)
├── README.md             # this file
├── sources.md            # every source, exact endpoint/repo/API
├── ranking.md            # scoring rubric, incl. the benchmark-rank signal
├── security.md           # non-negotiable safety rules for this radar
└── scripts/              # collect.sh, run.sh, install_timer.sh (separate build pass)
```

See `sources.md` for the full source list, `ranking.md` for how a collected
item becomes one of the top 3 suggestions, and `security.md` before touching
either.
