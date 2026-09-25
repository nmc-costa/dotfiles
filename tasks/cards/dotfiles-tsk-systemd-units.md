---
task_id: dotfiles-tsk-systemd-units
title: "ensure-tsk-sweep.sh + systemd units, following the existing ensure-*.sh convention"
project: dotfiles
phase: done
created: "2026-09-21T13:25:25.559170+00:00"
touched: "2026-09-25T21:58:26.000789+00:00"
energy: ""
estimate: ""
deadline: ""
blocked_by: dotfiles-tsk-notify-sweep
origin: ""
---

# dotfiles-tsk-systemd-units

ensure-tsk-sweep.sh + systemd units, following the existing ensure-*.sh convention

## History
- 2026-09-25T21:53:11.799822+00:00: backlog -> planning (actor: claude/agent) — Owner approved systemd timer for tsk sweep this session; blocker dotfiles-tsk-notify-sweep is done
- 2026-09-25T21:53:12.128632+00:00: planning -> in_progress (actor: claude/agent) — Starting implementation in dedicated worktree on branch claude/tsk-sweep-timer
- 2026-09-25T21:58:04.830768+00:00: in_progress -> review (actor: claude/agent) — PR #93 open: ensure-tsk-sweep.sh + tsk-sweep.{service,timer}, verified with bash -n + systemd-analyze --user verify
- 2026-09-25T21:58:25.632126+00:00: review -> validation (actor: claude/agent) — PR #93 merged (squash a3c0c70)
- 2026-09-25T21:58:26.000789+00:00: validation -> done (actor: claude/agent) — Validated live on omarchy: timer enabled, first sweep ran 22:58 (heartbeat fresh), next fire 23:00; brief.py no longer reports dead sweep

Worktrees (this machine): [worktrees/dotfiles-tsk-systemd-units.md](worktrees/dotfiles-tsk-systemd-units.md) — `python3 ~/dotfiles/tasks/worktree.py list --task-id dotfiles-tsk-systemd-units`
