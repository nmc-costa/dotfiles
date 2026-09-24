# Continuous repo organization & simplification

Design for keeping the governed repos (`~/dotfiles`, `~/Projects/architect`,
`~/Projects/notes`; `~/Work/notes` only on request; any other `~/Work/*` only
with explicit per-run permission) organized and simple, as a ladder of rungs
that are each useful on their own: **1 prevention → 2 manual skill →
3 recurring card → 4 autonomous worktree tournament → draft PR**. Rung 4
is the first concrete implementation of
`.agents/instructions/base-personas/master-continuous-optimization.md`'s final
phase. Written before implementation, same convention as the other files in
`tasks/plans/`.

Produced 2026-09-24 by a `/plan-orchestra` run: 5 parallel researchers + 1
tie-breaker → evidence map (appendix) → Opus planner (3 architectures
compared, one chosen) → 2 rounds of independent Opus critique (v1: 7 material
findings, v2: 3 material findings). The round-2 findings are applied below as
**orchestrator amendments that were not re-critiqued** (skill's 2-round cap).

## 1. Three candidate architectures

**A. Local-first.** One script, `scripts/tree_tidy.py`, with subcommands `scope | map | metrics | gate | tournament`, does everything deterministic. Rung 2 = a skill; rung 3 = a recurring card. Rung 4 runs cheap candidates via `claude -p --model` (flag confirmed in `claude --help`), each inside a `bwrap` sandbox that sees only its own worktree; an opus judge picks the winner; `gh pr create --draft` opens it. Scheduled by a systemd user timer with `Persistent=true` (same pattern as the existing `dotfiles-sync.timer`).

**B. Cloud-first.** One cloud routine checks out all three repos (T1b); candidates and judge run in the same session. Per-step model choice undocumented (T1c, L).

**C. CI-first.** Per-repo claude-code-action matrix workflows (E17); a central evaluator uses a PAT to check out the other repos (T1a).

| Criterion | A Local | B Cloud | C Actions |
|---|---|---|---|
| Setup cost | Low | Low, untestable offline | High (PAT, secrets, 3 workflows) |
| Cross-repo consistency | Full | Yes (T1b, M) | PAT only (T1a) |
| Safety / reward-hacking resistance | High: gate from clean `main`; OS sandbox | Low: gate shares candidates' session | Medium: candidate can edit the workflow |
| Cost per run | Subscription; exact per-agent tiers | Subscription; tiering unverified | Subscription (T1d) + runner minutes |
| Works laptop-off | No (`Persistent=true` catches up) | Yes (E16) | Yes (E17) |
| Value per rung | Rungs 1-3 need no LLM runtime | Rung 4 only | Rung 4 only |

## 2. Chosen: A (local-first)

Cross-repo consistency needs one view of all repos: Actions only gets it with a PAT (T1a), and cloud routines can't reliably run cheap candidates alongside an expensive judge (T1c, L). Local is the only runtime where the Work/ boundary is enforced by the OS rather than by a prompt, and where the gate runs from code the candidates can't touch (E12). Rungs 1-3 ship as plain scripts — "script before rule", `pocFirst` (yaml:103). A laptop-off gap only delays a weekly job.

Named risk: headless `claude -p` under systemd is unproven — rung 4a runs manually first.

## 3. Decisions T1-T5

- **T1:** rung 3 = a card spawned by `recur.py`; rung 4a = `tree_tidy.py tournament`, run manually; rung 4b = weekly local timer, via the manifest agile-workspace-schedule builds, with the entry at `.agents/automation/jobs/tree-tidy-tournament.yaml` (an existing allowed dir). Cloud/CI rejected (T1a, T1c, E14).
- **T2:** Generated on demand, never committed. `tree_tidy.py map <repo>` prints Markdown to stdout for agents (depth 3, with each dir's declared purpose; E5 L, E6, E7). `--json` writes `~/.cache/tree-tidy/<repo>/<sha>.json` for metrics and the judge; `--ref` rebuilds any past commit. Delete `docs/directory_tree.md` (hand-written, already stale); repoint its refs in CLAUDE.md:77, README.md:113, GEMINI.md:12, AGENTS.md:147 to the `map` command.
- **T3:** SSOT = `workspace-standards.yaml` + each repo's `docs/standards.yml` (I1). `validate_workspace_standards.py` gains `--check-root <repo>` (walks tracked + untracked-not-ignored; fixes I2) and `--check-path <file>`. `validate_dotfiles.sh` §1 hardcoded arrays deleted; it calls `--check-root` (I3). No ls-lint (E2). Reconcile the YAML to git-tracked reality: add `.agy .codex .copilot .gemini bin HANDOFF.md .gitattributes`; rename `.chezmoisource` → `.chezmoi-source`. Add optional schema key `privatePaths`; notes gets `privatePaths: [calls, health]`.
- **T4:** archive-and-reorg: leave alone (`tasks/**` is protected). card-priority → recurring-cards: depend-on, for rung 3 only. agile-workspace-schedule: depend-on, for 4b only. systemd-units: leave alone. cross-harness-orchestra: leave alone (may import tree_tidy's worktree functions later). agent-autonomy-charter: link only (draft-PR-only). master-continuous-optimization: rung 4 is its final phase — one line in the file links to it.
- **T5:** `tree_tidy.py scope` is the only repo resolver. Default = the 3 in-scope repos; `agentic_instructions` hard-excluded. `~/Work` refused unless `--permit <abs>` is given on that run's command line; `TREE_TIDY_NONINTERACTIVE=1` (scheduled runs) makes `--permit` a hard error. Candidate sandbox: `bwrap --ro-bind / /` with `--tmpfs` over `~/Work`, `~/Projects`, `~/dotfiles` and the target's `privatePaths` inside the worktree; the only rw mounts are the worktree and a per-run `CLAUDE_CONFIG_DIR` seeded with a credentials copy. Candidates get `--disallowedTools Bash,WebFetch,WebSearch` (Read/Edit/Write/Glob/Grep only). Since they can't run commands, candidates return moves as JSON, which the script applies with `git mv`.

## 4. Build plan

**Rung 1 — prevention.** Add 3 lines to AGENTS.md's existing section (lines 7-11, I7) — no new instruction file: "before creating a file, run `tree_tidy.py map .`"; "prefer editing an existing file; place new files by each dir's declared purpose"; "never add root entries; new top-level areas only by PR". Mechanism: `.agents/hooks/root-guard.sh`, a `PreToolUse` hook on Write, installed via `session-start-hooks.json` + a `PreToolUse` section in `install_session_start_hooks.py`. It no-ops unless the git toplevel is in scope and has a standards file; otherwise it calls `--check-path` and exits 2 on a new, non-allowlisted root entry. Done when: a Write to `~/dotfiles/foo.md` is blocked while `docs/foo.md` and `/tmp/foo.md` are allowed, and `--check-root` flags notes' `.gitignore` and architect's `.pytest_cache` (I6).

**Rung 2 — manual skill.** `.agents/skills/tree-tidy/SKILL.md` (≤150 lines): (1) script: `scope` → `map --json` → `metrics --out before`; (2) LLM: research only if `review.nextDue` has passed, limited to `sourcesToRecheck` + repo-type conventions; plan ≤10 changes; (3) apply: `git mv` + the script's link rewriting; `/simplifyhit` on touched instruction/skill/persona files (I8); `/simplify` on the code diff (E9); (4) script: `gate` → `metrics --out after`; (5) draft PR on `claude/tree-tidy-<repo>-<runid>`, where runid = `YYYYMMDD-<6hex>`. Model: human's session (Sonnet). Done when a notes run passes the gate and opens a draft PR.

**Rung 3 — recurring.** `tasks/recurring.yaml` template `dotfiles-tsk-tree-tidy-run`, every 14 days, body "run /tree-tidy on the next repo in rotation". Done when a `recur.py` dry-run spawns it.

**Rung 4a — manual tournament.** `tree_tidy.py tournament --repo <rotation>`, rotating dotfiles → architect → notes. Idempotent:
- Skip if any open PR on the repo has a head branch matching `claude/*tidy*`.
- Skip if HEAD equals the last null-result sha stored in `~/.local/state/tree-tidy/<repo>.json`.
- Worktrees live in `~/.cache/tree-tidy/<runid>/cand<n>` on local branches `claude/tree-tidy-cand<n>-<runid>`, removed in `finally` + `git worktree prune`.

Seeds per repo type (3 candidates: 2× haiku, 1× sonnet):
- dotfiles: placement (haiku); instruction reduction under simplifyhit rules (haiku); cross-repo alignment (sonnet, given the other repos' maps as text).
- architect: placement (haiku); code simplification (haiku); alignment (sonnet).
- notes: placement (haiku); README/index consolidation (haiku); alignment (sonnet).

Judge: opus, reading real maps of all three repos. Winner → draft PR `claude/tree-tidy-tourney-<repo>-<runid>`. Every outcome is appended to `events.jsonl` as a handoff note. Done when 3 manual runs (one per repo) each end in a draft PR or a recorded null.

**Rung 4b — schedule.** The manifest entry from T1, weekly, `Persistent=true`.

## 5. Equivalence gate + rubric

The gate runs from a clean export of dotfiles `main` (`git archive main scripts .agents/skills/simplifyhit/scripts`) into `~/.cache/tree-tidy/<runid>/gatekit` — never from a candidate's worktree. Checks, in order; any failure disqualifies:
1. Protected paths untouched: `tests/**`, `.github/workflows/**`, `tasks/**`, all standards files, `privatePaths`; in dotfiles also `scripts/**`, `.agents/skills/*/scripts/**`, `.agents/hooks/**`.
2. Diff cap: ≤400 changed lines, ≤30 renames.
3. Per repo:
   - dotfiles: `validate_dotfiles.sh`; `validate_workspace_standards.py` on the YAML and with `--check-root`; `bash -n` on `setup.sh`/`sync.sh`; `tasks/rebuild_*.py` output byte-identical before vs after.
   - architect: `pytest tests/` passes with the same or higher collected count; `compileall`.
   - notes: files other than README/index may only be moved; content hashes may differ only in link targets.
4. Rule coverage (replaces keyword counting), on touched instruction files:
   - Deterministic: 100% of the before-version's backticked identifiers and file paths still appear somewhere in the after-set.
   - LLM (opus), pass/fail: every normative rule in the before-version is mapped to a location in the after-version. An unmapped rule disqualifies; merged rules pass.
5. All repos: no new broken relative links; nothing deleted without a rename target.

**Judging.** Contestants are the gated candidates plus the **baseline** (the unchanged repo). Every pair is judged pairwise in both orders (A/B and B/A); a split verdict counts as a tie (E11). Diffs are anonymized and the prompt is length-neutral ("size is not merit"). The judge model differs from the candidate models (opus judges haiku/sonnet; self-preference, E11).

**Score = 60% deterministic + 40% judge.** The baseline's deterministic delta is 0.
- Deterministic (normalized deltas): root/placement violations 15; duplication % 15; instruction tokens 15; cross-repo consistency 15 (Jaccard of top-level dir roles + README sections).
- Judge (pairwise win rate): placement matches each dir's purpose 15; navigability 10; sibling consistency 10; meaning preserved 5.
- A winner must beat the baseline's score by ≥5 points, else the result is null.
- Weights are authored, not borrowed (E13, L).

## 6. Metrics & gates

`tree_tidy.py metrics` uses only the Python standard library — no jscpd/npx (E8's method reimplemented). Computed:
- root entries/violations; entries per dir (flag >25); max depth;
- duplication % via normalized 6-line shingle hashing over code + Markdown;
- approximate instruction tokens (chars/4) for AGENTS.md, CLAUDE.md, `.agents/instructions/**`, SKILL.md (E6, E7);
- SKILL.md files >500 lines; broken links; `audit_instruction_health.py` score; lines of code.

Blocking gates: a new root violation; duplication up; broken links up; any SKILL.md >500 lines; instruction health <80%; net instruction tokens up; fewer tests.

## 7. Kanban changes

5 new cards (4 in v2; the cadence card is split per R2-C), each created with: `tasks/append_event.py --type task.created --actor-kind human --actor-id nmc-costa --task-id <id> --payload '{"project":"dotfiles","title":"…","blocked_by":"…"}'`. Priorities are applied once card-priority lands.

Not yet created: the planning session's `--actor-kind agent` write was rejected by the agent proposal quota (D13: 3 open, expiry 14d) on 2026-09-24. The human creates these cards directly (`--actor-kind human`, since the human is the one deciding).

| task_id | title | blocked_by | prio |
|---|---|---|---|
| dotfiles-tsk-tree-tidy-core | Standards root-check + allowlist reconcile, tree_tidy.py scope/map/metrics, root-guard hook, AGENTS.md lines, delete directory_tree.md | "" | P1 |
| dotfiles-tsk-tree-tidy-skill | Rung 2: /tree-tidy skill + tree_tidy.py gate | dotfiles-tsk-tree-tidy-core | P1 |
| dotfiles-tsk-tree-tidy-tournament | Rung 4a: sandboxed haiku/sonnet tournament, opus judge, draft PR | dotfiles-tsk-tree-tidy-skill | P1 |
| dotfiles-tsk-tree-tidy-recurring | Rung 3: recurring.yaml template, every 14 days (amended R2-C) | dotfiles-tsk-tree-tidy-skill, dotfiles-tsk-recurring-cards | P2 |
| dotfiles-tsk-tree-tidy-schedule | Rung 4b: weekly jobs manifest entry (amended R2-C) | dotfiles-tsk-tree-tidy-tournament, dotfiles-tsk-agile-workspace-schedule | P2 |

Handoff notes on existing cards:
- agile-workspace-schedule: "manifest at `.agents/automation/jobs/`; first consumer tree-tidy-tournament".
- archive-and-reorg: "tasks/ excluded from tree-tidy".
- agent-autonomy-charter: "tree-tidy = draft PRs only".

Plus one line in `master-continuous-optimization.md` pointing to the tournament.

## 8. Risks

1. **Fails first: sandbox auth.** A credentials copy in a per-run `CLAUDE_CONFIG_DIR` may not authenticate under `bwrap`. The first manual 4a run exits non-zero before any candidate runs; fix by read-only binding `~/.claude/.credentials.json`.
2. **Wiki-style links in notes** escape the link rewriter; the broken-link gate catches it on the first rung-2 run.
3. **All haiku candidates fail the gate.** After 3 consecutive nulls, the events log surfaces it in `/task-brief`, and one seed moves from haiku to sonnet.
4. **Judge bias.** The split-verdict rate across both orders is logged; above 30%, the judge weight drops to 20%.
5. **Headless `claude -p` under systemd** — proven manually in 4a before 4b exists.

## Changes from v1

1. Work/ is enforced by the OS: bwrap sandbox + Bash disallowed; moves come back as JSON and the script applies them.
2. ~16 new files → 3 (`tree_tidy.py`, `root-guard.sh`, SKILL.md); the root walk moves into `validate_workspace_standards.py`; jscpd dropped; 7 cards → 4.
3. Rung 1 = 3 AGENTS.md lines + the hook; no new instruction file.
4. Tree maps generated on demand, never committed; `docs/directory_tree.md` deleted.
5. Idempotent runs: run-id suffix, `finally` cleanup, skip on null-result sha, skip on any open `*tidy*` PR.
6. Keyword counting → rule-coverage check; seeds set per repo type.
7. Jobs manifest under `.agents/automation/jobs/`; rung 3 keeps its dependency on the recurring-cards chain but is off rung 4's critical path.
8. Minor fixes: gate from a clean export, full protected list, hook no-ops outside scope, worktrees in ~/.cache, baseline as a contestant, `privatePaths`, `claude --help` cited for the flags.

## Round-2 amendments (applied after the 2-round critique cap, not re-critiqued)

- **R2-A: candidates wouldn't start inside the sandbox.** `~/.local/bin/claude` is a bash wrapper that runs
  `mise use -g` (a write) before exec, and under `bwrap --ro-bind / /` that write fails. Fix: `tree_tidy.py` resolves
  `mise which claude` *outside* the sandbox and execs that binary directly. This replaces risk #1 as "what fails first".
- **R2-B: copying credentials can rotate the user's refresh token.** Fix: run `claude setup-token` once to mint a
  long-lived token, pass it as `CLAUDE_CODE_OAUTH_TOKEN` in the sandbox env, copy no credential files, and wipe the
  per-run `CLAUDE_CONFIG_DIR` in the existing `finally`.
- **R2-C: ladder order was inverted in the card graph.** The old cadence card bundled rung 3 with 4b and was blocked
  by the tournament. It is now split in two (see §7), so rung 3 ships right after the skill.

## Accepted risks (minor, carried into implementation)

- **The gate's rule-coverage step uses opus, the same model as the judge.** Run it after the deterministic checks
  and log its verdict separately.
- **Notes: gate vs `/simplify`.** The notes gate allows content edits only to README/index, yet rung 2 runs
  `/simplify` on code diffs. Skip `/simplify` on notes (it has `scripts/`, which stays out of scope for now).
- **Rung 2 can collide with an open PR.** Rung 2 has no "open `claude/*tidy*` PR" skip; add the same check the
  tournament uses.
- **Incomplete list of `directory_tree.md` references.** The repoint list also needs CLAUDE.md:126,
  docs/AUDIT_REPORT.md and docs/SUBAGENTS_VERIFICATION.md. AGENTS.md:147 needs rewording, not repointing.
- **Two weights are inferences.** N=3 candidates and the 60/40 rubric weights are authored, not sourced (E13).
  Review them after 6 runs, using the human's merge/close decisions as ground truth.
- **Laptop-off gap.** Accepted: the job is weekly, and `Persistent=true` catches up on the next boot.

## Appendix: evidence map

Confidence: H = verified locally or primary doc; M = secondary source; L = inference.

### Internal state (dotfiles + governed repos)
| # | Claim | Source | Conf |
|---|---|---|---|
| I1 | `workspace-standards.yaml` defines `repoRoot.allowedFiles/allowedDirs` per repo (dotfiles, architect, notes, worknotes via own standards.yml) | .agents/instructions/workspace-config/standards/workspace-standards.yaml:27-43 | H |
| I2 | `validate_workspace_standards.py` validates YAML shape only; never walks the filesystem | scripts/validate_workspace_standards.py (no iterdir/listdir/glob/walk; verified by main agent) | H |
| I3 | Only `validate_dotfiles.sh` §1 enforces root, with its OWN hardcoded allowlist that has drifted from the YAML (.agy .codex .copilot .gemini bin HANDOFF.md .gitattributes; `.chezmoi-source` vs YAML `.chezmoisource`) | scripts/validate_dotfiles.sh:60-65 (verified) | H |
| I4 | No validator runs in CI; no pre-commit config; only workflow is vscode-docs-monitor.yml | .github/workflows/ (verified) | H |
| I5 | `tasks/scripts/pre-push.sample` and `setup_git_hooks.sh` referenced by global CLAUDE.md do NOT exist in this checkout | `ls tasks/scripts` = append_event.py, dispatch.py (verified) | H |
| I6 | Current root drift: notes has `.gitignore` not allowlisted; architect `.pytest_cache` unflagged; Work/notes clean but its standards.yml header mislabeled "for notes" | inventory researcher, file reads | M |
| I7 | AGENTS.md:7-11 already says: standards yaml is mandatory (clean root), run validator after edits, propose via PR | AGENTS.md:7-11 | H |
| I8 | No tree-mapping skill exists; `simplifyhit` exists with structural gate `audit_instruction_health.py` (≥80%) but no behavior/coverage regression gate | .agents/skills/simplifyhit/SKILL.md:260-279 | H |
| I9 | Recurring cards already designed: `tasks/recurring.yaml` + `tasks/recur.py`, new instance per cadence; blocked by card-priority (Part A, no blockers) | tasks/plans/priority-and-recurring-cards.md:76-133 | H |
| I10 | Overlapping open cards: archive-and-reorg (tasks/ tree, planning, blocked by claim-protocol), card-priority, recurring-cards, systemd-units, agile-workspace-schedule, cross-harness-orchestra, agent-autonomy-charter. Repo-hygiene + standards-schema cards all DONE | tasks/cards/*.md | H |
| I11 | master-continuous-optimization is design-only, last phase; §13.5 says literal per-task benchmark is cost-prohibitive, favors cheap-first cascade | base-personas/master-continuous-optimization.md:20-24; notes §13.5 | H |
| I12 | Card creation CLI: `tasks/append_event.py --type task.created --actor-kind ... --task-id ... --payload '{...}'` | tasks/append_event.py:4-6 | H |
| I13 | All 4 in-scope repos have GitHub remotes | `git remote -v`, runtime researcher | H |

### External
| # | Claim | Source | Conf |
|---|---|---|---|
| E1 | No published research/standard on agents cluttering repo root; gap is real | RESEARCH_NOTES.md + dev.to search, 2026-09-24 | M |
| E2 | ls-lint: YAML-configured dir/filename linter, JSON output, used by Nuxt/Renovate | ls-lint.org, 2026-09-24 | H |
| E3 | pre-commit `fail` hook = standard client-side path-regex block | adamj.eu 2024-01-24 | H |
| E4 | GitHub community-health resolution .github/ → root → docs/ | docs.github.com | H |
| E5 | Markdown cheaper/better than JSON for LLM narrative context; no benchmark for tree-maps specifically | vendor blogs 2025-26 | L |
| E6 | Anthropic: smallest high-signal token set; SKILL.md <500 lines, progressive disclosure | anthropic.com/engineering/effective-context-engineering-for-ai-agents; platform.claude.com skills best-practices | H |
| E7 | Context rot: all 18 frontier models degrade with input length before limit | trychroma.com/research/context-rot | H |
| E8 | jscpd detects duplicates in code AND markdown, CI thresholds, JSON/SARIF | jscpd.dev | H |
| E9 | `/simplify` built-in reviews only current diff, not whole repo | secondary summaries (primary doc not loaded) | M |
| E10 | Parallel worktrees + judge is a community pattern, not an official feature; gate = tests/lint then judge + human | claudedirectory.org, spillwavesolutions/parallel-worktrees | M |
| E11 | LLM-judge biases: position (fix by swapping order, not prompting), verbosity (length-neutral prompt ~-50%), self-preference | arxiv 2604.23178, 2603.08091; futureagi.com | M |
| E12 | Reward hacking in coding agents (deleting tests, disabling hooks) is documented; mitigate with deterministic judge-independent guards | arxiv 2605.21384, 2609.02246 | M |
| E13 | No published rubric for org/standardization/consistency; must be authored | tournament researcher | L |
| E14 | Local systemd timers: none exist yet for tasks/; only laptop-on | ~/.config/systemd/user; cards | H |
| E15 | `/loop`: session-scoped, dies with session | secondary | M |
| E16 | Cloud routines: laptop-off, subscription rate limits, GitHub needed for push/PR | code.claude.com/docs/en/claude-code-on-the-web | H |
| E17 | GH Actions + claude-code-action: github.com only, per-job `--model`, OAuth token or API key, native PR + logs | code.claude.com/docs/en/github-actions | H |

### Discarded
- "Ralph plugin popularized 4-8 worktrees" — unverified primary source.
- Recommended N=3-4 — kept only as [inference], no benchmark.

### Unresolved tensions for the planner
- T1 Runtime: GH Actions (per-repo) vs cloud routine vs local — evaluator needs cross-repo view. (tie-breaker result appended below)
- T2 Tree-map format: human asked ".md and/or json"; research favors MD-only for agent consumption; JSON may still serve evaluator diffing/cross-repo comparison.
- T3 Single source of truth for root allowlist: YAML vs validate_dotfiles.sh hardcoded arrays vs proposed ls-lint config.
- T4 Scope boundary with dotfiles-tsk-archive-and-reorg (tasks/ subtree) and recurring-cards dependency chain.
- T5 Work/ repos: Work/notes allowed on request; other Work/ repos require explicit per-run human permission.

### Tie-breaker T1 (runtime, multi-repo)
| # | Claim | Source | Conf |
|---|---|---|---|
| T1a | claude-code-action's default GitHub App token is scoped to the current repo, cannot push elsewhere; multi-repo needs PAT + actions/checkout per repo, or one workflow per repo | anthropics/claude-code-action docs/security.md, 2026-09-24 | H |
| T1b | One cloud routine can orchestrate several GitHub repos in one run, billed against the subscription usage pool | claude.ai/code routines docs via haiku tie-breaker | M |
| T1c | Per-step model tier inside a cloud routine: NOT documented (unverified) | tie-breaker "likely" = inference | L |
| T1d | GH Actions CAN bill against subscription via CLAUDE_CODE_OAUTH_TOKEN (conflicts with tie-breaker claim of API-only; trust E17 primary doc) | code.claude.com/docs/en/github-actions | H |
Discarded: "routines have full Anthropic API key access" (unsupported).
Main-agent note: prior spike `dotfiles-tsk-spike-workflow-model` (DONE) confirmed a local Workflow script with real per-phase model override runs — relevant to per-agent tiering in a LOCAL run.
| T1e | Workflow tool is invocable only from a TOP-LEVEL session, not from a delegated subagent; per-phase model override (haiku/opus) verified in a real run | tasks/cards/dotfiles-tsk-spike-workflow-model.md (handoff, run wf_1c1da6c5-023) | H |
