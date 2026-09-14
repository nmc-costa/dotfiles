# STANDARDS.md

Nomenclatura, convenções e estrutura de diretórios padrão para repositórios `crush-config` (dotfiles) e `agent-framework` (agentes).

**Community Standards Base:** LangChain, Mem0, Anthropic, GitHub Copilot, OpenAI Skills

---

## 📋 GLOSSÁRIO

| Termo | Significado | Exemplo |
|-------|------------|---------|
| **Skill** | Capacidade/ferramenta discreta que um agente pode usar | `data-analyzer`, `web-research`, `code-reviewer` |
| **Agent** | Persona/entidade inteligente com habilidades específicas | `architect`, `engineer`, `reviewer` |
| **Tool** | Função/API executável (sinónimo de skill em alguns contextos) | bash, grep, file-read |
| **Prompt** | Template de instrução/contexto | system prompt, task instruction |
| **Instruction** | Regra específica de domínio (usa-se "prompt" em preferência) | — |
| **Workflow** | Sequência de passos para um agente (não usar "instruction") | agent initialization, persona setup |
| **Framework** | Sistema completo de orquestração de agentes | agent-framework |
| **Config/Configuration** | Ficheiro de settings ou dotfiles | crush-config |

---

## 📁 ESTRUTURA DE DIRETÓRIOS

### Repositório: `crush-config` (Dotfiles)

**Propósito:** Configuração estável, sincronizada entre máquinas. Referencia versões específicas do framework de agentes.

```
crush-config/
├── .agents/
│   ├── skills/                          # Skills "pinned" (symlinks para docs)
│   │   ├── diagnose-crash/
│   │   │   └── SKILL.md
│   │   └── omarchy/
│   │       └── SKILL.md
│   └── workflows/                       # Agent personas (referências)
│       ├── init.md
│       └── architect.md
├── .claude/
├── .vscode/
├── .github/
│   ├── copilot-instructions.md
│   └── workflows/
├── agent-versions.json                  # Pinning explícito
├── AGENTS.md                            # Registry + status de versões
├── CLAUDE.md                            # Contexto Claude
├── GEMINI.md                            # Contexto Gemini
├── README.md                            # Setup + estrutura
├── STANDARDS.md                         # Este ficheiro
├── AUDIT_REPORT.md                      # Compliance report
├── setup.sh
├── sync-skills.sh
└── test-subagents.sh
```

### Repositório: `agent-framework` (Desenvolvimento)

**Propósito:** Framework de agentes em desenvolvimento ativo. Source of truth para skills e workflows.

```
agent-framework/
├── skills/                              # Skills "canónicas"
│   ├── data-analyzer/
│   │   ├── SKILL.md                     # Documentação completa
│   │   ├── scripts/
│   │   │   ├── analyzer.py
│   │   │   └── utils.py
│   │   ├── references/
│   │   │   └── api-guide.md
│   │   ├── assets/
│   │   │   └── template.html
│   │   └── tests/
│   │       └── test_analyzer.py
│   └── code-reviewer/
│       └── SKILL.md
├── agents/                              # Agent definitions
│   ├── architect/
│   │   ├── AGENTS.md                    # Persona definition
│   │   ├── config.yaml                  # Agent configuration
│   │   └── references/
│   │       └── reasoning-strategy.md
│   └── engineer/
│       └── AGENTS.md
├── workflows/                           # Agent workflows/initialization
│   ├── init.md
│   ├── onboarding.md
│   └── troubleshooting.md
├── prompts/                             # Prompt templates (opcional)
│   ├── system/
│   │   └── architect-system.md
│   └── task/
│       └── code-review-task.md
├── config/                              # Global configuration
│   ├── model-config.yaml                # Model routing, token budgets
│   ├── tools-config.yaml                # Available tools registry
│   └── capabilities.json                # Feature matrix
├── scripts/                             # Utilities
│   ├── validate-skills.sh
│   ├── lint-prompts.py
│   └── publish-release.sh
├── docs/                                # General documentation
│   ├── ARCHITECTURE.md
│   ├── CONTRIBUTING.md
│   └── FAQ.md
├── package.json                         # Versioning + publishing
├── CHANGELOG.md                         # Version history
├── AGENTS.md                            # Skills registry
├── README.md
├── STANDARDS.md                         # Este ficheiro (cópia/ref)
└── .github/
    └── workflows/
        └── release.yml                  # Publish to npm/registry
```

---

## 📝 CONVENÇÕES DE NOMENCLATURA

### Nomes de Repositórios
- ✅ `crush-config` — Configuração (dotfiles) - RECOMENDADO
- ✅ `agent-framework` — Framework de agentes - RECOMENDADO
- ✅ `agents-core` — Alternativa para framework
- ❌ `agentic_instructions` — Não standard (usar `agent-framework`)
- ❌ `skills` — Ambíguo (usar dentro de `agent-framework`)

### Nomes de Diretórios
- **Kebab-case** (lowercase com hyphens): `my-skill`, `code-analyzer`, `web-research`
- **Sem espaços ou underscores**
- **Máximo 64 caracteres**

Exemplos:
```
✅ data-processor
✅ nlp-pipeline
✅ system-validator
❌ dataProcessor (camelCase)
❌ data_processor (snake_case)
❌ Data Processor (spaces)
```

### Nomes de Ficheiros

| Tipo | Pattern | Exemplo |
|------|---------|---------|
| Skill doc | `SKILL.md` | `data-analyzer/SKILL.md` |
| Agent doc | `AGENTS.md` | `agents/architect/AGENTS.md` |
| Agent config | `config.yaml` | `agents/architect/config.yaml` |
| Workflow | `[name].md` | `workflows/init.md` |
| Prompt template | `.prompt.md` | `prompts/system-prompt.md` |
| Instruction | — usar `[name].md` | `docs/best-practices.md` |
| Script | `[name].sh`, `[name].py` | `scripts/validate-skills.sh` |
| Config global | `config.yaml`, `settings.json` | `config/model-config.yaml` |

### Nomes de Skills

**Format:** `kebab-case`, descritivo, máx. 64 chars

```
✅ data-analyzer
✅ web-research
✅ code-reviewer
✅ nlp-text-processor
❌ skill-data-analyzer (redundante)
❌ DataAnalyzer (camelCase)
❌ my_data_analyzer (underscores)
```

### Nomes de Agents

**Format:** `kebab-case`, persona/role-based

```
✅ architect
✅ code-engineer
✅ security-validator
✅ project-manager
❌ Agent (demasiado genérico)
❌ my_architect (underscores)
```

---

## 📄 ESTRUTURA DE SKILL.md

Padrão emergente da comunidade (Agent Skills Spec):

```markdown
# Skill Name

Brief one-sentence description.

Longer paragraph explaining what this skill does, when to use it, and what value it provides.

## Triggers

Palavras-chave que activam a skill quando o agente as deteta:
- trigger-word-1
- trigger-word-2
- "multi-word trigger"
- regex pattern optional

## Usage

### Basic Example
```code
example_code_here
```

### Advanced Usage
```code
more_complex_example
```

## Requirements

- Required tool/capability 1
- Required tool/capability 2
- Python 3.9+ or similar

## Limitations

- Known limitation 1
- Known limitation 2

## Related Skills

- [Other Skill](../other-skill/SKILL.md)
- [Another Skill](../another-skill/SKILL.md)

## Implementation Details

How this skill is implemented, dependencies, etc.

## See Also

- Reference docs
- External links
```

**Opcional: YAML Frontmatter** (emergindo como standard)

```yaml
---
name: data-analyzer
description: Analyze and process structured data
model: gpt-4
tools: [bash, python, grep]
triggers:
  - analyze data
  - data processing
  - compute statistics
user-invocable: true
estimated-cost: medium
---
```

---

## 📄 ESTRUTURA DE AGENTS.md

**Propósito:** Registry de agentes e skills disponíveis.

```markdown
# Agents Registry

## Available Agents

| Agent | Role | Status | Version |
|-------|------|--------|---------|
| architect | System design, orchestration | Stable | 2.1.0 |
| engineer | Implementation, coding | Stable | 2.1.0 |
| reviewer | Code/design review | Stable | 1.9.0 |

## Available Skills

| Skill | Category | Triggers | Version |
|-------|----------|----------|---------|
| data-analyzer | Analytics | analyze, compute | 2.0.0 |
| web-research | Research | search, research | 1.8.0 |
| code-reviewer | Review | review, audit | 2.1.0 |

## Skill Definitions

### data-analyzer
- **Location:** `skills/data-analyzer/SKILL.md`
- **Version:** 2.0.0 (pinned in crush-config)
- **Status:** Production
- **Last Updated:** 2026-09-14

...
```

---

## 📄 ESTRUTURA DE ARQUIVO agent-versions.json

**Localização:** `crush-config/agent-versions.json`

**Propósito:** Pinning explícito de versões para reprodutibilidade entre máquinas.

```json
{
  "metadata": {
    "snapshot_date": "2026-09-14",
    "snapshot_by": "setup.sh v1.2.0",
    "crush_config_version": "1.0.0"
  },
  "framework": {
    "name": "agent-framework",
    "version": "2.1.0",
    "repository": "https://github.com/nmc-costa/agent-framework",
    "branch": "main"
  },
  "skills": {
    "data-analyzer": "2.0.0",
    "web-research": "1.8.0",
    "code-reviewer": "2.1.0",
    "omarchy": "1.0.0"
  },
  "agents": {
    "architect": "2.1.0",
    "engineer": "2.1.0",
    "reviewer": "1.9.0"
  },
  "compatibility": {
    "min_crush_version": "1.0.0",
    "min_node_version": "18.0.0",
    "supported_os": ["linux", "macos"]
  }
}
```

---

## 🔗 LINKING ENTRE REPOSITÓRIOS

### Padrão Recomendado: NPM Packages + Symlinks (Docs)

**agent-framework** publica como npm:
```json
{
  "name": "@crush/agent-framework",
  "version": "2.1.0",
  "main": "dist/index.js",
  "exports": {
    ".": "./dist/index.js",
    "./skills": "./skills/index.js",
    "./agents": "./agents/index.js"
  }
}
```

**crush-config** referencia versão específica:
```bash
# .agents/skills/ contém symlinks para documentação
ln -sf ~/agent-framework/skills/data-analyzer/SKILL.md \
       ~/crush-config/.agents/skills/data-analyzer-ref.md

# agent-versions.json pina a versão
"data-analyzer": "2.0.0"

# AGENTS.md documenta o status
## data-analyzer v2.0.0
- Status: Pinned in crush-config
- Location: @crush/agent-framework/skills/data-analyzer
```

### Fluxo de Atualização

```
1. Desenvolvimento em agent-framework/
   - Cria feature branch
   - Atualiza SKILL.md, testa
   - Merge para main
   - CI publica v2.1.1

2. Notificação automática
   - GitHub issue criada em crush-config
   - "New agent-framework: 2.1.1 available"

3. Upgrade manual em crush-config
   - Maintainer avalia CHANGELOG
   - npm install @crush/agent-framework@2.1.1
   - Testa localmente
   - Atualiza agent-versions.json
   - git commit, push
   - ./sync-skills.sh propagates

4. Outras máquinas
   - git pull
   - ./setup.sh (lê agent-versions.json)
   - Automáticamente usa v2.1.1
```

---

## ✅ CHECKLIST DE CONFORMIDADE

### Ao Criar Nova Skill

- [ ] Nome em kebab-case (máx. 64 chars)
- [ ] Directório em `agent-framework/skills/<name>/`
- [ ] `SKILL.md` presente com seções obrigatórias
- [ ] Triggers documentados
- [ ] Exemplos de uso incluídos
- [ ] Scripts em `scripts/` subdirectório
- [ ] Referências em `references/` subdirectório
- [ ] Tests em `tests/` subdirectório
- [ ] Version em `package.json` atualizada
- [ ] CHANGELOG.md atualizado
- [ ] Registado em `AGENTS.md`

### Ao Atualizar crush-config

- [ ] `agent-versions.json` atualizado
- [ ] `AGENTS.md` reflete versões pinned
- [ ] Symlinks apontam para local correto
- [ ] `./test-subagents.sh` passa
- [ ] AUDIT_REPORT.md refeito
- [ ] README.md actualizado com datas

### Git Commits

**Format:** `[repo] type: description`

```
agent-framework: Add data-analyzer skill for structured data processing
crush-config: Update agent-framework to v2.1.0
crush-config: Pin data-analyzer v2.0.0 from agent-framework
```

---

## 🔄 SINCRONIZAÇÃO

### Quando Sincronizar

| Mudança | Sincroniza Imediatamente? | Nota |
|---------|---------------------------|------|
| Patch version (2.1.0 → 2.1.1) | ✅ Sim | Bug fixes |
| Minor version (2.1.0 → 2.2.0) | ⏳ Avalia | Novas features |
| Major version (2.1.0 → 3.0.0) | ❌ Planejar | Breaking changes |
| Doc updates | ✅ Sim | Sem impacto funcional |
| Bug fix em skill já pinned | ✅ Sim | Mesmo major.minor |

### Scripts de Sincronização

```bash
# Em crush-config
./sync-skills.sh              # Copia docs/referencias
./setup.sh                    # Cria symlinks, instala versions
npm install @crush/agent-framework@2.1.0  # Pin versão
```

---

## 📚 REFERÊNCIAS

- **LangChain Standard:** github.com/langchain-ai/langchain (monorepo pattern)
- **Mem0 Pattern:** github.com/mem0ai/mem0 (plugin registry)
- **Anthropic:** Claude SDK + instructions pattern
- **Agent Skills Spec:** agentskills.io/specification
- **GitHub Copilot:** .github/{agents,skills,prompts,instructions}

---

## 📌 NOTAS FINAIS

1. **Manter Separado:** `crush-config` (estável) vs `agent-framework` (dev)
2. **Semântica Clara:** Skills/Agents, não "instructions"
3. **Versioning:** SemVer em `agent-framework`, explicit pinning em `crush-config`
4. **Documentação:** SKILL.md é o padrão (com opcional YAML frontmatter)
5. **Linking:** NPM packages + symlinks para docs (não submodules)
6. **Compliance:** Use `test-subagents.sh` e AUDIT_REPORT.md regularmente

---

**Última Atualização:** 2026-09-14  
**Baseado em:** Pesquisa comunitária (LangChain, Mem0, Anthropic, GitHub)  
**Mantido por:** nmc-costa
