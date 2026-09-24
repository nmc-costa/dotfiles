# Plan — `/harness-orchestra` (card `dotfiles-tsk-cross-harness-orchestra`)

> Planned 2026-09-24 by Claude Code (Opus 5.5) in plan mode; approved by the owner the same day. Implementation not started.

## Context

The owner wants a skill, invocable from **any** harness, that fans a task out across several
harness+provider+model combos ("1 Claude Code Opus + 1 Copilot CLI GPT-5"). Each agent gets its own
git worktree on a harness-prefixed branch (`claude/`, `copilot/`, `agy/`). Harnesses don't talk to each
other, so closure goes through handoff markdown files plus `events.jsonl`, never IPC.

Owner decisions (2026-09-24):
- permissions: `auto` by default, `yolo` optional;
- agy branch prefix: `agy/`;
- output: headless by default, plus a visible mode. See §Visibility for how this is satisfied.

**Principle: adopt, don't build.** `tasks/README.md` already decided (2026-09-18) to *adopt*
`agent-deck` as the L2 execution engine for Copilot and other harnesses.
`tasks/evaluations/agent-deck/README.md` (2026-09-21) confirmed it installs and runs Claude + Copilot side by side here.
This skill is the first real use of that decision. We build only the thin layer that is specific to `tasks/`.

## Prior-art research (2026-09-24)

| Tool | Harnesses | Worktree + branch | Model per agent | Prompt delivery | State here | Verdict |
|---|---|---|---|---|---|---|
| **agent-deck** v1.16.16 (MIT) | Claude (full), Copilot (launch/org), any command via `-c` | `launch -w <branch> -b --location <path>`, free-form branch names (so `claude/x` works) | `-model` for claude/codex/gemini/opencode; for copilot/agy through the command itself, `-c "copilot --model gpt-5.5 …"` | `-message-file <f>`, sent once the agent is ready (tmux); `-assert-done` adds a completion sentinel | **Installed**, evaluated, already adopted for L2 | **Adopt** |
| workmux (MIT, 2.7k★) | Claude, Copilot, **agy** (with status hooks), Gemini, Codex… | `add base -a A -a B`: one worktree per agent in a single command; `--branch-template` accepts `{{agent}}/…` | named agents in config (`cc-opus: "claude --model opus"`) | automatic per agent; `--headless` **only creates the worktree, doesn't launch the agent** | Not installed | Fallback if agent-deck fails on agy in the smoke test |
| Composio agent-orchestrator (Apache, 12k★) | 27 agents | yes, plus PR | yes | desktop GUI | — | Rejected: desktop GUI, no scriptable CLI, doesn't fit "invocable from any harness" |
| vibe-kanban, ccmanager, claude-squad | several | yes | partial | own UI | — | Rejected: each brings its own board or TUI and would compete with `tasks/kanban.md` |

Sources:
- local `agent-deck launch --help`
- https://github.com/raine/workmux
- https://github.com/ComposioHQ/agent-orchestrator
- https://github.com/kbwo/ccmanager
- https://github.com/BloopAI/vibe-kanban
- https://nimbalyst.com/blog/best-git-worktree-tools-ai-coding-2026/

## Verified CLI facts (live, `omarchy`, 2026-09-24)

- **claude 2.1.280**
  - Model: `--model <alias|full>`.
  - Permissions: `--permission-mode auto` or `--dangerously-skip-permissions`.
  - `-w` creates a branch named `worktree-<name>`, which **breaks the prefix policy**. Don't use it; agent-deck `-w` creates the worktree instead.
- **copilot 1.0.88**
  - Model: `--model <id>`. Valid list comes from `copilot help config`; there's **no plain `gpt-5`**. Real options: `gpt-5.5`, `gpt-5.6-sol/terra/luna`, `gpt-5-mini`, `gpt-6-astra`, …
  - Permissions: auto = `--allow-all-tools --no-ask-user`; yolo = `--yolo`.
  - Also useful: `--add-dir`, `-C`.
- **agy 1.2.10**
  - Model: `--model <id>`. List comes from `agy models` (`gemini-3.8-flash-high`, `gemini-3.1-pro-high`, `claude-opus-4-6-thinking`, …).
  - Permissions: auto = `--mode accept-edits`; yolo = `--dangerously-skip-permissions`.
  - Also useful: `--add-dir`.
- **agent-deck**
  - `launch [path] -c <cmd> -w <branch> -b --location <path> -t <title> -message-file <f> [-auto-mode|-skip-permissions] -json`
  - `session output <id>`, `status -v`, `worktree list/cleanup`.

## Design: what we build (~200 LOC Python + 1 SKILL.md)

### 1. `tasks/orchestra.py`: the deterministic core (D14)

`launch --task-id X --agent 'claude:opus:<subtask>' --agent 'copilot:gpt-5.5:<subtask>' [--permissions auto|yolo] [--launch]`

1. **Validate models** against the live lists:
   - copilot: parse `copilot help config`;
   - agy: `agy models`;
   - claude: the alias set or a `claude-…` prefix.
   An unknown model fails **before** anything is created, and the error lists the valid ones.
2. **Naming:**
   - `run_id = <task-id>-<UTC yyyymmddHHMM>`
   - `label = <harness>-<model-slug>`
   - `branch = <prefix>/<task-short>-<model-slug>` with `PREFIX = {claude: "claude/", copilot: "copilot/", agy: "agy/"}`
   - worktree = `~/dotfiles.worktrees/<harness>+<task-short>-<model-slug>`, the existing convention.
3. **Brief per agent:** the output of `brief.py --prompt-only` (§2) is written to `tasks_root()/handoffs/<run_id>/<label>.brief.md`.
4. **Command per harness**, from a table built from the verified facts. Every command includes `--add-dir ~/dotfiles/tasks`
   so the agent can write events and handoffs to the canonical root (`paths.tasks_root()`).
   Examples:
   - `claude --model opus --permission-mode auto --add-dir …`
   - `copilot --model gpt-5.5 --allow-all-tools --no-ask-user --add-dir …`
   - `agy --model gemini-3.1-pro-high --mode accept-edits --add-dir …`
5. **Per agent:**
   1. `agent-deck launch <repo> -c "<cmd>" -w <branch> -b --location <wt> -t <label> -g orchestra/<run_id> -message-file <brief> -json`, capturing the session id;
   2. `claims.acquire(role=implementer, actor_kind=agent, actor_id=<harness>)`;
   3. append `orchestra.agent_launched`: {run_id, label, harness, model, branch, worktree, deck_session, handoff_path, permissions}, signed `agent`/`<lead harness>`.
6. **Dry-run by default:** prints the commands and briefs, creates nothing.

`status --run-id R`
- Folds the `orchestra.*` events.
- For each agent, adds `agent-deck session show/status --json` (alive or waiting),
  `git rev-list --count main..<branch>`, whether the handoff exists, and the PR (`gh pr list --head <branch> --json url`).
- Read-only.

`collect --run-id R`
- Concatenates the handoffs of the finished or blocked agents and releases their claims.
- Prints a summary for the lead, who runs `move_task.py --to-phase review --handoff "<summary + PRs>"`.
- Never removes worktrees and never merges. The human does `agent-deck worktree finish --no-merge` or `cleanup` after merging.

**Why events on the parent card instead of child cards:** it avoids the agent-proposal quota of 3 in
`append_event.py`, and it avoids phase-CAS contention between agents. Only the lead moves the card.

### 2. `tasks/brief.py`: orchestra contract

`prompt_for_task` gains `--run-id --agent-label --harness --subtask --handoff-path --owned-files`.
The prompt then gets a fixed contract appended:
- **Scope:** only the subtask and the listed files, in this worktree.
- **Finish line** (the same in `auto` and `yolo`; the mode only decides whether permission prompts appear):
  1. validate;
  2. commit;
  3. `git push -u origin <branch>`;
  4. `gh pr create --draft --base main`;
  5. write the handoff md at `<handoff-path>` (template: Status done|blocked / Done / Left / Branch / PR / Commits / Next step / Blockers);
  6. `python3 ~/dotfiles/tasks/append_event.py --type orchestra.agent_finished --actor-kind agent --actor-id <harness> --task-id <parent> --payload {run_id,label,branch,pr_url,handoff_path,status}`.
- **Never:** merge, push to `main`, force-push, move the parent card, or sign as `human`.
- **Blocked** (for example, a push refused in `auto`): write the handoff with `status: blocked` and the reason, then stop.

### 3. The skill: `.agents/skills/harness-orchestra/SKILL.md`
- Thin shell over `orchestra.py`.
- Symlinked from `.claude/skills/harness-orchestra` and `.github/skills/harness-orchestra`. agy discovers `.agents/` on its own.
- Phases:
  1. Parse "1 claude opus + 1 copilot gpt 5" into specs. **Confirm with the human** any resolved model name (e.g. "gpt 5" → `gpt-5.5`?).
  2. Split into disjoint subtasks with explicit file ownership. If the task doesn't split, say so; no gratuitous fan-out (same rule as plan-orchestra).
  3. Dry-run, and the human confirms.
  4. `--launch`. The lead moves `planning → in_progress`.
  5. Follow up with `orchestra.py status`, `agent-deck` (TUI), or `tmux attach`.
  6. `collect`, a parent handoff, then a move to `review`.
- Rules:
  - `yolo` only on the human's explicit request;
  - never merge;
  - more than 4 agents needs confirmation (Pro plan cost).

### 4. Visibility (the owner's "headless + visible" decision)
agent-deck always runs each agent in its own **detached** tmux session. `launch` returns right away,
so it's headless from the caller's point of view. And any agent can be watched or steered at any time with
`agent-deck` (fleet TUI, `agent-deck status -v`) or `tmux attach`.
That removes the need for a `--visible` flag and for the `-p`/`-i` split.
Opening panes inside herdr stays out of scope: it would be a later L3 integration, and the agent-deck evaluation already
flags the policy of "which multiplexer is the source of truth" as an open question.

### 5. Docs (same commit, mandatory CHEATSHEET rule)
- `tasks/CHEATSHEET.md`: a new `orchestra.py` row and an "Orchestrate across harnesses" section.
- `tasks/harness-provider-model-index.md`: real Copilot/agy model lists (2026-09-24). Also note that agent-deck is now used in practice.
- `tasks/README.md` "Status": L2 agent-deck is **in use**.
- `AGENTS.md` / `CLAUDE.md`: add `harness-orchestra` to the skills.
- Run `./scripts/validate_dotfiles.sh`.

### Explicitly out of scope
- A `worktrees.py` of our own: agent-deck already does this.
- Headless `-p` launches.
- A herdr `--visible` mode.
- Rewriting `dispatch.py`.

The existing bug in `dispatch.py` (copilot/agy run with `-i` and `stdin=/dev/null`) goes on a separate card,
`dotfiles-tsk-dispatch-interactive-fix`. The likely fix is to route it through `agent-deck launch` too.

## Files
- **New:** `tasks/orchestra.py`, `.agents/skills/harness-orchestra/SKILL.md`, 2 symlinks.
- **Modified:** `tasks/brief.py`, `tasks/CHEATSHEET.md`, `tasks/README.md`, `tasks/harness-provider-model-index.md`, `AGENTS.md`, `CLAUDE.md`.
- **Reused:** `paths.tasks_root()`, `append_event.append`, `claims.acquire/release/active_claims`, `lifecycle.current_phase`, `brief.prompt_for_task`, `agent-deck launch/status/session output/worktree`.

## Verification
1. **Dry-run with `TSK_ROOT` pointing at a scratch copy.** The commands must be correct and nothing gets created (no worktree, no event, no agent-deck session).
2. **Validation:** `copilot:gpt-5:x` and `agy:foo:x` fail with the list of valid models.
3. **Real smoke test** on a throwaway card created by the human, `dotfiles-tsk-orchestra-smoke`.
   - Three agents: `claude:haiku` + `copilot:gpt-5-mini` + `agy:gemini-3.8-flash-low`.
   - Trivial subtask: one line in a scratch file per agent.
   - Confirm:
     - 3 worktrees exist, on branches `claude/…`, `copilot/…`, `agy/…`;
     - agent-deck delivered the message to all 3. This is critical for agy, which is **not** in agent-deck's support table;
     - 3 pushes and 3 draft PRs;
     - 3 handoff mds;
     - 3 `orchestra.agent_finished` events signed `agent`;
     - `status` and `collect` output is correct.
   - Then close the PRs and run `agent-deck worktree cleanup`.
4. **If agy fails to receive the message through agent-deck:** for agy only, fall back to `-c "agy --model M -i \"$(cat brief)\""`,
   with the prompt passed as an argument. That is still inside agent-deck/tmux. Record it in the evaluation.
5. Re-read `events.jsonl` after every write (lesson from HANDOFF v5).

## Risks / accepted
- **agy under agent-deck is unverified:** covered by Verification 3 and 4.
  If that also fails, workmux (which supports agy natively) is the fallback. It would be a separate install decision for the owner.
- **agy `accept-edits` may block shell commands such as push:** the handoff then says `blocked`. `yolo` for agy is the owner's call.
- **Merge conflicts between PRs:** mitigated by file ownership, not eliminated.
- **agent-deck has no rich status for Copilot:** irrelevant here, because the completion signal is our event plus handoff, not the TUI.

## After approval
1. Worktree `claude/cross-harness-orchestra`.
2. Save this plan to `tasks/plans/cross-harness-orchestra.md`, commit, push, and open a draft PR.
3. `python3 tasks/move_task.py --task-id dotfiles-tsk-cross-harness-orchestra --to-phase in_progress --actor-kind agent --actor-id claude --handoff "Plano em tasks/plans/cross-harness-orchestra.md (PR #…): adotar agent-deck (L2) + orchestra.py fino + contrato no brief.py + skill. Próximo: implementar §1-§5, smoke test §Verification 3."`
4. Re-read the event afterwards.
