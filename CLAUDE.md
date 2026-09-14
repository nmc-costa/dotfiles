# CLAUDE.md

Orientações para Claude Code quando trabalha neste repositório.

## O Que É Este Repositório

`~/dotfiles` é o **repositório central de configuração e sincronização** para:
- Agentes de IA (Crush, Copilot, Gemini, Cline)
- Skills e workflows de agentes
- Contexto global e instruções
- Setup e automação

## Estrutura

```
dotfiles/
├── .agents/                    ← Agentes (skills/, workflows/, + harnesses/, instructions/, prompts/, automation/ — ver lacunas abaixo)
├── .claude/                    ← Configuração Claude, incl. .claude/skills/ (9 skills HITs — divergem de .agents/skills/)
├── .vscode/                    ← Configuração VS Code (settings.json contém API key — ver lacunas abaixo)
├── .github/                    ← GitHub config, duplica grande parte de .agents/
├── AGENTS.md                   ← Guia completo de agentes
├── README.md                   ← Overview
├── setup.sh                    ← One-click machine setup (hardcoded para nmc-costa)
└── sync-skills.sh              ← Sincronizar skills
```

## Projetos Reais

Os projetos vivem **fora** de dotfiles:
- **`~/Projects/`** — Repos pessoais (agentic_instructions, HIcode, ibots, roi_lab, etc.)
- **`~/Work/`** — Repos profissionais (mobai, RAGFusion, sp_xai_nos, etc.)

Cada um é um repositório git independente. Ver `directory_tree.md` para mapa completo.

## Skills Disponíveis

Skills são extensões de agentes. Localização: `~/.agents/skills/`

### diagnose-crash
- **Propósito:** Diagnosticar crashes de programas via core dumps
- **Triggers:** segfault, SIGABRT, coredumpctl, "why did X crash"
- **Ver:** `~/.agents/skills/diagnose-crash/SKILL.md`

### omarchy
- **Propósito:** Customização de Hyprland, window manager, desktop
- **Triggers:** Hyprland, hyprctl, keybindings, temas, gaps, borders
- **Ver:** `~/.agents/skills/omarchy/SKILL.md`

## Adicionar Nova Skill

1. Cria pasta:
   ```bash
   mkdir -p ~/dotfiles/.agents/skills/nova-skill
   ```

2. Adiciona `SKILL.md` (obrigatório):
   ```markdown
   # Nova Skill
   
   Descrição breve.
   
   ## Triggers
   - keyword1
   - keyword2
   ```

3. Adiciona outros ficheiros (opcional)

4. Versiona e sincroniza:
   ```bash
   cd ~/dotfiles
   git add .agents/skills/nova-skill/
   git commit -m "Add nova-skill for [propósito]"
   git push
   ./sync-skills.sh
   ```

Ver `AGENTS.md` para guia completo.

## Contexto Global

README.md/AGENTS.md descrevem `~/.context-global.md`, `~/claude.md`, `~/directory_tree.md` e `agent-versions.json` como symlinks/ficheiros do `~/dotfiles/`. **Nesta máquina nenhum destes existe** — não assumas que estão presentes sem verificar. A direção de sincronização (repo→sistema via symlinks, vs. sistema→repo) ainda não foi decidida como standard — ver secção seguinte.

## Setup Nova Máquina

```bash
cd ~
git clone https://github.com/nmc-costa/dotfiles.git dotfiles-tmp
cd dotfiles-tmp
./setup.sh --dotfiles
# Follow instructions for config checkout
```

Depois:
```bash
./sync-skills.sh
```

## Importantes

- **Não editar skills em `~/.agents/skills/`** — sempre editar em `~/dotfiles/.agents/skills/` e sincronizar
- **Skills são shared** — se adicionas nova skill, todos os agentes a veem
- **Workflows em `.agents/workflows/`** — personas e inicializações

## ⚠️ Lacunas Conhecidas (audit 2026-09-14)

Não tratar os seguintes ficheiros/afirmações como verdade atual sem verificar primeiro:

- **`AUDIT_REPORT.md` e `STANDARDS.md` têm afirmações falsas ou aspiracionais** — ex.: `AUDIT_REPORT.md` afirma "sem paths hardcoded" e "sem referências a `dtx/`", ambas contradeitas pelo conteúdo real (`.vscode/github.code-workspace`, `.github/copilot-instructions.md`). `STANDARDS.md` descreve `.copilot/`, `.gemini/`, `.cursor/`, `agent-versions.json` que não existem.
- **Decisão de sincronização em aberto**: sistema→repo vs. repo→sistema ainda não é standard. Até estar decidido, `setup.sh`/`sync-skills.sh` podem não refletir o estado real da máquina (ex.: `~/.claude`, `~/.agents`, `~/.vscode` não são symlinks nesta máquina, apesar do que README/AGENTS.md descrevem).
- **`.agents/` e `.github/` têm conteúdo duplicado e órfão** (harnesses/, instructions/, prompts/, automation/) com referências a um caminho `/my/agentic_instructions/...` que não existe neste repo nem em `~/Projects/agentic_instructions`. Tratar como legado até ser limpo — não usar como fonte de verdade.
- **`.claude/skills/` (9 skills HITs) diverge do modelo documentado** de "single source of truth em `.agents/skills/`" — `.agents/skills/` só tem `diagnose-crash` e `omarchy`. As skills HITs vivem só em `.claude/skills/`, nunca sincronizadas via `sync-skills.sh`, e diferem do conteúdo equivalente em `.github/skills/`.
- **`.vscode/settings.json` contém uma API key real** para um endpoint custom. Repo é privado/uso pessoal (risco aceite pelo dono), mas não propagar este ficheiro para outros repos, exemplos, ou contextos partilhados.
- **`setup.sh` tem listas de repos hardcoded** (`WORK_REPOS`, `PROJECTS_REPOS`) específicas de `nmc-costa` — não é portável para outro utilizador sem editar o script diretamente.

## Documentação

- **`AGENTS.md`** — Guia completo (agentes, skills, workflows, troubleshooting)
- **`README.md`** — Overview e estrutura
- **`SUBAGENTS_VERIFICATION.md`** — Checklist de setup e verificação

---

**Para projectos específicos:** Ver repos em `~/Projects/` ou `~/Work/` — cada um tem seu próprio `CLAUDE.md`.
