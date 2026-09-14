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
├── .agents/                    ← Agentes
│   ├── skills/                 ← Skills (diagnose-crash, omarchy, etc.)
│   └── workflows/              ← Personas e workflows (init.md, architect_html_sciml.md)
├── .claude/                    ← Configuração Claude
├── .vscode/                    ← Configuração VS Code
├── .github/                    ← GitHub config (copilot-instructions.md, etc.)
├── AGENTS.md                   ← Guia completo de agentes
├── README.md                   ← Overview
├── setup.sh                    ← One-click machine setup
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

Ficheiros de contexto para agentes (symlinks do `~/dotfiles/`):
- `~/.context-global.md` — Contexto geral
- `~/claude.md` — Instruções Claude
- `~/directory_tree.md` — Mapa de diretórios

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

## Documentação

- **`AGENTS.md`** — Guia completo (agentes, skills, workflows, troubleshooting)
- **`README.md`** — Overview e estrutura
- **`SUBAGENTS_VERIFICATION.md`** — Checklist de setup e verificação

---

**Para projectos específicos:** Ver repos em `~/Projects/` ou `~/Work/` — cada um tem seu próprio `CLAUDE.md`.
