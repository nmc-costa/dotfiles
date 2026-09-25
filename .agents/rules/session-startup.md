# Session startup

At the start of a session anywhere in this repository, read:

- `CHEATSHEET.md` — where things go, and §4's persistent cross-session TODO list.
- `tasks/board.md` and `tasks/README.md` — the workspace's task tracker (an
  append-only event log projected into a table). Check it for open/relevant
  work before starting something new, and append an event with
  `python3 tasks/append_event.py` when you finish something worth tracking
  there.
- `HANDOFF.md` at the repo root (or at the root of the subsystem you're
  working in), if present — read its **top block**: the previous session's
  state and next step, possibly from a different harness/model. When you stop
  with work unfinished, leave one with `.agents/skills/handoff/SKILL.md`
  (`python3 ~/.agents/skills/handoff/handoff.py new|check|prompt`).

Added 2026-09-16 as a dedicated file under `.agents/rules/*.md` — a
directory-scan convention confirmed real by a direct Antigravity diagnostic
(it walks up from the open file to the repo root looking for `GEMINI.md`,
`AGENTS.md`, and `.agents/rules/*.md`; it does not look for `CLAUDE.md`,
`CHEATSHEET.md`, or `.github/copilot-instructions.md`). The same content is
also inlined in `AGENTS.md` and `GEMINI.md` for tools that read those
instead — this file exists so a tool using only the `.agents/rules/`
convention still gets it without depending on either.
