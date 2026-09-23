---
task_id: dotfiles-tsk-spike-herdr-commander-build
title: "Spike (hands-on): patch herdr-commander to overlay placement, wire real .vscode/tasks.json, verify picker end-to-end"
project: dotfiles
phase: done
created: "2026-09-23T21:37:34.416378+00:00"
touched: "2026-09-23T22:03:01.173023+00:00"
energy: deep
estimate: ""
deadline: ""
blocked_by: ""
origin: me
---

# dotfiles-tsk-spike-herdr-commander-build

Spike (hands-on): patch herdr-commander to overlay placement, wire real .vscode/tasks.json, verify picker end-to-end

## History
- 2026-09-23T21:41:06.833393+00:00: backlog -> planning (actor: claude/agent)
- 2026-09-23T21:41:11.593189+00:00: planning -> blocked (actor: claude/agent)
- 2026-09-23T22:02:36.300293+00:00: blocked -> in_progress (actor: claude/agent) — cargo-missing block was a false negative (PATH do mise em processo de fundo); build, patch overlay, herdr plugin link e teste do picker ja tinham sido feitos com sucesso
- 2026-09-23T22:02:41.861600+00:00: in_progress -> review (actor: claude/agent) — build+overlay+link+picker test confirmados; cleanup (pane close, unlink) feito e reverificado; veredito escrito em tasks/evaluations/herdr-commander/README.md
- 2026-09-23T22:02:54.825853+00:00: review -> validation (actor: claude/agent)
- 2026-09-23T22:03:01.173023+00:00: validation -> done (actor: claude/agent)

## Latest handoff
_@ blocked_

🛑 Blocked: cargo not available on this machine. Required for step 1: 'cargo build --release'. Check system setup or move this spike to a machine with Rust toolchain installed.
