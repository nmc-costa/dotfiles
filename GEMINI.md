# GEMINI.md

Instruções para Gemini quando trabalha neste repositório.

## Contexto

`~/dotfiles` é o repositório central de configuração e sincronização de ambiente entre máquinas. Contém:

- **Agentes:** Configurações do Crush, Copilot, Gemini, Cline em `.agents/`
- **Skills:** Extensões de agentes em `.agents/skills/`
- **Workflows:** Personas e workflows em `.agents/workflows/`
- **Contexto:** `AGENTS.md`, `CLAUDE.md`, `docs/directory_tree.md`
- **Automação:** `setup.sh`, `sync-skills.sh`

## Estrutura de Projeto

Os projetos reais vivem em:
- **`~/Projects/`** — Repos pessoais (agentic_instructions, HIcode, ibots, roi_lab, etc.)
- **`~/Work/`** — Repos profissionais (mobai, RAGFusion, sp_xai_nos, etc.)

Cada projeto é um repositório git independente com seu próprio remoto.

## Usar Este Repo

1. **Ver estrutura:** `cat ~/dotfiles/README.md`
2. **Ver skills disponíveis:** `ls -la ~/.agents/skills/`
3. **Adicionar nova skill:** Ver `AGENTS.md` > "Adicionar Nova Skill"
4. **Setup nova máquina:** `cd ~/dotfiles && ./setup.sh --dotfiles`

## Boas Práticas

- Não editar skills diretamente em `~/.agents/skills/` — sempre editar em `~/dotfiles/.agents/skills/` e sincronizar
- Para workflows pessoais: usar `~/.agents/workflows/` (symlink para `~/dotfiles/.agents/workflows/`)
- Para nuevas skills: adicionar a `~/dotfiles/.agents/skills/` e fazer `git commit + ./sync-skills.sh`

## Documentação Completa

Ver `AGENTS.md` para guia detalhado de agentes, skills, workflows e sincronização entre máquinas.
