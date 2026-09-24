---
task_id: dotfiles-tsk-github-to-agents
title: Migrar .github/ para .agents/ e apagar .github (Copilot já lê AGENTS.md)
project: dotfiles
phase: backlog
created: "2026-09-24T14:04:22.171539+00:00"
touched: "2026-09-24T14:04:22.171539+00:00"
energy: mechanical
estimate: ""
deadline: ""
blocked_by: ""
origin: "pedido direto do owner 2026-09-24 via /task-brief (criado por claude em nome do owner): o GitHub Copilot agora usa AGENTS.md, logo .github/copilot-instructions.md deixou de ser o único standard. Âmbito: (1) fundir o conteúdo útil de .github/copilot-instructions.md (168 linhas: mermaid, session startup, session memory) em AGENTS.md/.agents/instructions e remover duplicação; (2) mover .github/skills/{model-routing-monitor,session-memory} + routing_rule_test_harness.py + routing_test_results_phase1.json para .agents/skills/ (project-doc-lifecycle, setup-dotfiles, task-brief já são symlinks para .agents/skills — só apagar); (3) atualizar as ~35 referências a .github em AGENTS.md, CLAUDE.md, README.md, CHEATSHEET.md, .gitignore, scripts/, docs/, .agents/harnesses/, .agents/instructions/, tasks/; (4) apagar .github. DECISÃO EM ABERTO: .github/workflows/vscode-docs-monitor.yml é um GitHub Actions workflow e o GitHub só corre workflows a partir de .github/workflows/ — apagar .github mata-o (e o CI de branch-naming referido no CLAUDE.md global, se existir). Opções: manter só .github/workflows/, ou remover o workflow de propósito (há scripts/setup_vscode_monitor_cron.sh como alternativa local). Confirmar também que o Copilot CLI/VS Code descobre skills em .agents/skills antes de apagar .github/skills."
---

# dotfiles-tsk-github-to-agents

Migrar .github/ para .agents/ e apagar .github (Copilot já lê AGENTS.md)

## History
- (no phase_changed events yet — still in its original created phase)
