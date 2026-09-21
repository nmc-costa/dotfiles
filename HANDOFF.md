# HANDOFF — dotfiles (agent-OS unification + repo conventions)

**Data:** 2026-09-21. Este ficheiro é o handoff do repo `~/dotfiles` como um
todo — não é permanente, atualiza-se in place, apaga-se/arquiva-se quando a
lista "por fazer" ficar vazia. Ponto de entrada global: `~/HANDOFF.md`.

## Correção importante face ao handoff anterior

Este ficheiro **substituiu** o antigo `~/handoff.md` (fora de qualquer repo
git, só nesta máquina) — mesclado via PR #37, `~/handoff.md` já apagado
(2026-09-21, confirmado presente este ficheiro antes de apagar o antigo).

## Trabalho ativo #1 — Unificação agente-OS (PR1-PR7)

Ver `docs/AGENT_OS_UNIFICATION_PLAN.md` para o plano completo (7 decisões
já tomadas). Estado, verificado com `gh pr view 34` em 2026-09-21:

- ✅ Plano mesclado, backup da chave age feito (#24, #29).
- **PR1 (#34) — `claude/pr1-chezmoi-migration` — ABERTO, por rever.** Não
  mesclado. Implementado e testado nesta máquina (`./scripts/validate_dotfiles.sh`
  30/30), mas o passo manual pós-merge (`chezmoi.toml`, `chezmoi apply`,
  limpar `.vscode/settings.json` órfão — ver corpo da PR / `docs/SECRETS.md`)
  só se aplica depois do merge.
- PR2-PR7: nada começado. PR2 precisa do hostname + specs de monitor das
  outras 2 máquinas Omarchy do dono antes de escrever `machines.toml`.
- Convenção desta sequência: **um PR de cada vez, parar para revisão do
  dono entre cada um** — não mesclar automaticamente mesmo com autorização
  geral de merge.

## Trabalho ativo #2 — subsistema `tasks/` (orquestração de tarefas)

PR #30 já mesclou entretanto (`tasks/handoff.md` v4, Onda 1 fechada,
PRs #28/#30-#33/#35 fundidas — ver `tasks/HANDOFF.md`, renomeado nesta PR).

**Descoberta importante ao fazer o rename** (2026-09-21): existe agora um
design novo, `tasks/plans/claim-protocol.md`, produzido depois de um
incidente real — uma sessão anterior correu `move_task.py` a partir de uma
worktree partilhada por 5 subagentes e isso criou **4 cópias divergentes**
de `tasks/events.jsonl`, com um evento real (`dotfiles-tsk-dispatch-launcher`)
perdido silenciosamente num merge git, recuperado só à mão. Duas causas-raiz,
ainda não corrigidas (cards `dotfiles-tsk-tasks-root-resolver` e
`dotfiles-tsk-jsonl-merge-driver`, ambos em `todo`):
1. os scripts `tasks/*.py` resolvem o caminho de dados via
   `Path(__file__).parent` — correr a partir de uma worktree escreve na
   cópia *dessa worktree*, não na canónica;
2. `events.jsonl` não tem merge driver próprio, um merge normal do git
   pode escolher "prefer branch" e perder eventos.

**Consequência direta para esta e futuras sessões:** nunca correr
`append_event.py`/`move_task.py` de dentro de uma worktree enquanto o
resolver não estiver corrigido — só a partir do checkout principal
(`~/dotfiles`). É por isso que esta PR faz o rename (edição de texto pura,
sem tocar em `events.jsonl`) numa worktree, mas **não** cria o card
`dotfiles-handoff-standardization` aqui.

## Trabalho ativo #3 — PR #37 (mesclada): convenção `HANDOFF.md`

Motivo: havia dois handoffs (acima) com nomes/locais diferentes e sem
convenção nenhuma — risco real de um agente novo não saber qual ler, ou de
sessões paralelas colidirem (confirmado: 3+ worktrees ativas em simultâneo
nesta máquina quando esta PR foi aberta).

**Convenção adotada** (confirmada pelo dono, 2026-09-21):

- Nome do ficheiro: sempre `HANDOFF.md` — maiúsculas, singular. Alinha com
  os irmãos já existentes no root de cada pasta (`README.md`, `AGENTS.md`,
  `CLAUDE.md`, `GEMINI.md`, `CHEATSHEET.md`).
- Localização: no root do âmbito que descreve, nunca numa worktree ou
  subpasta arbitrária:
  - `~/HANDOFF.md` — índice global, cross-repo, só apontadores (ver esse
    ficheiro).
  - `<repo>/HANDOFF.md` — handoff do repo inteiro (este ficheiro).
  - `<repo>/<subsistema>/HANDOFF.md` — só quando o subsistema já tem os
    seus próprios docs de topo (precedente: `tasks/` já tem `README.md`,
    `CHEATSHEET.md`, `KICKOFF.md` próprios) — ex.: `tasks/HANDOFF.md`,
    ainda por migrar (ver acima).
- Ciclo de vida: não permanente, atualizar in place, apagar/arquivar
  quando "por fazer" ficar vazio.

**O que a PR #37 fez (mesclada, ✅):**
- Este ficheiro (`~/dotfiles/HANDOFF.md`), `~/HANDOFF.md` (índice global,
  fora de git), `~/handoff.md` antigo apagado.
- `scripts/validate_dotfiles.sh`, `README.md`, `CLAUDE.md` atualizados.

**Esta PR seguinte (`claude/tasks-handoff-rename`) faz:**
- `tasks/handoff.md` → `tasks/HANDOFF.md` (git mv puro).
- Autorreferências internas + 2 referências cruzadas (`tasks/rebuild_graph.py`,
  `tasks/plans/claim-protocol.md`) atualizadas para o nome novo.
- **Não toca em `events.jsonl`/`kanban.md`/`board.md`/`cards/`** —
  deliberado, ver acima.

**O que ficou por fazer:**
- Card formal no sistema `tasks/` (`dotfiles-handoff-standardization`) —
  por criar a partir do checkout principal (nunca de uma worktree, até o
  `tasks-root-resolver` estar corrigido). No momento em que isto foi
  escrito, o checkout principal tinha alterações locais não commitadas em
  `tasks/events.jsonl`/`kanban.md`/`cards/dotfiles-tsk-tasks-root-resolver.md`
  (provavelmente resíduo da criação dos 3 cards do `claim-protocol`, card
  ainda em `todo`, não necessariamente uma escrita ativa) — por precaução,
  o card desta tarefa não foi criado agora, para não committar por engano
  trabalho de outra sessão ainda por rever.
- Nota curta sobre a convenção `HANDOFF.md` em `CHEATSHEET.md` (root do
  dotfiles) — ainda não escrita.
- Duas linhas soltas " HEAD" / " origin/main" perto da linha ~48/53 de
  `README.md` — resíduo de um merge mal resolvido, pré-existente, **não
  relacionado com este trabalho**. Vale a pena uma sessão futura limpar.

## Próxima ação

1. Esta PR (`tasks/handoff.md` → `tasks/HANDOFF.md`) mescla-se.
2. Verificar se `tasks/events.jsonl` no checkout principal está estável
   (sem alterações locais não commitadas de outra sessão) antes de criar
   o card `dotfiles-handoff-standardization` — a partir do checkout
   principal, nunca de uma worktree.
