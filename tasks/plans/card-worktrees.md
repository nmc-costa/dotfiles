# Card worktrees — one git worktree per (harness, card), same for every harness (2026-09-24)

Card: `dotfiles-tsk-card-worktrees` (prerequisite of
`dotfiles-tsk-cross-harness-orchestra`). Produced via a `plan-orchestra` run:
4 parallel researchers (archify, community worktree tools, per-harness
primitives, local `tasks/` integration) → 1 tie-break (agent-deck vs gtr) →
evidence map → decisive plan → 2 rounds of adversarial critique
(round 1: REVISE, 8 flaws; round 2: ACCEPT WITH FIXES, 2 flaws) → this v2.

Owner's ask: a skill that gives each agent a worktree of the card it is
working, like Claude Code's but identical for all harnesses, visible from
the cards folder — and "use what the community does best, don't reinvent
the wheel".

## Decisions

| # | Decision | Why (evidence) |
|---|---|---|
| T1 | Engine = small stdlib `tasks/worktree.py` over plain `git worktree add / list --porcelain / remove`; stdout contract copies gtr's `new --porcelain` record shape (tab-separated fields, progress on stderr) | The job is 3 git commands and git's own porcelain *is* the community format. gtr is not installed and its `list` format is undocumented (E10); agent-deck can't create a worktree without registering a session (E9); archify is a diagram skill, not worktree tooling (E1) |
| T2 | Path `<repo-parent>/<repo>.worktrees/<harness>/<task-id>` (`~/dotfiles.worktrees/claude/<id>`); repo = main checkout of `tasks_root()`; no `--repo` in v1 | Sibling layout already in use here (E12) and worktrunk's `../repo.x` convention (E11); outside the repo so nothing to gitignore; one repo means the command and the view can't disagree |
| T3 | Branch `<harness>/<task-id>`; harness from `--harness` else `$TSK_HARNESS`; no auto-detect | Matches the harness-prefix branch policy; each harness exposes different env markers, a wrong guess means a wrong branch (E7) |
| T4 | Visibility: git is the source of truth; `worktree.py` regenerates the **gitignored, per-machine** `tasks/cards/worktrees/<id>.md` + `README.md`; every tracked card gets one fixed, path-free link line | Cards are git-tracked and rebuilt constantly — embedding machine-local paths would churn/conflict across sessions (critique r1 #2). No event type (would bump other writers' CAS token, E4); no symlinks (E6) |
| T5 | "Managed" = resolved path equals `base/<harness>/<task-id>` and the task exists; existing branch without a managed worktree → exit 1 unless `--reuse-branch` | Branch-suffix matching would adopt/prune unrelated work: `claude/dotfiles-tsk-archive-and-reorg` already exists from another workflow (critique r1 #3) |
| T6 | Cross-harness mechanism = process cwd. `dispatch.py --worktree` creates the worktree, launches with `cwd=` + `TSK_HARNESS`, prepends a fixed preamble to the prompt. Self-started sessions: one identical pointer line in `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.github/copilot-instructions.md`. `.agents/skills/task-worktree/SKILL.md` for harnesses that load skills | cwd is the only thing that works for agy (no cwd/worktree flag, E7); hooks aren't portable (Copilot's is broken, E8); mid-session `cd` into a sibling dir isn't honoured uniformly (critique r2 #2), so the pointer says *relaunch*, not `cd` |
| T7 | Cleanup explicit only: `remove`, `prune` (dry-run unless `--apply`, done cards only). Guard refuses (exit 2) dirty (incl. untracked), locked, or caller-inside; then `git worktree remove` without `--force`; branch never deleted | Removing a running agent's cwd is destructive; git's own dirty check is a second guard |

Also fixed on the way: `tasks/brief.py` still read `Path(__file__).parent /
"events.jsonl"` — the exact divergent-log bug `paths.py` fixed elsewhere —
so a worktree copy of `dispatch.py` briefed from a stale log. It now uses
`tasks_root()`.

## CLI

| Command | Stdout | Exit |
|---|---|---|
| `create --task-id X [--harness H] [--base REF] [--reuse-branch]` | `path\tbranch\tcreated\|existing` | 0; 1 bad input / branch exists; 3 git |
| `path --task-id X [--harness H]` | bare path | 1 absent |
| `list [--task-id X] [--json]` | `task_id\tharness\tbranch\tpath\tclean\|dirty\tlocked\|-` | 0 |
| `remove --task-id X [--harness H]` | `removed\tpath\tbranch-kept` | 2 guard |
| `prune [--apply]` | `would-remove\|removed\|refused\tpath\treason` | 2 if any refused |
| `view` | regenerates `tasks/cards/worktrees/` | 0 |

Tests: `python3 -m unittest discover -s tasks/tests -v` — throwaway git repo
+ `TSK_ROOT`, subprocess only; every test asserts the live
`~/dotfiles/tasks/events.jsonl` mtime is unchanged.

## Evidence map

| # | Claim | Source | Conf. |
|---|---|---|---|
| E1 | archify (tt-a1i, MIT) = diagram-generation skill, not worktrees; relevant only as a distribution model (`npx skills add … -g` into many harnesses) | github.com/tt-a1i/archify, dshmarket listing, 2026-09-24 | high |
| E2 | claim-protocol §B mandated one worktree per task; no code implemented it | claim-protocol.md §B; grep tasks/*.py | high |
| E3 | `tasks_root()` = `$TSK_ROOT` else `~/dotfiles/tasks` — worktree copies write the one real log | tasks/paths.py | high |
| E4 | Claims live outside events.jsonl because `last_event_id_for_task` doesn't filter by type | claim-protocol.md §A2, tasks/claims.py | high |
| E5 | `dispatch.py` launched without `cwd`; orchestra card planned to extend it | tasks/dispatch.py, orchestra card | high |
| E6 | Cards are generated, disposable, git-tracked; generator only writes `<id>.md` | tasks/generators/rebuild_cards.py | high |
| E7 | Native worktree: Claude `-w`/EnterWorktree, Gemini 0.60 `-w`, Codex 0.156 `--worktree`/`-C`; Copilot 1.0.88 `-C` only; agy 1.2.10 none — each with its own layout | `<cli> --help`, 2026-09-24 | high |
| E8 | Copilot CLI sessionStart hook broken; LCD = cwd + shared instructions/skill | .agents/harnesses/*.md | high |
| E9 | agent-deck 1.16.16: worktree only via `add`/`launch -w` (always a session); `worktree list --json` sees all worktrees | local `--help`, 2026-09-24 | high |
| E10 | gtr: bash, Apache-2.0, `new <branch> --porcelain` → path/branch/hook_status TSV; not installed; list fields undocumented | github.com/coderabbitai/git-worktree-runner, 2026-09-24 | high |
| E11 | Rejected: claude-squad (AGPL/TUI), agentapi (archived), crystal (deprecated), vibe-kanban (sunsetting), ccmanager (TUI), container-use (containers), uzi (blunt reset); worktrunk viable alt | survey, 2026-09-24 | med-high |
| E12 | Live: ~4 worktrees in `~/dotfiles.worktrees/`, ~13 in `.claude/worktrees/` | `git worktree list` | high |
| E13 | Branch-policy hook/CI files referenced in CLAUDE.md/AGENTS.md don't exist on disk | ls tasks/scripts, .github/workflows | high |

## Accepted risks

- **Policy enforcement is prose-only (E13).** `worktree.py` only ever
  produces policy-shaped branches, but nothing rejects a bad one. Separate card.
- **Skill discovery outside Claude is unverified.** `sync.sh` installs skills
  into `~/.agents/skills` and `~/.claude/skills` only; Copilot/Gemini/Codex/agy
  rely on the instruction-file pointer or the dispatch preamble.
- **`dispatch.py` providers are still claude/copilot/agy.** gemini/codex can
  use `worktree.py` directly but can't be auto-launched until the orchestra
  card adds them.
- **One-time card churn:** every tracked card gains the fixed link line once.
- **Legacy worktrees** (`.claude/worktrees/*`, flat `~/dotfiles.worktrees/*`)
  are never managed or pruned — left for manual cleanup.
- **Other repos** (cards whose `project` isn't dotfiles) aren't covered in v1.

## Out of scope

gtr/worktrunk/agent-deck integration (agent-deck can later point at
`worktree.py path`); `--repo`/project→repo mapping; branch-policy hook/CI;
branch deletion/merge/`--force`; automatic cleanup in `move_task`/`sweep`;
`claim.py` changes; `dispatch --model`; plugin/extension packaging;
session-start hooks; migrating legacy worktrees.
