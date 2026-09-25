# 🔌 Antigravity Reference

**Status:** partially verified 2026-09-16, via a direct diagnostic prompt
run against the actual tool (not inferred from docs). Confirmed real:
Antigravity's own self-report of its directory-scan mechanism (see
"Confirmed Discovery Mechanism" below). **Not yet resolved:** in the same
test session, Antigravity reported reading zero files automatically at
startup, even though it also described a mechanism that should have picked
up `AGENTS.md`/`GEMINI.md` — it flagged this itself as conditional on the
session starting inside the actual working tree root, and on "the top-level
rule-injection mechanism" firing. Re-test from inside `~/dotfiles` itself
(not a parent or unrelated directory) before trusting that the fix below is
fully live; if it still reports nothing auto-loaded, treat this file's
mechanism description as real but not yet actually wired for you.

---

## Confirmed Discovery Mechanism (Antigravity's own self-report, 2026-09-16)

Two formal mechanisms, per the tool itself:

1. **Directory/workspace rules:** walks up from the open file / working
   directory to the repo root, looking for fixed filenames:
   - `GEMINI.md` and `AGENTS.md`
   - Files under `.agents/rules/*.md`
2. **Skills/workspace-extension discovery:** looks for a fixed-name folder
   at the repo root: `.agents/` (or `.agent/`, `_agents/`, `_agent/`).

**Confirmed NOT scanned for:** `CLAUDE.md`, `CHEATSHEET.md`,
`.agents/AGENT.md` (Copilot-only). Don't add pointers there expecting
Antigravity to see them — it won't.

Given this, the session-startup fix lives in three places, redundantly, so
whichever mechanism actually fires for a given session picks it up:
- `AGENTS.md` (sessionHygiene section)
- `GEMINI.md` ("At the start of a session, also read")
- `.agents/rules/session-startup.md` (dedicated, matches the
  `.agents/rules/*.md` glob directly)

No more manual first-message prompt needed *if* one of the three above is
actually being picked up — verify with the re-test described in Status
above before assuming it's live.

---

## Workspace Configuration (Global)

Regardless of harness, these rules apply repo-wide, defined under
`.agents/instructions/workspace-config/`:

- **Model Routing** — `.agents/instructions/workspace-config/model-routing.instructions.md`
- **Daily Optimization** (chronicle workflow) — `.agents/instructions/workspace-config/daily-optimization.instructions.md`
- **Token Tracking** — `.agents/instructions/workspace-config/token-tracking.instructions.md`
- **Mermaid Diagrams** — `.agents/instructions/workspace-config/mermaid.instructions.md`

## Task-Specific Skills

```
Trigger          | Skill          | Purpose
─────────────────┼────────────────┼─────────────────────────────
@projectHITs     | projecthits    | Project charters + WPs
@presentHITs     | presenthits    | Executive presentations
@reviewHITs      | reviewhits     | Peer review & critique
@diagramHITs     | diagramhits    | Mermaid diagrams
@documentHITs    | documenthits   | Documentation synthesis
@mockupHITs      | mockuphits     | Interactive prototypes
@architect       | archi          | Meta-orchestrator, coordinates the rest
```

Confirmed 2026-09-16: Antigravity discovers the `.agents/` folder by name
for skills/extensions (see above), so `.agents/skills/` should already be
reachable without a symlink — not yet confirmed whether it recognizes the
`@mention` trigger syntax above or needs keyword-based intent detection
instead (the fallback `gemini.md` also proposes).

## Discovery

No central `REGISTRY.md` in this repo — browse instead:

- Skills: [`.agents/skills/`](../skills/)
- Instructions: [`.agents/instructions/`](../instructions/)
- Harnesses: [`.agents/harnesses/`](.)

## Deployment Checklist

- [x] Confirm Antigravity's real discovery mechanism — done 2026-09-16 via
      direct diagnostic, see above
- [x] Add the Session Startup pointer to files it actually scans
      (`AGENTS.md`, `GEMINI.md`, `.agents/rules/session-startup.md`)
- [ ] Re-test from inside `~/dotfiles` to confirm the pointer is actually
      picked up automatically now (the first diagnostic showed the
      mechanism exists but reported nothing auto-loaded in that session)
- [ ] Confirm whether the `@mention` skill-trigger table above works as-is
      or needs a keyword-based fallback
- [ ] Master persona (`.agents/instructions/base-personas/archi.md`) —
      confirm Antigravity actually reads into `.agents/instructions/` once
      it discovers the `.agents/` folder, or only `.agents/skills/`
