---
task_id: dotfiles-tsk-verify-setup-skill-gaps
title: "Investigate 2 findings from first real run of setup-dotfiles/verify_setup.sh: _templates flagged missing from synced skills dirs, chezmoi status failure"
project: dotfiles
phase: review
created: "2026-09-23T12:05:14.218406+00:00"
touched: "2026-09-24T15:35:49.164078+00:00"
energy: mechanical
estimate: ""
deadline: ""
blocked_by: ""
origin: "setup-dotfiles skill dogfooding (PR #69), user-directed"
---

# dotfiles-tsk-verify-setup-skill-gaps

Investigate 2 findings from first real run of setup-dotfiles/verify_setup.sh: _templates flagged missing from synced skills dirs, chezmoi status failure

## History
- 2026-09-23T12:05:38.611692+00:00: backlog -> planning (actor: claude/agent)
- 2026-09-23T12:05:38.681225+00:00: planning -> in_progress (actor: claude/agent)
- 2026-09-24T15:35:49.164078+00:00: in_progress -> review (actor: claude/agent) — PR #76 opened: fixes both findings (_templates false-positive, stale ~/.dtx-providers refs) + adds the actor-safety docs. validate_dotfiles.sh: 35 passed, 0 failed.

## Latest handoff
_@ in_progress_

Findings confirmed: (1) _templates missing from synced skills dirs is NOT a sync.sh bug -- sync.sh intentionally requires SKILL.md per skill dir (see sync.sh:150-152 comment), _templates has none. Real bug is in verify_setup.sh's own check, which needs to mirror that same SKILL.md-presence rule. (2) chezmoi status failure was a timing artifact: PR #70 (chezmoi-source-rename) merged concurrently right after PR #69 and fixed it -- confirmed 'chezmoi status' now runs cleanly post-pull. Also need to update verify_setup.sh's stale ~/.dtx-providers references to ~/.custom_providers per that same PR.
