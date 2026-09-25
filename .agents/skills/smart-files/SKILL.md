---
name: smart-files
description: >
  Create a "smart file" POC: a single zero-setup HTML file (vanilla JS, inline CSS, JSON as DB) that
  lives in a cloud drive (Teams/OneDrive, Dropbox, GDrive, GitHub) and gives non-technical users a
  dashboard-style interface for a basic digitisation need (PM, timesheets, site logs, checklists,
  registers) — agent-ready (AGENTS.md + stdlib CLI + skill, any provider) and sold in priced phases
  with diagrams, ROI (time + tokens) and price per phase. Use when the user asks for a "ficheiro
  inteligente", smart file, single-file HTML tool/POC, a Wrike/Excel/OneNote replacement for a client,
  or a new POC under Projects/notes/pocs/.
---

# smart-files

Build sellable single-file POCs that people actually adopt, and that any agent can operate.
Reference implementation: `~/Projects/notes/pocs/strike_pm/` (read its `README.md`, `AGENTS.md`,
`docs/PLAN.md` §2 and `tests/` before starting). Pattern origin: github.com/nmc-costa/HITtwintag.

## Non-negotiable rules

1. **One file runs the app.** `<poc>.html`: vanilla JS + inline CSS, **no CDN, no build, no framework,
   no network calls**, < 120 KB (demo data embedded as `<script type="application/json" id="exemplo">`).
2. **JSON files are the source of truth; localStorage is not.** On `file://` localStorage is undefined
   behaviour (Firefox may throw). Use it (and IndexedDB) only for identity, folder handle and an unsaved
   draft, always in try/catch, keys namespaced `<app>:v1:<espacoId>:…`.
3. **Two save modes, both first-class:**
   - *Ligado* (Edge/Chrome desktop): `showDirectoryPicker` on the team folder, handle kept in IndexedDB,
     debounced autosave (re-read → merge → `createWritable`). Its viability on managed PCs is **unverified
     until the P0.0 spike** — never promise it before.
   - *Ficheiro* (Firefox/Safari/blocked Edge): load folder via `<input webkitdirectory>` or drag & drop;
     **Guardar** downloads the person's own files to replace in the folder.
4. **Tell the truth about "one click".** No cloud executes `.html` on click (OneDrive/SharePoint/Teams,
   Dropbox, GDrive download it or show text; GitHub raw is text/plain; iOS can't open `file://`).
   P0 promise = *"sync the folder, double-click the `.html`"* on desktop. Mobile starts at the hosted phase.
5. **One writer per file — split data by owner.** Shared structure files (owner: PMO, monotonic `versao`,
   read-only in *Ficheiro* mode) + per-person files (`<dado>_<pessoa>_<AAAA-MM>.json`, `pessoas/<pessoa>.json`).
   Never compare clocks across PCs. Conflict copies: detect by filename **prefix**, merge by record key,
   **never delete** — move to `_arquivo/`.
6. **Deterministic record keys.** `k|<pessoa>|<data>|<alvo>` (no origin in the key → no double counting);
   origin (`app|repetir|cli|checkin`) and state (`confirmado|rascunho`) are attributes. Every write path
   (UI repeat, CLI, scheduled agent) is an idempotent upsert. Tombstones (`apagado: true`), never removal.
7. **Local dates only.** Never `toISOString()` for days (UTC shifts late-evening entries); timestamps as
   ISO with local offset.
8. **Frictionless for zero-knowledge users.** Default view = the daily task; primary action ≤ 2 clicks;
   "repeat yesterday" = 1 click; big targets; plain PT-PT; empty states that say what to do; example data
   one click away; `+h`-style action available in every view; undo toast; works at 360 px and keyboard-only.
   If a feature needs explaining, it is not P0.
9. **Agent-ready and provider-agnostic.** Every POC ships, inside P0:
   - `AGENTS.md` — data locations, schema, allowed operations, rules ("never hand-edit JSON", "agent
     writes only drafts", "ask when unsure", "send the model only the person's own data").
   - `skills/<poc>/SKILL.md` — the same contract as an installable skill.
   - `tools/<poc>.py` — **Python 3 stdlib-only** CLI (`config`, `tasks`/list, the primary write verb,
     summary, `validate`, `arquivar`): validates, writes atomically (`tmp` + `os.replace`), **only drafts,
     only the caller's own file**, exit codes `0 ok · 1 data · 2 refused · 3 exists`.
   - The human confirms drafts in the HTML with one click ("Confirmar tudo").
   The **daily check-in agent** (OS scheduler → notification → "what did you do?" → the person's own agent
   CLI, e.g. `claude -p` / `gemini -p` / `codex exec` / `copilot -p` → CLI drafts) is **Módulo A**, priced
   separately and gated on the client's IT deploying Python + an approved agent CLI centrally.
10. **Every POC folder is a future repo.** Self-contained; nothing references files outside it; old attempts
    go to `legacy/` (moved, never deleted).

## Folder layout (`~/Projects/notes/pocs/<poc>/`)

```
<poc>/
├── <poc>.html              the smart file
├── data/exemplo.json       realistic demo "pacote" (also embedded in the HTML)
├── README.md               PT-PT for the end user: 3 steps, how to register, save modes, FAQ, limits
├── AGENTS.md · skills/<poc>/SKILL.md · tools/<poc>.py · tools/embutir_exemplo.py
├── tests/correr.sh         CLI tests + CLI→HTML round-trip + E2E (headless Chromium over CDP)
├── docs/EVIDENCE.md        plan-orchestra evidence map (claim → source → confidence)
├── docs/PLAN.md            decisions, P0 spec, phases (mermaid), ROI, pricing, accepted risks, status
├── docs/img/               screenshots for README and the client guide
└── legacy/
```

## Workflow

1. **Clarify** in one message: the need, the users, the one daily action, company size. Assume and label
   what's missing (`Pressuposto`) — don't stall.
2. **Plan with `/plan-orchestra`** (mandatory). Researchers: (a) domain rules/regulation the data must
   satisfy, (b) what the incumbent tool gets wrong + fastest UX pattern, (c) scale path + costs,
   (d) existing code to reuse. **Reuse `strike_pm/docs/EVIDENCE.md` §A/B/E** (cloud, browser, pricing
   facts) instead of re-researching; refresh only if > 6 months old. Planner writes `docs/PLAN.md`;
   2 critique rounds max, then list accepted risks.
3. **Build P0** from `templates/smart-file-skeleton.html` (storage, save/load, drag & drop, unsaved state,
   tabs, toast, modal, local dates). Copy `strike_pm/tools/strike.py` structure for the CLI.
4. **Test** — `tests/correr.sh` must be green: no console errors / no network (`templates/cdp_check.mjs`),
   every view renders, primary action ≤ 2 clicks works, idempotency, conflict-copy merge, CLI hashes test
   (only own file changes), size < 122 880 bytes. Look at screenshots of every view before calling it done.
5. **Register the card** in `~/dotfiles/tasks`: `append_event.py --type task.created` (project `notes`,
   task-id `notes-poc-<poc>`), then move it through `move_task.py` with a `--handoff` pointing to
   `docs/PLAN.md`.

## Phases & pricing (reuse the shape, recompute the numbers)

| Phase | Scope | Pay trigger |
|---|---|---|
| P0.0 Spike | 1 day on a managed client PC + real sync client: does the HTML open, can it write? | Client decides to evaluate |
| P0 Ficheiro | single HTML + JSON + agent layer (AGENTS/SKILL/CLI) + 4-week pilot support | Spike not black; pilot accepted |
| Módulo A | daily check-in agent on the person's own agent CLI | IT deploys Python + agent CLI centrally |
| P1 Partilhado | hosted (GitHub Pages/SharePoint/Apps Script) + real identity + same JSON via API + mobile | Pilot adoption gate met |
| P2 Auditoria | submit/approve/lock, regulation rules, restricted data | First audit/report ≤ 3 months away |
| P3 Produto | integrations, NL entry, migration importer, portfolio | Incumbent tool cancelled |

- **Price** = billable days × day rate (default **400 €/day**, `Pressuposto`) × (1 + risk: 25 % closed
  scope, 30 % if client IT is involved). Always show the arithmetic.
- **Tokens** = MTok in/out × current list price (check the `claude-api` skill or claude.com/pricing —
  never from memory) with the model mix stated.
- **ROI** = incumbent licences avoided (**only from the phase that really allows cancelling**) + minutes
  saved/person/week × users × loaded hourly cost, as a **low/base/high** range; payback in months.

## Anti-patterns

- React/Tailwind/CDN "for speed" → breaks offline and zero-setup (the original strike_pm failed here).
- Promising "click in Teams and it opens" → false; trust dies at the first demo.
- One shared JSON edited by many people, or clock-based "latest wins" across PCs → silent data loss.
- Origin in the record key, non-idempotent "repeat"/agent writes → double-counted hours.
- Agents or the model writing JSON directly; agents confirming their own drafts.
- Logins, roles, settings pages in P0 → adoption killers (they belong to P1/P2).
- Pricing without the formula, or counting licence savings before the phase that allows cancelling.
