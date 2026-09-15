# CLAUDE.md

Orientações para Claude Code quando trabalha neste repositório.

## Resumo rápido

```
dotfiles/
├── .agents/           ← Fonte de verdade: skills/, instructions/, harnesses/, prompts/, workflows/, validation/, automation/
├── .claude/            ← Config Claude Code; .claude/skills/<nome> = symlinks para .agents/skills/<nome>
├── .github/            ← Config GitHub + CI; várias subpastas são symlinks para .agents/
├── .vscode/            ← Config VS Code (settings.json = API key real, gerido por chezmoi+age)
├── .chezmoisource/     ← Source dir do chezmoi, só para .vscode/settings.json
├── scripts/            ← Utilitários (VS Code docs monitor)
├── docs/               ← Tudo o que não é lido automaticamente por convenção (ver índice abaixo)
├── AGENTS.md, CLAUDE.md, GEMINI.md   ← Lidos automaticamente por cada ferramenta
├── docs/SECRETS.md     ← chezmoi+age secrets doc
├── README.md, CHEATSHEET.md
└── setup.sh, sync-skills.sh, test-subagents.sh
```

**Docs-chave:** `README.md` (overview + directory tree completo + Guidelines para humano/agente) · `CHEATSHEET.md` (onde vai cada coisa + TODO persistente) · `docs/STANDARDS.md` (convenções; secções propostas/não implementadas marcadas explicitamente como tal desde 2026-09-15) · `docs/SUBAGENTS_VERIFICATION.md` (checklist) · `docs/AUDIT_REPORT.md` (audit; corrigido 2026-09-15 para refletir hardcoded paths/`dtx/` reais) · `docs/SECRETS.md` (chezmoi+age). **Antes de qualquer mudança estrutural, corre `./scripts/validate_dotfiles.sh`** — é o avaliador que confirma raiz limpa, docs obrigatórios presentes, e a tree deste ficheiro/README a bater com a realidade.

## Standards do workspace (novo, 2026-09-15)

`.agents/instructions/workspace-config/standards/workspace-standards.yaml` + `workspace-standards.schema.json` definem os defaults que **todos** os repos deste workspace devem seguir (raiz limpa, secções obrigatórias no README, língua técnica=inglês, etc.) — cada repo tem a sua própria instância em `docs/standards.yml` que herda destes defaults e só declara desvios. `.agents/instructions/workspace-config/standards/RESEARCH_NOTES.md` documenta a investigação SOTA que informou o desenho (nem tudo tem prova — o campo do diagrama no README é preferência do dono, não SOTA, e está marcado como tal).

**Revisão periódica (implícita, corre em background):** um hook `SessionStart` (`~/.claude/hooks/workspace-standards-review-check.sh`) verifica `review.nextDue` a cada sessão nova do Claude Code e, se estiver atrasada, injeta um lembrete forte no contexto — não bloqueia a sessão, mas espera-se que o agente trate disso antes de mais trabalho substancial, a menos que o pedido da sessão seja claramente estreito e não relacionado. Para harnesses sem hooks (Copilot, Gemini CLI, etc.), o mesmo protocolo está descrito aqui em prosa — lê `review.nextDue` em `.agents/instructions/workspace-config/standards/workspace-standards.yaml` no início de uma sessão e aplica a mesma regra.

Sempre que editares `workspace-standards.yaml`/`.schema.json`, corre `python3 scripts/validate_workspace_standards.py .agents/instructions/workspace-config/standards/workspace-standards.yaml` antes de committer — YAML gerado por LLM tem mais tendência a erros de indentação do que JSON, por isso a validação não é opcional aqui.

**Trabalho em aberto** (detalhe completo em `CHEATSHEET.md` §4, §4.1, §4.2):

| Item | Estado |
|---|---|
| Backup da chave privada age (`~/.config/chezmoi/key.txt`) | Manual, pendente |
| Criar fine-grained PAT (github.com/settings/tokens) + `gh auth` | Adiado pelo dono, sem prazo — bloqueia `gh pr create` e arquivar repos via API |
| Repo hygiene (raiz limpa, README com tree+índice+guidelines) — `dotfiles`, `architect`, `~/Projects/notes`, `~/Work/notes` | Feito em cada repo (branches `claude/repo-hygiene-*` pushed); falta unificar o formato entre os 4 e mesclar |
| Arquivar `agentic_instructions` no GitHub | Bloqueado por `gh auth` acima |
| Decidir direção de sincronização (repo→sistema vs. sistema→repo) | Em aberto |
| Backlog de `~/Projects/notes/ideas/` | Só tracking, ver `CHEATSHEET.md` §4.1 — nada aprovado para construir |

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

Cada um é um repositório git independente. Ver `docs/directory_tree.md` para mapa (parcialmente desatualizado, ver `README.md` para o directory tree atual).

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

README.md/AGENTS.md descrevem `~/.context-global.md`, `~/claude.md`, `~/directory_tree.md` (symlink para `~/dotfiles/docs/directory_tree.md`) e `agent-versions.json` como symlinks/ficheiros do `~/dotfiles/`. **Nesta máquina nenhum destes existe** — não assumas que estão presentes sem verificar. A direção de sincronização (repo→sistema via symlinks, vs. sistema→repo) ainda não foi decidida como standard — ver secção seguinte.

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
- **Ver `CHEATSHEET.md` para o fluxo completo** de trabalho (onde vai cada coisa, roadmap do workspace ágil, TODOs em aberto). **Regra obrigatória:** qualquer mudança à estrutura de `.agents/` (nova skill, novo harness, resolução de um TODO) tem de atualizar `CHEATSHEET.md` no mesmo commit — não deixar para depois, é assim que este ficheiro não apodrece como o `STANDARDS.md` apodreceu.

## ⚠️ Lacunas Conhecidas (audit 2026-09-14, atualizado 2026-09-15 após correção de STANDARDS.md/AUDIT_REPORT.md)

Não tratar os seguintes ficheiros/afirmações como verdade atual sem verificar primeiro:

- **Decisão de sincronização em aberto**: sistema→repo vs. repo→sistema ainda não é standard. Até estar decidido, `setup.sh`/`sync-skills.sh` podem não refletir o estado real da máquina (ex.: `~/.claude`, `~/.agents`, `~/.vscode` não são symlinks nesta máquina, apesar do que README/AGENTS.md descrevem).
- **`.vscode/settings.json` contém uma API key real** para um endpoint custom. Repo é privado/uso pessoal (risco aceite pelo dono), mas não propagar este ficheiro para outros repos, exemplos, ou contextos partilhados. **TODO:** migrar para chezmoi+age (decidido, ainda não executado — bloqueado em `sudo pacman -S chezmoi age`, que requer password interativa).
- **`setup.sh` tem listas de repos hardcoded** (`WORK_REPOS`, `PROJECTS_REPOS`) e o username `nmc-costa` hardcoded no `clone()` (URLs SSH/HTTPS) — não é portável para outro utilizador sem editar o script diretamente. **Nota:** existe uma correção (env vars `GITHUB_USER`/`WORK_REPOS`/`PROJECTS_REPOS`) no commit `0304d1d` da branch `claude/todo-continuation-and-notes-backlog`, mas **não está mesclada** nesta branch nem em `main` — não assumir que está resolvido até essa branch ser integrada.
- **`.vscode/github.code-workspace` tem um path hardcoded** `"dtx/repos/sp_xai_nos"` — referência real a `dtx/` que ainda existe no repo (verificado 2026-09-15, único hit fora de conteúdo histórico/arquivado).

**Resolvido nesta ronda (deixou de ser lacuna):**
- `.agents/` e `.github/` já não têm conteúdo duplicado/órfão — `.github/{harnesses,instructions,prompts,automation,CONTRIBUTING.md,skills/project-doc-lifecycle}` são agora symlinks para `.agents/`, e todos os paths mortos para `/my/agentic_instructions/...` e `/home/user/github/...` foram corrigidos ou substituídos por notas que documentam o bug antigo explicitamente. `.claude/skills/` também deixou de divergir de `.agents/skills/`: as 9 skills HITs (`archi`, `diagramhits`, `documenthits`, `mockuphits`, `presenthits`, `projecthits`, `reviewhits`, `simplifyhit`, `project-doc-lifecycle`) agora vivem como conteúdo real em `.agents/skills/`, com `.claude/skills/<nome>` como symlink.
- `docs/AUDIT_REPORT.md` e `docs/STANDARDS.md` já não contêm afirmações falsas apresentadas como verdade atual. `AUDIT_REPORT.md` foi reescrito (2026-09-15) para reportar com precisão que **existem** `dtx/` e paths hardcoded (ver acima) em vez de negar isso — `.github/copilot-instructions.md`, que a nota anterior também apontava como fonte de contradição, foi re-verificado e está limpo (corrigido no commit `8900ac6`, antes desta ronda). `STANDARDS.md` foi reescrito para marcar `.copilot/`, `.gemini/`, `.cursor/`, `agent-versions.json` e o repositório `agent-framework` como **`[PROPOSTO — não implementado]`** em vez de os apresentar como estrutura atual. Ambos os ficheiros continuam a precisar de leitura crítica (documentam trabalho em aberto por natureza), mas já não mentem sobre o estado atual do repo.

## Documentação

- **`AGENTS.md`** — Guia completo (agentes, skills, workflows, troubleshooting)
- **`README.md`** — Overview, directory tree e estrutura
- **`docs/SUBAGENTS_VERIFICATION.md`** — Checklist de setup e verificação

---

**Para projectos específicos:** Ver repos em `~/Projects/` ou `~/Work/` — cada um tem seu próprio `CLAUDE.md`.
