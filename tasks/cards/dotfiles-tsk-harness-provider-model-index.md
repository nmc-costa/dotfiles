---
task_id: dotfiles-tsk-harness-provider-model-index
title: Build a validated harness x provider x model orchestration index
project: dotfiles
phase: in_progress
created: "2026-09-23T11:52:17.170402+00:00"
touched: "2026-09-23T12:00:09.249287+00:00"
energy: ""
estimate: ""
deadline: ""
blocked_by: ""
origin: ""
---

# dotfiles-tsk-harness-provider-model-index

Build a validated harness x provider x model orchestration index

## History
- 2026-09-23T11:59:38.966240+00:00: backlog -> planning (actor: nmc-costa/human) — Owner flagged high priority, requested real planning + branch execution
- 2026-09-23T12:00:09.249287+00:00: planning -> in_progress (actor: claude/agent)

## Latest handoff
_@ in_progress_

Verified reality on this machine (hostname omarchy: Intel iGPU only, 38GB RAM, no discrete GPU -- matches owner's 'Lenovo E14' profile, NOT the RTX 3070 Ti desktop, which is unverified from here). Confirmed installed via mise/which: opencode, pi, dsh (@deepseek-ai/dsh, but .agents/harnesses/deepskee.md says its integration is an unverified template), copilot (standalone CLI, no gh copilot extension installed), omp, claude. ollama installed but daemon not running, no models pulled. No aider anywhere. Only one custom provider registered (.agents/providers/registry/dtx-glm53-flash.json, GLM-5.3-Flash via LiteLLM proxy) -- no DeepSeek API/Anthropic API key/OpenRouter configured, those were the owner's pasted draft's invention. tasks/dispatch.py only dispatches claude/copilot/agy. Owner already pays for Claude Pro + Copilot Pro, wants no new metered spend. Writing tasks/harness-provider-model-index.md on branch claude/harness-provider-model-index now.
