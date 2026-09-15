# tasks/

Sistema de tracking de tarefas do workspace (PoC). Vive aqui, não num repo
separado — decisão fixada por D2/D7 do doc "Workspace Ágil" (`Repo-Cérebro`
= `dotfiles/`) e D11 (eventos vão para o log central do repo do workspace).
Contexto completo das decisões: `KICKOFF.md` (o pedido original) e o plano
que resolveu as tensões que ele deixou em aberto vive na sessão que o
implementou — ver `notes/ideas/architecture/Workspace Agil para Agentes
Multiplataforma.md` (D1–D18) e `notes/ideas/agents/Agente Orquestrador -
Jarvis do Diretor Humano.md` (schema de tarefa, §5.2) para as fontes.

## Modelo: duas camadas

1. **`events.jsonl`** — log de eventos append-only. É a **fonte de verdade**
   (D9/D10): cada linha é um facto que aconteceu, nunca se edita uma linha
   já escrita — uma correção é sempre um evento novo. Nunca editar à mão.
2. **`tarefas.md`** — tabela gerada a partir do log (colunas por §5.2 do doc
   Jarvis: id, título, projeto, estado, energia, estimativa, prazo,
   bloqueado_por, origem, criado, tocado). É uma **vista descartável e
   reconstruível**, nunca editada à mão — o equivalente PoC ao índice
   SQLite/DuckDB que D9 descreve para escala maior.

## Como usar

Acrescentar um evento (única forma de escrever no log):

```bash
python3 tasks/append_event.py --type tarefa.criada \
  --actor-kind humano --actor-id nmc-costa \
  --task-id dotfiles-minha-tarefa \
  --payload '{"titulo":"...", "projeto":"dotfiles", "energia":"mecânica", "origem":"eu"}'

python3 tasks/append_event.py --type tarefa.estado_mudou \
  --actor-kind humano --actor-id nmc-costa \
  --task-id dotfiles-minha-tarefa \
  --payload '{"estado":"em curso"}'
```

Regenerar a tabela depois de qualquer mudança ao log:

```bash
python3 tasks/rebuild_view.py
```

## Estados (D12)

`new → todo → em curso → em validação → feito`. `bloqueada` e `abandonada`
(enum mais antigo do doc Jarvis) não são estados próprios nesta PoC:
"bloqueada" é qualquer estado com `bloqueado_por` preenchido; "abandonada"
é a tarefa a ficar sem eventos novos, sinalizada no `tocado` (apodrecimento),
sem coluna de estado dedicada.

## Proveniência decide a porta (D13)

Tarefa criada por um humano entra direto em `todo`. Proposta de um agente
(`actor.kind: agente`) entra em `new`, com quota de 3 propostas abertas em
simultâneo, expiração de 14 dias, e deduplicação por fingerprint do
`payload` — tudo aplicado automaticamente por `append_event.py`, não por
convenção humana (D14: script antes de regra).

## Fora de âmbito nesta PoC

Automação (cron/systemd/GitHub Actions), índice SQLite/DuckDB, `tarefas.csv`
(só quando `tarefas.md` passar "umas dezenas de linhas" — regra do próprio
doc Jarvis §5.4), a persona Jarvis/orquestrador em si. Ver o histórico da
sessão que criou isto para o raciocínio completo.
