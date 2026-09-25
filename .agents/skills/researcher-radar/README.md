# researcher-radar

The umbrella for this repo's family of headless daily-digest "radar" agents.
Not a radar itself — it documents the shared architecture and points at the
member radars that actually collect and brief.

## Family

| Radar | Watches | Timer |
|---|---|---|
| [`omarchy-radar`](../omarchy-radar/README.md) | Omarchy Linux (Quattro) community | `omarchy-radar.timer`, 08:00 |
| [`harness-radar`](../harness-radar/README.md) | AI coding-agent/harness ecosystem + benchmark leaderboards | `harness-radar.timer`, 08:20 |

Both share one library, `.agents/automation/radar-common/lib.sh` — the
git-worktree isolation, state management, `claude -p` invocation wrapper,
secret-scan, `flock` guard, and notification helper are written once there,
not duplicated per radar.

## Shared shape

Every radar is a standalone, independently invokable/removable skill folder:

```
.agents/skills/<radar-name>/
├── SKILL.md       # frontmatter + when-to-use + pointers (also read by the unattended agent step)
├── README.md      # this kind of file — human-facing overview
├── sources.md     # every source, exact endpoint/repo/API
├── ranking.md     # the scoring rubric + brief format
├── security.md    # what the automated agent may never do
└── scripts/
    ├── collect.sh        # deterministic, no LLM, data-fetch only
    ├── run.sh            # orchestrator: collect → claude -p in a worktree → commit → notify
    └── install_timer.sh  # copies systemd/<name>/*.{service,timer} into place (does NOT enable)
```

## Why a shared library instead of copy-pasting each radar's `run.sh`

The security-critical plumbing (worktree isolation so the LLM never touches
the user's real `~/dotfiles` checkout, no Bash/git tools for the LLM, the
read allowlist + secret-scan against a public-repo secret-leak vector, atomic
state writes, the `flock` overlap guard) needs to be written and reviewed
**once**. `radar-common` is that once; each radar's own files stay focused on
what makes it different — its sources, its ranking rubric, its own
read-allowlist for "compare against what's actually installed/configured."

## Knowledge reuse

Merging an approved `radar/<name>/<date>` branch also updates a durable "last
verified" fact ledger under `docs/radar-knowledge/` — check it before a fresh
research pass re-establishes a fact it may already answer. See
[`SKILL.md`](SKILL.md#knowledge-reuse-check-docsradar-knowledge-before-re-researching).

## Adding a radar

See [`SKILL.md`](SKILL.md#adding-a-new-radar).

## Safety in one line

Every radar only ever proposes; nothing is auto-applied, auto-merged, or
pushed, and the LLM step never runs Bash, git, or anything it collects — see
each radar's own `security.md` for the full rule set.
