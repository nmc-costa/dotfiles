---
task_id: dotfiles-tsk-chezmoi-config-drift
title: "Corrigir ~/.config/chezmoi/chezmoi.toml pos-PR1 (destDir=$HOME, sourceDir=home/) + limpar ~/dotfiles/.dtx-providers/ + corrigir PROVIDERS.md e render-litellm-config.sh"
project: dotfiles
phase: done
created: "2026-09-23T12:03:34.482691+00:00"
touched: "2026-09-23T12:03:53.628656+00:00"
energy: ""
estimate: ""
deadline: ""
blocked_by: ""
origin: ""
---

# dotfiles-tsk-chezmoi-config-drift

Corrigir ~/.config/chezmoi/chezmoi.toml pos-PR1 (destDir=$HOME, sourceDir=home/) + limpar ~/dotfiles/.dtx-providers/ + corrigir PROVIDERS.md e render-litellm-config.sh

## History
- 2026-09-23T12:03:38.393039+00:00: backlog -> planning (actor: nmc-costa/human)
- 2026-09-23T12:03:41.820549+00:00: planning -> in_progress (actor: nmc-costa/human)
- 2026-09-23T12:03:45.567554+00:00: in_progress -> review (actor: nmc-costa/human) — PRs #70, #71 fundidas; chezmoi.toml corrigido na maquina real, chezmoi apply confirmado no-op, .dtx-providers duplicado removido
- 2026-09-23T12:03:49.083860+00:00: review -> validation (actor: nmc-costa/human)
- 2026-09-23T12:03:53.628656+00:00: validation -> done (actor: nmc-costa/human)

## Latest handoff
_@ done_

chezmoi.toml corrigido (destDir=$HOME, sourceDir=.chezmoi-source), chezmoi diff confirmado vazio, .dtx-providers duplicado removido. Bonus: bug real de permissoes (0644 vs 0600 esperado) encontrado e corrigido na fonte (PR #71) - faltava o prefixo private_ no proprio ficheiro, so estava na pasta.
