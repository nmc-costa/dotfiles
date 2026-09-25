# Agent Autonomy Charter — plan (2026-09-24)

**Status:** approved plan (owner decisions recorded in §9, 2026-09-25). Nothing implemented yet. Card:
`dotfiles-tsk-agent-autonomy-charter` (phase `planning`).
Produced by an Opus `Plan` agent with online research (sources at the end);
repo claims in §0 spot-checked by the dispatching session.
**Composes with:** `docs/AGENT_OS_UNIFICATION_PLAN.md` §7 (Decision 7,
path-scoped write permissions) and `tasks/plans/human-in-the-loop-notifications.md`
(the delivery channel). It forks neither.

---

## TL;DR (PT)

- **O quê:** um "estatuto de autonomia" curto (cerca de 60 linhas), partilhado
  por todos os agentes (Claude Code, Copilot CLI, Codex, Antigravity/Gemini).
  Define **o que os agentes decidem sozinhos** (quase tudo) e os **8 únicos
  gatilhos** em que te podem interromper.
- **Regra-base:** porta de dois sentidos (reversível) → o agente decide e faz
  até ao fim (branch → PR → CI verde → merge se for mecânico ou já aprovado) e
  depois reporta numa linha. Porta de sentido único (irreversível: dinheiro,
  segredos, enviar para fora como tu, apagar o irrecuperável, reescrever
  histórico, `~/Work`) → pára e manda-te um **BLUF de no máximo 5 linhas**:
  decisão, opções + recomendação, default se não responderes, prazo.
- **Sem resposta tua:** numa decisão reversível aplica-se o default quando o
  prazo acaba. Numa irreversível nada acontece e o card vai para `blocked`.
- **Onde vive:** `.agents/instructions/workspace-config/autonomy.instructions.md`,
  que já é distribuído a todos os harnesses via `sync.sh` e os ponteiros.
  Um bloco "core" de cerca de 15 linhas é copiado entre marcadores para os
  ficheiros de entrada de cada ferramenta, com check de CI contra divergências.
  O ficheiro fica **trancado (L2)** para os agentes.
- **Entrega:** reutiliza `events.jsonl` → `sweep.py`/`notify.py`/`brief.py`
  (novo facto `decision_needed`). Não há canal novo.
- **Medição:** interrupções por tarefa, taxa de aceitação dos defaults e
  reversões tuas de ações autónomas, tudo em `tasks/metrics.md`.
- **Recomendação:** avançar com 6 PRs pequenos (A–F). Precisas de decidir
  **só 4 coisas** (§9). A principal é aliviar a regra "o dono é o diretor".

---

## 0. Corrections to the brief (verified in the repo)

1. **`.agents/agentsmd/` and `.agents/policy/` do not exist yet.** `AGENTS.md`
   is still hand-written. The generator and the policy lock are *planned*
   (unification PR2–PR7, card `dotfiles-tsk-agent-os-pr2-pr7`, `backlog`,
   blocked by PR #34). So the charter needs an **interim lock** (PR-B), and
   is handed over to `write-policy.yaml` once that file lands.
2. **Existing text contradicts the goal and must be removed:**
   - `AGENTS.md:153`: "No automatic commits without explicit confirmation" (Claude).
   - `AGENTS.md:158`: "Doesn't modify files without intervention" (Copilot).
   - `task-brief` SKILL step 4, "Do not pick a task yourself", which mirrors
     the "owner is the director" rule in `tasks/README.md`.
3. **Claude Code already runs in auto mode** (`~/.claude/settings.json`:
   `"defaultMode": "auto"`). By default its classifier blocks "merging a pull
   request no human has approved". Permissive merge therefore needs an
   explicit `autoMode.allow` entry in **user** settings. Project-level
   `.claude/settings.json` is ignored for `autoMode`.
4. **Conflict:** Decision 7 marks `~/Work/**` as L2 (no edits at all). A path
   gate read literally would block all employer-repo work. The intent is
   "never copy Work content into shared config". Rescope it when
   `write-policy.yaml` lands (Q3).

---

## 1. Evidence map

| # | Claim | Source | Use |
|---|---|---|---|
| E1 | Autonomy is a design decision separate from capability. Five user roles: L1 Operator, L2 Collaborator, L3 Consultant, L4 **Approver** (involvement only on failure or high risk, with conditions set in advance), L5 Observer | Feng/McDonald/Zhang, Knight Institute 2025: https://knightcolumbia.org/content/levels-of-autonomy-for-ai-agents-1 · https://arxiv.org/abs/2506.12469 | **Vocabulary.** Workspace default = L4 |
| E2 | Anthropic advises against mandating human approval of every action. It favours visibility plus simple intervention. Experienced users auto-approve in over 40% of sessions; only 0.8% of actions look irreversible | https://www.anthropic.com/research/measuring-agent-autonomy | Exception-only escalation + post-hoc digest |
| E3 | Human control before high-stakes decisions; plan mode as the oversight point | https://www.anthropic.com/news/our-framework-for-developing-safe-and-trustworthy-agents | An approved plan counts as the human decision |
| E4 | Claude Code auto mode: a classifier with `allow`/`soft_deny`/`hard_deny`/`environment` prose rules. It reads CLAUDE.md. `autoMode` is read from user or managed settings only | https://code.claude.com/docs/en/permission-modes · https://code.claude.com/docs/en/auto-mode-config · https://claude.com/blog/auto-mode | Claude enforcement adapter |
| E5 | Constrain the action space; legibility; attributability; interruptibility; human approval for irreversible actions | https://cdn.openai.com/papers/practices-for-governing-agentic-ai-systems.pdf | One-way-door trigger; actor attribution |
| E6 | Type 1 (one-way door) vs Type 2 (two-way door) decisions. Using the Type 1 process for Type 2 decisions causes slowness | Bezos 2015 letter: https://s2.q4cdn.com/299287126/files/doc_financials/annual/2015-Letter-to-Shareholders.PDF | **Core escalation test** |
| E7 | RAPID: one named Decider; Agree = veto on predefined grounds only | https://umbrex.com/resources/frameworks/organization-frameworks/bain-rapid-decision-framework/ (secondary) | Agent decides two-way doors; the owner decides one-way doors. The veto belongs to deterministic gates, not to the owner's attention |
| E8 | BLUF: put the bottom line first | https://www.armywriter.com/AR25-50.pdf · https://en.wikipedia.org/wiki/BLUF_(communication) | Escalation template |
| E9 | AGENTS.md is schema-free Markdown; the nearest file wins; stewarded by AAIF / Linux Foundation | https://agents.md/ · https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation | Charter = prose, no new schema (`communityFirst`) |
| E10 | Each harness has its own permission layer, but none is cross-harness or decision-scoped:<br>• Codex: `approval_policy` + `sandbox_mode`<br>• Copilot CLI: `--allow-tool`/`--deny-tool`<br>• Gemini CLI: TOML policy engine<br>• Antigravity: allow/ask/deny | https://developers.openai.com/codex/agent-approvals-security · https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/allowing-tools · https://geminicli.com/docs/reference/policy-engine/ · https://agenticcontrolplane.com/blog/antigravity-permissions-reference (secondary) | Enforcement delegated to native layers via adapters |
| E11 | The initiator's approval of a Copilot-agent PR doesn't count toward required reviews; Copilot code review can approve PRs | https://github.com/orgs/community/discussions/179997 · https://github.blog/changelog/2026-09-01-copilot-code-review-can-now-approve-pull-requests/ | Self-approval under the same identity is weak |
| E12 | Autonomy level is a deployment choice | https://arxiv.org/abs/2311.02462 | Levels are set per domain |

**Not verified:**
- There is no authoritative SAE-style L0–L5 standard for software agents, so Knight L1–L5 is used instead.
- Microsoft and Google agent-governance guidance was not fetched.
- Per-path deny syntax for Copilot CLI and Codex.
- The path of Antigravity's permissions file.
- Whether branch protection is on for `nmc-costa/dotfiles`.
- Whether non-Claude harnesses follow the "read every `*.instructions.md`" pointer.

**Adoption (`communityFirst`):** Knight levels, Bezos doors, RAPID and BLUF.
The only new work is the glue: one prose charter plus thin native-layer adapters.

---

## 2. Composition with Decision 7

Two orthogonal axes. The **effective** permission is the stricter of the two.

| Axis | Owner | Question |
|---|---|---|
| Path level L0/L1/L2 (`write-policy.yaml`) | the gate (reads `origin/main`) | May this file be edited or applied? |
| Decision class (this charter) | agent judgement, bounded by the triggers | May I decide this myself, and do I tell the owner before, after, or never? |

| Class | Knight | Agent does | Owner sees |
|---|---|---|---|
| **A-OBS** | L5 Observer | Acts; logs to `events.jsonl`/git | Nothing unless they look |
| **A-APP** (default) | L4 Approver | Acts end-to-end; escalates only on a trigger | Digest line after the fact |
| **A-CON** | L3 Consultant | Prepares everything, sends a BLUF, applies the default at the deadline if reversible | One BLUF |
| **A-OWN** | L1 Operator | Prepares; never executes; card → `blocked` | One BLUF; nothing happens without a reply |

- A path at L2 is always A-OWN.
- A path at L1 may be edited and PR'd, but applying it to the machine stays
  human.
- Whether an agent may merge a PR is decided in §3.

---

## 3. Domain / decision matrix

"Done end-to-end" means the agent does **not** stop to ask "should I
continue?", "is this OK?" or "which name?".

| Domain | Class | Done end-to-end = | Escalate only if |
|---|---|---|---|
| Research, reading, web fetch, local analysis | A-OBS | Answer with sources | never |
| `tasks/` cards via `append_event.py`/`move_task.py` (always `actor-kind=agent`) | A-OBS | Card moved + handoff | CAS guards overwrite |
| Picking the next task | A-APP *(if Q1 = A)*, else A-CON | Take the top human-originated or already-planned item; state it in one line and start | nothing ready → BLUF |
| Proposing new tasks | A-OBS | `append_event.py`, agent kind (quota, D13) | never |
| `validation` sign-off | existing SLA | 4h SLA; more than 2 loops → human | T7 |
| `docs/**`, README, CHEATSHEET, CLAUDE.md, GEMINI.md, `global/**` | A-APP | Branch → PR → CI green → self-merge | T3 |
| `.agents/skills|prompts|workflows|instructions/**` (except charter and standards) | A-APP | Same + `./sync.sh` | T3 |
| `.agents/instructions/workspace-config/standards/**` | A-CON | PR + BLUF | always |
| **The charter itself**, `.agents/policy/**` | **A-OWN** | Draft a PR only | always |
| L1 paths (`setup.sh`, `sync.sh`, `bin/`, `scripts/`, `.github/`, `.githooks/`, `home/`, `os/`) | A-APP for the PR; merge per the git row; apply = human | PR + CI | apply needed; outside an approved plan (T8) |
| git: branch, commit, push own branch, rebase own unpushed work, open PR | A-OBS | — | never |
| **git self-merge** | A-APP when all hold:<br>(a) CI green<br>(b) PR body cites `Plan: <path>` or `Mechanical: <reason>`<br>(c) no path above L1<br>(d) no trigger fired<br>(e) repo is `nmc-costa/*`<br>Otherwise A-CON | Squash-merge, delete branch, move card | (a)–(e) fail |
| force-push, push to main, `--no-verify`, amending pushed commits, raw checkout/reset/stash/clean on shared `events.jsonl` | A-OWN (forbidden) | — | always |
| `~/Projects/*` | A-APP (a repo's `AGENTS.local.md` may tighten this) | as above | T1–T8 |
| `~/Work/*` *(Q3)* | Code, tests and pushing own branch = A-APP; **PR creation, merge, CI and infra = A-OWN** | Ready branch + BLUF | any outward action |
| Project-local package installs (venv, npm, mise-pinned) | A-APP | Install, pin, commit lockfile | — |
| System installs (pacman/yay), first Omarchy plugin install, any removal | A-OWN | Exact command in a BLUF | always |
| Secrets, credentials, `*.age`, `~/.config/chezmoi` | A-OWN | Never read or print | always (P0 if exposure is suspected) |
| Money | A-OWN | Quote + BLUF | always |
| Tokens / compute | A-APP within caps (Q2) | — | T4 |
| External comms (Slack, email, public posts, others' repos, publishing) | Drafts = A-OBS; **sending as the owner = A-OWN** | Draft + link in digest | before sending |
| Comments in the owner's own repos | A-APP | — | public repo + sensitive content |
| Deleting files | Agent-created or git-recoverable = A-APP; otherwise A-OWN | — | T1 |
| Live machine config (chezmoi, systemd, Hyprland) | Decision 7 L1 | PR | apply |

---

## 4. Escalation triggers (the only reasons to interrupt)

| ID | Trigger | Test | Default if no answer |
|---|---|---|---|
| **T1** | One-way door | Can the agent fully undo it within about 10 min, with no one else noticing? No → T1 | Don't do it; card → `blocked` |
| **T2** | Material ambiguity | Two readings give different deliverables, and doing the reversible or cheaper one first is not possible | Recommended reading, applied at the deadline |
| **T3** | Conflict with a recorded decision | Contradicts a plan, a D-number, a card, memory, or this charter | Keep the recorded decision |
| **T4** | Cost | Real money > 0, or a cap reached | Stop that path; continue other work |
| **T5** | Security | Secrets, auth, disabling checks, third-party code execution, routing around a denial | Don't |
| **T6** | Outward / identity | Acting as the owner toward humans or employer systems | Keep as a draft |
| **T7** | Stuck | Loop cap exceeded, same failure 2×, or blocked more than 24h | `blocked` (P0) |
| **T8** | Scope expansion | New subsystem or dependency class, or more than about 2× the planned diff | Do the in-scope part; propose the rest as a `new` card |

**Anti-triggers:** never escalate for these.
- naming, formatting, choosing between equivalent libraries
- fixing tests, step ordering
- "should I continue?" / "is this done?"
- mechanical merges and doc updates
- anything an approved plan already decided

**Batching:** one BLUF per task per session. Keep working on everything the
pending decision doesn't block.

### Escalation template (≤ 5 lines, BLUF)

```
DECISION <task-id> [T1|...|T8, P0|P1]: <question in one line>
A) <option> · B) <option> → recommend A: <why, <=15 words>
If no answer by <ISO datetime, default +4h>: <default action> (<reversible|parked in blocked>)
Done so far: <1 line + PR/card link>
Reply: "A", "B", or free text.
```

### Completion report (not an interrupt)

```
DONE <task-id>: <result in one line> · PR #<n> <merged|open> · follow-ups: <cards or "none">
```

---

## 5. Where it lives and how it reaches every harness

**Source:** `.agents/instructions/workspace-config/autonomy.instructions.md`
(`applyTo: "**"`).
- The existing pointer files already cover it: `.claude/CLAUDE.md`,
  `.codex/AGENTS.md`, `.copilot/copilot-instructions.md`, `.gemini/GEMINI.md`.
- `sync.sh` distributes it to `~/.agents/instructions/`.

**Budget:** about 60 lines / roughly 900 tokens. Rationale and citations go
in `docs/AUTONOMY_CHARTER_EVIDENCE.md`, which is not auto-loaded.

**Inlined core block:** about 15 lines / roughly 250 tokens between
`<!-- AUTONOMY:CORE BEGIN/END -->` markers.
- Goes in: `AGENTS.md`, `GEMINI.md`, `.github/copilot-instructions.md`,
  `.agents/rules/session-startup.md`, and the four per-tool pointer files.
- It is inlined because pointer-following is unverified for non-Claude tools,
  following the same duplication pattern as the notification plan's N4.
- Later it folds into `.agents/agentsmd/25-autonomy.md` once unification
  PR6's `agentsmd-render` exists.

Draft core block:

```
## Autonomy (workspace charter — full text: ~/.agents/instructions/workspace-config/autonomy.instructions.md)
- Default: act end-to-end without asking (branch → commit → PR → CI green → self-merge when the PR is
  mechanical or implements an approved plan, in the owner's own repos). Report after, in one line.
- Interrupt the owner ONLY for: T1 irreversible, T2 ambiguity that changes the deliverable, T3 conflict
  with a recorded decision, T4 money/caps, T5 security, T6 acting as the owner toward others,
  T7 stuck/loop cap, T8 scope beyond the agreed plan.
- Escalate with the 5-line BLUF (decision, options + recommendation, default + deadline, done so far).
  Reversible → apply the default at the deadline. Irreversible → do nothing; card to blocked.
- Never: handle secrets, spend money, send external messages as the owner, force-push/push main,
  edit this charter or .agents/policy/**, sign tasks/ events as a human.
- Never ask: naming, formatting, "should I continue?", "is this OK?", mechanical merges.
```

**Per-harness enforcement adapters.** These are permission changes, so the
owner applies them (A-OWN). Fragments are versioned under
`.agents/harnesses/<tool>/`.

| Harness | Fragment |
|---|---|
| Claude Code | `autoMode.environment` += owner's repos `github.com/nmc-costa/*`<br>`autoMode.allow` += merging an agent-authored PR in `nmc-costa/*` when CI is green and the body cites `Plan:`/`Mechanical:`; never in `~/Work`<br>`permissions.deny` on the charter + `.agents/policy/**`<br>Keep `"$defaults"` |
| Codex CLI | `approval_policy = "on-request"`, `sandbox_mode = "workspace-write"` |
| Copilot CLI | `bin/cpx` flags: `--allow-tool 'write'`, `--allow-tool 'shell(git:*)'`, `--deny-tool` for force-push / `--no-verify` (syntax to verify) |
| Gemini / Antigravity | `~/.gemini/policies/autonomy.toml` (deny writes to charter paths, `ask_user` for force-push); Antigravity allow/ask/deny arrays (path to verify) |

**Self-amendment lock:**
1. **Interim (PR-B):**
   - Claude `permissions.deny`, which applies in every mode.
   - The Gemini TOML deny.
   - A `charter-lock` CI job that requires the `owner-approved` label.
     Honest limit: agents use the owner's `gh` identity, so this is a speed
     bump, not a wall.
2. **Final:** an L2 glob in `write-policy.yaml`. The gate reads it from
   `origin/main`, so an unmerged edit has no effect.
3. **Optional hard wall:** signed commits on charter paths with a key loaded
   via `ssh-add -c` (confirmation on every use).

---

## 6. Delivery: reuse the notification plan

- **New fact:** `decision_needed` (added to `lifecycle.FACT_TYPES`), written
  by a thin `tasks/escalate.py` that wraps `append_event.append()`. It
  validates:
  - trigger ∈ T1–T8
  - at least 2 options
  - a recommendation
  - `default` and `deadline`
  - `reversible: bool`
  - rendered BLUF ≤ 5 lines
- **Priority:** T1/T5/T7 → P0 (individual toast); everything else → P1
  digest via `notify.py`.
- **`sweep.py`:** at the deadline, for reversible decisions only, emits
  `decision.default_applied`. It is CAS-guarded, so a human
  `decision.resolved` always wins. Irreversible decisions move the card to
  `blocked`, which feeds the existing `blocked_too_long` P0 path.
- **`brief.py`:** lists `decision_needed` first. The agent transcribes the
  owner's answer as `decision.resolved`, then runs `notify.py --ack`.
- **Interactive sessions:** the agent prints the same BLUF as its final
  message and keeps doing independent work. The event is logged regardless,
  so the metric is the same across harnesses.

---

## 7. Rollout (small PRs)

| PR | Content | Level | Acceptance |
|---|---|---|---|
| **A — charter text** | `autonomy.instructions.md`; evidence doc; core block in the 8 target files; remove `AGENTS.md:153,158`; update `.agents/instructions/README.md` + CHEATSHEET | L0 | `validate_dotfiles.sh` passes; 2 markers per target file; core ≤ 220 words; full file ≤ 1,000 tokens; no "without explicit confirmation" wording left. **Owner merges.** |
| **B — lock** | `scripts/check_autonomy_core.sh` (in `validate_dotfiles.sh` + CI); `charter-lock` job; Claude deny fragment; Gemini TOML fragment | L1 | CI fails on a hand-edited copy; a Claude `Edit` on the charter is denied after the owner applies the fragment |
| **C — escalation plumbing** | `tasks/escalate.py`; `decision_needed` fact; `sweep.py` default-at-deadline with CAS; `brief.py` ordering; cards show the pending decision | L0 | Tests: BLUF > 5 lines rejected; default applied exactly once; a human answer 1s before the deadline wins (10-way race); irreversible → `blocked` |
| **D — self-merge + director rule** | `scripts/can_self_merge.sh`; `task-brief` SKILL + `tasks/README.md` per Q1; Claude `autoMode` fragment | L1/L0 | Dry-run on 5 past PRs gives the expected verdicts; Claude merges a mechanical doc PR without a prompt |
| **E — other harness adapters** | Codex, `bin/cpx` (with `dotfiles-tsk-cpx-copilot`), Antigravity fragments | L1 | Smoke prompts per harness: merge a mechanical PR → does it; send a Slack message → drafts only; edit the charter → refused |
| **F — metrics** | "Autonomy" section in `rebuild_metrics.py`; demo extended with one escalation | L0 | Metrics below appear in `metrics.md` |
| *(later)* | `25-autonomy.md` fragment; L2 glob; remove the interim check | with unification PR2/PR6 | `agentsmd-render --check` green |

**Sequencing:** A → B → (C ∥ D) → E → F. Only the final fold-in depends on
unification.

### Success metrics (review after 2 weeks)

| Metric | Target | Tuning signal |
|---|---|---|
| Interrupts per completed task | median 0, mean ≤ 0.3 | Higher → triggers too sensitive |
| Escalations missing a default or deadline | 0 | — |
| Default acceptance rate | ≥ 80% | About 100% → demote that class to A-APP |
| Owner overrides of autonomous actions | < 5% of autonomous merges | Higher → tighten that domain |
| Native-layer denials per session | trending down | Missing `allow`/`environment` rules |
| One-way-door actions without a BLUF | 0 | Any occurrence → incident + rule fix |

---

## 8. Risks

1. **Same identity.** Agents use the owner's `gh`/git identity, so GitHub
   can't tell agent merges from owner merges, and the label lock is
   bypassable. Mitigations: native denies, the future L2 gate, optional
   signed commits.
2. **Pointer-following is unverified** outside Claude. Mitigated by the
   inlined core and the PR-E smoke tests.
3. **The auto-mode classifier may still block merges** if the `allow`
   wording doesn't match its rule semantics. Check with
   `claude auto-mode config` / `critique`.
4. **Default-at-deadline racing the owner's answer.** The CAS makes the human
   write win, and only reversible decisions auto-apply.
5. **`Mechanical:` creep.** Watch the override-rate metric;
   `can_self_merge.sh` caps a `Mechanical:` PR at 15 changed files.
6. **The `~/Work/**` L2 glob** in Decision 7 must be rescoped (Q3).

## 9. Owner decisions (answered 2026-09-25)

**Resolved:** Q1 = A (auto-start), Q2 = B (~2M tokens / ~90 min cap), Q3 = A (code + push own branch in `~/Work`; PRs/merge/CI/external stay the owner's; rescope Decision 7 glob), Q4 = A for `nmc-costa/*` L1 paths, B (owner merges) for `.github/**` and `.githooks/**`. PR-A can start.

Original questions, for the record:


1. **Director rule (T3).** When nothing is pending, may the agent start the
   top human-originated or already-planned backlog item and say so in one
   line?
   - A) auto-start
   - B) keep asking
   - → recommend **A**. Default if no answer: B.
2. **Per-task cap.**
   - A) no extra cap
   - B) escalate above about 2M tokens or about 90 min of wall-time
   - → recommend **B**.
3. **`~/Work` repos.**
   - A) agents may code and push feature branches; PRs, merges, CI and
     external actions stay the owner's
   - B) local edits only
   - → recommend **A**, plus rescoping the Decision 7 glob.
4. **Self-merging L1 PRs** that implement an approved plan step with CI green.
   - A) allowed
   - B) always the owner's merge
   - → recommend **A** for `nmc-costa/*`, except **B** for `.github/**` and
     `.githooks/**`.

---

Sources: see the evidence map (§1).
