---
name: chronicle
description: >
  Mine this machine's interaction history (Claude session transcripts,
  tasks/events.jsonl, merged PR churn) into improvement candidates with
  cited evidence — repeated commands worth scripting, instruction language
  worth codifying, rework loops, churny files. Propose-only: output is a
  candidates report and, when the owner picks one, a chronicle/* PR that
  never merges itself. Use when the user says "chronicle", "mine our
  interactions", "what should we turn into a skill", "propose improvements
  from history". Thin shell over chronicle.py — all real logic lives there.
---

# /chronicle

Thin shell over `chronicle.py` (same directory; D14: script before rule).
Everything is **propose-only** (same rule as Copilot CLI's `/chronicle`):
the miner writes nothing to the repo, opens nothing, merges nothing — the
agent curates, the owner approves, humans merge.

## What to do

1. **Mine:**
   ```bash
   python3 .agents/skills/chronicle/chronicle.py mine --since <YYYY-MM-DD> [--min-count 3]
   ```
   Read-only over `~/.claude/projects/**/*.jsonl` (transcripts),
   `tasks/events.jsonl` (via `tasks/paths.tasks_root()` — the one real log
   even from a worktree), and merged PR files (gh). Secret-redaction runs
   on every quote; still treat the report as eyes-only.
2. **Report keyword-compact** (output-frame): one status line — sources
   scanned, candidate counts per kind — then only the top candidates with
   their counts. The full report goes to a file (`--out`, session
   scratchpad), not into chat.
3. **Curate with the owner**: for each real candidate, say what you'd build
   (a script, a SKILL.md, an instructions edit) in one line, and ask via a
   questionnaire (output-frame) which to propose. Discard noise — a high
   count alone is not a proposal.
4. **Propose** each accepted candidate on a branch `chronicle/<date>-<slug>`
   from `main`: the change itself (skill skeleton / instructions edit /
   script), plus the evidence table (counts + quotes, curated) in the PR
   body. **Human-only merge** — never enable auto-merge on chronicle PRs.
5. **Chain to finish**: once the PR is open, `/pr-finish` handles the
   preflight.

## What NOT to do

- Don't quote raw transcripts into a PR — quotes are truncated and
  redacted, but curate: an unpublished report is private, a PR is public.
- Don't act on a candidate (create the skill, edit instructions) outside a
  propose-only PR — history is evidence, not a mandate.
- Don't mine other people's machines or sync transcripts anywhere; this
  stays local to this machine.

## Chains

- `→ /pr-finish --task-id <id>` — when the propose-only PR is open and should be preflighted.
- `→ /task-brief` — after the owner rejects all candidates and you need the next thing to do.
