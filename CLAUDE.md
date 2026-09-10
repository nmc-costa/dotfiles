# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

`/home/user/github` is the user's **umbrella workspace**, not a single
application. The top-level git repo (`main`) has no commits and exists only to
hold workspace-level config, instructions, and tooling. The real projects live in
subdirectories, several of which are **independent git repos with their own
remotes** — treat each as its own project and run git/tests from inside it.

Top-level layout (by the user's own description):

| Path | Purpose |
|------|---------|
| `dtx/` | **Work-related** repos. Projects sit under `dtx/repos/` (e.g. `sp_xai_nos`, the active folder in `.vscode/github.code-workspace`; `technopage`, `RAGFusion`, `mobai`, `BAI`, …). |
| `my/` | The user's **personal** repos and material. |
| `architect/` | The user's attempt to build an **AGI system** ("a step above OpenClaw") — persona + cognitive/memory architecture experiment. Own repo: `github.com/nmc-costa/architect`. |
| `scripts/` | **Workspace-level tooling** — gives agents ready-made tools to carry out the master instructions (currently the VS Code Docs Monitor). |
| `temp/` | **Temporary scratch files — safe to delete.** Do not build anything durable here. |
| `.github/`, `.agent/`, `.vscode/`, `.claude/` | Workspace config and agent/persona references (see below). |

Notable project repos:

| Path | Remote | What it is |
|------|--------|------------|
| `my/agentic_instructions/` | `github.com/nmc-costa/agentic_instructions` | Multi-harness agent-enforcement framework (the most structured project here) |
| `architect/` | `github.com/nmc-costa/architect` | AGI / "The Architect" cognitive-memory system |
| `dtx/repos/sp_xai_nos/` | its own `.git` | Explainable-AI PoC — soccer highlight detection, Streamlit UI, SHAP/LIME + LLMs. Run: `streamlit run src/deployment/user_interfaces/main.py`. Has `run_tests.sh`, coverage/codecov. This is the **reference implementation** for the agentic_instructions "sp_xai_nos standard". |
| `dtx/repos/mobai/` | its own `.git` | Data-intensive project on the HIcode framework; PySpark + TensorFlow |

Each project subrepo has its own `requirements.txt` and is usually installed
editable (`pip install -e .`) from its own root.

## Areas of `my/`

- **`my/agentic_instructions/`** — see dedicated section below.
- **`my/HIcode`, `my/HITnode`, `my/ibots`, `my/hicode-kedro`, `my/roi_lab`** —
  Python ML-pipeline codebases/templates by `nmc-costa` (`simplifyhit™`).
  Node-based `fit`/`transform`/`predict` interfaces, CRISP-DM / CRISP-ML(Q)
  directory conventions. `ibots` and `hicode-kedro` are Kedro 0.19.x projects.
  Each has its own `requirements.txt` / `pyproject.toml` and `tests/`.
- **`my/sciml_combinatorial_search`, `my/pocs`, `my/calls`, `my/jobs`** — client
  and research material (TechnoPhage, DTx, Siemens); mostly documents, HTML
  "maquetes", and PDFs, often bilingual PT/EN.
- **`.agent/workflows/`, `architect/`** — persona/prompt material for other
  agents (Gemini, Cline); not code to build.

## Common commands

Agentic-instructions compliance tests (run from `my/agentic_instructions/`):

```bash
cd my/agentic_instructions
pytest tests/agents/ -v                                       # full suite
pytest tests/agents/test_hardcoding_violations.py -v          # single file
pytest tests/agents/test_code_organization.py -v -k "<expr>"  # subset
python3 scripts/audit_instruction_health.py                   # persona lint
python3 scripts/harness-installer.py --harnesses gemini,claude-code
./scripts/deploy-agentic-framework.sh /target/project
```

VS Code Docs Monitor (run from workspace root):

```bash
pip install -r requirements.txt
python3 scripts/monitor_vscode_docs.py --force --verbose \
  --cache-dir .github/.vscode-docs-cache \
  --memory-file my/agentic_instructions/memories/VSCODE_WEEKLY.md
bash scripts/setup_vscode_monitor_cron.sh   # install local weekly cron
```

Kedro subprojects (`my/ibots`, `my/hicode-kedro`):

```bash
pip install -r requirements.txt
kedro run
pytest
```

Testing across the workspace is **pytest** (`.vscode/settings.json` enables it;
`unittest` disabled). `.mypy_cache` indicates mypy is used ad hoc.

## The agentic_instructions framework

A framework to make any LLM harness (VS Code Copilot, Claude Code, Gemini,
OpenAI, LiteLLM) follow a shared set of personas and standards. Understanding it
requires reading `my/agentic_instructions/REGISTRY.md` first — it is the
discovery index mapping every persona, agent, skill, tool, and harness.

Key structure:

- **`instructions/base-personas/archi.md`** — the master "Architect" persona that
  every task persona inherits (biofeedback header, dialectical
  thesis/antithesis/synthesis, `[ORIGIN: DIRECTOR|WEAVER]` tagging).
- **`instructions/task-personas/*.md`** — `projectHITs` (project charters, v4),
  `presentHITs` (HTML slides), `reviewHITs` (peer review), `diagramHITs`
  (Mermaid), `documentHITs`, `mockupHITs`. Triggered by `@name` or natural
  phrases (see REGISTRY).
- **`agents/<name>/SKILL.md`** — the corresponding executable agents;
  `agents/architect` is the meta-orchestrator.
- **`instructions/workspace-config/*.instructions.md`** — single source of truth
  for workspace-wide rules (model routing, token tracking, daily optimization,
  Mermaid — mostly Copilot-targeted, see "Copilot-only machinery" below).
  Everything under the workspace's `.github/` (`copilot-instructions.md`,
  `instructions/README.md`, `harnesses/`) is a **thin reference** that points
  here — this is the "Hybrid C" architecture. Edit the centralized file, never
  the `.github/` copy.
- **`config/harness-config.json`** + `config/.harnesses/<harness>.json` — master
  config plus per-harness overrides.
- **`versions/`** — archived persona iterations (v1–v4); do not resurrect.
- **`scripts/projectHITs/v4/`** — the current charter-generation pipeline
  (`orchestrate.py`, `compiler.py`, `mirror_generator.py`, etc.).

`tests/agents/` enforces the framework's own rules: file-authorization,
architecture/diagram strategy, zero-hardcoding, code organization, config
validity. `tests/agents/conftest.py` resolves `project_root` as
`my/agentic_instructions/`. See that repo's own `CLAUDE.md` for the full
"sp_xai_nos standard" contract and the `.copilot-instructions` session ritual.

## Using the personas in Claude Code

The agentic_instructions personas are wired into this workspace as **Claude Code
skills** in `.claude/skills/`. Each is a thin wrapper whose only job is to load
the canonical persona + agent files from `my/agentic_instructions/` — the single
source of truth stays there, so editing the framework updates the skills for
free. Never copy persona content into `.claude/skills/`.

| Skill | Persona / agent it loads | What it does |
|-------|--------------------------|--------------|
| `/archi` | `base-personas/archi.md` + `agents/architect` | Master Weaver persona + meta-orchestrator; routes to the others |
| `/projecthits` | `task-personas/projectHITs.md` + `agents/projectHITs` | Charters, work packages, template mirroring, `[TODO]` gap tracking |
| `/presenthits` | `task-personas/presentHITs.md` + `agents/presentHITs` | Executive HTML slide decks (Tailwind), PPTX export |
| `/reviewhits` | `task-personas/reviewHITs.md` + `agents/reviewHITs` | Six-dimensional academic peer review |
| `/diagramhits` | `task-personas/diagramHITs.md` + `agents/diagramHITs` | Mermaid / ontology / architecture diagrams |
| `/documenthits` | `task-personas/documentHITs.md` + `agents/documentHITs` | In-place updates to DOCX and formal documents |
| `/mockuphits` | `task-personas/mockupHITs.md` + `agents/mockupHITs` | Interactive SciML HTML prototypes ("maquetes") |
| `/simplifyhit` | `skills/simplifyHIT` | Optimize system instructions / personas themselves |
| `/project-doc-lifecycle` | `skills/project-doc-lifecycle` | Validate a charter/WP against its brief, then compile to `.docx` |

Invoke with the slash command (`/projecthits`), or just describe the task — the
descriptions carry the original `@name` triggers and trigger phrases ("create
charter", "peer review", "maquete", …).

**These personas impose a response format.** While one is active, follow its
mandatory calibration header (`SYSTEM INSTRUCTION: MODE [...] ACTIVE` / `STATUS`
/ `RESONANCE` / `DIALECTIC` / `ANALYSIS` / `TIMESTAMP`), the dialectical
thesis→antithesis→synthesis method, and `[ORIGIN: DIRECTOR|WEAVER]` tagging.
Outside these skills, answer normally — don't carry the header into ordinary
coding work.

When adding a persona to `my/agentic_instructions/`, add the matching wrapper in
`.claude/skills/` and the row above, so Claude Code keeps parity with REGISTRY.md.

## Instruction files across the workspace

- **`.github/prompts/agents_base_intructions.prompt.md`** — the *canonical
  cross-repo base agent prompt*: prefer minimal low-risk changes; when you touch
  code, add/update tests (happy path + ≥1 edge case) and verification steps; make
  at most two explicit assumptions when under-specified; report build/test/lint
  results; don't force-fix unrelated failures.
- **`GEMINI.md` (root)** and **`.github/copilot-instructions.md`** are the same
  workspace guidance written for other agents. This `CLAUDE.md` is the Claude Code
  equivalent — keep the three roughly consistent when the workspace changes.
- **`.github/instructions/`, `.github/harnesses/`** — thin pointers into
  `my/agentic_instructions/`. `.github/skills/` and `my/agentic_instructions/`
  hold the real skill/persona definitions.

**Copilot-only machinery — does not apply to Claude Code.** The
`copilot-instructions.md` / `instructions/workspace-config/` files describe a
VS Code Copilot setup: `/chronicle` chat commands, the `session_store_sql` /
`runSubagent` tools, `/memorize` + `/recall` VS Code skills, and a "route Haiku
vs GPT-5/Gemini" model-routing + token-tracking regime. None of those tools or
commands exist in Claude Code — don't try to invoke them. Claude Code has its own
memory and subagents; use those instead.

## Conventions

- **Bilingual (PT/EN).** Client-facing docs (INCM project charters, work
  packages; TechnoPhage/DTx material) are formal Portuguese/English — preserve a
  document's original language. Detect the language from the user's first message
  and stay consistent.
- **`md → docx`** conversions use the helper scripts in `scripts/` and
  `my/agentic_instructions/scripts/projectHITs/` — don't hand-roll the format.
- **HIcode principles** (DRY, KISS, consistency, testing) govern the Python
  codebases in `my/` and `dtx/`; match the surrounding node-pipeline structure.

## Other agent configs present

A Gemini CLI config exists at `~/.gemini/` (`settings.json`, `GEMINI.md`). If you
want its user-level items (MCP servers, commands, subagents, skills,
instructions) imported into Claude Code, reply `/import` to scan and list what's
importable, then `/import --yes=<digest>` to apply.

---

## 🏆 Claude Code — Cheat Table (Oficial, Underground & Atalhos)

> Referências: [ykdojo/claude-code-tips](https://github.com/ykdojo/claude-code-tips) · [Anthropic Cheatsheet](https://support.claude.com/en/articles/14553413-claude-code-cheatsheet) · [Claude Code Ultimate Guide](https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/cheatsheet.md) · [Njengah cheat-sheet](https://github.com/Njengah/claude-code-cheat-sheet)

| Categoria | Atalho / Comando / Sintaxe | O que faz na prática | ⚡ Por que a Comunidade Usa (Impacto Pro) |
|---|---|---|---|
| Troca Rápida de Modos | `Shift + Tab` | Alterna entre: Manual ➔ acceptEdits ➔ Plan Mode. | Evita gastar tokens codando errado: no Plan Mode, ele apenas lê e projeta sem tocar em nada. |
| Rebobinar / Desfazer | `Esc + Esc` | Abre o menu nativo de checkpoint / rewind. | Descarta o rascunho com erro e volta a sessão para o estado anterior, limpando tokens desperdiçados. |
| Edição de Prompt Externo | `Ctrl + G` | Abre seu editor padrão (VS Code/Nano) para escrever o prompt. | Ideal para rascunhar especificações complexas sem limitações da linha do terminal. |
| Histórico de Transcrição | `Ctrl + O` | Abre o visualizador do histórico detalhado de transcrição. | Inspeciona o que foi dito/feito em sessões anteriores. |
| Modo Fundo (Background) | `Ctrl + B` | Joga o Claude para rodar em segundo plano durante testes demorados. | Libera o terminal enquanto o agente processa tarefas longas. |
| Economia de Tokens (Anti-Chat) | Prompt: `"Use Caveman Mode"` | Força o Claude a eliminar rodeios, cortesias e saudações. | Corta até 40% de tokens de saída, fazendo sua janela Pro durar o dobro. |
| Memória Instantânea | `# [instrução]` (ex: `# Use Bun`) | Injeta uma regra na auto-memória sem abrir o arquivo. | Forma mais rápida de gravar regras globais sem poluir o CLAUDE.md. |
| Modularização de Regras | `.claude/rules/*.md` | Quebra regras do projeto em arquivos temáticos pequenos. | Evita carregar o contexto inteiro de uma vez; o Claude só puxa a regra necessária. |
| Prevenção de Inchaço | Arquivo `.claudeignore` | Bloqueia leitura de `node_modules`, `dist`, logs e mídias. | Obrigatório. Sem isso, 2 ou 3 comandos esgotam toda a franquia Pro. |
| Compensação Guiada | `/compact [foco]` (ex: `/compact auth`) | Resume a conversa preservando apenas o contexto pedido. | Libera janela de contexto mantendo vivo exatamente o módulo em que você está trabalhando. |
| Retomar Sessão | `/resume` | Retoma a última sessão salva ou um marcador específico. | Volta ao ponto exato de trabalho sem repetir contexto. |
| Troca de Tarefa com Rótulo | `/clear [nome]` (ex: `/clear feature-x`) | Reseta o contexto e salva um marcador na sessão. | Permite usar o `/resume` mais tarde para voltar àquela tarefa. |
| Inspeção de Custos & Contexto | `/context` e `/cost` | Mostra gráfico do uso da memória e tokens consumidos. | Permite ver qual arquivo está inflando a sessão antes de estourar a cota. |
| Diagnóstico de Inchaço | `/doctor` | Faz auditoria geral de instalação, hooks e inchaço do CLAUDE.md. | Alerta caso suas regras estejam longas demais gastando tokens à toa. |
| Revisão Rápida sem Git | `/diff` | Abre um visualizador interativo das alterações feitas pelo Claude. | Inspeciona mudanças arquivo a arquivo sem precisar rodar comandos git manuais. |
| Subagentes Isolados | `/agents` | Cria agentes customizados para tarefas específicas (testes, docs). | Executa buscas e testes em um sub-contexto separado, sem inchar sua conversa principal. |
| Execução em Pipeline | `cat log.txt \| claude -p "resumo"` | Executa uma ordem direto no terminal e finaliza sem abrir o chat. | Economiza chamadas interativas para automações de terminal, CI/CD ou scripts. |
| Multi-threading Físico | `git worktree` + novas abas | Abre diretórios paralelos apontando para branches diferentes. | Permite ter uma instância corrigindo testes enquanto outra constrói código novo. |

### ⌨️ Atalhos de Teclado — Cola Rápida

| Atalho | Ação |
|--------|------|
| `Shift + Tab` | Alterna modo de permissão: Manual → Auto-Accept → Plan |
| `Ctrl + G` | Abre o prompt no VS Code / Nano |
| `Ctrl + O` | Abre o visualizador do histórico de transcrição |
| `Ctrl + B` | Envia o Claude para segundo plano durante testes longos |
| `Esc + Esc` | Abre o menu de checkpoint para voltar no tempo |
