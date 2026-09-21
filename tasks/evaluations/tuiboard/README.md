# tuiboard evaluation (2026-09-18)

Fase-0 de-risking spike for the orchestration architecture decided in
`tasks/README.md`'s "Orchestration architecture" section — specifically the
"evaluate `tuiboard` before writing anything in Rust" item. **Result:
tuiboard passes.** It's a good candidate base for the eventual `tsk board`
UI layer.

## What was tested

[`NazzarenoGiannelli/tuiboard`](https://github.com/NazzarenoGiannelli/tuiboard)
(MIT, 114★, Bun + OpenTUI + SolidJS), installed from source into a scratch
directory (not this repo, not globally) and run against a throwaway board
file with our decided 6-stage lifecycle (`Backlog → Planning → In Progress →
Review → Validation → Done`), with one dummy task (`T-0001`) moved through
every column.

## Findings

**Safety.** Read `package.json` and grepped `src/` for network calls before
installing anything: no `postinstall`/`preinstall` scripts, dependencies are
all well-known (`@opentui/*`, `chokidar`, `js-yaml`, `solid-js`), and the
only network-capable feature (an optional Google/Microsoft 365 calendar
overlay) requires explicit interactive OAuth setup — never called
automatically. Left off in the test config.

**Local.** The board is plain markdown on disk. The "Agents (live)" panel
reads `~/.claude/`, `~/.codex/`, etc. read-only, locally, with zero network
calls — confirmed by the grep above, not just by the README's claim.

**Fast.** Near-instant startup, ~165MB RSS, CPU settles after the initial
render. Nothing alarming for a terminal app.

**Architecturally important finding: tuiboard has no interactive
"move task to another column" command.** It's a pure watch-and-render tool
(`chokidar` on the board files) — moving a task between columns means
editing which `##` heading the task line sits under, and the live-reload is
instant. This is exactly the shape our `tsk` CLI needs: `tsk` writes to the
task file, tuiboard just reflects it. Confirmed empirically (see `states/`)
by editing `example-board.md` directly six times and capturing the
re-rendered board after each edit — every transition (including the
`Done`-column-hides-and-counts-separately behavior the README promises)
worked exactly as documented.

**Bonus:** the live Agents panel showed real, current Claude Code sessions
on this machine with zero configuration — including the session that ran
this very evaluation.

## Files here

- `example-board.md` — the throwaway board file, left in its final state
  (`T-0001` in `Done`)
- `example-config.yaml` — the isolated `TUIBOARD_CONFIG` used (points at a
  scratch path outside this repo — not reusable as-is, kept for reference)
- `states/1-backlog.txt` … `states/6-done.txt` — `tmux capture-pane -p`
  text snapshots after each of the 6 transitions
- `all-states-combined.txt` — all 6 states concatenated with headers, for a
  single-file read-through

## Not yet tested

Multi-vendor session detection (only Claude Code sessions were live on this
machine during the test — Codex/OpenCode/Pi panels are implemented per the
tuiboard README but unverified here), the herdr integration path (`H` to
jump to a session), and whether contributing our state machine to tuiboard
vs. forking it is the better call — both still open per `tasks/README.md`.

## Instalação real, 2026-09-21

Segue-se a instalação persistente (não-scratch), substituindo o spike acima.

**Comandos exatos usados:**

```bash
# 1. bun via mise (plugin core, já disponível — sem plugin extra a adicionar)
mise use -g bun@latest
# -> mise ~/.config/mise/config.toml tools: bun@1.4.2

# 2. tuiboard, global, a partir do próprio repo GitHub (confirmado via README
#    do NazzarenoGiannelli/tuiboard: "bun install -g github:..." é o método
#    suportado; "bun install -g tuiboard" via npm também existe mas o install
#    from-source do GitHub foi o escolhido para ficar preso a um commit)
bun install -g github:NazzarenoGiannelli/tuiboard
# -> installed tuiboard@github:NazzarenoGiannelli/tuiboard#4fc179b
#    binaries: tuiboard, tb
#    warn: To run "tuiboard", add the global bin folder to $PATH:
#    export PATH="/home/nbugz/.cache/.bun/bin:$PATH"
```

Binário instalado em `/home/nbugz/.cache/.bun/bin/tuiboard` (symlink para
`/home/nbugz/.cache/.bun/install/global/node_modules/tuiboard/bin/tuiboard.ts`).
`bun pm ls -g` confirma `tuiboard@github:NazzarenoGiannelli/tuiboard#4fc179b`
entre os 113 pacotes globais instalados.

**Config, caminho persistente:**

`~/.config/tuiboard/config.yaml` (primeira opção de descoberta global do
próprio tuiboard, por ordem: `$TUIBOARD_CONFIG` > `.tuiboard/config.yaml` a
subir diretórios > `~/.config/tuiboard/config.yaml` > auto-discovery):

```yaml
boards:
  - path: /home/nbugz/dotfiles/tasks/kanban.md
    name: dotfiles

done_column: Done
```

Aponta deliberadamente para o caminho absoluto do `tasks/kanban.md` do
**repositório principal** (`/home/nbugz/dotfiles/tasks/kanban.md`), não para
a cópia local desta worktree (`.claude/worktrees/wave1-parallel-dispatch/tasks/kanban.md`),
que é transitória e desaparece quando a worktree for removida.

**Confirmação visual (renderiza o board real):**

```bash
tmux new-session -d -s tuiboard_verify -x 220 -y 40 "/home/nbugz/.cache/.bun/bin/tuiboard"
sleep 3
tmux capture-pane -t tuiboard_verify -p > tasks/evaluations/tuiboard/real-install-render.txt
tmux kill-session -t tuiboard_verify
```

Ver `real-install-render.txt` para a captura completa. Confirmado nela:

- Header: `15 open · 13 done · 7 cols` — bate certo com o `tasks/kanban.md`
  real no momento da captura (15 tarefas em Backlog, 13 em Done).
- Coluna **Backlog (15)** lista as tarefas reais, incluindo
  `dotfiles-tsk-tuiboard-install` (esta própria tarefa) e
  `dotfiles-tsk-roadmap-graph`, `dotfiles-tsk-notify-sweep`, etc. — nomes
  exatos do ficheiro real, não dados de exemplo.
- Colunas **Planning** e **In Progress** presentes e vazias, tal como no
  ficheiro real nesse instante — confirma que os 7 nomes de coluna do nosso
  lifecycle (`Backlog/Planning/In Progress/Review/Validation/Done/Blocked`)
  são todos lidos corretamente do `##` heading format.
- Painel **Agents (live) · 27** — deteção automática, zero configuração, de
  27 sessões Claude Code reais ativas na máquina neste momento, incluindo a
  própria worktree desta tarefa (`worktree-wave1-parallel-dispatch`).

Nota sobre o que o header/colunas mostram vs. o estado desta tarefa: os dois
`move_task.py` do Passo 1 desta tarefa (`backlog → planning → in_progress`)
regeneraram o `tasks/kanban.md` **desta worktree** (é isso que o próprio
script faz — reconstrói o ficheiro na árvore onde corre, a partir do
`tasks/events.jsonl` partilhado), não o `tasks/kanban.md` do checkout
principal, que só é regenerado quando alguém corre `move_task.py` a partir
de lá. Por isso a captura acima ainda mostra `dotfiles-tsk-tuiboard-install`
em Backlog: é o estado real e atual do ficheiro real no momento da captura,
exatamente o que se pedia para confirmar (tuiboard não inventa dados — lê o
ficheiro tal como está). Assim que o orquestrador correr `move_task.py`
(ou equivalente) a partir do checkout principal, o mesmo `tuiboard` já a
correr vai refletir a mudança automaticamente (live-reload via `chokidar`,
confirmado no spike original).

**Nota de âmbito de máquina vs. repo:** a instalação do `bun` (via
`~/.config/mise/config.toml`) e do `tuiboard` (via `bun install -g`, dentro
de `~/.cache/.bun/`) e a config em `~/.config/tuiboard/config.yaml` vivem
fora deste repositório — não aparecem em nenhum diff git, só ficam
versionados os ficheiros dentro de `tasks/evaluations/tuiboard/`.
