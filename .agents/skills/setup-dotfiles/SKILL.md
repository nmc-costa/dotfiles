---
name: setup-dotfiles
description: >
  Set up ~/dotfiles on a new machine end to end: run ./setup.sh, run ./sync.sh,
  then verify the result actually matches what those scripts are supposed to
  produce. Use when the user asks to configure a new machine, bootstrap/install
  dotfiles, or asks "did the setup work" / "is everything installed correctly"
  after cloning this repo. Triggers: new machine setup, setup.sh, sync.sh,
  bootstrap dotfiles, /setup_dotfiles, verify dotfiles install, post-setup
  checklist. Thin shell over verify_setup.sh for the check step — all real
  verification logic lives there, this skill only tells the agent how to run
  the three steps in order and how to read the output.
---

# /setup-dotfiles

New-machine bootstrap for this repo, followed by a real (not doc-trusting)
verification pass.

## What to do

1. **Confirm the repo is cloned.** If it isn't yet:
   ```bash
   git clone https://github.com/nmc-costa/dotfiles.git ~/dotfiles
   cd ~/dotfiles
   ```
   (SSH also works if the user already has keys set up.) If it's already
   cloned, `cd` into it and make sure it's a normal checkout, not a bare one
   (`.git` is a directory, not a `gitdir:` pointer file).

2. **Ask before choosing `setup.sh` flags** — cloning a dozen `~/Work`/
   `~/Projects` repos is a real, visible side effect the human should pick,
   not something to guess:
   - Full new machine (agent config **and** all `~/Work`/`~/Projects`
     repos): `./setup.sh`
   - Just this machine's agent config, repos already present or not wanted
     here: `./setup.sh --links-only`
   - Preview first: add `--dry-run` to either.

3. **Run `./sync.sh`** (repo root, no flags needed for a normal user-level
   sync). Only add `--system` (copies `skills/` to the Omarchy system
   location, needs sudo) if the user explicitly asks for it.

4. **Secrets are a separate, manual, sensitive step — never automate it.**
   `~/.vscode/settings.json`'s API key and `~/.custom_providers/dtx_providers.env`
   are chezmoi+age encrypted; restoring them needs the human to paste their
   private key from Bitwarden. Point them at `docs/SECRETS.md`'s
   "New-machine setup" section and let them run `chezmoi apply` themselves.
   Do not ask for, generate, or handle the key content yourself.

5. **Run the verification script:**
   ```bash
   .agents/skills/setup-dotfiles/verify_setup.sh
   ```
   This is the real logic (D14: script before rule) — it checks the file
   symlinks `setup.sh` creates, the root-context symlinks, that `~/.agents`
   and `~/.claude` came out as real directories with every skill synced in,
   `chezmoi`/age state, `gh` auth, and a couple of things this repo's own
   docs get wrong about its current behavior (see below). It's read-only
   and safe to re-run any time; exits non-zero only if something FAILed.

6. **Report the script's OK / WARN / FAIL lines back to the human in your
   own words:**
   - `OK` — confirmed working as designed.
   - `WARN` — expected on a fresh machine (no age key yet), a manual step
     (`chezmoi apply`, `gh auth login`), or a known doc/reality gap — not
     something broken by this run.
   - `FAIL` — `setup.sh`/`sync.sh` should have produced this and didn't;
     re-run the relevant script, or fix by hand using the message's detail,
     then re-run `verify_setup.sh`.

## What NOT to do

- Don't script or attempt to restore the age private key yourself — it's a
  credential the human pastes from Bitwarden, never something to fetch,
  generate, or read on their behalf.
- Don't run `./sync.sh --system` or anything needing `sudo` without asking
  first.
- Don't treat a `WARN` as a `FAIL` — a missing age key or unauthenticated
  `gh` on a brand-new machine is expected, not a setup bug.
- Don't hand-verify symlinks/directory state by re-deriving the logic
  yourself instead of running `verify_setup.sh` — two of its checks exist
  specifically because this repo's own `README.md`/`AGENTS.md` contradict
  what `setup.sh` actually does now (see below); re-deriving from the docs
  will get those two wrong.

## Known repo/doc gaps this skill works around

- `README.md`/`AGENTS.md` still describe `~/.agents` and `~/.claude` as
  symlinks. Since the 2026-09-17 `sync.sh` rewrite they're real directories
  reconciled by a manifest instead (a symlink here breaks that
  reconciliation — see `CLAUDE.md`'s Known Gaps). `verify_setup.sh` checks
  the real, current behavior.
- `README.md`/`AGENTS.md` also describe `~/.vscode`/`~/.custom_providers`
  (renamed 2026-09-23 from `~/.dtx-providers`, PR #70) as symlinks, while
  `setup.sh`'s own `undo_legacy_dir_symlink` comments say both are now real
  directories written by `chezmoi apply` instead. `verify_setup.sh` reports
  whichever is actually true on the machine rather than asserting either
  doc's claim, and separately warns if a leftover `~/.dtx-providers` from
  before the rename is still on disk.
- `.claude/CLAUDE.md` (this repo's own pointer file) references
  `./setup.sh --install-hooks`, `./sync.sh --install-hooks`, and
  `tasks/scripts/setup_git_hooks.sh`/`pre-push.sample` for the branch-naming
  pre-push hook — none of these exist in `setup.sh`, `sync.sh`, or
  `tasks/scripts/` as of 2026-09-23. `verify_setup.sh` flags this as a
  `WARN`, since it's a documentation gap this skill didn't create and isn't
  scoped to fix.

## Files

- `verify_setup.sh` — the verification checklist described above.
