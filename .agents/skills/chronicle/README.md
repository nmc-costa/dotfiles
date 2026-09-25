# chronicle — daily background improve (automation notes)

Owner-directed (2026-09-25): chronicle must run in the background once a day,
produce its improvement via **branch → PR → merge** (so a fallback revert is
always possible), consuming the radar briefs as online-research input.

## How it runs

- `scripts/run.sh` — the whole flow (radar-family shape): mine → briefs →
  headless agent (default `opencode`, `CHRONICLE_AGENT=claude` switches) →
  push `chronicle/improve-<date>` → PR → gated auto-merge. See
  [security.md](security.md) for the four gates.
- `systemd/chronicle-improve/` — `--user` timer (daily 08:00 + jitter,
  persistent) and hardened oneshot service. **Not auto-installed**: after
  merge + `./sync.sh`, enable with
  `systemctl --user enable --now chronicle-improve.timer` (owner-run).
- State: `~/.local/state/chronicle-improve/` (`last-pr`, `run.log`).

## Testing without side effects

```bash
CHRONICLE_DRY_RUN=1 .agents/skills/chronicle/scripts/run.sh
```

Mines for real, builds the agent prompt, prints paths — no agent run, no
push, no PR.

## Relationship to the radars

The radars (`omarchy-radar`, `harness-radar`) do the *online* research and
write `briefs/*.md`; this job *consumes* the newest brief of each radar as
research input alongside locally mined candidates. It does not collect
anything online itself. De-duplication check done 2026-09-25: no other
background job was improving skills (only `tsk-sweep` hygiene + weekly
`dotfiles-sync` were active; the radar timers were not yet installed on this
machine).
