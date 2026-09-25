# omarchy-radar

A headless, daily digest of the Omarchy Linux (Quattro) community, compared
against this machine's real config, proposing (never applying) the top 3
changes worth making. One of two member radars in the `researcher-radar`
family — see
[`../researcher-radar/README.md`](../researcher-radar/README.md) for the
shared architecture, and [`../harness-radar/README.md`](../harness-radar/README.md)
for the sibling radar watching the AI coding-agent ecosystem instead.

## State-dir and schedule (decided here)

| Decision | Value |
|---|---|
| State directory | `~/.local/state/omarchy-radar/` |
| systemd timer | `omarchy-radar.timer` |
| `OnCalendar` | `08:00` |

`harness-radar` uses its own state dir (`~/.local/state/harness-radar/`) and a
staggered `OnCalendar=08:20`, so the two radars' timers never fire at the same
moment and never contend for the same cold-start window. Both use
`Persistent=true` so a missed run (machine asleep at trigger time) fires
promptly on next wake/boot.

## Pipeline

```
collect.sh  →  skip if inbox empty & no source errors  →  claude -p (disposable git worktree, no Bash/git tools)  →  run.sh verifies diffs, secret-scans, commits  →  notify
```

1. **`collect.sh`** (deterministic, no LLM, idempotent) fetches every source
   in `sources.md`, dedupes against `~/.local/state/omarchy-radar/seen.json`,
   and writes `~/.local/state/omarchy-radar/inbox/<date>.json`. If every
   category is empty and nothing errored, `run.sh` stops here — no agent
   call, no brief, no notification (keeps token cost and notification noise
   proportional to actual news).
2. **`run.sh`** creates a disposable `git worktree` at
   `~/.local/state/omarchy-radar/worktrees/<date>` on a new
   `radar/omarchy-radar/<date>` branch, and invokes `claude -p` with cwd set
   to that worktree root, `--allowedTools "Read,Grep,Glob,Write(briefs/*)"`,
   `--disallowedTools "WebFetch,WebSearch,Bash"`, and no
   `--dangerously-skip-permissions`. The agent's whole job is described in
   `SKILL.md`'s Decision Framework and `ranking.md`'s rubric.
3. `run.sh` (back in deterministic bash) computes the **real** `diff -u` for
   any tracked-file proposal, runs a secret-scan grep pass over the finished
   brief, commits inside the worktree only, removes the worktree, and only
   then promotes `seen.json.pending` → `seen.json` and fires the success
   notification. `main`'s actual checkout is never switched, read-locked, or
   modified at any point.

Full security model (read-allowlist, deny rules, why there's no Bash for the
LLM step, the secret-scan safety net): [`security.md`](security.md).

## Where output lands

- `briefs/omarchy-radar-<date>.md` — the brief itself, only ever committed on
  a `radar/omarchy-radar/<date>` branch, never on `main`.
- `briefs/omarchy-radar-<date>.proposals/` — full proposal files for any
  suggestion touching a file `dotfiles` tracks (the brief itself gets the
  verified diff spliced in by `run.sh`, not a model-written one).
- Nothing under `~/.config` is ever written to. A suggestion touching a live,
  untracked config file gets an explicitly-labeled, AI-drafted-and-unverified
  diff in the brief for readability only.

## Acceptance criteria (must hold before enabling the timer)

- Running `collect.sh` twice in a row produces an **empty** inbox the second
  time (dedupe actually works).
- A brief reads in under ~2 minutes.
- `git -C ~/dotfiles branch --show-current` stays `main` throughout a full
  `run.sh` invocation, and `git status` on `main` is unchanged afterward.
- `git -C ~/dotfiles worktree list` shows the worktree created and then
  removed — nothing left behind.
- The `radar/omarchy-radar/<date>` branch has exactly one new commit touching
  only its own `briefs/omarchy-radar-<date>.md` (and proposal files, if any).
- Running `run.sh` a second time the same day detects the branch already
  exists and skips cleanly — no clobber, no duplicate commit.
- Two concurrent `run.sh` invocations serialize via `flock` rather than racing
  on `seen.json`/the inbox file.
- A dead source (e.g. Reddit 429, the news-radar feed unreachable) shows up as
  `error` in `status.json`, not as silent "nothing new" — and N consecutive
  failures fires its own warning notification.

See the plan's full `Testing` section for the exhaustive step-by-step; this is
the summary a human re-checks before flipping the timer on.

## Delivery channels

Success and warning notifications go through
`.agents/automation/radar-common/lib.sh`'s notification helper, adapted from
`tasks/notify.py`'s existing pattern: `herdr notification show` first (so the
brief surfaces inside `herdr`, where sessions are already watched), with an
unconditional `notify-send` fallback. Two further options, not built as part
of this radar but worth knowing about:

- **Day-one, zero-code candidate**: `jankeesvw/omarchy-notification-center` or
  `njpatel/omapager` — real, installable Omarchy plugins
  (`omarchy plugin add <url> --enable`) that turn the notification stream
  into a persistent, re-openable history instead of a vanishing popup. Listed
  in `sources.md` as a known-good candidate suggestion for the very first
  real brief to surface, rather than force-installed here.
- **Optional Claude Code `statusLine` badge** (`scripts/statusline-badge.sh`
  in `radar-common`, wired manually into the user's own `settings.json` if
  wanted): a one-line "unread brief" indicator. Claude-Code-only.

## Knowledge reuse

Merging an approved `radar/omarchy-radar/<date>` branch also updates
`docs/radar-knowledge/omarchy.md` — a running "last verified" ledger (repo
identities, which aggregator is authoritative, etc.) so a future session
doesn't re-pay the research cost this radar's design already paid once. This
update happens by hand, as part of the human's merge, never by the unattended
agent.

## See also

- [`SKILL.md`](SKILL.md) — triggers and the Decision Framework the automated
  step follows
- [`sources.md`](sources.md) — every source, exact endpoint
- [`ranking.md`](ranking.md) — scoring rubric and brief format
- [`security.md`](security.md) — the non-negotiable safety rules
- [`../researcher-radar/README.md`](../researcher-radar/README.md) — the
  radar family overview
- `.agents/automation/radar-common/` — the shared plumbing this radar's
  `run.sh` calls into
