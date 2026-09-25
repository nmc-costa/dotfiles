# Session handoffs (every harness, every model)

**On start:** if a `HANDOFF.md` exists at the root of the repo you're in,
or of the subsystem you're about to work on, read its **top block** before
starting — it's the previous session's state and next step, possibly from a
different harness or model. Re-verify its Snapshot against live state
(`git status`, `git log`, open PRs) before acting on it. `~/HANDOFF.md` is
the cross-repo index — check it when the task spans repos.

**On stop with work unfinished** (out of tokens/usage, switching harness or
model, end of day): leave a handoff with the `handoff` skill —
`.agents/skills/handoff/SKILL.md`, script
`python3 ~/.agents/skills/handoff/handoff.py new|check|prompt`. If your
harness can't load skills, follow that SKILL.md by hand; the script is
plain Python 3, no dependencies.

Where it goes, and when to delete it: CHEATSHEET.md, "Leave/find a
session-continuity handoff".
