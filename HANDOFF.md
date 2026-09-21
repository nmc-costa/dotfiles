# HANDOFF — dotfiles (agent-OS unification + repo conventions)

**Data:** 2026-09-21. Este ficheiro é o handoff do repo `~/dotfiles` como um
todo — não é permanente, atualiza-se in place, apaga-se/arquiva-se quando a
lista "por fazer" ficar vazia. Ponto de entrada global: `~/HANDOFF.md`.

## Correção importante face ao handoff anterior

Este ficheiro **substitui** o antigo `~/handoff.md` (fora de qualquer repo
git, só nesta máquina). Esse ficheiro **ainda não foi apagado** — a remoção
é um passo manual pós-merge desta PR (ver "Próxima ação" abaixo), para não
haver um momento em que nenhum dos dois existe.

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

**Resolvido, 2026-09-21.** PR #30 mesclou entretanto (junto com #35, #36,
#40 — Onda 1 fechada). `tasks/handoff.md` foi renomeado para
`tasks/HANDOFF.md` numa PR de seguimento desta (`claude/tasks-handoff-md-rename`),
que também cria o card `dotfiles-handoff-standardization` para fechar esta
tarefa formalmente no sistema `tasks/`. Ver `tasks/HANDOFF.md` para o
estado corrente do subsistema.

## Trabalho ativo #3 — Esta PR: convenção `HANDOFF.md`

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
    já migrado.
- Ciclo de vida: não permanente, atualizar in place, apagar/arquivar
  quando "por fazer" ficar vazio.

**O que esta PR fez:**
- Este ficheiro (`~/dotfiles/HANDOFF.md`).
- `scripts/validate_dotfiles.sh`: `HANDOFF.md` adicionado a
  `ALLOWED_ROOT_FILES` (senão o check de "clean root" acusa-o).
- `README.md`: árvore de diretórios + tabela "Root files" atualizadas.
- `CLAUDE.md`: árvore "Quick summary" atualizada.

**O que ficou por fazer (não incluído nesta PR, deliberadamente):**
- Card formal no sistema `tasks/` (`dotfiles-handoff-standardization`) e o
  rename `tasks/handoff.md` → `tasks/HANDOFF.md` — feitos numa PR de
  seguimento (`claude/tasks-handoff-md-rename`), depois de PR #30 mesclar.
- Nota curta sobre a convenção `HANDOFF.md` em `CHEATSHEET.md` (root do
  dotfiles) — ainda não escrita.
- Duas linhas soltas " HEAD" / " origin/main" perto da linha ~48/53 de
  `README.md` — resíduo de um merge mal resolvido, pré-existente, **não
  relacionado com esta PR**, não corrigido aqui deliberadamente (fora de
  âmbito). Vale a pena uma sessão futura limpar isto à parte.

## Próxima ação

1. Esta PR mescla-se (autorização explícita do dono, 2026-09-21 — "Faz
   pull request, merge and sync").
2. **Feito, 2026-09-21**: `~/handoff.md` (o antigo, fora de git) apagado,
   depois de confirmar que este ficheiro já estava presente e correto no
   checkout principal.
3. **Feito, 2026-09-21**: `tasks/handoff.md` renomeado para
   `tasks/HANDOFF.md`, card `dotfiles-handoff-standardization` criado no
   sistema `tasks/` e fechado — ver `claude/tasks-handoff-md-rename`.
