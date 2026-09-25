# chronicle — security model (daily improve run)

This documents the security posture of `scripts/run.sh`, the headless daily
improve job (card `dotfiles-tsk-chronicle-daily-improve`). It follows the
[researcher-radar](../researcher-radar/SKILL.md) family model: a deterministic
collect step, one confined agent step, propose-then-gate delivery, and a
documented revert path.

## Trust boundaries

| Step | What runs | Trust level |
| ---- | --------- | ----------- |
| Mine | `chronicle.py` — local reads only (transcripts, `tasks/events.jsonl`, merged-PR churn), no network, no third-party code | deterministic, safe |
| Briefs | copies of `briefs/*.md` written by the local radars — **read as data, never executed** | data only |
| Agent | one headless LLM run (`opencode run`, or `claude -p` via `radar-common`) inside a disposable worktree | untrusted output, gated below |
| Deliver | `gh pr create` + gated `gh pr merge --auto --squash` | gates enforced from GitHub's own state |

## Hard gates before anything lands on `main`

1. **Path allowlist** — every file in the PR (queried from GitHub, not from
   local claims) must match `^\.agents/(skills|opencode)/`. Anything else →
   the PR is commented and left open; no merge. This keeps instructions
   files (`.agents/instructions/**`), `tasks/**`, scripts and dotfiles out
   of reach of the unattended agent.
2. **MERGEABLE + CLEAN** — checked via `gh pr view` before enabling
   auto-merge; conflicts or blocked states leave the PR open.
3. **CI green** — `gh pr merge --auto --squash` only asks GitHub to merge
   when checks pass; GitHub enforces this, not the script.
4. **1 PR/day** — branch name `chronicle/improve-<date>` is deduplicated
   against open + recently-merged PRs, plus a `last-pr` state file.

## Containment

- The agent works in a **disposable git worktree** off fresh `origin/main`
  (`~/dotfiles.worktrees/chronicle/improve-<date>`), removed after the run;
  the main checkout is never switched, committed, or written.
- The mine step runs with cwd = canonical checkout for correct data
  resolution, but writes only to a `mktemp -d` dir.
- The systemd unit (see `systemd/chronicle-improve/`) runs hardened:
  `NoNewPrivileges`, `PrivateTmp`, `ProtectHome=read-only`,
  `ProtectSystem=strict`, with an explicit `ReadWritePaths` allowlist.
- The agent prompt itself forbids touching `tasks/`, `.claude/`,
  `opencode.json` — defense in depth under gate 1.

## Secrets & redaction

`chronicle.py` already redacts secrets and filters boilerplate before any
candidate leaves the machine. Mined output goes into the PR body (capped at
4 KB). No credentials are read, written, or echoed by `run.sh`.

## Failure posture

Any failure (`die`, agent crash, gate failure, auto-merge rejection) exits 0
and leaves an open PR or a log line — a skipped day is never a timer failure,
and human review is always the fallback. Revert after a landed improvement is
plain `git revert <squash-sha>`.
