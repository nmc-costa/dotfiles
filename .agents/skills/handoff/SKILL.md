---
name: handoff
description: >
  Write a session handoff that any other harness, provider or model can pick
  up (Claude Code, Copilot CLI, Antigravity, Gemini CLI, OpenCode, ...) —
  a plain-markdown HANDOFF.md block with a generated state snapshot plus
  the narrative only the current session knows. Use when the user is about
  to stop, is running out of tokens/usage, wants to switch harness or model
  mid-task, or asks to "hand off", "leave a handoff", "pass this to another
  agent", "/handoff". Thin shell over handoff.py (D14: script before rule).
---

# /handoff

Leave a handoff the next session can act on without this conversation —
whoever it is. The receiving side needs **no skill**: each block tells its
reader what to do, so "read `<path>/HANDOFF.md`" works on any harness.

`handoff.py` sits next to this file. Run it as
`python3 ~/.agents/skills/handoff/handoff.py` (or
`~/dotfiles/.agents/skills/handoff/handoff.py`) from inside the repo the
handoff is about.

## Is this a task card instead?

If the work is a single card in a repo with a `tasks/` system, the card is
the handoff: use `python3 tasks/brief.py --prompt-only --task-id <id>` (or
`tasks/dispatch.py` to launch another CLI with it). Use `/handoff` for
everything else — work spanning several cards, not on a card yet, or in a
repo with no `tasks/` at all. When both apply, do both and name the card in
the handoff's **Next step**.

## What to do

1. **Pick the scope** (CHEATSHEET.md's HANDOFF.md convention):
   repo root (default) · `--dir <subsystem>` when the subsystem already has
   its own top-level docs (e.g. `--dir tasks`) · `--global` for `~/HANDOFF.md`
   when the work spans repos.
2. **Create the block:**
   ```bash
   python3 ~/.agents/skills/handoff/handoff.py new --title "<short title>" \
     --by <your harness> --model <your model id> [--dir ...|--global]
   ```
   It prepends a block to HANDOFF.md with the Snapshot (branch, upstream,
   PR, commits, uncommitted changes, `tasks/brief.py` output) already
   generated. Never hand-write or edit the Snapshot.
3. **Replace every `<!-- TODO ... -->`** in the new block with real content:
   - **Goal** — what the human asked for, quoting them where it matters.
   - **Done** — only what is finished *and verified*, with commit/PR/file refs.
   - **Decisions** — each choice + its reason, so it isn't re-litigated.
   - **Open / risks** — unfinished, unverified, broken, or colliding with
     another session. Say so plainly; an optimistic handoff is worse than none.
   - **Next step** — one concrete action first (a command or a file), then
     the rest in order.
   Write for a reader with zero context and possibly a weaker model: full
   paths, exact commands, no "as discussed above".
4. **Prune history:** in older blocks below yours, delete items your block
   now supersedes. If nothing in the file is pending any more, the whole
   file should be deleted instead of written (the convention: HANDOFF.md
   is not permanent).
5. **Validate:** `handoff.py check [--dir ...|--global]` must print `OK`.
   Fix and re-run until it does.
6. **Persist it:** commit HANDOFF.md alongside the work (and push if the
   repo has a remote and the user's git rules allow) — an uncommitted
   handoff in a worktree dies with the worktree.
7. **Give the human the prompt:** run `handoff.py prompt [...]` and show
   its output — one line to paste into any harness, plus ready launch
   commands for `claude` / `copilot -i` / `agy -i` / `gemini -i`.

## What NOT to do

- Don't put secrets, tokens or credentials in a handoff — it's committed.
- Don't skip `check`, and don't satisfy it with filler ("TBD", "see chat").
- Don't edit an older block to make it current — add a new block on top.
- Don't launch another session yourself unless the human asks; printing the
  prompt is the default (a launch is a real, autonomous side effect).

## Receiving a handoff

If a HANDOFF.md exists at the root of the repo or subsystem you're working
in, read its top block before starting (see
`.agents/instructions/workspace-config/handoff.instructions.md`). Trust the
narrative, but re-verify the Snapshot — it's a picture of the past.
