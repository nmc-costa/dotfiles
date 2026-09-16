# Kickoff: open the pending pull requests

**Status:** not started. `gh` isn't authenticated (PAT deferred by the owner,
no ETA as of 2026-09-15). This file is the seed for a **future, fresh**
session, once `gh auth login` works — do not resume this session for it
(reloading full history costs far more than a short prompt here; see
`sessionHygiene` in `.agents/instructions/workspace-config/standards/
workspace-standards.yaml`, and `CHEATSHEET.md` §7).

## Copy from here down into the new session

Lê `~/dotfiles/CLAUDE.md` e `~/dotfiles/CHEATSHEET.md`, depois este ficheiro.
`gh auth status` já deve estar OK — confirma primeiro.

**Nota prática (2026-09-15):** `gh auth login` é uma credencial **por máquina**,
não por sessão nem por repo — pode ter sido feita numa sessão só com contexto
de `dotfiles` (ex.: por acesso remoto/limitado nessa altura) e continua válida
aqui, mesmo que esta sessão tenha acesso aos 4 repos e essa não tivesse. Se
`gh auth status` já disser OK mas nunca viste o login acontecer nesta sessão,
é normal — confirma e segue em frente. Depois abre os PRs
abaixo, **por esta ordem** (alguns repos têm branches irmãs divergentes que
precisam de reconciliação manual, não é só clicar "merge" em todas).

Só as branches `claude/*` listadas abaixo são desta sessão — ignora
quaisquer outras branches `copilot/*` ou antigas que encontres nos repos,
não são deste trabalho.

### 1. `dotfiles` — ⚠️ duas branches irmãs divergentes

`claude/workspace-standards-schema` já contém `claude/repo-hygiene-dotfiles`
(é descendente direta). `claude/todo-continuation-and-notes-backlog` é
**irmã**, não descendente — ambas editam `setup.sh` de forma independente.

1. Abrir e mergear `claude/workspace-standards-schema` primeiro (é a mais
   completa — contém a arrumação da raiz, o schema, o `sync.sh`, o timer,
   `tasks/`):
   ```
   gh pr create --repo nmc-costa/dotfiles --base main --head claude/workspace-standards-schema \
     --title "Repo hygiene + workspace-standards schema + tasks/ kickoff" \
     --body "Squash of this session's dotfiles work: root cleanup, validate_dotfiles.sh, the workspace-standards JSON Schema + YAML defaults (docs/standards -> .agents/instructions/workspace-config/standards/ after an owner correction), sync.sh generalized to sync all of .agents/ (was sync-skills.sh, skills-only), a weekly systemd timer running it, tasks/ seeded with two kickoff prompts, and (2026-09-15, later commit) a new developmentApproach.pocFirst workspace default. See commit messages for full detail per change."
   ```
1b. `claude/tasks-poc` descende de `claude/workspace-standards-schema` (ponto
   anterior ao commit do `developmentApproach` acima, mas sem conflito —
   toca só em `tasks/` e nas linhas de `tasks/` do README) — mergear depois
   do passo 1:
   ```
   gh pr create --repo nmc-costa/dotfiles --base main --head claude/tasks-poc \
     --title "tasks/: PoC of the task-tracking system" \
     --body "JSONL event log (source of truth, D9/D10) + generated tarefas.md view (D12/D13 states+provenance), seeded with the 11 real open claude/* branches across all 4 repos, plus (2026-09-16, later commit) a deferred kanban state and a note on why Backlog.md's AC:BEGIN/END anchors weren't adopted. See commit messages for the full reasoning."
   ```
1c. `claude/community-index-poc` descende de `claude/workspace-standards-schema`
   (mesmo ponto que 1b, sem overlap com `tasks-poc` — toca no schema/yaml de
   `communityFirst`, `community-index/` novo, e `RESEARCH_NOTES.md`) —
   independente de 1b, pode mergear em qualquer ordem depois do passo 1:
   ```
   gh pr create --repo nmc-costa/dotfiles --base main --head claude/community-index-poc \
     --title "Add communityFirst default + community-index PoC" \
     --body "New workspace-standards default: check what the community already maintains before building non-trivial subsystems, applied bidirectionally with developmentApproach.pocFirst. PoC of communityFirst.index: index_topics.py queries the public GitHub Search API (unauthenticated, manual cadence) for 3 real topics, with real snapshots committed. RESEARCH_NOTES.md records this session's actual landscape-scan verdicts (tasks/ vs. Backlog.md/claude-task-master, the hygiene schema vs. AGENTS.md/Repolinter, the Jarvis orchestrator vs. khoj, omarchy-voice vs. VoxClaude). See commit message for full detail."
   ```
1d. `claude/omarchy-agent-launcher-gap` descende de `claude/workspace-standards-schema`
   (mesmo ponto que 1b/1c, sem overlap — toca só em
   `.agents/skills/omarchy/LOCAL_ADDENDUM.md` novo e uma nota em `CLAUDE.md`)
   — independente das outras duas, pode mergear em qualquer ordem depois do
   passo 1:
   ```
   gh pr create --repo nmc-costa/dotfiles --base main --head claude/omarchy-agent-launcher-gap \
     --title "Document the omarchy agent-launcher gap in a local addendum" \
     --body "The vendored omarchy/diagnose-crash skill files (re-verified byte-identical to /usr/share/omarchy, 2026-09-16) don't cover the omarchy agent launcher subsystem (9+-agent launcher, default agent, Super+Shift+Ctrl+A, Agents Panel, crash-capture integration) documented at omarchy.org/manual/ai/. LOCAL_ADDENDUM.md is new and additive, never touches the 6 vendored files. Also documents the official plugin manifest standard and a VoxClaude-vs-omarchy-voice trade-off for voice-to-agent, left as an open question for the owner. See commit message for full detail."
   ```
2. Depois de mergeado, `claude/todo-continuation-and-notes-backlog` vai
   provavelmente conflituar em `setup.sh` (uma branch tornou os repo-lists
   configuráveis via env var, a outra corrigiu o parsing de `--dry-run`).
   **Resolver à mão** — os dois patches não se anulam, são complementares,
   deve dar para aplicar ambos. Depois de resolvido:
   ```
   gh pr create --repo nmc-costa/dotfiles --base main --head claude/todo-continuation-and-notes-backlog \
     --title "Reconcile persistent TODO with actual repo state" \
     --body "See commit message — closes out stale TODO items that were already done, notes/ideas backlog tracked in CHEATSHEET §4.1."
   ```

### 2. `architect`

`claude/env-leak-fix` é independente (não é desta sessão, já existia) — pode
ser mergeada em qualquer altura, sem relação com o resto.

```
gh pr create --repo nmc-costa/architect --base main --head claude/env-leak-fix \
  --title "Close .env leak gap, add missing dependency"
gh pr create --repo nmc-costa/architect --base main --head claude/workspace-standards-schema \
  --title "Repo hygiene + workspace-standards instance" \
  --body "Persona-activation text moved out of README into docs/persona/, real README written and pytest-verified (21 passed / 8 pre-existing failures), docs/standards.yml added. See commit messages for full detail."
```

### 3. `notes` — ⚠️ a reconciliação mais delicada dos quatro repos

`claude/repo-hygiene-notes` e `claude/ideas-review-fixes` são **irmãs**
divergentes da mesma base (`0b6c723`). `claude/workspace-standards-schema`
descende de `ideas-review-fixes`, **não** de `repo-hygiene-notes` — por isso
não tem as secções novas do README que `repo-hygiene-notes` acrescentou.

**Não mergear `workspace-standards-schema` antes de resolver isto** — o
`docs/standards.yml` que lá está assume que o README já tem as secções
Directory tree / What's where (index) / Guidelines, que só existem em
`repo-hygiene-notes`.

1. Mergear `claude/repo-hygiene-notes` primeiro (estrutura do README):
   ```
   gh pr create --repo nmc-costa/notes --base main --head claude/repo-hygiene-notes \
     --title "README rewrite + validate_notes.sh"
   ```
2. Rebase `claude/ideas-review-fixes` sobre o `main` atualizado (deve ser
   limpo — toca sobretudo em `ideas/*.md`, não no README raiz), depois:
   ```
   gh pr create --repo nmc-costa/notes --base main --head claude/ideas-review-fixes \
     --title "Source-checked fixes across 5 ideas/ planning docs" \
     --body "Plan-mode review of Workspace Agil, Jarvis, harness-vision, and the two audio-interface docs — citations verified, stale claims corrected (Manus acquisition, ETH Zurich study magnitude, etc). See commit messages, one per doc, for full detail."
   ```
3. Rebase `claude/workspace-standards-schema` sobre o resultado, confirmar
   que `python3 scripts/validate_workspace_standards.py docs/standards.yml`
   ainda passa, e só então:
   ```
   gh pr create --repo nmc-costa/notes --base main --head claude/workspace-standards-schema \
     --title "workspace-standards instance"
   ```

### 4. `Work/notes` (org `DTx-DSML`) — cadeia linear, sem conflito

```
gh pr create --repo DTx-DSML/notes --base main --head claude/repo-hygiene-worknotes \
  --title "README rewrite + validate_notes.sh"
gh pr create --repo DTx-DSML/notes --base main --head claude/workspace-standards-schema \
  --title "workspace-standards instance"
```

Nota: repo de organização, não pessoal — o dono pode querer rever com mais
cuidado antes de mergear, mesmo que o `gh pr create` corra sem erro.

## Fim do que copiar

Depois de todos os PRs abertos (mergear fica ao critério do dono, não abrir
e mergear tudo automaticamente sem ele ver), marca em `CHEATSHEET.md` §4 e
apaga/arquiva este ficheiro — já não serve.
