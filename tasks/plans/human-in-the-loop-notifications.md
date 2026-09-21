# Plano: notificação por exceção e arranque cross-provider

**Estado: plano aprovado, nada implementado.** Produzido pela skill `plan-orchestra`
(2026-09-20/21): 6 investigadores em paralelo + 1 desempate, mapa de evidências
verificado, 2 rondas de plano↔crítica adversarial com contexto limpo (o máximo
permitido pela skill). A segunda ronda de crítica devolveu veredito **"ship it"**
com um addendum de 8 correções, aqui já incorporado. Nenhuma parte deste
documento foi aceite sem verificação empírica direta na máquina real.

## Objetivo

O dono só é necessário quando algo precisa mesmo dele (SLA expirado, limite de
loops excedido, tarefa bloqueada). Vê isso num kanban (`tuiboard`) e responde
em linguagem natural numa sessão CLI qualquer — nunca edita ficheiros, nunca
invoca o orquestrador diretamente. Três CLIs (Claude Code, Copilot CLI,
Antigravity — sucessor do Gemini CLI, descontinuado a 2026-06-18) partilham o
mesmo `tasks/events.jsonl` como fonte de verdade.

## Pré-requisito bloqueante

**Merge da PR #20 — feito, 2026-09-21.** `move_task.py`, `rebuild_kanban.py` e
`kanban.md` já estão em `main`. O resto deste plano ainda reescreve ~3 dos
4 ficheiros que a PR trouxe (ver §5) — o merge deu uma base limpa e
bisectável, não uma fundação estável a preservar intacta.

---

## Mapa de evidências

| # | Afirmação | Fonte | Confiança | Estado após crítica |
|---|---|---|---|---|
| 1 | herdr deteta "quer atenção" via manifesto de ecrã (pattern-matching TOML sobre output do terminal), igual para Claude Code e Copilot CLI | herdr.dev/docs/integrations/ | Alta | Confirmado |
| 2 | `herdr notification show`/`pane report-agent` — API exata | herdr.dev/docs/cli-reference/ | Alta | Confirmado; forma real do JSON é `{"id":...,"result":{"reason":...,"shown":bool}}` |
| 3 | Exit codes do herdr não documentados | ausência na doc + github.com/herdrdev/herdr/discussions/668 | Confirmado (lacuna) | Mitigado — sucesso lido de `.result.shown`, nunca do exit code |
| 4 | Passthrough OS do herdr depende de `delivery="system"` | herdr docs | Média→**Alta** | **Confirmado nesta máquina**: `~/.config/herdr/config.toml:100` |
| 5 | `agentPushNotifEnabled` é mecanismo separado do herdr | code.claude.com/docs/en/settings-reference | Alta | Confirmado; decisão: o daemon não lhe mexe |
| 6 | `SessionStart` do Claude Code injeta `additionalContext` automaticamente antes do 1º prompt | code.claude.com/docs/en/hooks | Alta | Confirmado, mas **o hook citado como precedente não está versionado no repo** (achado novo, ver §5) |
| 7 | Não existe convenção de arranque uniforme entre CLIs na comunidade | agents.md, morphllm.com, dev.to | Alta | Confirmado |
| 8 | Copilot CLI lê `AGENTS.md`/`CLAUDE.md`/`copilot-instructions.md` com `@caminho` relativo, opt-in via `include-custom-instructions` desde v1.0.86 | docs.github.com | Alta | Confirmado |
| 9 | **`sessionStart` do Copilot CLI está partido** — dispara depois do 1º prompt, não antes | issue #2201, ainda aberta, sem fix até v1.0.86+ | Alta | Confirmado por desempate dedicado |
| 10 | Gemini CLI descontinuado 2026-06-18, sucedido por Antigravity CLI (herda hooks/skills/subagents) | Google Developers Blog | Alta | Confirmado |
| 11 | Nem Gemini CLI nem Antigravity suportam auto-descoberta de `.agents/rules/*.md` | gemini-cli issue #26013, aberta | Alta | Confirmado — a suposição anterior (self-report do Antigravity) era falsa |
| 12 | CrewAI é o único dos 3 frameworks estudados com notificação real (email+webhook) e fallback por timeout | docs-platform.crewai.com | Alta | Confirmado — precedente citado para o padrão SLA→auto-validação |
| 13 | herdr tem rate-limit em rajada, indocumentado, não configurável | testado empiricamente (2 rondas) | Alta | **Medido com precisão**: rate-limited a 0.5s, shown a 1.0s — janela <1s |

---

## O plano

### 0. Write path unificado

`append_event.py::append()` é o **único writer físico** de `events.jsonl`.
`move_task.py` deixa de escrever diretamente (hoje duplica o `open("a")`) e
passa a chamar `append()` — é a CLI de transição de fase, não um segundo
writer. Novo `tasks/lifecycle.py` centraliza `PHASES`, `LEGAL_TRANSITIONS`,
`FACT_TYPES`, `HUMAN_ACTOR_KINDS`, `dedup_key()`.

```python
PHASES = ("backlog","planning","in_progress","review","validation","done","blocked","deferred")
LEGAL_TRANSITIONS = {
  "backlog":     {"planning","deferred"},
  "planning":    {"in_progress","backlog","deferred","blocked"},
  "in_progress": {"review","blocked","deferred"},
  "review":      {"in_progress","validation","blocked"},
  "validation":  {"done","in_progress","blocked"},
  "blocked":     {"in_progress","planning","deferred"},
  "deferred":    {"backlog","planning"},
  "done":        set(),
}
# Correção da Fase 5 ronda 2: o log real usa "humano"/"agente" (PT), não
# "human"/"agent" — 22/22 eventos existentes usam a grafia PT.
HUMAN_ACTOR_KINDS = ("humano", "human")
```

Transição ilegal → `exit 2` (requer uma exceção nova; hoje `validate_and_enrich`
lança `ValueError` e ambos os `main()` capturam para `exit 1` — a introdução do
allowlist tem de trazer o novo tipo de erro, não presumir que já existe).

### 1. Lista de eventos → ação

| Evento / facto | Produtor | Ação automática | Notifica? | Escalonamento |
|---|---|---|---|---|
| `→validation` (agente) | `move_task.py` | arma SLA 4h | não, de imediato | — |
| SLA 4h expirado | derivado pelo sweep | auto-validação **por CAS** (§2) | sim (P2, a posteriori) | 4h pré-aviso a 3h30 |
| `loop_cap_exceeded` (>2 loops) | sweep conta `review.judge_failed` | marca `human_only:true`; **nunca** auto-valida | P0 | 4h, para sempre |
| `→blocked` | `move_task.py` | nenhuma | P0 | 24h |
| `agent.session_stalled` | **derivado** pelo sweep (mtime `state.json` >45min + pane herdr viva) | nenhuma | P1 | 1h — ver correção no §5 |
| `review.judge_failed` / `budget.daily_cap_reached` | **fora de âmbito (camada L2/execução)** | consumidor pronto, sem produtor ainda | — | — |
| `daemon.error` | falha do próprio sweep | — | P0, **fora desta tabela** (ver watchdogs, §4) | — |

Regra única de supressão: um novo `raised` só se suprime se existir um
`raised` **e** um `delivered` com o mesmo `dedup_key`
(`f"{task_id}:{fact_type}:{age_seconds // ESCALATION_PERIOD[fact_type]}"`).
Um `raised` sem `delivered` correspondente **auto-cura** no sweep seguinte —
"3 raised, 0 delivered" deixa de ser uma métrica sem leitor e passa a ser o
próprio gatilho de retry. Ao 5º `raised` sem `delivered` na mesma chave,
`notification.undeliverable` + promove ao digest.

### 2. CAS — proteger a decisão humana (a peça mais crítica do plano)

**Camada A (mecânica, correta desde a 1ª crítica):** `append(event,
expect_last_event_id=None)` — se dado, `flock(LOCK_EX)` sobre um sidecar
`tasks/.events.lock` (nunca sobre o `events.jsonl`), relê a cauda dentro do
lock, aborta com `exit 3` + `notification.cas_aborted` se o último evento
dessa `task_id` já não for o esperado. Appends normais (sem
`expect_last_event_id`) continuam sem lock — já confirmado seguro a 20 vias
em paralelo, não se re-resolve o que já está resolvido.

**Camada B — regra corrigida pela Fase 5 ronda 2** (a regra original tinha
3 bugs independentes: vocabulário PT/EN errado, `parent_event_id` indefinido
no caminho comum, e âncora demasiado ampla que deixava um simples `--ack`
vetar uma auto-validação legítima):

> Descarta um evento `O` (`actor.kind` fora de `HUMAN_ACTOR_KINDS`) que mova
> para `validation`/`done` **só se** existir um evento humano do tipo
> `task.phase_changed` (não qualquer evento) para a mesma `task_id`, com
> `ts` estritamente entre `ts(parent_event_id(O))` e `ts(O)`. Se
> `O.parent_event_id` for `None`, ancorar no evento de mudança de fase
> anterior mais recente dessa `task_id`, não falhar aberto.

**Extensão obrigatória da Fase 5 ronda 2:** `--expect-last-event-id`
(Camada A) passa a ser exigido em **todo** o `move_task.py` que escreva para
`validation`/`done` — não só nas escritas do sweep — para que o caminho sem
lock nunca alcance as fases contendidas (o docstring da PR #20 já diz que o
chamador pretendido é um agente, não o humano; hoje esse caminho comum fica
sem proteção nenhuma).

`loop_cap_exceeded`: o sweep nem propõe auto-validação se `human_only:true`
— verificado antes do CAS, que fica como segundo cinto, não o primeiro.

### 3. Notificação — digest, não rajada

Ponto de saída único: `tasks/notify.py`. Um sweep = **no máximo um** toast
herdr, formato digest (`"tsk: N factos precisam de ti"` + top-3 +
`"…e mais K"`). O `raised` continua por-facto; só a *entrega* é coalescida.
Exceção P0 (`loop_cap_awaiting_human` >8h, `blocked` >72h): toast individual
após `time.sleep(2)` (medido: janela de rate-limit recupera em <1s, `2s` tem
margem folgada) **mais** `notify-send` incondicional (sem rate-limit).
Sucesso sempre lido de `.result.shown==true`, nunca do exit code.

Gate de CI determinístico (`tasks/validate_herdr_contract.sh`):
```bash
a=$(herdr notification show "tsk-probe-1" | jq -r .result.reason)
b=$(herdr notification show "tsk-probe-2" | jq -r .result.reason)
[ "$a" = "shown" ] && [ "$b" = "rate_limited" ] || { echo "FAIL: contrato herdr mudou ($a,$b)"; exit 1; }
```
Deteta uma mudança real de API em vez de depender de estado ambiente.

### 4. Dois watchdogs fora do sweep

O sweep é o único produtor de notificações **e** de `inbox.md` — se morrer,
tudo parece bem. Dois caminhos que não passam por ele:

1. **`OnFailure=`** no systemd unit → uma segunda unit oneshot que corre só
   `notify-send -u critical "tsk-sweep FALHOU" "..."` — zero Python, zero
   `events.jsonl`, não pode falhar pelas mesmas razões que o sweep.
2. **Heartbeat lido pelo humano**: o sweep faz `touch tasks/.sweep-heartbeat`
   no fim de cada ronda bem-sucedida; `brief.py` verifica esse mtime **antes**
   de ler `inbox.md` — se >15min, banner grande "o sweep parece morto" antes
   de mostrar qualquer outra coisa. A sessão do humano está garantidamente
   viva quando ele olha para ela; o sweep não está.

**Endurecimento da Fase 5 ronda 2** (achado N3, verificado ao vivo — há um
job dir real, `~/.claude/jobs/a17dbcac/`, sem `state.json`): todo o acesso a
`~/.claude/jobs/*/state.json` tem de ser `try`-guardado, senão um
`FileNotFoundError` não tratado crash-loopa o sweep antes de tocar no
heartbeat, e os dois watchdogs disparam para sempre de 5 em 5 minutos. A
unit ganha `TimeoutStartSec=120` para que um sweep *pendurado* (não
apenas falhado) também acione `OnFailure=`.

### 5. Skill cross-provider `/task-brief`

Não `/kanban-orchestra` — colidiria semanticamente com a `plan-orchestra` já
existente (fan-out multi-agente, o oposto disto). Casca fina sobre
`tasks/brief.py` (lógica toda determinística em Python — regra D14 do repo,
"script antes de regra"): verifica heartbeat primeiro, lista inbox por
prioridade, só pergunta "em que queres trabalhar?" se não houver nada
pendente. Nunca escolhe trabalho sozinha.

| CLI | Gatilho | Estado real |
|---|---|---|
| Claude Code | hook `SessionStart` | Funciona — **mas o precedente citado (`workspace-standards-review-check.sh`) não está no repo.** `~/.claude/hooks/` e `~/.claude/settings.json` são ambos locais, não versionados (achado N1, Fase 5 ronda 2). O plano tem de criar e versionar o script do hook e um fragmento de `settings.json` — não pode assumir que "já há precedente" cobre isto |
| Antigravity | hook próprio + `.agents/rules/session-startup.md` | Ver correção abaixo |
| Copilot CLI | wrapper `bin/cpx` (`brief.py` + `exec copilot "$@"`, `alias copilot=cpx`) | `sessionStart` próprio está partido (issue #2201); nada se constrói em cima dele |

**Correção da Fase 5 ronda 2 (achado N4) — manter a duplicação inline, não
importar:** a ideia original (promover `.agents/rules/session-startup.md` a
fonte única, importada via `@caminho` a partir de `AGENTS.md`/`GEMINI.md`/
`.github/copilot-instructions.md`) foi **revertida**. O próprio
`session-startup.md` já documenta a duplicação como mitigação deliberada:
*"este ficheiro existe para que uma ferramenta que só siga a convenção
`.agents/rules/` continue a ter o conteúdo, sem depender de nenhum dos
outros"*. `.github/copilot-instructions.md` não tem mecanismo de expansão de
`@import` — ficaria com uma string morta. A confusão a corrigir não era sobre
a duplicação, era sobre a auto-descoberta de `.agents/rules/` em si (que não
existe, gemini-cli #26013). Ação real: manter os três ficheiros com o texto
inline, e **atualizar o ponteiro em todos** de `tasks/board.md` para o novo
`tasks/inbox.md`.

### 6. Ficheiros a criar/alterar

**Novos:** `tasks/lifecycle.py`, `tasks/sweep.py`, `tasks/notify.py`,
`tasks/brief.py`, `tasks/policy.yaml`, `tasks/validate_herdr_contract.sh`,
`.agents/skills/task-brief/SKILL.md` (+ symlinks `.claude/skills/`,
`.github/skills/`), `bin/cpx`, **o hook `SessionStart` do Claude Code e o
fragmento de `settings.json` que hoje só existem localmente** (achado N1).

**Systemd — correção da Fase 5 ronda 2 (achado N2):** a "verificação prévia"
da ronda anterior ("nenhuma unit está versionada ou instalada por script")
estava **errada**. `.agents/providers/proxy/dtx-litellm-proxy.service` já é
git-tracked, e `.agents/providers/proxy/ensure-proxy.sh` já o instala
(`cp` → `~/.config/systemd/user`, `daemon-reload`, `enable --now`). Convenção
já estabelecida: unit ao lado do subsistema + `ensure-*.sh` próprio. Seguir
essa convenção (`tasks/ensure-tsk-sweep.sh` + units ao lado de `tasks/`) em
vez de inventar `.agents/automation/systemd/` + `setup.sh::setup_systemd_units()`.

**Alterados:** `append_event.py` (allowlist + `append()` com CAS),
`move_task.py` (chama `append()`, ganha `--expect-last-event-id` obrigatório
em `validation`/`done`), `rebuild_kanban.py` e `rebuild_view.py` (guarda da
Camada B — **mesma lógica em código partilhado**, não duas reimplementações
independentes, achado N5), `tasks/README.md`, `CHEATSHEET.md` (regra já
existente: mudança em `.agents/` atualiza-o no mesmo commit),
`AGENTS.md`/`GEMINI.md`/`.github/copilot-instructions.md` (só o ponteiro
muda, texto inline mantido), `.gitignore` (`tasks/inbox.md`,
`.sweep-heartbeat`, `.events.lock`).

**Gerados, não versionados:** `tasks/inbox.md`, `.sweep-heartbeat`,
`.events.lock`. Derivam de `events.jsonl` (que É versionado) — o histórico
de notificações vive nos eventos `notification.raised/delivered/acked`, não
no projetado.

### 7. Fluxo do humano

1. Toast (digest herdr, ou `notify-send` se o herdr estiver rate-limited ou
   ausente).
2. Abre qualquer sessão CLI. O hook corre `brief.py`: heartbeat primeiro →
   inbox por prioridade → pergunta de diretor só se nada estiver pendente.
3. Responde em linguagem natural. Nunca edita ficheiros (tuiboard é
   read-only, confirmado — sem caminho de write-back).
4. O agente traduz:
   ```bash
   python3 tasks/move_task.py --task-id X --to-phase Y \
     --actor-kind human --actor-id nmc-costa --reason "..." \
     --expect-last-event-id <id>
   python3 tasks/notify.py --ack --dedup-key "<chave>"
   ```
5. `kanban.md`/`inbox.md` regeneram, tuiboard re-renderiza (chokidar), a
   escalada do toast para.

---

## Riscos aceites conscientemente

| # | Risco | Porque é aceite |
|---|---|---|
| R1 | Painel "Agents" do tuiboard e salto `H` do herdr só testados com Claude Code — Copilot/Antigravity não confirmados a aparecer lá | O contrato real é o `brief.py` na CLI; o painel é decoração, nada depende dele |
| R2 | `HERDR_PANE_ID` é coordenada posicional reutilizável | Mitigado: guarda-se `{pane_id, session_id}`, verificam-se os dois antes de `report-agent` |
| R3 | `review.judge_failed`/`budget.daily_cap_reached` sem produtor (trabalho da camada de execução, fora deste plano) | Consumidor já pronto na allowlist; aceite explicitamente como faseamento |
| R4 | `inbox.md` gitignorado, sem histórico próprio | O histórico real vive nos eventos `notification.*` em `events.jsonl` (versionado); `inbox.md` é projeção pura, como `board.md`/`kanban.md` |
| R5 | Wrapper `cpx` é opt-in — `copilot` direto perde o briefing | Mitigado por `alias copilot=cpx` no shell rc; o board fica correto na mesma |
| R6 | Rate-limit do herdr indocumentado, pode mudar num update | O gate de CI (`validate_herdr_contract.sh`) deteta a mudança de contrato |
| R7 | ~~Merge da PR #20 é ação humana fora deste plano~~ — feito 2026-09-21 | Resolvido |
| R8 | Sweep de 5 em 5 min, não processo de vida longa | Stateless (o relógio do SLA vive no log); granularidade de 5 min é irrelevante para SLA de 4h/escaladas de 30min |

## Próximos passos

1. ~~Merge da PR #20.~~ Feito.
2. Fase 0 de-risking (já delineada no `tasks/README.md`): instalar Agent
   Deck, confirmar CAS sob escrita concorrente, confirmar um script
   `Workflow` com `model` por fase, confirmar que um plugin herdr trivial
   abre um popup.
3. Implementar por esta ordem: `lifecycle.py` → `append()` com CAS →
   `notify.py`/`brief.py`/`sweep.py` → hook do Claude Code (com o script e o
   fragmento de `settings.json` versionados) → wrapper `cpx` → hook do
   Antigravity → units systemd (seguindo a convenção `ensure-*.sh` já
   estabelecida).
4. Teste de aceitação: duas sessões CLI diferentes (ex.: Claude Code +
   Copilot via `cpx`) a trabalhar em paralelo no mesmo `tasks/`, uma tarefa
   forçada a exceder o SLA e confirmar que a auto-validação não apaga uma
   rejeição humana concorrente (o cenário exato do Finding 2).
