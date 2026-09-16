# Kickoff: task-tracking system for the workspace

**Status:** not started. This file is the seed — read it, then plan, then build.
**Created:** 2026-09-15, at the end of a long session that built the repo-hygiene
pattern and the `workspace-standards` schema this task must comply with.

This is the prompt to paste into a **new** Claude Code session (fresh
context — cheaper than `--resume`, which reloads everything; see
`sessionHygiene` in `.agents/instructions/workspace-config/standards/workspace-standards.yaml`,
which is the default this file itself is an example of applying).

---

## Copy from here down into the new session

Lê `~/dotfiles/CLAUDE.md` e `~/dotfiles/CHEATSHEET.md` primeiro, depois este ficheiro
(`~/dotfiles/tasks/KICKOFF.md`) — é o teu ponto de partida para planear e
implementar um sistema de tracking de tarefas para todo o workspace.

### O que já está decidido, e o que ainda não está

**Decidido (não redecidir):**
- Vive em `~/dotfiles/tasks/` — pasta neste repo, **não um repo isolado**. Foi a
  instrução explícita do dono desta sessão ("parece-me claro que... uma pasta
  tasks/ no dotfiles parece ser o melhor sítio").
- É a base para as ideias em `~/Projects/notes/ideas/architecture/Workspace Agil
  para Agentes Multiplataforma.md` (doc principal) e `~/Projects/notes/ideas/agents/
  Agente Orquestrador - Jarvis do Diretor Humano.md` (camada de orquestração
  humana por cima). **Lê os dois antes de desenhar nada** — já têm decisões
  fechadas (secção "Decisões Fechadas"/`D1`-`D14` no primeiro documento) que este
  sistema tem de respeitar, não reinventar.
- Tem de cumprir o `workspace-standards.yaml` já criado nesta sessão
  (`.agents/instructions/workspace-config/standards/`) — raiz limpa, README com
  Directory tree + What's where (index) + Guidelines (For you/For agents),
  validado por `scripts/validate_workspace_standards.py`.

**Por decidir nesta próxima sessão — não assumir, resolver com investigação real:**

1. **Tensão a resolver primeiro:** o documento do Jarvis (§16, "Como Hospedar: o
   Repo é o Agente") propõe explicitamente um **repo próprio** para o Arquiteto
   com `worksheets/tarefas.csv` lá dentro — o oposto da decisão "pasta no
   dotfiles" de agora. Não ignorar isto silenciosamente: ler §16 inteira, e
   decidir explicitamente — ou (a) a pasta `tasks/` no dotfiles substitui esse
   repo próprio e o §16 fica desatualizado (dizer porquê, e corrigir esse
   documento), ou (b) `tasks/` no dotfiles é só a *camada* e o repo próprio do
   Jarvis continua a fazer sentido para outra coisa (dizer o quê). Não avançar
   com a implementação sem fechar isto.
2. **Formato:** o doc Workspace Agil já decidiu (`D9`) log de eventos append-only
   em JSONL como fonte de verdade, com SQLite/DuckDB como índice descartável —
   e nada de knowledge graph. O Jarvis propõe `tarefas.md`/`tarefas.csv` com
   colunas fixas (`id`, `título`, `projeto`, `estado`, `energia`, `estimativa`,
   `prazo`, `bloqueado_por`, `origem`, `criado`/`tocado` — ver §5.2 do Jarvis).
   Reconciliar os dois: o `tasks/` deste repo é provavelmente as *worksheets*
   (tabela mestra legível), não o log de eventos em si (que já tem casa
   decidida no D11 — repo central do workspace, que pode ou não ser este
   mesmo `tasks/`, confirmar).
3. **Escala inicial real:** este workspace já tem ~11 branches abertas em 4 repos
   à espera de PR/merge desta sessão (ver `CHEATSHEET.md` §4 e a lista de
   branches no fundo deste ficheiro) — **usa-as como as primeiras tarefas reais**
   a entrar no sistema, não dados de exemplo inventados. É o teste mais honesto
   de que o desenho aguenta uso real desde o primeiro dia.
4. **PoC mínima antes de construir tudo:** o Jarvis (§14) já defende
   explicitamente começar pela PoC mais pequena possível (worksheets estáticas,
   sem notificações, sem sessão viva) antes de qualquer automação. Segue esse
   conselho aqui também — não construir o job agendado/dispatcher antes de
   validar que a tabela em si é fiável e útil.

### Como orquestrar isto (pediu-se explicitamente agentes em paralelo)

**Fase 1 — Planeamento (bloqueia a fase 2, não saltar):**
Lança agentes em modo `Plan` (só leem/investigam, não escrevem ficheiros) em
paralelo, um por pergunta, para não perderes o dia todo a ler os documentos à
mão:
  - Um agente lê o Workspace Agil doc inteiro (é grande, ~2000 linhas) e extrai
    só o que é relevante para `tasks/`: D9, D11, §4.5, §5 (se existir; confirmar
    número da secção atual), §14.3, e a tabela de tarefas do §0.6.
  - Um agente lê o Jarvis doc inteiro e extrai: §5 (worksheets, schema de
    `tarefas.md`), §14 (PoC mínima), §16 (hospedagem — a tensão do ponto 1
    acima).
  - Um agente lê `workspace-standards.schema.json`+`.yaml` e `scripts/
    validate_workspace_standards.py` (incluindo a resolução de `extends` já
    implementada) para saber exatamente que regras `tasks/` tem de cumprir.
  - Junta os três relatórios tu mesmo (a sessão principal, não outro agente) e
    escreve um plano concreto — schema das colunas, formato de ficheiro
    (`.md` pequeno vs `.csv` acima de umas centenas de linhas, já é a regra do
    Workspace Agil doc), e a resolução explícita da tensão do ponto 1.
  - **Antes de implementar, faz `EnterPlanMode`/apresenta o plano ao dono e
    espera aprovação** — isto é uma decisão de arquitetura nova, não uma
    correção mecânica como o resto desta sessão.

**Fase 2 — Implementação (só depois da fase 1 aprovada):**
Agentes em paralelo por componente, cada um numa branch `claude/tasks-<algo>`
(nunca `main` diretamente, mesmo padrão desta sessão inteira):
  - Ficheiros base (`tasks/tarefas.md` ou `.csv`, `tasks/README.md` com o
    índice/guidelines já estabelecidos)
  - `tasks/standards.yml` (instância do workspace-standards, `extends` o
    ficheiro central)
  - Um validador próprio (`scripts/validate_tasks.py` ou semelhante — segue o
    padrão de `scripts/validate_workspace_standards.py`/`validate_dotfiles.sh`)
  - Seed real: as ~11 branches pendentes desta sessão, entradas na tabela

Depois de cada componente passar o validador, junta tudo, corre
`./scripts/validate_dotfiles.sh`, empurra a branch, dá o link de comparação —
não abras PR (`gh` não está autenticado nesta máquina, confirmar se isso mudou).

### Estado no fim da sessão anterior (2026-09-15) — verificar antes de confiar

Branches por PR, todas em `nmc-costa/dotfiles` exceto onde marcado:
- `claude/todo-continuation-and-notes-backlog`
- `claude/repo-hygiene-dotfiles`
- `claude/workspace-standards-schema` (a mais recente — este ficheiro está lá)
- `nmc-costa/architect`: `claude/env-leak-fix`, `claude/repo-hygiene-architect`, `claude/workspace-standards-schema`
- `nmc-costa/notes`: `claude/repo-hygiene-notes`, `claude/ideas-review-fixes`, `claude/workspace-standards-schema` (⚠️ esta última diverge de `repo-hygiene-notes` — ver `CHEATSHEET.md`)
- `DTx-DSML/notes`: `claude/repo-hygiene-worknotes`, `claude/workspace-standards-schema`

**Não assumir que isto ainda é verdade** — corre `git -C ~/dotfiles branch -a` (e
equivalente nos outros 3 repos) e `gh auth status` para confirmar o estado real
antes de agir sobre esta lista.

---

## Fim do que copiar

Se a sessão nova chegar a uma conclusão natural própria (ex.: fase 1 terminada,
fase 2 é um trabalho grande e independente), aplica-lhe a mesma regra
(`sessionHygiene`) — sugere sessão nova, dá um prompt de arranque, atualiza este
ficheiro ou o `CHEATSHEET.md` com o que ficou feito antes de terminar.
