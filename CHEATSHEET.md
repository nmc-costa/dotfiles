# CHEATSHEET.md

A forma de trabalhar neste workspace, num só sítio — para não teres de te lembrar. Atualiza esta tabela sempre que a estrutura de `.agents/` mudar (é regra, ver `CLAUDE.md`).

## 1. Onde vive cada coisa

| Queres... | Vai a... |
|---|---|
| Adicionar/editar uma skill (Claude Code, Copilot, Gemini) | `.agents/skills/<nome>/SKILL.md` — é a **única fonte real**. `.claude/skills/<nome>` e `.github/skills/<nome>` são symlinks para aqui, nunca edites lá. |
| Adicionar/editar uma persona ou instrução | `.agents/instructions/{base-personas,task-personas,workspace-config,automation}/` |
| Adicionar/editar um guia de harness (Claude Code, Gemini, OpenAI, LiteLLM, VS Code Copilot) | `.agents/harnesses/<nome>.md` — usa `.agents/harnesses/TEMPLATE.md` como ponto de partida |
| Adicionar/editar um prompt reutilizável | `.agents/prompts/{chronicle,_templates}/` |
| Guardar um output real (validação, exemplo de cliente, sessão) | `.agents/validation/<skill>/` — nunca em `.agents/skills/<skill>/examples/` (essa pasta é só para exemplos genéricos/anonimizados) |
| Ver o estado da fusão `agentic_instructions` → `dotfiles` | `CLAUDE.md` → secção "⚠️ Lacunas Conhecidas" |

**Regra de ouro:** se editaste algo dentro de `.claude/skills/` ou `.github/skills/` diretamente, editaste um symlink partido conceptualmente — o ficheiro real está em `.agents/skills/`. Confirma com `readlink -f <caminho>` antes de editar se tiveres dúvidas.

## 2. Adicionar uma skill nova (fluxo completo)

```bash
mkdir -p ~/dotfiles/.agents/skills/nova-skill
cat > ~/dotfiles/.agents/skills/nova-skill/SKILL.md <<'EOF'
---
name: nova-skill
description: <o que faz e quando usar>
---
EOF

# symlink para os outros harnesses lerem também
ln -s ../../.agents/skills/nova-skill ~/dotfiles/.claude/skills/nova-skill

cd ~/dotfiles
git add .agents/skills/nova-skill/ .claude/skills/nova-skill
git commit -m "Add nova-skill for [propósito]"
git push
```

## 3. Os 3 repos e o papel de cada um

| Repo | Papel | Estado |
|---|---|---|
| `~/dotfiles` | Repo de controlo único: config de sistema + `.agents/` (skills/instruções/harnesses/validação) como fonte de verdade | Ativo, é aqui que trabalhas daqui em diante |
| `~/Projects/agentic_instructions` | Biblioteca original de personas/skills | **Arquivado** (conteúdo já fundido para `dotfiles/.agents/`) — não editar, só consultar histórico |
| `~/Projects/architect` | Playground pessoal de investigação sobre a persona "The Architect"/memória/auto-avaliação | Separado, não fundido — tem um padrão de testes "vermelho por design" que vale a pena copiar para `.agents/validation/` no futuro, mas o conteúdo em si (memory/, evolution/, architect_log/) fica lá |

## 4. TODO list persistente (fonte de verdade entre sessões)

A lista de tarefas que o Claude Code cria numa sessão (a ferramenta de tracking interna) **não sobrevive a uma sessão nova** — só sobrevive com `--resume`/`--continue`, que recarrega tudo (o oposto de poupar tokens). Esta tabela é o substituto persistente: qualquer sessão nova lê isto, recria a sua própria todo list interna a partir daqui, e **risca aqui** (não só na sessão) quando um item fica feito.

- [x] Migrar `.vscode/settings.json` (API key) para chezmoi+age — feito 2026-09-14, commit `ef2a52f`. Falta: fazer backup da chave privada (`~/.config/chezmoi/key.txt`) para um gestor de password ou cópia física — **isto é manual, ninguém o faz por ti**.
- [ ] Rever e dar `git push` aos commits locais em `dotfiles` (12 commits) e `architect` (1 commit) — nada foi enviado ainda para o remoto.
- [ ] Arquivar `agentic_instructions` no GitHub (Settings → Archive this repository) — só depois do push acima.
- [ ] Decidir direção de sincronização (repo→sistema vs. sistema→repo) — em aberto, ver `CLAUDE.md` → Lacunas Conhecidas.
- [ ] `setup.sh` com listas de repos hardcoded (`nmc-costa`) — conhecido, não bloqueante, só importa se partilhares o repo.

**Regra:** ao começar uma sessão nova, pede-lhe explicitamente para ler esta lista e criar a sua todo list interna a partir dela (ver secção 7). Ao terminar uma tarefa, o commit que a fecha tem de marcar o `[x]` aqui.

## 5. Roadmap do "Workspace Ágil" (ordem validada nas tuas notas — `~/Projects/notes/ideas/architecture/Workspace Agil para Agentes Multiplataforma.md` §13.7)

Não saltar fases — cada uma é pré-requisito da seguinte. O otimizador autónomo ("OS vivo") é a **última**, não a primeira.

| Fase | O quê | Estado neste workspace |
|---|---|---|
| 1. Ver | `agtop` + Langfuse/OTel do Claude Code | Por fazer |
| 2. Arrumar | chezmoi + regras partilhadas + segredos | **Em curso** (TODO #1 acima) |
| 3. Limitar | Perfis de limites por máquina, `RandomizedDelaySec` | Por fazer |
| 4. Agendar | Manifesto `jobs/*.yaml` + systemd timers | Por fazer |
| 5. Estruturar | Esquema comum tarefa→swarm→agente→modelo→estado | Por fazer |
| 6. Julgar | Critérios de aceitação verificáveis | Por fazer |
| 7. Escolher | **Routing de modelos por custo/performance** — `LiteLLM Router` (não RouteLLM, sem manutenção desde 2024). Local: Ollama + Qwen3-Coder-30B (24GB VRAM) ou Qwen3-8B (8GB). Cloud: DeepSeek V4 (barato/volume), Claude Sonnet 5 (default), Claude Opus 5 (raciocínio difícil) | Documentado, por instalar |
| 8. Otimizar | GEPA sobre uma skill real, medindo antes/depois | Por fazer — depende de 4-6 estarem feitas; evidência independente diz que ganhos em multi-agente são instáveis, medir antes de confiar |

## 6. Como manter isto vivo

Esta tabela apodrece como qualquer doc estático se ninguém a atualizar. A regra fica no `CLAUDE.md`: qualquer sessão que mude a estrutura de `.agents/` (nova skill, novo harness, resolução de um TODO) atualiza esta tabela no mesmo commit — não depois, não "quando der jeito".

## 7. Saltar para sessão nova sem perder o fio (poupar tokens)

1. Fecha/ignora a sessão atual — não precisas de `/compact` nem de `--resume`. Abre uma sessão nova (`claude`, sem `--resume`/`--continue`, contexto limpo).
2. Primeira mensagem, sempre:
   > "Lê `~/dotfiles/CLAUDE.md` e `~/dotfiles/CHEATSHEET.md`. Cria uma todo list a partir da secção 4 (TODO list persistente) e continua a partir daí."
3. A sessão nova cria a sua própria todo list interna (ferramenta de tracking do Claude Code) espelhando a secção 4 — isso mantém-na focada e visível para ti dentro dessa sessão.
4. Quando um item fica feito, tem de ser marcado `[x]` **aqui**, na secção 4, no mesmo commit que o fecha — a todo list interna da sessão morre com ela; esta tabela é a que sobrevive.
