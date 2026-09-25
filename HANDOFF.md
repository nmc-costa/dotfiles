<!-- handoff:block 2026-09-25T22:53Z -->
# Handoff — Radar consolidation sweep: both timers live, 2 unmerged briefs, PR #103 landed - owner wants ONE session (2026-09-25)

> **To whoever picks this up (any harness, any model):** this top block is the
> current handoff; blocks below it are history. Check the Snapshot against live
> state (`git status`, `git log`, open PRs) before acting on it, then start at
> **Next step**. When you stop with work unfinished, add a new block on top
> (`/handoff`, or `handoff.py new`) rather than editing this one.

## Goal

Owner opened a `researcher-radar` session and asked "all" — a full radar status sweep (timers, state, briefs). Mid-sweep the owner redirected to consolidation, verbatim: `"faz handoff disto porque tenho outras sessoes a correr radars e preciso de ter so uma sessaõ"` — several parallel radar sessions are running; only ONE session should own the radars going forward. This session ends here and hands over; it installed nothing and decided nothing.

## Done

All verified 2026-09-25 ~22:52Z against live state (`systemctl --user list-timers --all`, `ls ~/.local/state/<radar>/`, `git -C ~/dotfiles log`/`ls-tree`):

- **Both timers installed + ACTIVE**: `omarchy-radar.timer` next fire Sat 2026-09-26 08:02:39 WEST; `harness-radar.timer` next fire 08:21:47 WEST. Units + `omarchy-radar.service.d/` drop-in present in `~/.config/systemd/user/`.
- **Both radars ran end-to-end ~23:31–23:52 WEST today**: fresh state in `~/.local/state/omarchy-radar/` (history.db 57KB, seen.json, status.json, snapshots) and `~/.local/state/harness-radar/` (history.db 94KB, prompt file, status.json).
- **Both first briefs exist on local, unmerged branches**: `radar/omarchy-radar/2026-09-25` @ `377dc27` and `radar/harness-radar/2026-09-25` @ `7357d35` — each with `briefs/<radar>-2026-09-25.md` + `.ranked.json`.
- **PR #103 confirmed in `main`** (`e586b98`, harness-agnostic agent step `--prepare`/`--finalize` + opencode nested backend) — it landed after the 22:51Z block below.
- **Point-in-time anomaly recorded**: at ~22:21Z `router.sh list/status` reported "not installed/enabled" and "no status.json"; state existed minutes later — the other sessions' runs were concurrent with this sweep. A single `router.sh status` reading can be stale while runs are in flight; verify with `systemctl` + `ls` before acting on it.
- **Live collision witnessed (meta-lesson for `handoff.py`)**: this session's first handoff block was silently clobbered by the harness-radar session's concurrent `handoff.py new` (read-modify-write, no `flock`). A block may have been lost again — the block directly below this one (harness-radar slice, 22:53Z) plus the 22:51Z one are both intact.

## Decisions

- **None.** Owner redirected the offered "install timers / first run" paths into "handoff instead" — the other sessions had already installed and run everything. Propose-only rule stands untouched: both brief branches left unmerged, nothing pushed or merged here.

## Open / risks

- **A harness-radar agent step may still have been MID-RUN at write time** (`last-agent-output.json` was 0 bytes at 22:50Z). Its session's handoff block sits directly below this one (same minute) — **read it; it is authoritative on the agent-backend rework and remaining work** ("remaining: omarchy run.sh mirror + docs").
- **Both brief branches are local** — check `git branch -r` / pushed state before any branch cleanup, or the first briefs are lost.
- **Unverified here**: whether the GLM drop-in `~/.config/systemd/user/omarchy-radar.service.d/override.conf` (`RADAR_CLAUDE_BIN`) is now redundant post-#103 (nested backend defaults to opencode); whether omarchy-radar's `run.sh` got the #103 mirror rework.
- **`handoff.py` has no write lock** — concurrent `/handoff` in the shared checkout silently loses a block (happened here). Fix idea: `flock` the file in `handoff.py` (one-line card-worthy).
- **Shared checkout has other sessions' uncommitted work** (`tasks/cards/*`, `tasks/events.jsonl`): never `git checkout --/reset/stash/clean` those; commit only files you wrote.
- Claude weekly limit until **Sep 29, 11:00 Europe/Lisbon** — only matters if `RADAR_AGENT_BACKEND=claude` is used.

## Next step

1. In the single consolidated session: **read the handoff block directly below this one** (harness-radar slice) — its Open/risks + Next step hold the remaining radar work.
2. Sweep anything newer: `cd ~/dotfiles && git log --oneline -8` (past `e586b98`), `gh pr list`, `git branch -a | grep radar`, plus any HANDOFF.md block newer than this one.
3. Owner reviews + merges both brief branches (squash; each touches only `briefs/`): `git -C ~/dotfiles show radar/omarchy-radar/2026-09-25:briefs/omarchy-radar-2026-09-25.md` and `git -C ~/dotfiles show radar/harness-radar/2026-09-25:briefs/harness-radar-2026-09-25.md`.
4. Check the GLM drop-in for redundancy: `cat ~/.config/systemd/user/omarchy-radar.service.d/override.conf` — if opencode backend is confirmed live, delete the drop-in and `systemctl --user daemon-reload`.
5. Tomorrow ~08:02 / 08:21 WEST: verify the first unattended runs (`systemctl --user list-timers`, `jq . ~/.local/state/<radar>/status.json`, new `radar/<name>/2026-09-26` branches).

## Snapshot

_Generated by `handoff.py` at write time — verify against live state before trusting it._

- **Written:** 2026-09-25 22:53 UTC on `omarchy` by `opencode` / `local/zai-org/GLM-5.3-Flash`
- **Repo:** `/home/nbugz/dotfiles` — branch `main`
- **Upstream:** `origin/main` — 0 ahead, 0 behind

Uncommitted changes:

```
 M tasks/cards/dotfiles-tsk-chronicle-d7.md
 M tasks/cards/dotfiles-tsk-researcher-radar.md
 M tasks/cards/dotfiles-tsk-skill-gauntlet-prompting.md
 M tasks/events.jsonl
?? briefs/
```

`tasks/brief.py` at write time:

```
Nothing pending. What do you want to work on?
```

---

<!-- handoff:block 2026-09-25T22:53Z -->
# Handoff — radar consolidation: harness-agnostic agent step landed (PR #103), harness-radar first brief + timer live — remaining: omarchy run.sh mirror + docs (2026-09-25)

> **To whoever picks this up (any harness, any model):** this top block is the
> current handoff; blocks below it are history. Check the Snapshot against live
> state (`git status`, `git log`, open PRs) before acting on it, then start at
> **Next step**. When you stop with work unfinished, add a new block on top
> (`/handoff`, or `handoff.py new`) rather than editing this one.

## Goal

Owner is consolidating three parallel radar sessions into ONE (`"faz handoff disto porque tenho outras sessões a correr radars e preciso de ter só uma sessão"`). This session's slice was `harness-radar` end-to-end plus the owner's architecture correction: the agent step must be **harness-agnostic** — the session that invokes the skill IS the agent (`"onde eu estou a chamar a skill deve ser o agente que corre os scripts"`), and the nested CLI backend must run on the owner's **opencode + custom DTX provider** (`"isto tem de ser feito com o opencode com o custom provider"`), not on quota-dead `claude`.

## Done

- **PR #103 merged (`e586b98`, on top of PR #100's `6067903`)** — the agent step is now harness-agnostic:
  - `harness-radar/scripts/run.sh` has three modes: `--prepare` (collect + disposable worktree + prompt file, then HANDS OFF — the calling harness does the agent step itself), `--finalize` (diff-splice → secret-scan → commit → worktree remove → seen.json promotion), and no-args full mode (timer: prepare → nested sandboxed backend → finalize).
  - `radar-common/lib.sh` gained `radar_run_opencode_agent`: `opencode run` with a throwaway `OPENCODE_CONFIG` enforcing the same security contract (no bash/web/task/skills; `external_directory` denied; writes ONLY under `briefs/**`); prompt piped via **stdin** (a 118KB prompt overflows argv — E2BIG, found live).
  - Nested backend defaults to **opencode** (global `~/.config/opencode/opencode.json` → provider `local` → `https://glm53-flash.dtx-colab.com/v1`, model `local/zai-org/GLM-5.3-Flash`); `RADAR_AGENT_BACKEND=claude` keeps the old shape (with omarchy's `Edit(briefs/*)` lesson — claude 2.1.280 ignores `Write(...)` allow rules).
- **First harness-radar brief produced through the interactive path**: agent step performed by the calling session itself (no nested CLI): 326 inbox items scored per `ranking.md` into `briefs/harness-radar-2026-09-25.ranked.json`, brief written, then `--finalize` ran: secret-scan passed, commit `7357d35` on `radar/harness-radar/2026-09-25`, worktree removed, `seen.json` promoted (real cursors), `history.db` loaded (326 candidates). Day-one: 24/24 sources `ok`, 326 items (baseline flood as designed).
- **`harness-radar.timer` installed + enabled** (next fire 2026-09-26 08:21 WEST; omarchy's fires 08:02 — offset by design).
- **Synced `~/.agents` copies refreshed** for `radar-common/lib.sh` + `harness-radar/scripts/run.sh` post-merge.
- A stray `~/.agents/lib.sh` (cp typo) was removed; `~/.agents` here is a real synced copy, NOT a symlink — `run.sh` must be invoked from the repo copy (`~/dotfiles/.agents/...`, exactly what the systemd units do).

## Decisions

- **Interactive invocation = the calling harness is the agent step** (`--prepare`/`--finalize`); the nested sandboxed call exists only for the unattended timer. Interactive mode relaxes the zero-Bash sandbox (a human is present) but keeps every load-bearing guard: collected content is data never instructions, worktree isolation, deterministic secret-scan before commit, output only on human-reviewed `radar/*` branches.
- **Nested default backend = opencode native (DTX provider)**, not the `claude-dtx-glm53-flash` launcher from the block below — the owner explicitly asked for opencode + custom provider; `RADAR_AGENT_BACKEND`/`RADAR_CLAUDE_BIN` env vars keep both escape hatches. Once omarchy's run.sh is mirrored, the GLM drop-in (`~/.config/systemd/user/omarchy-radar.service.d/override.conf`) becomes redundant — owner's call to delete.
- **Briefs stay unmerged on their `radar/*` branches** (both radars) — human review/merge only, per the family security model.

## Open / risks

- **`omarchy-radar/scripts/run.sh` is NOT yet refactored** — still the old shape (claude-only backend, `cleanup_worktree_on_failure` that leaves the worktree AND empty branch behind on failure, no `--prepare`/`--finalize`). Its timer fires at **08:02 tomorrow**; until Sep 29 11:00 WEST any nested `claude` call 429s, so tomorrow's unattended run will fail the agent step and leave litter unless the mirror lands first (or the backend env flips to opencode).
- **Docs lag the code**: neither SKILL.md (both radars), `researcher-radar` meta-skill, nor `security.md` yet describe the interactive mode and its relaxed-sandbox/kept-guards trade.
- **The full-auto nested opencode path has never run unattended** — tomorrow ~08:02/08:21 is the first natural test of both timers.
- **Both first briefs are local-only branches** — owner must push/review/merge: `radar/omarchy-radar/2026-09-25` @ `377dc27`, `radar/harness-radar/2026-09-25` @ `7357d35`.
- Claude weekly quota 429 until **Sep 29, 11:00 Europe/Lisbon** (any nested `claude` backend fails until then; opencode unaffected).
- Shared checkout: `tasks/events.jsonl` + cards are other sessions' live writes — never `git checkout --/reset/stash/clean` them. Untracked repo-root `briefs/` predates this session (see chronicle block below) — untouched.
- Chronicle PRs **#98** and **#102** still await owner merge (blocks below — not this slice).

## Next step

1. **Mirror the run.sh refactor to `~/dotfiles/.agents/skills/omarchy-radar/scripts/run.sh`** using `.agents/skills/harness-radar/scripts/run.sh` @ `e586b98` as the template (same three modes + `radar_discard_failed_attempt`; keep omarchy's own prompt allowlist text — `~/.config/hypr/`, `~/.config/omarchy/`, `~/.config/foot/`, `~/.bashrc`; keep claude's allowed list as `Read,Grep,Glob,Edit(briefs/*)` per the 2.1.280 Edit-rule lesson; set the nested default backend to opencode). `bash -n`, then commit on a `claude/*` branch → PR → squash merge → refresh `~/.agents/skills/omarchy-radar/scripts/run.sh` from the repo copy. Do this BEFORE 08:02 if possible.
2. Update the docs in the same PR: both radars' `SKILL.md` (new "Interactive invocation" section: prepare → you are the agent step → finalize), `researcher-radar/SKILL.md` (family-level note), `harness-radar/security.md` (the interactive-mode sandbox trade, explicitly).
3. Tomorrow: verify both timers' first unattended runs — `systemctl --user list-timers`, `jq . ~/.local/state/{omarchy,harness}-radar/status.json`, new `radar/<name>/2026-09-26` branches, no leftover worktrees under `~/.local/state/*/worktrees/`.
4. Owner: review + merge the two brief branches (paths in Open/risks); then optionally delete the redundant GLM drop-in override (see Decisions).
5. Append a `task.note` to `dotfiles-tsk-researcher-radar` via `python3 tasks/append_event.py --type task.note --actor-kind agent --actor-id <your harness> ...` (never human-attributed).

## Snapshot

_Generated by `handoff.py` at write time — verify against live state before trusting it._

- **Written:** 2026-09-25 22:53 UTC on `omarchy` by `claude` / `zai-org/GLM-5.3-Flash`
- **Repo:** `/home/nbugz/dotfiles` — branch `main`
- **Upstream:** `origin/main` — 0 ahead, 0 behind

Uncommitted changes:

```
 M tasks/cards/dotfiles-tsk-chronicle-d7.md
 M tasks/cards/dotfiles-tsk-researcher-radar.md
 M tasks/cards/dotfiles-tsk-skill-gauntlet-prompting.md
 M tasks/events.jsonl
?? briefs/
```

`tasks/brief.py` at write time:

```
Nothing pending. What do you want to work on?
```

---

<!-- handoff:block 2026-09-25T22:51Z -->
# Handoff — omarchy-radar: installed, 3 pipeline bugs fixed, first brief on radar branch, timer live (GLM-routed agent step) (2026-09-25)

> **To whoever picks this up (any harness, any model):** this top block is the
> current handoff; blocks below it are history. Check the Snapshot against live
> state (`git status`, `git log`, open PRs) before acting on it, then start at
> **Next step**. When you stop with work unfinished, add a new block on top
> (`/handoff`, or `handoff.py new`) rather than editing this one.

## Goal

Owner is consolidating three parallel radar sessions into one ("eu tenho que juntar isto numa só unica sessão, mas existem 3 sessoes de radars que estão a dar o mesmo erro"). This session's slice: install `omarchy-radar` end-to-end on this machine, fix its pipeline, produce the first brief, enable the timer. The shared error killing all radar sessions: **Claude weekly usage limit** (resets Sep 29, 11:00 Europe/Lisbon) — every `claude` CLI call fails with "You've hit your weekly limit".

## Done

- **omarchy-radar installed + timer live**: units copied to `~/.config/systemd/user/`, `systemctl --user enable --now omarchy-radar.timer` (OnCalendar=08:00, Persistent=true, next fire 2026-09-26 ~08:02). Explicitly-flagged manual enable, per the skill's README.
- **collect.sh validated**: all 9 sources `ok` in `~/.local/state/omarchy-radar/status.json`; dedupe acceptance criterion met (second same-day run → byte-identical inbox).
- **3 pipeline bugs found + fixed** (now in `main` via PR #100, commit `6067903`):
  1. `collect.sh:279` (news feed) + Reddit collector — jq `index(.filter)` passes a path filter to `index()`, which errors **and exits 0**: new feed items were silently marked seen without ever entering the inbox (permanent data loss on promotion). Fixed with the `as $g`/`as $i` binding pattern (matches the MCP collector's existing style).
  2. Reddit `.json` endpoint 403-blocks this machine's UA/IP class → switched collector to the Atom `.rss` feed (200 OK, stdlib ElementTree) + updated `sources.md`.
  3. `run.sh:151` — `Write(briefs/*)` allow rule is **no longer honored by Claude Code 2.1.280** ("only Edit(path) rules are; Edit rules cover all file-editing tools") → changed to `Edit(briefs/*)`. Without this the agent scores everything then cannot write the brief.
- **`radar-common/lib.sh`: `RADAR_CLAUDE_BIN` override added** (default stays `claude`; backwards compatible) so a machine can route the agent step through an opt-in provider launcher.
- **First brief produced end-to-end**: branch `radar/omarchy-radar/2026-09-25`, commit `377dc27`, files `briefs/omarchy-radar-2026-09-25.md` + `.ranked.json`. All README acceptance criteria verified: single commit touching only its own brief files, worktree removed, `main` checkout untouched, secret-scan passed, `seen.json` promoted, 156 candidates in `~/.local/state/omarchy-radar/history.db`.
- **Claude-limit workaround live** (owner's own dtx stack): `uv tool install "litellm[proxy]"` → `dtx-litellm-proxy.service` active on 127.0.0.1:4444 (master key auto-generated at `~/.custom_providers/proxy.env`) → launcher `~/.local/bin/claude-dtx-glm53-flash` (via `.agents/providers/adapters/claude-code.sh apply dtx-glm53-flash`) → machine-local drop-in `~/.config/systemd/user/omarchy-radar.service.d/override.conf` sets `RADAR_CLAUDE_BIN` to it. Smoke-tested, then used for the real run (GLM-5.3-Flash).

## Decisions

- **Agent step routed through the owner's GLM proxy** rather than waiting for the Sep 29 reset — the day-one flood (597 inbox items) would otherwise be marked seen without ever being briefed (silent loss, same failure mode as bug 1). Revert = delete the drop-in file above; daily cost after day one is small (only genuinely new items).
- **Reddit via `.rss`, not `.json`** — the JSON endpoint 403s this machine; RSS is the only keyless endpoint that still serves it.
- **Brief left unmerged on its branch** — the radar's own security model reserves review/merge for the human; this session did not push or merge it.

## Open / risks

- ~~A radar session was STILL WORKING in this shared checkout at handoff time (~22:5xZ)~~ **Resolved**: that session's work landed as PR #103 (`e586b98`, harness-agnostic `--prepare`/`--finalize` + opencode backend) — see the top block, which supersedes the backend decision below.
- **Brief branch `radar/omarchy-radar/2026-09-25` is local-only** — push/merge it before any cleanup of stale branches, or the first brief is lost.
- ~~`harness-radar` is not installed on this machine~~ **Done** — timer installed + enabled by the session above (next fire 08:21).
- **`dtx_providers.env`-backed proxy is live** (`dtx-litellm-proxy.service` enabled) — daily radar runs spend the owner's GLM quota unattended; acceptable per owner's "do it all", but worth knowing.
- Claude weekly limit resets **Sep 29, 11:00 Europe/Lisbon**; until then any headless `claude` call fails the same way for every session.

## Next step

1. ~~Sweep for the other two radar sessions' output~~ — done: their work is merged (PR #103) and handed off in the **top block**; start there.
2. Decide the single agent-step backend (opencode native vs `claude-dtx-glm53-flash` launcher) and make `omarchy-radar` + `harness-radar` use it consistently; delete whichever drop-in/env becomes redundant. — *Top block decided: opencode native by default; mirroring omarchy's run.sh + drop-in cleanup remain.*
3. Review + merge the first brief: `git -C ~/dotfiles show radar/omarchy-radar/2026-09-25:briefs/omarchy-radar-2026-09-25.md`, then merge the branch (it only touches `briefs/`).
4. Tomorrow ~08:02, verify the timer's first unattended run: `systemctl --user list-timers omarchy-radar.timer`, `jq . ~/.local/state/omarchy-radar/status.json`, new `radar/omarchy-radar/2026-09-26` branch.
5. ~~Install `harness-radar`'s timer the same way~~ — done (top block).

## Snapshot

_Generated by `handoff.py` at write time — verify against live state before trusting it._

- **Written:** 2026-09-25 22:51 UTC on `omarchy` by `opencode` / `local/zai-org/GLM-5.3-Flash`
- **Repo:** `/home/nbugz/dotfiles` — branch `main`
- **Upstream:** `origin/main` — 0 ahead, 0 behind

Uncommitted changes:

```
 M .agents/automation/radar-common/lib.sh
 M .agents/skills/harness-radar/scripts/run.sh
 M .gitignore
 M tasks/cards/dotfiles-tsk-chronicle-d7.md
 M tasks/cards/dotfiles-tsk-researcher-radar.md
 M tasks/cards/dotfiles-tsk-skill-gauntlet-prompting.md
 M tasks/events.jsonl
?? briefs/
```

`tasks/brief.py` at write time:

```
Nothing pending. What do you want to work on?
```

---

<!-- handoff:block 2026-09-25T22:26Z -->
# Handoff — Chronicle D7 built (PR #98) — d4-d6 merged+deployed by owner (2026-09-25)

> **To whoever picks this up (any harness, any model):** this top block is the
> current handoff; blocks below it are history. Check the Snapshot against live
> state (`git status`, `git log`, open PRs) before acting on it, then start at
> **Next step**. When you stop with work unfinished, add a new block on top
> (`/handoff`, or `handoff.py new`) rather than editing this one.

## Goal

Continue the chronicle skill-layer plan from the previous handoff: land D4-D6 (3 PRs were awaiting owner review), build D7, then the owner's added requirement: chronicle must run **in the background once a day** producing improvements via branch→PR→merge with a fallback path. Owner picked "merge all 3", "D7 only", "auto-merge with gates", and "opencode + radar briefs as input" via questionnaires this session.

## Done

- **D4-D6 merged by the owner's own hand mid-session** (22:18–22:19Z, squash `f7b5168`/`bf99fc4`/`736dc08`, order D6→D4→D5 as suggested; PR #97 radar docs also merged). Their head branches vanished because the repo auto-deletes merged branches — initial `mergeable: unknown` confusion was this, not a problem.
- **Main realigned + pushed** (was 2/2 diverged: local had events-sync `2842866` + duplicate handoff commit `94a06e4`, patch-id-identical to origin's `f1c98e2`): events-sync committed (`337415d`), origin merged in (`707b00e`, conflicts only in derived views/cards — resolved by taking origin's state then regenerating from the union-merged log), pushed.
- **jsonl-union merge driver was NOT registered locally** (`.gitattributes` referenced it, `git config` had it missing = the exact silent-fallback failure mode its comment warns about). Registered locally from setup.sh's exact line. **Other machines/checkouts probably need the same** — setup.sh covers it, existing checkouts may not have it.
- **d4-d6 worktree pruned**; `./sync.sh` ran clean — `pr-finish` + `chronicle` skills now live in `~/.agents/skills/`.
- **Card `dotfiles-tsk-chronicle-d4-d6` is in `validation`** (parallel claude session moved it 22:19:51Z; validation→done is the owner's call).
- **D7 built — card `dotfiles-tsk-chronicle-d7` (human-attributed, owner-directed), PR #98, CI green, MERGEABLE/CLEAN, card in `review`:**
  - `.agents/opencode/command/{pr-finish,chronicle,task-brief,handoff}.md` — thin global slash commands over the synced skills.
  - `.agents/opencode/plugin/chronicle-chain.js` — server plugin: on `session.idle`, scans the final assistant reply for the D6 footer `Next: /skill <args>` (markdown-tolerant, must start with `/`, prose ignored) and stages it into the TUI input via `tui.prompt.append`. Propose-only, per-session dedup, errors swallowed (headless-safe). 10 behavioral tests pass (ran against a fake client; verified API shapes against installed opencode 1.18.32 / @opencode-ai/plugin 1.18.29 types).
  - `sync.sh` — `opencode/` subdir mirror: only `command/` + `plugin/` → `~/.config/opencode/`; opencode.json/node_modules/herdr's plugins/ never touched; skipped if opencode absent.
  - pr-finish (D4's own skill) preflighted #98 end-to-end.
- **Daily background improve built — card `dotfiles-tsk-chronicle-daily-improve` (human-attributed), PR #102, CI green, MERGEABLE/CLEAN, card in `review`:**
  - `chronicle/scripts/run.sh` — daily: mine (read-only) → newest radar briefs as research input → headless agent (`opencode` default, claude switchable) makes ≤1 small skill edit on `chronicle/improve-<date>` in a disposable worktree → evidence-cited PR → **gated auto-merge**.
  - Gates (owner-approved override of human-only merge **for this job only**): path allowlist `.agents/(skills|opencode)/**` checked from GitHub's file list; MERGEABLE+CLEAN; CI green via `--auto --squash`; 1 PR/day. Fallback: `git revert <squash-sha>` in every PR body; failed gate = propose-only.
  - `chronicle/security.md` (threat model) + `systemd/chronicle-improve/{service,timer}` (daily 08:00+jitter, hardened like the radars) — **timer not auto-installed**.
  - Dry-run verified with real data: 2 candidate groups mined, `omarchy-radar-2026-09-25.md` picked up from `~/.local/state/omarchy-radar/worktrees/` (radars write briefs there, not `<repo>/briefs/` — lookup checks both).

## Decisions

- **D7 only** — owner deferred D8 (voxtype voice engine) explicitly.
- **FR #5971 (custom sidebar panels) verified still OPEN** — v1 sticks to `tui.prompt.append`; the real panel is a follow-up when the FR lands (noted in `.agents/opencode/README.md`).
- **Card created human-attributed** — owner directed D7 in chat (same rule as the D4-D6 card); agent phase-moves signed `agent/opencode` with `--expect-last-event-id` CAS.
- **Sync mirror scoped to `command/` + `plugin/` only** — `~/.config/opencode/opencode.json` holds a live API key; it must never enter sync or the repo.
- Propose-only rule stands everywhere (plugin stages text, never submits; merges human-directed).

## Open / risks

- **FIRST RUNS DONE (2026-09-26, owner-directed test-all):** chronicle daily-improve ran end-to-end and its gated auto-merge MERGED PR #106 (`0d97f4f`, task-brief SKILL.md improvement with cited evidence; revert cmd in body). Two run.sh bugs found+fixed on #102: chronicle.py `--json`/`--out` are mutually exclusive (→ two miner calls); gate 3 now queues `--auto` on UNSTABLE too (GitHub enforces CI green). harness-radar (merged #103) ran its full nested **opencode** pipeline and committed `radar/harness-radar/2026-09-26` (1 suggestion, honest caveats, ranked.json + history.db populated, 213 seen items). omarchy-radar #104 code: clean skip path validated. router.sh: both radars `enabled+active`.
- **Quota matrix (probed 2026-09-26 ~00:00):** claude weekly-locked (Sep 29), copilot no quota, gemini CLI dead (migrate to Antigravity), codex 401, **agy 429 (~91h)**. opencode is the ONLY working agent — every run today routed to it; multi-agent dispatch is one env-var per skill once any quota returns.
- **PRs #98 (D7), #102 (daily improve), #104 (omarchy fix) all pending owner merge.** #104 is time-sensitive: **both radar timers are installed+active** — at next 08:00 omarchy-radar fires the OLD claude-hardcoded script and fails until #104 lands.
- **Radar timers are installed+active** (parallel session installed them; units also landed on main via #100/#103). chronicle-improve timer still NOT installed (awaits #102 merge + owner `systemctl --user enable --now chronicle-improve.timer`).
- **The daily-improve gate model is a deliberate exception** to the human-only-merge rule (owner-directed); pr-finish's default and every other skill remain propose-only.
- **Owner validation pending** for cards `dotfiles-tsk-chronicle-d4-d6` (in `validation`) and, later, `dotfiles-tsk-chronicle-d7`.
- **D8 not built** (voxtype + ydotoold; plan note on done card `dotfiles-tsk-chronicle-skill-layer`).
- **Shared checkout has other sessions' live work**: modified `tasks/cards/*` + `tasks/events.jsonl` (derived views / live log — regenerable, never `git checkout --/reset/stash/clean` them). The previously-untracked radar-family dirs were merged via PR #100; a radar session was still editing `lib.sh`/`harness-radar` at handoff time (see top block).
- `sync.sh --dry-run` hang is pre-existing (verified at base `2842866` last session); real sync runs fine.

## Next step

1. Owner reviews + merges PR #98 (D7) and PR #102 (daily improve): `gh pr merge <n> --squash` (propose-only — not agent's call).
2. Post-#98: `move_task.py --task-id dotfiles-tsk-chronicle-d7 --to-phase validation --actor-id <harness> --expect-last-event-id <last>` → `./sync.sh` → restart opencode → test `/task-brief` and a `Next:` footer staging live.
3. Post-#102: `./sync.sh` → `systemctl --user enable --now chronicle-improve.timer` → next morning check `~/.local/state/chronicle-improve/run.log` + the auto-PR (first real end-to-end improve).
4. Owner validates d4-d6 (+d7 after its validation) → `done`.
5. Optional next slices if the owner says go: D8 (voxtype voice engine + ydotoold; plan on card `dotfiles-tsk-chronicle-skill-layer`) and installing the radar timers (see Open/risks).

## Snapshot

_Generated by `handoff.py` at write time — verify against live state before trusting it._

- **Written:** 2026-09-25 22:26 UTC on `omarchy` by `unknown`
- **Repo:** `/home/nbugz/dotfiles` — branch `main`
- **Upstream:** `origin/main` — 1 ahead, 0 behind

Uncommitted changes:

```
 M tasks/cards/dotfiles-tsk-chronicle-d4-d6.md
?? .agents/automation/radar-common/
?? .agents/skills/harness-radar/
?? .agents/skills/omarchy-radar/
?? .agents/skills/researcher-radar/
?? briefs/
?? docs/radar-knowledge/
?? systemd/
```

`tasks/brief.py` at write time:

```
Nothing pending. What do you want to work on?
```

---

<!-- handoff:block 2026-09-25T22:15Z -->
# Handoff — Chronicle slice D4-D6 built + 3 PRs ready for review (2026-09-25) (2026-09-25)

> **To whoever picks this up (any harness, any model):** this top block is the
> current handoff; blocks below it are history. Check the Snapshot against live
> state (`git status`, `git log`, open PRs) before acting on it, then start at
> **Next step**. When you stop with work unfinished, add a new block on top
> (`/handoff`, or `handoff.py new`) rather than editing this one.

## Goal

Continue the chronicle skill-layer plan: owner said go (in chat, 2026-09-25) for building D4-D6 now — "D6 primeiro — o footer + questionário, a lição de hoje — depois D4, depois D5" — with the orphan worktree cleaned up. Done this session; next session reviews/merges the PRs.

## Done

- **Card `dotfiles-tsk-chronicle-d4-d6` created human-attributed** (owner directed in chat), `backlog → planning → in_progress`; 3 progress notes appended (last: `156ba431`).
- **Orphan worktree removed** (was clean, branch kept): `~/dotfiles.worktrees/opencode/dotfiles-tsk-chronicle-skill-layer`.
- **D6 — `9da4fc8`, PR #94**: `output-frame.instructions.md` gained the keyword-compact rule (time-on-screen; status lines; dashboard UX is the direction), the questionnaire rule (recommended first, ready-to-run options, native ask-tool; owner accepts by reading chat alone), and "Skill stacking and Chains" (stacking `/a /b`; `## Chains` in SKILL.md bodies, descriptions stay tight; `Next:` footer line only when a chain applies). `skill-template.md` gained `## Chains`; seeded into task-brief / task-worktree / handoff.
- **D4 — `2d8c6ce` + `189f485`, PR #95**: `/pr-finish` (`.agents/skills/pr-finish/`, script + SKILL.md). Propose-only default; `--auto` enables `gh pr merge --auto --squash` ONLY when card still in `review` + CI green + `MERGEABLE` + `CLEAN/HAS_HOOKS`; refuses (exit 2) otherwise; idempotent by card+PR (live-tested on merged PR #92; 8 gate tests pass). Card-phase lookup falls back to the canonical tasks root (`tasks/paths.tasks_root()`) so a worktree whose branch predates the card still resolves it.
- **D5 — `74adf08`, PR #96**: `/chronicle` (`.agents/skills/chronicle/`). Read-only miner over Claude transcripts + `tasks/events.jsonl` (via `tasks_root()`) + merged-PR churn; secret redaction + boilerplate filter + segment-aware command normalization; live mine run produced meaningful candidates. Propose-only: evidence-cited `chronicle/*` PRs, human-only merge.
- **All 3 PRs marked ready + preflighted with `/pr-finish`** (owner approved via questionnaire): #94/#95/#96 all `MERGEABLE`, `CLEAN`, CI green. NOT merged — merges are human-directed (propose-only rule).

## Decisions

- **PRs one per slice**, independent off `main` (no inter-PR conflicts): D6 #94, D4 #95, D5 #96.
- **`--auto` gate = card phase `review`**: the 2026-09-18 loop-cap/human-required-validation policy has no producer yet (`loop_cap_exceeded` needs `review.judge_failed`, see tasks/README.md), so phase is the conservative proxy — `validation`+ is never auto-merged.
- **Rework-loop detector shipped without data**: 0 `review → in_progress` transitions exist in the whole log (verified); it's correct, just no occurrence yet.
- **`sync.sh --dry-run` hang is pre-existing**: reproduced at base commit `2842866` in a throwaway worktree; not caused by this work. validate_dotfiles.sh's bash -n / link check / setup dry-run all pass.
- Owner questionnaire answers (2026-09-25): build all three D6→D4→D5; remove orphan worktree; then "Ready + /pr-finish nas 3"; then "Handoff + nova sessão".

## Open / risks

- **Merges pending owner direction** — the propose-only rule stands; nobody merges without the owner saying so in chat.
- **`origin/main` moved (+1)**: PR #93 (tsk-sweep timer) merged 21:58Z — `git pull` on `main` before branching further; the 3 PRs don't conflict with it (different files).
- **Other sessions' uncommitted work in the shared checkout** (standards yaml, AGENTS.md, CLAUDE.md, README, validate_dotfiles.sh, several tasks/ cards + events.jsonl): never `git checkout --/reset/stash/clean` those; commit only files you wrote.
- **D7-D8 not built** (next slice: D7 opencode custom commands + `tui.prompt.append`, follow opencode FR #5971; D8 voxtype voice engine + ydotoold injection). Full plan in the done card `dotfiles-tsk-chronicle-skill-layer`'s handoff note.
- Worktree `~/dotfiles.worktrees/opencode/dotfiles-tsk-chronicle-d4-d6` holds the 3 local branches (D6 checked out); keep until PRs merge, then `tasks/worktree.py prune`.

## Next step

1. Owner reviews PRs #94/#95/#96 and directs merges (squash, repo convention) — suggested order D6 → D4 → D5 so the Chains reference to `/pr-finish` lands early; run `python3 .agents/skills/pr-finish/pr-finish.py --task-id dotfiles-tsk-chronicle-d4-d6 --pr <n>` after any rebase for a fresh preflight.
2. After merges: `python3 tasks/move_task.py --task-id dotfiles-tsk-chronicle-d4-d6 --to-phase validation --actor-id <harness>` → owner validates → `done`; sync (`./sync.sh`) so the new conventions/skills reach `~/.agents/`.
3. Then the next slice, D7 (+D8 if the owner says go): start from the plan note on card `dotfiles-tsk-chronicle-skill-layer`.

## Snapshot

_Generated by `handoff.py` at write time — verify against live state before trusting it._

- **Written:** 2026-09-25 22:15 UTC on `omarchy` by `opencode` / `glm-5.3-flash`
- **Repo:** `/home/nbugz/dotfiles` — branch `main`
- **Upstream:** `origin/main` — 1 ahead, 1 behind

Uncommitted changes:

```
M  .agents/instructions/workspace-config/standards/workspace-standards.yaml
M  AGENTS.md
M  CHEATSHEET.md
M  CLAUDE.md
 M HANDOFF.md
M  README.md
M  scripts/validate_dotfiles.sh
 M tasks/board.md
 M tasks/cards/dotfiles-tsk-agent-actor-safety.md
 M tasks/cards/dotfiles-tsk-chronicle-skill-layer.md
 M tasks/cards/dotfiles-tsk-harness-provider-model-index.md
 M tasks/cards/dotfiles-tsk-skill-gauntlet-prompting.md
 M tasks/cards/dotfiles-tsk-systemd-units.md
 M tasks/events.jsonl
 M tasks/kanban.md
 M tasks/metrics.md
 M tasks/roadmap.md
 M tasks/roadmap.mmd
?? .agents/automation/radar-common/
?? .agents/skills/harness-radar/
?? .agents/skills/omarchy-radar/
?? .agents/skills/researcher-radar/
?? briefs/
?? docs/radar-knowledge/
?? systemd/
?? tasks/cards/dotfiles-tsk-chronicle-d4-d6.md
```

`tasks/brief.py` at write time:

```
Nothing pending. What do you want to work on?
```

---

<!-- handoff:block 2026-09-25T21:42Z -->
# Handoff — Chronicle skill layer - proxima fatia D4-D6 (2026-09-25)

> **To whoever picks this up (any harness, any model):** this top block is the
> current handoff; blocks below it are history. Check the Snapshot against live
> state (`git status`, `git log`, open PRs) before acting on it, then start at
> **Next step**. When you stop with work unfinished, add a new block on top
> (`/handoff`, or `handoff.py new`) rather than editing this one.

## Goal

Owner wants the "telepathic" skill layer (their words: "eu quase devia só encadear skills para comunicar mais rápido contigo... o menos possível escrito") — built in slices from a plan-orchestra run (6+2 researchers, 2 critique rounds). D1-D3 shipped and deployed today. This handoff covers the next slice, D4-D6.

## Done

- **D1-D3 shipped** (PR #92, squash-merged as `20a8bf6`, card `dotfiles-tsk-chronicle-skill-layer` → `done`): per-event hook installer + `--self-test`; `session-and-compact-hooks.json` (SessionStart + PreCompact); **PreCompact hook live** (`~/.claude/hooks/precompact_handoff.py`, wired in `~/.claude/settings.json` — deployed via `./sync.sh`, owner chose post-merge); `handoff.py snapshot --json` + `new --title-from-branch`.
- plan-orchestra evidence map + final plan D1-D8 delivered in chat (2026-09-25); key research: Copilot CLI `/chronicle improve` exists (propose-only); skill triggering is LLM-description-driven in all harnesses; no tool combines hotkeys + parameterized prompts + chaining + composition-autocomplete.
- Meta-lesson recorded as `task.note` on the done card: close every confirmable decision with a questionnaire (recommended first, options as ready-to-run commands, native ask-tool when available) — the owner accepts by reading the chat alone.
- `tasks/worktree.py`: `opencode` added to HARNESSES.

## Decisions

- **D4 auto-merge**: `pr-finish --auto` does `gh pr merge --auto` ONLY when CI green + no conflicts; never for cards past loop cap (human-required validation, 2026-09-18 policy); default remains print-commands.
- **D6**: stacking (`/skill-a /skill-b`) is the micro-language; "Chains" sections live in SKILL.md bodies (descriptions stay tight for E3 matching); footer pós-turno `→ /skill args` only when a chain applies; the questionnaire rule goes into `.agents/instructions/workspace-config/*.instructions.md` (shared via sync.sh to all agents).
- **D8**: voice engine = **voxtype** (owner choice), phrase→macro map, inject via ydotoold.
- **Positioning**: workspace-private now (A); open-source opencode plugin + write-up deferred (B/C), owner: "quero os 3 mas, agora só o A".
- **D6 (owner feedback 2026-09-25, verbatim intent):** chat output must be KEYWORD-compact — a status line ("thinking isto" style: what's happening + todo phase), expandable on click, minimal time on screen ("quero estar o mínimo de tempo a olhar para aqui"); long-running-chat CLIs "não são o futuro" — session-dashboard UX (Claude Code agent view / opencode FR #5971 / herdr pane) is the direction. Fold into the footer/questionnaire conventions.
- Propose-only rule stands: merges happen by human direction (today's merge was explicitly directed in chat).

## Open / risks

- **D4-D8 not built yet.** Full plan + owner decisions live in the done card's handoff note: `tasks/cards/dotfiles-tsk-chronicle-skill-layer.md`.
- **Agent proposal quota full** (3 open, D13) — my `task.created` for a D4-D6 card was rejected; the NEXT session should create that card **human-attributed** once the owner says go.
- Provider quota: claude at weekly limit until **Sep 29, 11:00 Europe/Lisbon**; copilot timing out; opencode online. Quota evidence + desired dispatch liveness-probe feature on card `dotfiles-tsk-dispatch-quota-check`.
- Worktree `~/dotfiles.worktrees/opencode/dotfiles-tsk-chronicle-skill-layer` (branch kept, card done) — remove when clean if unwanted: `python3 tasks/worktree.py remove`.
- Other sessions have uncommitted changes in the shared checkout (instructions files, roadmap) — never `git checkout --/reset/stash/clean` those; tasks/ views regenerate from `events.jsonl`.

## Next step

Run `python3 tasks/brief.py`, ask the owner whether to build D4-D6 now (card `dotfiles-tsk-chronicle-d4-d6`, create it human-attributed since the owner directs it), then `python3 tasks/worktree.py create --task-id <id> --harness opencode` and implement in that worktree, in order: D6 footer+questionário conventions (cheapest, closes today's lesson) → D4 `/pr-finish` (idempotent by card+PR#, owner's auto-merge rule) → D5 `/chronicle` miner (propose-only PR with cited evidence).

## Snapshot

_Generated by `handoff.py` at write time — verify against live state before trusting it._

- **Written:** 2026-09-25 21:42 UTC on `omarchy` by `opencode` / `glm-5.3-flash`
- **Repo:** `/home/nbugz/dotfiles` — branch `main`
- **Upstream:** `origin/main` — 1 ahead, 0 behind

Uncommitted changes:

```
M  .agents/instructions/workspace-config/standards/workspace-standards.yaml
M  AGENTS.md
UU CHEATSHEET.md
M  CLAUDE.md
M  README.md
M  scripts/validate_dotfiles.sh
 M tasks/board.md
 M tasks/cards/dotfiles-tsk-chronicle-skill-layer.md
 M tasks/cards/dotfiles-tsk-skill-gauntlet-prompting.md
 M tasks/events.jsonl
 M tasks/kanban.md
M  tasks/metrics.md
UU tasks/roadmap.md
UU tasks/roadmap.mmd
?? .agents/automation/radar-common/
?? .agents/skills/harness-radar/
?? .agents/skills/omarchy-radar/
?? .agents/skills/researcher-radar/
?? briefs/
?? docs/radar-knowledge/
?? systemd/
```

`tasks/brief.py` at write time:

```
⚠️  tasks/.sweep-heartbeat is 380min old (>15min) — the sweep looks dead. Facts below may be stale.

Nothing pending. What do you want to work on?
```

---

# Earlier handoff notes (free-form, pre-`/handoff`)

# HANDOFF — dotfiles (agent-OS unification + repo conventions)

**Data:** 2026-09-21, atualizado 2026-09-24. Este ficheiro é o handoff do
repo `~/dotfiles` como um todo — não é permanente, atualiza-se in place,
apaga-se/arquiva-se quando a lista "por fazer" ficar vazia. Ponto de
entrada global: `~/HANDOFF.md`.

## Trabalho ativo #4 — sessão 2026-09-24: skill `/setup-dotfiles` + incidente actor-safety

- **PR #69 (mesclada):** nova skill `.agents/skills/setup-dotfiles/`
  (`SKILL.md` + `verify_setup.sh`) — corre `./setup.sh` + `./sync.sh` num
  máquina nova e depois verifica o resultado real (não confia em
  README.md/AGENTS.md onde já se sabia estarem desatualizados).
- **PR #76 (mesclada):** corrigiu 2 falsos-positivos reais do
  `verify_setup.sh` descobertos ao correr a skill pela primeira vez
  (`_templates` sinalizado como "em falta" — não é bug do `sync.sh`, é a
  regra de exigir `SKILL.md` por skill, de propósito; referências a
  `~/.dtx-providers` desatualizadas por causa do rename da PR #70 para
  `~/.custom_providers`).
- **Incidente real durante a investigação (recuperado, nada perdido):**
  distinto do incidente de 2026-09-21 abaixo (esse já tem as duas
  causas-raiz corrigidas — `tasks-root-resolver` e `jsonl-merge-driver`,
  ambos `done`). Este foi novo: (1) uma escrita corretiva em
  `events.jsonl` foi assinada `actor-kind=human` em vez de `agent` (a
  regra certa: quem decide *esta escrita*, não de quem é a decisão que o
  payload descreve); (2) um `git checkout --` correu diretamente sobre
  `tasks/events.jsonl` no checkout principal partilhado, apagando um
  evento humano concorrente do working tree (só recuperado porque havia
  um diff guardado). Documentado e corrigido na PR #76: `tasks/README.md`
  ganhou as secções "Agent actor-kind: never impersonate the human" e
  "`tasks/events.jsonl` is live and shared — don't run raw git ops on
  it", com apontadores a partir de `AGENTS.md`/`CLAUDE.md` (os ficheiros
  que os agentes realmente leem ao arrancar sessão).
- **Por fazer:** card `dotfiles-tsk-agent-actor-safety` [HIGH PRIORITY]
  está em `validation`, não `done` — muda normas de comportamento para
  todas as sessões futuras, deixado para o dono confirmar antes de
  fechar.

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
- ~~Duas linhas soltas " HEAD" / " origin/main" perto da linha ~48/53 de
  `README.md` — resíduo de um merge mal resolvido, pré-existente, não
  relacionado com este trabalho.~~ **Feito 2026-09-22, PR #56 (aberta, por
  mesclar):** afinal eram 7 pares (3 em `README.md`, 2 em
  `.agents/skills/_templates/tool-template.md`, 2 em `skill-template.md`),
  não só os 2 originalmente notados aqui — conteúdo de ambos os lados
  verificado como completo e não duplicado antes de remover. A causa raiz
  também foi endereçada: `scripts/validate_dotfiles.sh` tinha um check para
  marcadores `<<<<<<< / ======= / >>>>>>>` mas não para este resíduo mais
  subtil (o nome da branch a solo numa linha); adicionado um segundo check
  para isso não passar despercebido outra vez.

## Próxima ação

Os 2 passos originais desta secção (rename `tasks/handoff.md` →
`tasks/HANDOFF.md`, criar o card `dotfiles-handoff-standardization`)
ficaram feitos entretanto — ver `tasks/HANDOFF.md` e o card já com 7
eventos no board. O único item genuinamente por fazer neste ficheiro,
agora, é o listado no "Trabalho ativo #4" acima: confirmação do dono para
fechar `dotfiles-tsk-agent-actor-safety` (`validation` → `done`).
