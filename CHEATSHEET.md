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
- [ ] **Criar fine-grained PAT** em github.com/settings/tokens?type=beta, scoped só a `dotfiles`+`architect` (`Contents: read/write`, `Pull requests: read/write`), com expiração (ex.: 90 dias). Um token por máquina chega. Depois: `gh auth login --with-token < token.txt` (correr tu mesmo, ex. via `! gh auth login --with-token < ~/token.txt`, para o token nunca aparecer numa conversa com o agente) + `gh auth setup-git`. **Status 2026-09-15: adiado pelo dono — sem prazo, será feito quando houver tempo.** Até lá, tudo o que precisa de `gh` (PR create, repo archive) fica bloqueado; push por SSH continua a funcionar normalmente.
- [x] ~~Adotar convenção `claude/<topico>` + PR~~ — SSH já autentica sem problemas (não é preciso mudar remote para HTTPS, isso só seria necessário se a autenticação fosse só via PAT/HTTPS). Estado 2026-09-15: `dotfiles` já tinha os 13 commits pendentes enviados diretamente para `main` antes desta convenção ser aplicada (histórico, não há o que retroactivamente mover para PR). `architect`: o commit pendente (`2172fe0`, "close .env leak gap and add missing google-generativeai dependency") foi movido para a branch `claude/env-leak-fix` (criada e enviada, `main` local voltou a espelhar `origin/main`) — falta abrir o PR, bloqueado por `gh auth` (item acima). URL manual entretanto: https://github.com/nmc-costa/architect/pull/new/claude/env-leak-fix
- [x] ~~Rever e dar `git push`/PR aos commits locais~~ — `dotfiles`: nada pendente, os 13 commits já estão em `origin/main` (push direto SSH, antes da convenção PR ficar ativa). `architect`: resolvido pelo item acima (branch enviada, falta só o PR).
- [ ] Arquivar `agentic_instructions` no GitHub (Settings → Archive this repository) — só depois do PR de `architect` acima e de decidir se `dotfiles` deve manter push direto ou passar a usar PRs a partir de agora.
- [ ] Decidir direção de sincronização (repo→sistema vs. sistema→repo) — em aberto, ver `CLAUDE.md` → Lacunas Conhecidas.
- [x] ~~`setup.sh` com listas de repos hardcoded (`nmc-costa`)~~ — feito 2026-09-15: `GITHUB_USER`, `WORK_REPOS`, `PROJECTS_REPOS` agora são overridable por env var, mantendo os valores atuais como default. Não requer mudanças de comportamento nesta máquina.
- [ ] **Sistema de tracking de tarefas em `tasks/`** (pedido 2026-09-15) — base do "Workspace Ágil". Planeamento + implementação ainda não começaram; o prompt de arranque está em `tasks/KICKOFF.md`, pronto a colar numa sessão nova com orquestração de agentes.

### 4.1 Backlog de `~/Projects/notes/ideas/` (trazido para aqui 2026-09-15, por ordem de prioridade da própria `ideas/README.md`)

**Importante:** isto é tracking, não trabalho aprovado para construir. Os ficheiros de `ideas/` são visão/investigação — a maioria explicitamente "ideia por validar, nada construído" (ex.: o documento do Jarvis). Antes de qualquer um destes virar código, precisa de uma sessão de scoping contigo — não é para um agente decidir sozinho o desenho de um orquestrador pessoal ou de um plano de negócio.

| Prioridade | Ideia | Ficheiro | Nota |
|---|---|---|---|
| 1 | Centralizar histórico de interação e meta-tasks (ledger partilhado) | `architecture/Workspace Agil para Agentes Multiplataforma.md` | Alimenta o Jarvis e o Digital Twin. Base de tudo o resto. |
| 1 | Adotar dotfiles como control plane | idem | Já em curso nesta própria tabela (fases 1-2 do roadmap §5 abaixo). |
| 1 | Validação `new` → `todo` para propostas de agente | idem + `agents/Agente Orquestrador - Jarvis do Diretor Humano.md` §5.3 | Regra: humano cria direto em `todo`; agente cria em `new` e pede validação. |
| 1 | Agente Orquestrador "Jarvis" (worksheets, orçamento de interrupção, ritual diário/semanal) | `agents/Agente Orquestrador - Jarvis do Diretor Humano.md` | **Nada construído.** Documento grande (18 secções) — precisa de PoC mínima (§14 do próprio doc) antes de qualquer construção maior. |
| 1 | Interface de captura de áudio live + transcrição local-first | `fast-prototyping/workspace-audio-interface.md` | MVP proposto, nada construído. |
| 1 | KVM audio listener agent (monitoriza áudio do sistema+mic, transcreve, cria issues) | `agents/KVM-audio-listener-agent.md` | Mesma família da interface acima; PoC scripts-base (`scripts/route_idea.py`, `scripts/streamline-audio-poc.sh`) já existem em `notes/scripts/`. |
| 1 | Harness > tamanho do modelo (síntese de fontes externas) | `architecture/harness-vision.md` | Próximo passo já documentado no próprio ficheiro: inserir a síntese no doc Workspace Ágil + `ideas/README.md`. Edição de docs, baixo risco — candidato fácil quando houver luz verde. |
| 2 | Digital Twin / Socratic ROI loop | `personal/My Digitaltwin - ROI AI Factory accelaration.md` | **Plano de negócio pessoal** (spin-off fora do DTX) — sensível, não é tarefa de engenharia a despachar a um agente sem ti. |
| 3 | Manter atualizado o transcript de referência (`20251203_the_architect_clean_html.md`) | idem | Só suporte de vocabulário; sem ação own.

**Regra:** ao começar uma sessão nova, pede-lhe explicitamente para ler esta lista e criar a sua todo list interna a partir dela (ver secção 7). Ao terminar uma tarefa, o commit que a fecha tem de marcar o `[x]` aqui.

### 4.2 Repo hygiene / tracking e organização (pedido 2026-09-15)

Objetivo, para cada repo: (1) raiz limpa — só `README.md` e os ficheiros que ferramentas de agente leem automaticamente por convenção (`CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `.clinerules`, etc.) ficam na raiz, o resto de `.md` solto vai para `docs/`; (2) `README.md` com directory tree atual, índice do que está em cada pasta, e uma tabela-resumo de tarefas/estado; (3) estrutura de diretórios validada contra a melhor prática pesquisada online para o tipo de repo.

| Repo | Estado antes (auditado 2026-09-15) | Tarefa |
|---|---|---|
| `dotfiles` | Raiz com 10 `.md` soltos + `README.md`; sem directory tree nem tabela-resumo no `README.md`/`CLAUDE.md` | Mover para `docs/` tudo o que não seja lido automaticamente por ferramenta; directory tree + índice + tabela-resumo no `README.md` e no `CLAUDE.md` |
| `~/Projects/architect` | `README.md` é na verdade o prompt de ativação da persona "Architect", não documentação de repo; ficheiros soltos na raiz | Criar `README.md` real com directory tree + índice; mover soltos para `docs/` |
| `~/Projects/notes` | `README.md` de 1 linha, sem índice das pastas | Directory tree + índice no `README.md` |
| `~/Work/notes` (repo da org `DTx-DSML`, não pessoal) | `README.md` de 1 linha | Directory tree + índice no `README.md` |
| `~/Projects/agentic_instructions` | — | **Excluído** — arquivado, não editar |

- [x] `dotfiles` — feito 2026-09-15, branch `claude/repo-hygiene-dotfiles`; inclui avaliador `scripts/validate_dotfiles.sh` (raiz limpa + docs obrigatórios + tree do README a bater com o disco) e secção `## Guidelines` no README com sub-secções "For you (human)" / "For agents"
- [x] `~/Projects/architect` — feito 2026-09-15, branch `claude/repo-hygiene-architect`
- [x] `~/Projects/notes` — feito 2026-09-15, branch `claude/repo-hygiene-notes`
- [x] `~/Work/notes` — feito 2026-09-15, branch `claude/repo-hygiene-worknotes`

**Nota de consistência (pedida 2026-09-15, depois dos 4 feitos em paralelo por agentes independentes) — RESOLVIDA:** cada repo tinha escolhido o seu próprio formato de README (títulos diferentes: "Directory tree"/"Structure", "Folder index"/"Index"). Unificado manualmente (não por agente, para garantir consistência real) nos 4: todos usam agora `## Directory tree` → `## What's where (index)` → `## Guidelines` (com `### For you (human)` e `### For agents`) como esqueleto comum, com secções extra específicas de cada repo a seguir. Commits: `dotfiles` (nesta branch), `architect@3f4c01e`, `~/Projects/notes@a1e1377`, `~/Work/notes@eda396c`.

- [ ] O avaliador (`scripts/validate_dotfiles.sh`) existe só no `dotfiles` por agora — replicar o mesmo tipo de check (raiz limpa + tree do README bate com o disco) para `architect`, `~/Projects/notes`, `~/Work/notes` fica por fazer, não pedido ainda.

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
