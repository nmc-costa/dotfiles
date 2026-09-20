**Status: committed plan, ready to execute against.** Produced by the `plan-orchestra`
workflow: 6 parallel research subagents (each citing sources with a `[fact]`/`[inference]`
tag) → an evidence map cross-checking their findings → a planner that committed to all 7
decisions against that evidence and the real state of this repo/machine → two rounds of
adversarial critique (each re-verifying claims directly against `~/dotfiles` and this
machine, not just against the plan's own prose) → one scoped bug-fix pass addressing every
finding from round 2 without reopening the 7 decisions.

Full evidence map (source + confidence per claim): [`docs/AGENT_OS_UNIFICATION_EVIDENCE.md`](AGENT_OS_UNIFICATION_EVIDENCE.md).

**Two items are deliberately narrowed rather than fully closed** (both called out again in
§12 below, with a mitigation):
- The plugin lockfile's `pin` is a reproducibility/drift control, not a supply-chain gate —
  `omarchy-plugin-add` clones and rescans upstream HEAD *before* the pin is checked out, so
  a first install of any new external plugin requires an explicit human
  `DOTFILES_PLUGINS_ALLOW_FIRST_INSTALL=1` opt-in after reviewing the code.
- The write-permission gate (§7) is a strong control, not a sandbox: it classifies `Write`/
  `Edit`/`NotebookEdit` by path and `Bash` by both `forbidden_commands` and best-effort path
  extraction from common write patterns (`sed -i`, `tee`, `cat >`, `cp`, `mv`, `install`,
  `patch`, …) — a sufficiently obfuscated Bash invocation (heredocs, computed paths) can
  still evade path classification.

---

# Plan v3 — `~/dotfiles` as the single living source of truth
### Agent instructions (all providers/harnesses) + Omarchy 4 "Quattro" OS config

**Status:** committed plan. Revision 3 = **v2 with a scoped bug-fix pass**. All 7 decisions
and the architecture are unchanged and are not reopened here.
**Date:** 2026-09-20. **Target machine:** Arch + Omarchy `4.0.4-1` (`pacman -Q omarchy`),
Hyprland 0.56.2, Quickshell 0.3.1, hostname `omarchy`.

---

## Changes from v2 (bug-fix pass)

No decision, boundary, tool choice or deliverable structure changed. 24 defects in the
shell/YAML/Lua written during the v1→v2 pass are fixed.

### MATERIAL

| # | Fix |
|---|---|
| **N1** | `setup.sh` now gets **one** real new flag, `--links-only`, added to its `case` parser (§0.1), and the migration runs *inside* it. `--migrate-only` is deleted entirely and bootstrap calls `setup.sh --links-only` exactly **once**, at step 5b. No undefined flag remains. |
| **N2** | `machines.toml` rewritten as valid TOML — one key per line, no `;` separators. Verified shape against `tomllib` rules; a `toml-parse` assertion is added to the `chezmoi` CI job so this class of error cannot recur. |
| **N3** | `check_invariance()` no longer loses `bad` in a pipeline subshell: the inner loop reads from a process substitution, and findings are counted in a temp file read back by the parent. It now returns non-zero on a violation. |
| **N4** | `cmd_sync`'s main loop no longer runs in a pipeline subshell — it reads from `< <(jq …)` and accumulates into `$FINDINGS_FILE`, which the parent reads before returning 10. `verify` now genuinely fails on drift, hash mismatch, missing or invalid plugins. |
| **N5** | The §5 renderer is rewritten in `python3`+`pyyaml` (already a dependency of this machine's existing SessionStart hook): it parses only the **first** frontmatter block, folds block scalars, strips quoting, and truncates to the first sentence. It reads the **repo's** `.agents/skills/` (committed, so deterministic in CI), with an `AGENTSMD_SKILLS` override. The committed §5 is regenerated to exactly what the renderer emits, so `agents-md --check` can pass. |
| **N6** | The gate emits `{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":…,"permissionDecisionReason":…}}` — the shape this machine's own `workspace-standards-review-check.sh` uses — and `exit 2` as the belt-and-braces block. Bootstrap step 10 now **registers** it in `~/.claude/settings.json`'s `hooks.PreToolUse` array idempotently with `jq`. |
| **N7** | The `Bash` branch now also (a) matches `apply_commands` and denies them when the working tree holds uncommitted L1/L2 edits, and (b) does best-effort path extraction for `sed -i`, `tee`, `cat >`, `>`/`>>`, `cp`, `mv`, `install`, `patch`, `python - <<`, classifying each extracted path through the same matrix. The residual gap (paths the extractor cannot see) is stated explicitly in §7 and §12.2 rather than claimed closed. |
| **N8** | `os/systemd/` now ships **all four** units — `dotfiles-sync.{service,timer}` (the existing local ones, committed verbatim) and `dotfiles-drift.{service,timer}`. Step 10 no longer `die`s: a missing unit source is a warning and the step continues. |
| **N9** | `bin/agentsmd-render` gains a `pointers` mode that rewrites a marked region in the five per-tool pointer files with §1–§2 verbatim; `sync.sh` is *not* modified for this (its core stays untouched) — bootstrap, `mise run agentsmd`, pre-push and CI call it. `.cursor/rules/workspace.mdc` is added to `setup_agent_file_symlink`'s list so the fifth file is actually wired. |
| **N10** | §2 and §12 now state the pin's real semantics: `omarchy-plugin-add` clones and rescans **upstream HEAD** first, so the pin is a **reproducibility / drift control, not a supply-chain gate**. A first install of an external plugin is flagged as requiring human review, and §12.1 ranks it as a real risk. |
| **N11** | §6 of the canonical AGENTS.md now names the file that actually exists — `.agents/instructions/workspace-config/standards/workspace-standards.yaml` — and the dangling "policy pointer in DISCOVERY.md" sentence is replaced by a real, distributable pointer: `.agents/harnesses/POLICY.md` (a pointer *to the repo path*, containing no rules), which keeps the policy itself undistributed. |

### MINOR

| # | Fix |
|---|---|
| **n1** | §0.1's unified diffs are replaced by explicit prose edit instructions ("delete lines X–Y", "insert after line Z") plus verbatim new code. No invalid hunk headers remain. |
| **n2** | Every citation of `sync.sh`'s dest-inside-src refusal corrected to `sync.sh:344-349`. |
| **n3** | The migration step is called **5b** everywhere, including the changelog. |
| **n4** | Pre-push check 4 now strips chezmoi attribute prefixes (`private_`, `encrypted_`, `readonly_`, `executable_`, `symlink_`, `exact_`, `dot_`) and the `.tmpl` suffix before resolving the upstream default, so all 9 tracked files are checked. |
| **n5** | `write-policy.yaml` gains globs for `.git/**`, `.agents/**` (base), `.agents/providers/**`, `.agents/AGENT.md`, `.agents/CONTRIBUTING.md`, plus an explicit first-line catch-all `**` at L1 so the coverage assertion cannot fail. |
| **n6** | The gate's glob→regex conversion is **anchored** (`^…$`) and `.`/`/` are escaped before `*`/`**` expansion. |
| **n7** | `os/omarchy/tracked-files.txt` now has a stated population rule, an initial content listing, and a generator (`bin/dotfiles-drift --suggest-tracking`) that appends newly-diverged candidates for human review. The census's blindness to owner-authored files is stated, with the deferred `nvim/`/`mise/` decision recorded. |
| **n8** | `cmd_adopt()` is now defined in `bin/dotfiles-plugins`, not only described. |
| **n9** | `~/.config/omarchy/shell.toml` is classified explicitly: chezmoi-managed, mode `0600`, tracked (it has no upstream counterpart and is owner-authored). |
| **n10** | Both leaks closed: bootstrap installs the state-dir fallback from `git show origin/main:` (not the working tree) **and** only when `origin/main` exists; `undo_legacy_dir_symlink` now excludes `policy/` from its `cp`. The "fresh clone has no origin/main" rationale is removed — it was wrong. |
| **n11** | `hyprland.lua`'s upstream half is now drift-checked (`diff <(head -n -4 tracked) shipped`), so an upstream change is detected despite the file being deliberately non-identical. The `package.path` precedence claim is corrected: `~/.local/state/?.lua` comes **first**, and drift warns if `~/.local/state/hypr/local.lua` exists and would shadow the escape hatch. |
| **n12** | §12.3 resequenced: `bin/dotfiles-bootstrap` moves to the last implementation PR, after the deliverables its steps depend on. |
| **n13** | Both `omarchy-shell`-dependent calls are guarded (`|| true` / `|| echo false`) so a dead shell produces a finding, never a hard `die`. |

---

## 0. Ground truth (re-verified)

### 0.1 What this plan changes in existing files (n1: prose instructions, not diffs)

Two existing scripts are modified. Both edits are stated as explicit instructions against
the current files so they are unambiguous.

#### `setup.sh` (238 lines today) — four edits

**Edit 1 — add the one new flag (N1).** In the argument loop at `setup.sh:9-16`, insert a
new case arm *before* the catch-all `--*` arm, and add the variable next to the other two
at `setup.sh:6-7`:

```bash
# near line 7, beside DRY_RUN / DO_DOTFILES
LINKS_ONLY=0

# inside the `case "$arg" in` block, BEFORE the `--*) ... exit 1 ;;` arm
    --links-only) LINKS_ONLY=1 ;;
```

`--links-only` is the **only** flag this plan adds. v2's `--migrate-only` is deleted; the
legacy-symlink migration runs unconditionally inside `--links-only` (see Edit 3), so
bootstrap needs exactly one invocation.

**Edit 2 — make repo cloning opt-out (m2).** Wrap the two clone loops at `setup.sh:56-57`
and the `--dotfiles` block at `setup.sh:59-66`:

```bash
if [[ $LINKS_ONLY -eq 0 ]]; then
  for r in "${WORK_REPOS[@]}";     do clone "$r" "$WORK_DIR/$r"; done
  for r in "${PROJECTS_REPOS[@]}"; do clone "$r" "$PROJECTS_DIR/$r"; done
  if [[ $DO_DOTFILES -eq 1 ]]; then
    ... existing bare-clone block, unchanged ...
  fi
fi
```

Rationale: `~/Work` content is L2 (§7). Bootstrap must never pull it as a side effect of a
step labelled "agents". Cloning moves to a human-run `bin/dotfiles-clone-repos`, which
simply calls `setup.sh` without `--links-only`.

**Edit 3 — delete whole-directory symlinking (M1/M2), replace with a migration.**

1. **Delete** the function `setup_agent_symlinks()` in full — `setup.sh:75-109` (35 lines,
   from the `setup_agent_symlinks() {` line through its closing `}`).
2. **Delete** its three call sites at `setup.sh:207-209`:
   `setup_agent_symlinks "agents"`, `… "vscode"`, `… "dtx-providers"`.
3. **Insert** in their place:

```bash
# M1/M2: the three whole-directory symlinks are gone.
#  - "agents": a whole-directory symlink makes ~/.agents and dotfiles/.agents the
#    same inode tree, so sync.sh's 3-way manifest degenerates (source and dest
#    hashes are always equal) and every live write by dtx-providers-tui lands in
#    the git working tree. sync.sh:344-349 already refuses to run in that state;
#    this removes the thing that creates it.
#  - "vscode" / "dtx-providers": both are now real directories written by
#    `chezmoi apply` (§1), which also moves the TUI's generated litellm-config.yaml
#    and proxy.env out of the git working tree.
undo_legacy_dir_symlink "agents"
undo_legacy_dir_symlink "vscode"
undo_legacy_dir_symlink "dtx-providers"
```

4. **Insert** the new function anywhere above those call sites:

```bash
# Convert a legacy whole-directory symlink back into a real directory.
# Idempotent: a real directory or a missing path is left untouched.
undo_legacy_dir_symlink() {
  local dest="$BASE_DIR/.$1"
  [[ -L $dest ]] || { echo "ok:   ~/.$1 is not a legacy symlink"; return 0; }
  local target; target=$(readlink -f "$dest")
  echo "migrating: ~/.$1 was a whole-directory symlink -> $target"
  (( DRY_RUN )) && { echo "(dry) would replace with a real copy"; return 0; }
  rm "$dest"                       # removes the LINK only, never the target
  mkdir -p "$dest"
  # n10: never seed a distributed copy of the write policy. policy/ is the one
  # .agents subdir that must not exist under ~/.agents (see .agents/policy/README.md).
  rsync -a --exclude 'policy/' "$target/" "$dest/"
  echo "ok:   ~/.$1 is now a real directory (sync.sh will reconcile it)"
}
```

**Edit 4 — wire the fifth pointer file (N9).** Add one line beside the existing four at
`setup.sh:215-218`:

```bash
setup_agent_file_symlink "cursor" "rules/workspace.mdc"
```

`setup_agent_file_symlink` already handles a nested path and `mkdir -p`s the parent.

`setup_agent_file_symlink` and `setup_root_symlink` are otherwise **unchanged and
retained** — those link single curated files, not directories, and nothing writes over them.

#### `sync.sh` (467 lines today) — one edit

Inside `main()`'s subdir loop, which begins at `sync.sh:396` (`for subdir in
"$AGENTS_SRC"/*/`), insert immediately after `subdir_name=$(basename "$subdir")`:

```bash
    # M12: policy/ defines what an agent may do. Distributing it would let an
    # agent publish its own permission change with `./sync.sh`, which the matrix
    # classifies L0. The write-policy gate reads from `git show origin/main:` —
    # the merged ref — so the policy has no distributed copy, by design.
    if [[ "$subdir_name" == "policy" ]]; then
      log "skip policy/ (never distributed — see .agents/policy/README.md)"
      continue
    fi
```

That is the entire `sync.sh` change. Its per-file reconciliation core is untouched,
`--check-discovery` is **not** added (m11), and pointer-file generation is **not** added
(N9 — that lives in `bin/agentsmd-render`, a separate script).

### 0.2 Corrected machine census (unchanged from v2; independently re-verified)

Omarchy ships two distinct trees, and v1 compared against the wrong one:

| Tree | What it is | A "default" for a `~/.config` file? |
|---|---|---|
| `/usr/share/omarchy/config/` | the **user-config skeleton** copied into `~/.config` at install | **Yes** — the comparison basis |
| `/usr/share/omarchy/default/` | a **Lua module library** loaded by name (`require("default.hypr.omarchy")`), never copied into `~/.config` | only as a fallback for paths absent from `config/` |

Sweep result: **12 diverged, 29 pristine.** In `~/.config/hypr/` there are **9** files, of
which only `looknfeel.lua` and `monitors.lua` diverge; `.luarc.json`, `autostart.lua`,
`bindings.lua`, `hyprland.lua`, `hyprsunset.conf`, `input.lua` and `xdph.conf` are
byte-identical to upstream and must **never** be tracked.

**Final tracked set for this machine (10 files):**

| File | Why |
|---|---|
| `hypr/monitors.lua` | diverged; the one template (§5) |
| `hypr/looknfeel.lua` | diverged |
| `hypr/hyprland.lua` | **becomes** diverged by this plan's deliberate 4-line local-override edit (§5/M11); drift-checked for upstream changes (n11) |
| `alacritty/alacritty.toml`, `foot/foot.ini`, `ghostty/config`, `kitty/kitty.conf` | diverged terminal configs |
| `git/config` | diverged |
| `omarchy/shell.json` | diverged, mode `0600` |
| `omarchy/shell.toml` | **n9:** owner-authored, no upstream counterpart, mode `0600`. Tracked. |

**Deliberately excluded**, each with a reason: `chromium/Default/Preferences` (browser
runtime state); `herdr/config.toml`, `opencode/opencode.json` (tool state with provider
wiring — deferred pending a secrets review); `omarchy/extensions/omarchy-menu.jsonc`
(deferred one upgrade cycle); `kitty/kitty.conf.bak.*` (backup artefact);
`omarchy/themes/**`, `omarchy/plugins/**` (3,700+ vendored files); `opencode/node_modules/**`.

**n7 — the census's known blind spot, stated plainly.** The sweep enumerates
`/usr/share/omarchy/config/` and compares each entry to `~/.config`, so it is *by
construction* blind to owner-authored files with no upstream counterpart. `nvim/` and
`mise/` were v1 candidates found only that way. **Decision for this pass: neither is
tracked yet.** `nvim/` is a plugin-managed tree with its own lockfile and lazy-loaded
state; `~/.config/mise/` holds machine-local tool installs. Both are recorded in
`os/omarchy/tracked-files.txt` as commented-out candidates so the next `dotfiles-adopt`
run surfaces them for an explicit yes/no rather than silently omitting them.

### 0.3 Other verified facts

| Fact | How verified |
|---|---|
| `~/.agents`, `~/.claude`, `~/.vscode`, `~/.dtx-providers` are all **real directories** today | `[[ -L ]]` on each |
| `sync.sh`'s dest-inside-src refusal is at **`sync.sh:344-349`** (n2) | read directly |
| `sync.sh` = 467 lines; `setup.sh` = 238; `main()` starts at `sync.sh:385`, its subdir loop at `sync.sh:396` | `wc -l`, `sed -n` |
| `dotfiles-sync.{service,timer}` exist in `~/.config/systemd/user/` and the timer is active; the repo has **no** `os/systemd/` yet | `systemctl --user list-timers`, `ls` |
| `omarchy-plugin-add <git-url>` clones the **default branch** into a staging dir, validates, reads `.id`, `mv`s to `$PLUGINS_DIR/$id`, leaves `.git` intact, then runs `omarchy-shell shell rescanPlugins`; refuses non-interactive without `--yes` | read `/usr/bin/omarchy-plugin-add` |
| `omarchy-plugin-enable <id> [placement]`; id matches `^[A-Za-z0-9][A-Za-z0-9._-]*$`, `omarchy.*` reserved | `omarchy-plugin-enable:4-6`, `omarchy-plugin-validate:52-57` |
| `omarchy-plugin-validate` rejects any symlink anywhere in a plugin folder (`.git` pruned) | `omarchy-plugin-validate:111-116` |
| Claude Code `PreToolUse` hooks use `hookSpecificOutput.permissionDecision` — this machine's `~/.claude/hooks/workspace-standards-review-check.sh` uses the same envelope shape for `SessionStart` | read directly; `~/.claude/settings.json` `.hooks` confirms the registration array format |
| `bootstrap.lua` sets `package.path` to `~/.local/state/?.lua` **first**, then `~/.config/?.lua`, then `$OMARCHY_PATH/?.lua` (n11) | read `/usr/share/omarchy/default/hypr/bootstrap.lua` |
| SKILL.md frontmatter is real YAML; `description` appears as a plain string, a single-quoted string, **and** a `>` block scalar across the 13 installed skills; `simplifyhit` has later `name:`-like lines in its body | read 4 SKILL.md files |
| `python3` + `pyyaml` are available and already relied on by an installed hook | that hook's own guard |
| `chezmoi data` exits 0; chezmoi 2.72.1, age 1.3.2, mise 2026.9.9 installed | run this session |
| `pacman -Q omarchy` = `4.0.4-1`; `/usr/share/omarchy/version` = `4.0.0.alpha` | both read (m1) |

### 0.4 Do-not list

- **No KV-cache persistence / "personal engram"** — holds.
- **No open decisions** — holds.
- **Don't touch `/usr/share/omarchy`** — holds; `sync.sh --system` is deprecated (§3).
- **Don't symlink Omarchy plugin folders** — holds, and is stricter than stated (symlinks
  rejected *anywhere inside*). Enforced in three places: `bin/dotfiles-plugins` at install
  time, `.githooks/pre-push`, and a dedicated CI job.

**Brief correction retained:** Claude Code *the product* is available on Bedrock, Vertex
and Foundry; only the **AGENTS.md-fallback feature** is absent there. Consequence in §4:
real per-tool pointer files are kept, never fallback alone.

---

## 1. Decision 1 — Dotfiles manager: **chezmoi**

*(Unchanged from v2. Reproduced for completeness.)*

**chezmoi**, scope widened from two encrypted files to every `$HOME` file that has actually
diverged, with a hard boundary against `sync.sh` (§3).

| Criterion | chezmoi | Why it wins |
|---|---|---|
| Per-machine templating | Native `.tmpl`, `.chezmoidata/`, `.chezmoi.hostname` | `monitors.lua` is pure hardware (3 monitors, one rotated) |
| Secrets | Native age, `decrypt()`, `.chezmoitemplates/` | Already adopted here; key generated; `docs/SECRETS.md` written |
| Real files, not symlinks | Default output **is** a real file | Decisive, given the plugin constraint and the upgrade-hash behaviour |

**Rejections:** **Stow** — it *is* a symlink farm, no Linux copy mode; fails the plugin
constraint; both community Quattro repos using it document symlink-conflict pain.
**Bare git** — real files but zero templating and zero secrets. **Nix home-manager** — the
only technically-equal alternative; rejected because Omarchy 4 is a pacman-managed,
upgrade-in-place distro whose own tooling assumes imperative Arch, so adopting it means two
state authorities for a reproducibility benefit Omarchy already provides.

**Upgrade-hash synergy:** Omarchy replaces any config file still matching a known default
hash on upgrade. Under Stow that *destroys a symlink* — a silent structural failure. Under
chezmoi the worst case is a real file's content being replaced, which `chezmoi diff` and
the weekly drift check surface as an ordinary diff.

```toml
# ~/.config/chezmoi/chezmoi.toml   (per-machine, NEVER committed)
sourceDir   = "/home/nbugz/dotfiles/home"
destDir     = "/home/nbugz"
workingTree = "/home/nbugz/dotfiles"
encryption  = "age"

[age]
    identity  = "/home/nbugz/.config/chezmoi/key.txt"
    recipient = "age1vp83ej2dzlchh6g5fu5nqvkrzy874e8m84x807dtv2vukf5df39sa7c43w"
```

Because `setup.sh` no longer symlinks them (§0.1), `~/.vscode` and `~/.dtx-providers`
become real chezmoi-written directories, moving `dtx-providers-tui`'s generated
`litellm-config.yaml` (which embeds a real upstream key) and `proxy.env` out of the git
working tree.

### Exit plan (backing out of chezmoi)

1. `chezmoi apply` — materialise everything.
2. `chezmoi managed --path-style absolute > /tmp/managed.txt` — exact inventory.
3. `chezmoi archive --output /tmp/dotfiles-plain.tar` — rendered, decrypted,
   template-free tree. Untar into any replacement.
4. Delete `~/.config/chezmoi/` and `home/`. Keep the `.age` blobs: plain age files,
   readable by `age -d -i ~/.config/chezmoi/key.txt`, independent of chezmoi.
5. Drop the `chezmoi apply` step from bootstrap. Nothing else changes, because §3 keeps
   chezmoi and `sync.sh` disjoint.

Cost: lose templating, hand-fork ~1 file per machine. Under an hour.

### mise: scoped out of dotfile management

mise is used only for dev-tool version pinning and as the task runner fronting this plan's
scripts, **never** as a dotfile tracker — `mise dot` beside chezmoi means two authorities
writing the same files. **Revisit trigger:** if Omarchy ships "Dots" as the default,
menu-integrated dotfiles UX in a stable release.

---

## 2. Decision 2 — Omarchy plugin strategy: lockfile keyed on manifest `id` + copy + hash

### CLI contracts (read from `/usr/bin/`)

| Tool | Real contract | Role here |
|---|---|---|
| `omarchy-plugin-add [git-url] [--enable] [--yes]` | `omarchy-git-url-check`, `git clone` of the **default branch** into `$PLUGINS_DIR/.add.tmp.$$`, `omarchy-plugin-validate`, read `.id`, refuse if id installed, `mv` to `$PLUGINS_DIR/$id`, `omarchy-shell shell rescanPlugins` | The install path for external plugins. Leaves `.git` intact. Needs `--yes` non-interactively. |
| `omarchy-plugin-clone <source-id> [--edit]` | Resolves a **catalog source-id**, `cp -aL`, no `.git`, fails if target exists | Forking a *built-in* plugin only. Not used for URLs. |
| `omarchy-plugin-enable <id> [placement]` / `-disable <id>` | Keyed on the **manifest id** | Enable/disable |
| `omarchy-plugin-validate <folder>` | schemaVersion==1, required fields, id regex, `omarchy.*` reserved, entry points exist, **no symlink anywhere inside** | Run after every install |

### N10 — what the `pin` actually guarantees, stated accurately

`omarchy-plugin-add` clones upstream's **default branch**, validates it, installs it, and
triggers a shell rescan **before** `cmd_sync` can check out the pinned commit. Therefore:

> **The `pin` is a reproducibility and drift control, not a supply-chain gate.** On a
> *first* install of an external plugin, the machine receives — and the running
> `omarchy-shell` rescans — whatever upstream HEAD is at that moment, not the audited
> commit. `--yes` (required for non-interactive bootstrap) also suppresses the tool's own
> "plugins run as arbitrary, unsandboxed code inside your long-lived omarchy-shell
> process" warning. A further consequence: if upstream HEAD fails `validate`, the install
> fails even when the pinned commit would have passed.

Two mitigations inside the design, neither of which changes the decision:

1. `cmd_sync` **refuses to first-install an external plugin non-interactively** unless
   `DOTFILES_PLUGINS_ALLOW_FIRST_INSTALL=1` is set. Bootstrap does not set it; it reports
   `NEEDS-REVIEW` instead. Adding third-party code to this machine stays a human act.
2. On every subsequent run the pin *is* enforced (`rev-parse HEAD` vs `pin`, then a
   detached checkout), so ongoing state is reproducible even though the first fetch is not
   gated.

### The lockfile — keyed on `id`

```json
{
  "version": 2,
  "plugins": [
    {
      "id":             "acme.weather",
      "label":          "Weather bar widget",
      "origin":         "external",
      "url":            "https://github.com/acme/omarchy-weather.git",
      "pin":            "9f3c1ab2e4d5c6b7a8901234567890abcdef1234",
      "enabled":        true,
      "placement":      ["--section", "right"],
      "content_sha256": "b41c…"
    },
    {
      "id":             "dtx.session-bar",
      "label":          "Session status bar",
      "origin":         "local",
      "src":            "os/omarchy/plugins-src/dtx.session-bar",
      "enabled":        true,
      "placement":      [],
      "content_sha256": "7ea9…"
    }
  ]
}
```

`id` is authoritative: the install directory is always `$PLUGINS_DIR/$id` because that is
what `omarchy-plugin-add` produces and what `enable`/`disable` take. For a local plugin,
`id` must equal `jq -r .id "$src/manifest.json"` — checked.

### `bin/dotfiles-plugins` (N4, n8, n13 fixed)

```bash
#!/usr/bin/env bash
set -euo pipefail
REPO="${DOTFILES_REPO:-$HOME/dotfiles}"
LOCK="$REPO/os/omarchy/plugins.lock.json"
PDIR="$HOME/.config/omarchy/plugins"
ID_RE='^[A-Za-z0-9][A-Za-z0-9._-]*$'          # omarchy-plugin-validate:55
ALLOW_FIRST="${DOTFILES_PLUGINS_ALLOW_FIRST_INSTALL:-0}"

# N4: findings must survive any subshell. A file is the only thing that does.
FINDINGS_FILE=$(mktemp); trap 'rm -f "$FINDINGS_FILE"' EXIT
note(){ echo "$*"; echo x >>"$FINDINGS_FILE"; }
findings(){ wc -l <"$FINDINGS_FILE" | tr -d ' '; }

# m3: mode + relative path + content. No `sed` delimiter hazard.
plugin_hash() {
  ( cd "$1" && find . -path ./.git -prune -o -type f -printf '%m %P\n' \
      | LC_ALL=C sort \
      | while read -r mode rel; do
          printf '%s %s %s\n' "$mode" "$rel" "$(sha256sum -- "$rel" | cut -d' ' -f1)"
        done ) | sha256sum | cut -d' ' -f1
}

check_installed() {                            # $1=id $2=want_hash -> status word
  local dir="$PDIR/$1"
  [[ -d $dir ]] || { echo missing; return; }
  omarchy-plugin-validate "$dir" >/dev/null 2>&1 || { echo invalid; return; }
  [[ "$(plugin_hash "$dir")" == "$2" ]] && echo ok || echo drifted
}

# n13: omarchy-shell may be down. Never let that become a hard failure.
plugin_is_enabled() {                          # $1=id -> true|false
  omarchy-plugin-list --json 2>/dev/null \
    | jq -r --arg i "$1" 'map(select(.id==$i))[0].enabled // false' 2>/dev/null \
    || echo unknown
}
rescan_shell(){ omarchy-shell shell rescanPlugins >/dev/null 2>&1 || \
  note "WARN: omarchy-shell rescan failed (is the shell running?)"; }

cmd_sync() {
  local mutate=1; [[ ${1:-} == --verify-only ]] && mutate=0

  # N4: read from a process substitution, NOT a pipeline, so the loop body runs
  # in THIS shell and `note` reaches the parent.
  while read -r p; do
    [[ -n $p ]] || continue
    local id origin want enabled dest status
    id=$(jq -r .id <<<"$p"); origin=$(jq -r .origin <<<"$p")
    want=$(jq -r .content_sha256 <<<"$p"); enabled=$(jq -r .enabled <<<"$p")
    [[ $id =~ $ID_RE   ]] || { note "FATAL: invalid plugin id '$id'"; continue; }
    [[ $id != omarchy.* ]] || { note "FATAL: '$id' uses the reserved omarchy.* namespace"; continue; }
    dest="$PDIR/$id"
    status=$(check_installed "$id" "$want")

    if [[ $origin == local ]]; then
      local src="$REPO/$(jq -r .src <<<"$p")"
      if [[ -n $(find "$src" -type l -print -quit) ]]; then
        note "FATAL: symlink inside $src — omarchy-plugin-validate rejects the whole plugin"; continue
      fi
      [[ "$(jq -r .id "$src/manifest.json")" == "$id" ]] \
        || { note "FATAL: manifest id in $src != lockfile id '$id'"; continue; }
      if [[ $status == ok ]]; then echo "ok:   $id (local, in sync)"
      elif (( mutate )); then
        rsync -a --delete --copy-links --exclude '.git' "$src/" "$dest/"
        omarchy-plugin-validate "$dest" || { note "FATAL: $id failed validate"; continue; }
        rescan_shell; echo "installed: $id (local)"
      else note "DRIFT: $id ($status)"; fi

    else
      local url pin; url=$(jq -r .url <<<"$p"); pin=$(jq -r .pin <<<"$p")
      if [[ $status == missing ]]; then
        # N10: a FIRST install fetches upstream HEAD, not the pin. Human act only.
        if (( ! mutate )); then note "MISSING: $id not installed"; continue; fi
        if [[ $ALLOW_FIRST != 1 ]]; then
          note "NEEDS-REVIEW: $id is not installed. A first install runs upstream HEAD of
          $url as unsandboxed code inside omarchy-shell BEFORE the pin is applied.
          Review the repo, then: DOTFILES_PLUGINS_ALLOW_FIRST_INSTALL=1 dotfiles-plugins sync"
          continue
        fi
        omarchy-plugin-add "$url" --yes || { note "FATAL: add failed for $url"; continue; }
        [[ -d $dest ]] || { note "FATAL: '$id' is not what $url installed (check manifest .id)"; continue; }
      fi
      # m4: no network unless the pin is not already checked out.
      if [[ "$(git -C "$dest" rev-parse HEAD 2>/dev/null || true)" != "$pin" ]]; then
        if (( ! mutate )); then note "DRIFT: $id is not at pinned $pin"; continue; fi
        git -C "$dest" rev-parse --verify --quiet "$pin^{commit}" >/dev/null \
          || git -C "$dest" fetch --quiet origin || { note "FATAL: fetch failed for $id"; continue; }
        git -C "$dest" checkout --quiet --detach "$pin" \
          || { note "FATAL: cannot check out $pin in $id"; continue; }
        rescan_shell
      fi
      omarchy-plugin-validate "$dest" || { note "FATAL: $id failed validate"; continue; }
      local have; have=$(plugin_hash "$dest")
      [[ $have == "$want" ]] || note "HASH MISMATCH: $id installed=$have locked=$want"
    fi

    if (( mutate )); then
      local cur; cur=$(plugin_is_enabled "$id")
      case "$cur" in
        unknown) note "WARN: cannot read plugin state for $id (omarchy-shell unavailable)" ;;
        *)
          if [[ $enabled == true && $cur != true ]]; then
            readarray -t place < <(jq -r '.placement[]?' <<<"$p")
            omarchy-plugin-enable "$id" "${place[@]}" || note "WARN: enable failed for $id"
          elif [[ $enabled != true && $cur == true ]]; then
            omarchy-plugin-disable "$id" || note "WARN: disable failed for $id"
          else echo "ok:   $id enabled=$enabled"; fi ;;
      esac
    fi
  done < <(jq -c '.plugins[]' "$LOCK")

  # Installed but not in the lockfile: report, NEVER auto-remove.
  local d n
  for d in "$PDIR"/*/; do
    [[ -d $d ]] || continue; n=$(basename "$d")
    jq -e --arg n "$n" '.plugins[]|select(.id==$n)' "$LOCK" >/dev/null 2>&1 \
      || note "UNTRACKED plugin installed: $n  (dotfiles-plugins adopt $n)"
  done

  (( $(findings) == 0 )) || return 10           # m10: shared exit convention
}

# n8: defined, not merely described.
cmd_adopt() {
  local id="$1" dir="$PDIR/$id" tmp
  [[ -d $dir ]] || { echo "not installed: $id" >&2; return 1; }
  omarchy-plugin-validate "$dir" || { echo "refusing to adopt an invalid plugin" >&2; return 1; }
  [[ "$(jq -r .id "$dir/manifest.json")" == "$id" ]] \
    || { echo "manifest id != directory name; refusing" >&2; return 1; }
  local hash; hash=$(plugin_hash "$dir")
  local label; label=$(jq -r '.name // .id' "$dir/manifest.json")
  local enabled; enabled=$(plugin_is_enabled "$id"); [[ $enabled == unknown ]] && enabled=false

  if [[ -d $dir/.git ]]; then                   # external
    local url pin
    url=$(git -C "$dir" remote get-url origin 2>/dev/null || true)
    pin=$(git -C "$dir" rev-parse HEAD)
    [[ -n $url ]] || { echo "no origin remote; adopt it as origin=local instead" >&2; return 1; }
    tmp=$(mktemp)
    jq --arg id "$id" --arg l "$label" --arg u "$url" --arg p "$pin" \
       --arg h "$hash" --argjson e "$enabled" '
       .plugins |= (map(select(.id != $id)) +
         [{id:$id,label:$l,origin:"external",url:$u,pin:$p,enabled:$e,placement:[],content_sha256:$h}])
       | .plugins |= sort_by(.id)' "$LOCK" >"$tmp"
  else                                          # local: copy the source in
    local src="$REPO/os/omarchy/plugins-src/$id"
    [[ -n $(find "$dir" -type l -print -quit) ]] \
      && { echo "installed copy contains a symlink; refusing to adopt" >&2; return 1; }
    rsync -a --delete --exclude '.git' "$dir/" "$src/"
    hash=$(plugin_hash "$src")
    tmp=$(mktemp)
    jq --arg id "$id" --arg l "$label" --arg s "os/omarchy/plugins-src/$id" \
       --arg h "$hash" --argjson e "$enabled" '
       .plugins |= (map(select(.id != $id)) +
         [{id:$id,label:$l,origin:"local",src:$s,enabled:$e,placement:[],content_sha256:$h}])
       | .plugins |= sort_by(.id)' "$LOCK" >"$tmp"
  fi
  echo "--- proposed lockfile change ---"; diff -u "$LOCK" "$tmp" || true
  mv "$tmp" "$LOCK"
  echo "Lockfile updated in the working tree. NOTHING was committed."
}

case "${1:-status}" in
  sync)   cmd_sync ;;
  verify) cmd_sync --verify-only ;;
  adopt)  cmd_adopt "${2:?plugin id required}" ;;
  status) cmd_sync --verify-only || true ;;
  *) echo "usage: dotfiles-plugins <sync|verify|adopt <id>|status>" >&2; exit 2 ;;
esac
```

**Removal is never automatic** — `omarchy-plugin-remove` is L2 (§7).

### The philosophy this forces

> **Track only what has actually diverged. Never mirror a pristine Omarchy default.**

One shared resolver, used by drift, adopt and pre-push:

```bash
# Resolve the upstream default for a path relative to $HOME.
# Checks the user-config skeleton FIRST, then the Lua module tree.
omarchy_default_for() {
  local rel="${1#./}" c d
  [[ $rel == .config/* ]] || return 1
  c="/usr/share/omarchy/config/${rel#.config/}";  [[ -f $c ]] && { echo "$c"; return 0; }
  d="/usr/share/omarchy/default/${rel#.config/}"; [[ -f $d ]] && { echo "$d"; return 0; }
  return 1
}
is_pristine(){ local def; def=$(omarchy_default_for "$1") && cmp -s "$HOME/$1" "$def"; }

# n4: chezmoi source path -> $HOME-relative path. Strips attribute prefixes on
# EVERY segment and the .tmpl suffix, so private_/encrypted_/*.tmpl files are
# checked too (2 of the 9 tracked files were being skipped).
chezmoi_source_to_rel() {
  local p="${1#home/}" out=""
  p="${p%.tmpl}"
  local IFS=/; for seg in $p; do
    seg="${seg#private_}"; seg="${seg#encrypted_}"; seg="${seg#readonly_}"
    seg="${seg#executable_}"; seg="${seg#symlink_}"; seg="${seg#exact_}"
    [[ $seg == dot_* ]] && seg=".${seg#dot_}"
    out="${out:+$out/}$seg"
  done
  echo "$out"
}
```

`~/.config/omarchy/{themes,plugins}/` are never chezmoi-managed under any circumstances.

---

## 3. Decision 3 — Boundary: global vs per-repo vs per-machine

*(Unchanged from v2, plus n9's classification.)*

### Content tiers

| Still true in another repo? | On another machine? | Tier | Lives in | Distributed by |
|---|---|---|---|---|
| Yes | Yes | **T1 GLOBAL** | `~/dotfiles/.agents/**` | `sync.sh` → `~/.agents/` + the five per-tool pointer files |
| No | — | **T2 PER-REPO** | `<that repo>/AGENTS.local.md` | nothing; dotfiles ships the template |
| Yes | No | **T3 PER-MACHINE** | `home/**` as a `.tmpl` + `.chezmoidata/machines.toml` | `chezmoi apply` |
| Yes | Yes, but employer content | **T3-LOCAL** | `~/Work/CLAUDE.md` from `global/WORK.CLAUDE.template.md` | copied by hand |

### Which tool owns which destination

> **If the destination directory is one a harness or tool writes live runtime state into,
> `sync.sh` owns it with real copies. Otherwise chezmoi owns it. Nothing is ever a
> whole-directory symlink.**

| Destination | Owner | Why |
|---|---|---|
| `~/.agents/**` (except `policy/`) | `sync.sh` | `dtx-providers-tui` writes into `providers/registry/` live. Requires the `setup.sh` change in §0.1. |
| `~/.agents/policy/` | **nobody** | M12: never distributed. `sync.sh` skips it; `undo_legacy_dir_symlink` excludes it (n10). |
| `~/.claude/`, `~/.gemini/`, `~/.codex/`, `~/.copilot/`, `~/.cursor/` | `sync.sh` + `setup_agent_file_symlink` | credentials, session DBs, logs, caches — real dirs, exactly one file-level symlink each |
| `~/.vscode/`, `~/.dtx-providers/` | chezmoi | real files (§0.1 removed the symlink calls) |
| `~/.config/**`, diverged files only | chezmoi | §0.2 |
| `~/.config/omarchy/{themes,plugins,defaults}/` | **neither** | Omarchy owns these trees |
| `~/.config/omarchy/hooks/` | **neither** (m9) | executable hooks Omarchy runs mid-upgrade; several are locally generated. Managing them invites a write race at the worst moment. |
| `~/.config/omarchy/{branding,extensions,themed}/` | chezmoi (m9) | curated; diverged-only |
| `~/.config/omarchy/shell.toml`, `shell.json` | chezmoi (n9) | owner-authored / diverged, both mode `0600`, both tracked |
| `/usr/share/omarchy/**` | **nobody** | pacman-owned. `sync.sh --system` prints a deprecation notice and exits 0 without writing. |

### Why not adopt one of the 5 agent-sync tools

None of the three symlinkers documents handling a destination the harness writes live
runtime state into. The two generators want to own the canonical source layout, colliding
with the hand-authored pointer files and `.agents/instructions/`.
**Decision: extend `sync.sh`, adopt none.** One idea is stolen — rulesync's
harness-coverage matrix, landing as `.agents/harnesses/DISCOVERY.md` plus a standalone
`bin/dotfiles-discovery-check`. **Not** added to `sync.sh`, which is already 467 lines.

**Revisit trigger (m11):** when either (a) the number of distinct destination *formats*
`sync.sh` must emit exceeds 3 (today: 1 — verbatim file copy), or (b) `DISCOVERY.md`
exceeds 12 harness rows.

---

## 4. Decision 4 — Canonical `AGENTS.md` ordering, invariance rule, and generator

### The principle

Every provider does **exact-prefix** cache matching: Anthropic (`cache_control`, cumulative
hash), OpenAI (KV reuse, full prefix), Gemini (implicit, recommends common content first),
DeepSeek (on-disk, prefix-unit, partial matches don't count). **Order by (stability ×
breadth of sharing), descending.**

**Scope of the claim:** §1–§6 are byte-identical **across every repo on one machine**, not
across machines (§5 enumerates this machine's installed skills).

### The invariance rule — mechanically checkable

> **No line in §1–§6 may name a filesystem path, script, or file that exists in only one
> repository.**

Enforced by `bin/agentsmd-render`'s `check_invariance` (fixed in N3) and the
`agents-md-invariance` CI job.

### The ordered list

| # | Section | Justification |
|---|---|---|
| 1 | **Identity & operating contract** | Changes never; identical everywhere — highest-value prefix bytes |
| 2 | **Non-negotiable rules** | Safety limits; must sit inside the cached prefix; as stable as §1 |
| 3 | **Workspace map** | Home-directory conventions, not any one repo's; stable per machine |
| 4 | **Environment invariants** | OS/WM/package-manager facts; changes on OS-major upgrades only |
| 5 | **Capability index** | Skill names + descriptions only; machine-global, ~monthly churn |
| 6 | **Workflow conventions** | Branch/commit/PR rules and *how to find* a repo's validators |
| 7 | **Repo context** | ← the per-repo boundary |
| 8 | **Current state** | Pointers only; most volatile, invalidates nothing above |
| 9 | **Appendix** | Bare paths; grows freely at the tail |

### The generator

**Source — `.agents/agentsmd/`:**

```
.agents/agentsmd/
├── manifest.yaml           # ordering + invariance metadata
├── 10-identity.md          # body of §1 (no heading — the renderer emits headings)
├── 20-nonnegotiables.md
├── 30-workspace-map.md
├── 40-environment.md
├── 50-capability-index.py  # N5: a real parser, not awk
└── 60-workflow.md
```

```yaml
# .agents/agentsmd/manifest.yaml
version: 1
shared_prefix_through: 60
invariance_denylist:
  - "validate_dotfiles.sh"
  - "CHEATSHEET.md"
  - "write-policy.yaml"
  - ".githooks/"
  - "This repo"
  - "AGENTS.local.md"
sections:
  - { id: 10, heading: "Identity and operating contract", source: 10-identity.md }
  - { id: 20, heading: "Non-negotiable rules",            source: 20-nonnegotiables.md }
  - { id: 30, heading: "Workspace map",                   source: 30-workspace-map.md }
  - { id: 40, heading: "Environment invariants",          source: 40-environment.md }
  - { id: 50, heading: "Capability index",                source: 50-capability-index.py,
      render: skills }
  - { id: 60, heading: "Workflow conventions",            source: 60-workflow.md }
local_tail: AGENTS.local.md
pointer_files:                       # N9
  - .claude/CLAUDE.md
  - .gemini/GEMINI.md
  - .codex/AGENTS.md
  - .copilot/copilot-instructions.md
  - .cursor/rules/workspace.mdc
```

#### N5 — the capability-index renderer, rewritten so it can actually pass

v2's awk broke three ways on real data (block scalars became a literal `>`, `simplifyhit`
picked up a later `name:`-like line in its body, quoting survived) and hard-coded
`$HOME/.agents/skills`, which is empty on a CI runner. Replaced by:

```python
#!/usr/bin/env python3
# .agents/agentsmd/50-capability-index.py
# Renders the §5 table. Reads the REPO's .agents/skills (committed, so a CI
# runner and this machine produce identical output). Override: AGENTSMD_SKILLS.
import os, sys, glob, yaml, re

root = os.environ.get("AGENTSMD_SKILLS") or os.path.join(sys.argv[1], ".agents", "skills")

def frontmatter(path):
    """Parse ONLY the first --- ... --- block. Fixes the `name: [InstructionName]`
    false match, which came from scanning the whole file."""
    with open(path, encoding="utf-8") as fh:
        if fh.readline().strip() != "---":
            return {}
        buf = []
        for line in fh:
            if line.strip() == "---":
                break
            buf.append(line)
    try:
        return yaml.safe_load("".join(buf)) or {}
    except yaml.YAMLError:
        return {}

rows = []
for p in sorted(glob.glob(os.path.join(root, "*", "SKILL.md"))):
    fm = frontmatter(p)
    name = str(fm.get("name") or os.path.basename(os.path.dirname(p))).strip()
    # yaml.safe_load already folds `>` block scalars and strips '…'/"…" quoting.
    desc = " ".join(str(fm.get("description", "")).split())
    # First sentence only, so a 12-line description does not dominate the prefix.
    m = re.match(r"(.+?[.!?])(\s|$)", desc)
    desc = (m.group(1) if m else desc)[:240].strip()
    if name:
        rows.append((name, desc))

print("Skills are discovered from `~/.agents/skills/<name>/SKILL.md`. Invoke by name.")
print()
print("| Skill | Use when |")
print("|---|---|")
for name, desc in rows:
    print(f"| `{name}` | {desc or '(no description)'} |")
print()
print("Which file each harness actually reads on startup: `~/.agents/harnesses/DISCOVERY.md`.")
```

Consequence, accepted deliberately: the committed §5 is now **exactly** the generator's
output — one row per installed skill, machine-ordered, first sentence of each
`description`. The hand-curated, six-HITs-collapsed table from v2 is gone, because a
hand-curated table cannot be diffed against a generator. The §5 shown in the canonical
file below is the generated form.

#### `bin/agentsmd-render` (N3, N5, N9 fixed)

```bash
#!/usr/bin/env bash
set -uo pipefail
ROOT="${2:-$PWD}"
SRC="${AGENTSMD_SRC:-$ROOT/.agents/agentsmd}"
MAN="$SRC/manifest.yaml"
BEGIN='<!-- AGENTSMD:PREFIX BEGIN - generated, do not edit -->'
END='<!-- AGENTSMD:PREFIX END -->'

render_prefix() {          # sections 1..shared_prefix_through, headings included
  local n=0
  while IFS=$'\t' read -r id heading source rmode; do
    n=$((n+1)); echo "## $n. $heading"; echo
    if [[ $rmode == skills ]]; then python3 "$SRC/$source" "$ROOT"
    else cat "$SRC/$source"; fi
    echo
  done < <(yq -r '.sections[] | [.id, .heading, .source, (.render // "")] | @tsv' "$MAN")
}

render() {
  echo "# AGENTS.md"; echo
  echo "<!-- SECTIONS 1-6 ARE GENERATED by bin/agentsmd-render from .agents/agentsmd/."
  echo "     Edit there and re-run; hand-edits here fail CI. Sections 7-9 come from"
  echo "     this repo's own AGENTS.local.md. -->"; echo
  render_prefix
  [[ -f "$ROOT/$(yq -r .local_tail "$MAN")" ]] && cat "$ROOT/$(yq -r .local_tail "$MAN")"
}

# N3: findings must survive the inner loop's subshell. A temp file is the only
# thing that does; v2 set `bad=1` on the right-hand side of a pipe and lost it.
check_invariance() {
  local hits limit; hits=$(mktemp); trap 'rm -f "$hits"' RETURN
  limit=$(yq -r .shared_prefix_through "$MAN")
  while read -r term; do
    [[ -n $term ]] || continue
    while read -r f; do
      [[ -n $f ]] || continue
      # Only text sections; the .py renderer is checked by its own output below.
      [[ $f == *.md ]] || continue
      if grep -qF -- "$term" "$SRC/$f" 2>/dev/null; then
        echo "INVARIANCE: '$term' appears in shared-prefix section $f" >&2
        echo x >>"$hits"
      fi
    done < <(yq -r --arg l "$limit" '.sections[]|select(.id <= ($l|tonumber)).source' "$MAN")
  done < <(yq -r '.invariance_denylist[]' "$MAN")
  # Also check the rendered prefix, which catches a denylisted term introduced
  # by the generated §5 rather than by a source file.
  while read -r term; do
    [[ -n $term ]] || continue
    render_prefix 2>/dev/null | grep -qF -- "$term" \
      && { echo "INVARIANCE: '$term' appears in the RENDERED prefix" >&2; echo x >>"$hits"; }
  done < <(yq -r '.invariance_denylist[]' "$MAN")
  [[ ! -s $hits ]]
}

# N9: keep each pointer file's §1-§2 region in sync, so the shared prefix really
# does extend across the pointer-file split. sync.sh is NOT modified for this.
render_pointers() {
  local mode="${1:-write}" rc=0 tmp body
  body=$(render_prefix | awk '/^## 3\./{exit} {print}')   # sections 1 and 2 only
  while read -r rel; do
    [[ -n $rel && -f "$ROOT/$rel" ]] || { echo "WARN: pointer file missing: $rel" >&2; continue; }
    tmp=$(mktemp)
    awk -v b="$BEGIN" -v e="$END" -v f="$tmp.body" '
      $0==b {print; while ((getline l < f) > 0) print l; skip=1; next}
      $0==e {skip=0}
      !skip {print}' "$ROOT/$rel" > "$tmp" < /dev/null 2>/dev/null || true
    printf '%s\n' "$body" > "$tmp.body"
    awk -v b="$BEGIN" -v e="$END" -v f="$tmp.body" '
      $0==b {print; while ((getline l < f) > 0) print l; skip=1; next}
      $0==e {skip=0; print; next}
      !skip {print}' "$ROOT/$rel" > "$tmp"
    if [[ $mode == check ]]; then
      cmp -s "$tmp" "$ROOT/$rel" || { echo "POINTER STALE: $rel" >&2; rc=1; }
    else mv "$tmp" "$ROOT/$rel"; fi
    rm -f "$tmp.body"
  done < <(yq -r '.pointer_files[]' "$MAN")
  return $rc
}

case "${1:-render}" in
  render)   check_invariance && render ;;
  pointers) check_invariance && render_pointers write ;;
  --check)  check_invariance \
              && diff -u "$ROOT/AGENTS.md" <(render) \
              && render_pointers check ;;
  *) echo "usage: agentsmd-render <render|pointers|--check> [repo-root]" >&2; exit 2 ;;
esac
```

Each pointer file keeps its own hand-written pointer paragraph; only the region between
`AGENTSMD:PREFIX BEGIN/END` is machine-owned. Those markers are added once, by hand, in the
PR that lands this (PR 6).

**Dependencies:** `yq` (Arch `extra`, kislyuk/yq — jq syntax, `--arg` supported),
`python3` + `pyyaml`. Both are in bootstrap's `DEPS`.

### Distribution consequence (the Bedrock/Vertex/Foundry correction)

Because the AGENTS.md-fallback feature is absent on Bedrock/Vertex/Foundry, the repo keeps
real per-tool pointer files rather than relying on fallback. `bin/agentsmd-render pointers`
— **not** `sync.sh` — keeps §1–§2 verbatim inside each of the five, so the prefix is shared
across the pointer-file split. `setup.sh` file-symlinks all five into place (§0.1 Edit 4
adds the Cursor one).

### The canonical `AGENTS.md`, fully written out

```markdown
# AGENTS.md

<!-- SECTIONS 1-6 ARE GENERATED by bin/agentsmd-render from .agents/agentsmd/.
     Edit there and re-run; hand-edits here fail CI. Sections 7-9 come from
     this repo's own AGENTS.local.md. -->

## 1. Identity and operating contract

You are a coding agent working for the owner of this workspace, a research engineer
who works across personal projects and employer repositories.

- Write all code, comments, commit messages and documentation in English.
- Converse in the language the owner writes to you in.
- Prefer being decisive over being exhaustive. When asked to choose, choose, and say
  why in one sentence.
- Never present an unverified claim as fact. If you did not read it or run it, say so,
  and say which of the two you did.
- Do not use emojis in any output.

## 2. Non-negotiable rules

- Never write, print, or transmit a credential. Secrets exist only inside encrypted
  blobs and locally-decrypted files that are excluded from version control.
- Never modify anything under `/usr/`. It belongs to the system package manager.
  Customise through the user configuration directory instead.
- Never create a symlink anywhere inside an Omarchy plugin folder. The shipped
  validator rejects the entire plugin if one exists at any depth.
- Never install or enable a third-party plugin on your own. A first install runs
  upstream code unsandboxed inside a long-lived process before any pin applies.
- Never commit to the default branch and never force-push. Work on a topic branch
  and open a pull request.
- Never run a destructive command (`rm -rf`, `git reset --hard`, `pacman -R`, or any
  plugin/theme removal) without explicit approval in the current turn.
- Never add a configuration file to version control when it is byte-identical to the
  version the operating system ships. The OS replaces such files on upgrade.
- Before applying any change to the live machine, check the workspace write-permission
  policy; when in doubt, propose rather than apply.

## 3. Workspace map

| Path | Contents | How to refer to it |
|---|---|---|
| `~/Projects/<repo>` | Personal projects and studies | `Projects/<repo>/...` |
| `~/Work/<repo>` | Employment repositories. Never copied into shared configuration. | `Work/<repo>/...` |
| `~/dotfiles` | The workspace configuration repository: agent instructions and OS config | `.dotfiles/<file>` |
| `~/.agents/`, `~/.claude/`, `~/.config/` | Distributed copies and live tool state. Never edit these directly. | — |

Repositories are organised by context (personal vs professional), never by hosting
platform. There is no `github/`, `gitlab/` or `bitbucket/` directory.

Edit in `~/dotfiles`; a distributed copy is an output, never a source.

## 4. Environment invariants

- Arch Linux running Omarchy 4 "Quattro"; window manager Hyprland, configured in Lua
  under `~/.config/hypr/`; the shell layer is Quickshell.
- Package manager `pacman`, AUR through `yay`. Dev-tool versions through `mise`.
- Home-directory configuration is rendered by `chezmoi`; agent instructions and skills
  are distributed by the workspace repository's own sync script.
- Omarchy replaces default configuration files by hash on upgrade, so only files that
  have actually diverged from the shipped version are tracked anywhere.
- The installed Omarchy version is what `pacman -Q omarchy` reports; the version file
  under `/usr/share/omarchy/` is not reliable.

## 5. Capability index

Skills are discovered from `~/.agents/skills/<name>/SKILL.md`. Invoke by name.

| Skill | Use when |
|---|---|
| `archi` | Architect Agent - Meta-Orchestrator |
| `calls2database` | Extract funding-call opportunities from EU/Horizon call PDFs and rank them by fit against DTx Colab's research teams and track record. |
| `diagnose-crash` | Diagnose why a program crashed on this machine, from a systemd-coredump core dump. |
| `diagramhits` | diagramHITs Agent - Diagram Architect |
| `documenthits` | documentHITs Agent - Document Update Architect |
| `mockuphits` | mockupHITs Agent - SciML Mockup Architect |
| `omarchy` | REQUIRED for end-user customization of Linux desktop, window manager, or system config. |
| `plan-orchestra` | Orchestrate a multi-agent research-and-planning workflow: clarify scope with the human, fan out closed sub-questions to research subagents, verify and reconcile their findings into an evidence map, have a single subagent commit to one decisive plan, subject that plan to adversarial critique, then deliver. |
| `presenthits` | presentHITs Agent - Executive Slide Architect |
| `project-doc-lifecycle` | Validate a formal project document (INCM Project Charter, WP1.md, work plan) against its project brief, auto-correct it in place, then compile it to .docx with the helper scripts. |
| `projecthits` | projectHITs Agent - Charter Architect (v4) |
| `reviewhits` | reviewHITs Agent - Peer Review Architect |
| `simplifyhit` | Optimize a system-instruction / persona / SKILL.md file for agent efficiency — semantic density, explicit critical rules, named anti-patterns, token budget, optional persona injection. |

Which file each harness actually reads on startup: `~/.agents/harnesses/DISCOVERY.md`.

## 6. Workflow conventions

- Branch naming: `claude/<topic>`. One topic per branch. Never commit to the default
  branch directly.
- Commit subject: imperative mood, lower case, at most 72 characters.
- The workspace-wide standards every repository must satisfy are defined in
  `~/.agents/instructions/workspace-config/standards/workspace-standards.yaml`. Read
  `review.nextDue` at the start of a session and honour the review protocol described
  there. Run the validators that file names before committing a change to it.
- Before any structural change to a repository, run the validators that repository
  documents in its README; if it documents none, run its test suite.
- Push is gated by a repository hook that scans for secrets. Never bypass a failing
  hook with `--no-verify`; fix the finding instead.
- Update the repository's own living documentation in the same commit as the change it
  describes, not in a follow-up.
- The workspace write-permission policy — which paths an agent may change on its own
  and which need a human — is summarised at `~/.agents/harnesses/POLICY.md`, which
  points at the authoritative file inside the workspace configuration repository.

## 7. Repo context

<!-- PER-REPO: this and everything below comes from AGENTS.local.md. -->

**dotfiles** — the single source of truth for agent instructions (all providers and
harnesses) and for this machine's Omarchy configuration.

- `.agents/` is the source of truth for agent content; `home/` is the chezmoi source
  for `$HOME`; `os/` holds machine state that is declared but not file-tracked.
- Entry points: `bin/dotfiles-bootstrap` (clone → machine ready, idempotent),
  `sync.sh` (agent content out), `bin/dotfiles-adopt` (machine → repo, diff first,
  never commits), `bin/dotfiles-drift` (report only; exit 10 means findings),
  `bin/dotfiles-plugins`, `bin/agentsmd-render`, `bin/dotfiles-clone-repos`.
- Validators, both required before any push: `./scripts/validate_dotfiles.sh` and
  `python3 scripts/validate_workspace_standards.py` on the standards YAML.
- Any change under `.agents/` updates `CHEATSHEET.md` in the same commit.
- Sections 1-6 of this file are generated. Edit `.agents/agentsmd/`, then run
  `mise run agentsmd`. Editing this file above section 7 fails CI.
- The write-permission matrix is `.agents/policy/write-policy.yaml`. It is never
  distributed and never self-amendable: the gate reads it from `origin/main`.
- `tasks/` is a separate initiative (multi-agent task board, decided 2026-09-18,
  unimplemented). Do not conflate it with the dotfiles-unification work.

## 8. Current state

- Open work and the persistent TODO list: `CHEATSHEET.md` §4.
- Cross-session task board: `tasks/board.md` (append via `tasks/append_event.py`;
  never hand-edit `board.md`).
- Known gaps and audit caveats: `CLAUDE.md`, "Known Gaps".

## 9. Appendix: further reading

- `docs/OS.md` — Omarchy tracking policy, the two default trees, plugin lockfile
- `docs/SECRETS.md` — chezmoi + age
- `docs/STANDARDS.md` — naming and structure conventions
- `.agents/harnesses/DISCOVERY.md` — which file each harness actually reads
- `.agents/policy/write-policy.yaml` — the write-permission matrix
- `README.md` — full directory tree and index
```

**N11 note.** §6's two dangling references are gone. The standards file named is the one
that exists (`.agents/instructions/workspace-config/standards/workspace-standards.yaml`,
distributed by `sync.sh` to `~/.agents/...`). The policy sentence now points at a new,
tiny, distributable file `.agents/harnesses/POLICY.md` whose entire content is a pointer —
"the authoritative matrix is `<repo>/.agents/policy/write-policy.yaml`; it is deliberately
not distributed; ask a human before changing anything it marks L1 or L2" — so M12's
no-distributed-copy lock still holds (a pointer is not the policy).

---

## 5. Decision 5 — Per-machine vs shared files

### Mechanism

**(a) Shared, identical everywhere** → plain file in `home/`, no suffix.

**(b) Shared shape, per-machine values** → `.tmpl` + `home/.chezmoidata/machines.toml`.

**N2 — valid TOML this time.** v2 used `;` as a key separator, which `tomllib` rejects, so
`chezmoi data` (a hard failure in bootstrap step 5) died on every machine.

```toml
# home/.chezmoidata/machines.toml   (committed; contains no secrets)

[machines.default]                 # ANY host not listed below
gpu          = "auto"
profile      = "personal"
gdkScale     = 1
monitorScale = 1.0
monitors = [
  { output = "", mode = "preferred", position = "auto", scale = 1.0 },
]

[machines.omarchy]                 # this laptop
gpu          = "amd"
profile      = "personal"
gdkScale     = 2
monitorScale = 1.6
monitors = [
  { output = "eDP-1",    mode = "preferred", position = "auto",   scale = 1.6 },
  { output = "HDMI-A-1", mode = "preferred", position = "1440x0", scale = 1.6 },
  { output = "DP-1",     mode = "preferred", position = "3360x0", scale = 1.0, transform = 1 },
]
```

A `toml-parse` assertion is added to the `chezmoi` CI job
(`python3 -c "import tomllib,sys; tomllib.load(open(sys.argv[1],'rb'))"`) so this cannot
recur.

```go-template
{{/* home/dot_config/hypr/monitors.lua.tmpl */ -}}
{{- $host := .chezmoi.hostname -}}
{{- if not (hasKey .machines $host) }}{{ $host = "default" }}{{ end -}}
{{- $m := index .machines $host -}}
-- GENERATED by chezmoi from home/.chezmoidata/machines.toml for {{ .chezmoi.hostname }}
-- (profile: {{ $host }}). Edit the TOML, not this file. See docs/OS.md.
-- `hl` is a global established by Omarchy's bootstrap.lua; no local binding needed.
hl.env("GDK_SCALE", "{{ $m.gdkScale }}")
{{ range $m.monitors }}{{ if .output -}}
hl.monitor({ output = "{{ .output }}", mode = "{{ .mode }}", position = "{{ .position }}", scale = {{ .scale }}{{ with .transform }}, transform = {{ . }}{{ end }} })
{{ end }}{{ end -}}
{{- if not (index $m.monitors 0).output }}
-- Unknown host: let Hyprland auto-detect every output rather than configure none.
hl.monitor({ output = ",", mode = "preferred", position = "auto", scale = 1 })
{{- end }}
```

**(c) The local-override hook (M11 fix retained, n11 corrections applied)**

`require_optional` is a module table with a `.module` method, not a global. Four lines are
appended to `hyprland.lua`, under Omarchy's own invitation comment
("Add any other personal Hyprland configuration below."):

```lua
-- Machine-local overrides. Loaded LAST so it can override anything above.
-- The file is deliberately NOT tracked in dotfiles and NOT managed by chezmoi:
-- it is the escape hatch for one-off hardware hacks that must not reach other hosts.
local require_optional = require("default.hypr.require_optional")
require_optional.module("hypr.local")
```

**n11a — module resolution, corrected.** `bootstrap.lua` builds `package.path` as
`~/.local/state/?.lua` **first**, then `~/.config/?.lua`, then `$OMARCHY_PATH/?.lua`. So
`hypr.local` resolves to `~/.local/state/hypr/local.lua` if that exists, and only otherwise
to the documented escape hatch `~/.config/hypr/local.lua`. v2 said `package.path` is
"rooted at `~/.config`", which was incomplete. The documented location stays
`~/.config/hypr/local.lua`, and `bin/dotfiles-drift` gains one check: warn if
`~/.local/state/hypr/local.lua` exists, because it would silently shadow the escape hatch.

**n11b — keeping the tracked `hyprland.lua` from going stale.** Tracking a full copy of a
file that is otherwise pristine means an upstream change to it is invisible: the pristine
guard cannot flag it (it is deliberately non-identical) and nothing else compares them.
Fix — `bin/dotfiles-drift` adds:

```bash
# The tracked hyprland.lua is the shipped file plus exactly the 5-line override
# block above (4 code/comment lines + 1 blank). Compare everything above that
# block to the shipped file so an upstream change is still detected.
HL_TRACKED="$REPO/home/dot_config/hypr/hyprland.lua"
HL_SHIPPED="/usr/share/omarchy/config/hypr/hyprland.lua"
if [[ -f $HL_TRACKED && -f $HL_SHIPPED ]]; then
  diff -q <(head -n -5 "$HL_TRACKED") "$HL_SHIPPED" >/dev/null \
    || note "hyprland.lua: upstream changed. Re-apply the override block onto the new
             shipped file: cp $HL_SHIPPED $HL_TRACKED && <re-append the 5-line block>"
fi
```

The override block's line count is asserted by a `structure` CI check so the `head -n -5`
cannot silently drift out of step with the block.

### Hardware conditionals beyond monitors

Same data file: `gpu = "nvidia"` gates
`{{ if eq $m.gpu "nvidia" }}require("default.hypr.nvidia"){{ end }}`; `profile = "work"`
gates work-only autostart entries. Adding a machine is one new `[machines.<hostname>]`
table plus `chezmoi apply`.

### Onboarding a second machine

```bash
git clone <repo> ~/dotfiles && ~/dotfiles/bin/dotfiles-bootstrap
# renders the `default` profile; every output auto-detected; display works. Then:
hyprctl monitors all
$EDITOR ~/dotfiles/home/.chezmoidata/machines.toml     # add [machines.<host>]
chezmoi apply && hyprctl reload
```

---

## 6. Decision 6 — Secrets

*(Unchanged from v2.)*

### What NEVER enters the repo

| Never committed | Why |
|---|---|
| `~/.config/chezmoi/key.txt` (the age **private** key) | Holding it plus the repo's blobs recovers every secret |
| `~/.config/chezmoi/chezmoi.toml` | Per-machine paths; names the identity file. (m8: no leading dot; `.chezmoi.toml.tmpl` is a different, source-state thing.) |
| Any plaintext API key, token, password, cookie, session JWT | — |
| `~/.dtx-providers/*` except the `.age` blob | `litellm-config.yaml` embeds a real upstream key; `proxy.env` holds a generated token |
| `.vscode/settings.json` in plaintext | Holds the GLM-5.3-Flash `apiKey` |
| `~/.claude/{.credentials.json,history.jsonl,sessions/,projects/,jobs/,shell-snapshots/}` | Live credentials and transcripts |
| `~/.gemini/state.json`, `~/.codex/*.sqlite*`, `~/.copilot/session-store.db*`, `~/.copilot/config.json` | Same, per harness |
| `~/Work/**`, including `~/Work/CLAUDE.md` | Employer content |
| `~/.config/opencode/opencode.json` until reviewed | Diverged and holds provider wiring |
| SSH/GPG private keys, `~/.netrc`, `~/.config/gh/hosts.yml` | — |
| Any file byte-identical to an Omarchy default | Same hard never-track class (§2) |

`.gitignore` additions: `home/**/*.env` (unless `.age`), `home/**/key.txt`,
`os/**/secrets*`, and **`chezmoi.toml`**.

### How secrets are injected

```
home/.chezmoitemplates/secrets.json.age     # age-encrypted, committed
```

```go-template
{{/* home/private_dot_dtx-providers/private_secrets.env.tmpl */ -}}
{{- $s := include ".chezmoitemplates/secrets.json.age" | decrypt | fromJson -}}
DTX_GLM53_FLASH_API_KEY={{ $s.glm53FlashApiKey }}
LITELLM_MASTER_KEY={{ $s.litellmMasterKey }}
```

```go-template
{{/* home/dot_vscode/settings.json.tmpl */ -}}
{{- $s := include ".chezmoitemplates/secrets.json.age" | decrypt | fromJson -}}
{ "…apiKey": "{{ $s.glm53FlashApiKey }}" }
```

Rotation is one edit for all consumers. **Day-1 acceptance test before anything depends on
it:** `chezmoi execute-template < home/dot_vscode/settings.json.tmpl | jq -e .`. If it
fails, fall back to the form already running in this repo — one `encrypted_<file>.age` per
destination — accepting N re-encryptions per rotation instead of 1.

**Rejected:** 1Password `op inject` (all-or-nothing failure, ~1s latency, 1000 req/24h,
one invocation per destination); `pass` (retrieval only); plain `.env` + `.gitignore`.

**Key backup is a hard bootstrap gate.** `CLAUDE.md:36` lists it as "Manual, pending" — the
largest unmitigated risk today. Bootstrap refuses to continue past the secrets step without
the key. This is action item #1 of §12.3.

### Exit plan (backing out of chezmoi+age)

1. `age -d -i ~/.config/chezmoi/key.txt home/.chezmoitemplates/secrets.json.age > /dev/shm/s.json`
2. Re-encrypt with sops (age backend, same key), git-crypt, or a password manager.
3. Replace the `.tmpl` consumers; destinations unchanged.
4. Rotate every value afterwards regardless.

---

## 7. Decision 7 — Write permissions

### The rule

- **L0 Autonomous** — edit the repo *and* apply.
- **L1 Propose only** — edit the repo, commit to `claude/*`, open a PR. **Must not apply.**
- **L2 Human only** — refuse and say why.

### The matrix

| Path / action | Level | Edit repo? | Apply to machine? | Note |
|---|---|---|---|---|
| `.agents/skills/**`, `.agents/prompts/**`, `.agents/workflows/**` | **L0** | Yes | Yes (`./sync.sh`) | Additive; a bad skill is ignored, not fatal |
| `.agents/instructions/**`, `.agents/agentsmd/**`, `.agents/harnesses/**`, `.agents/rules/**`, `.agents/validation/**`, `.agents/automation/**` (except `standards/`) | **L0** | Yes | Yes | Feeds AGENTS.md §1–§6; CI enforces invariance |
| `docs/**`, `README.md`, `CHEATSHEET.md`, `CLAUDE.md`, `GEMINI.md`, `AGENTS.local.md`, `global/**` | **L0** | Yes | n/a | Documentation |
| `tasks/**` via `append_event.py` (append only) | **L0** | Yes | n/a | Never hand-edit `board.md` |
| `./sync.sh --dry-run`, `chezmoi diff`, `bin/dotfiles-drift`, `dotfiles-plugins verify\|status`, `agentsmd-render --check` | **L0** | — | Read-only | Always allowed, including unattended |
| `home/**` (incl. `.chezmoidata/machines.toml`) | **L1** | Yes | **No** | A bad `monitors.lua` costs a display |
| `os/**` (`plugins.lock.json`, `plugins-src/**`, `packages/**`, `systemd/**`) | **L1** | Yes | **No** | A pin change installs third-party code |
| `setup.sh`, `sync.sh`, `bin/**`, `scripts/**`, `mise.toml` | **L1** | Yes | **No** | These *are* the apply mechanism |
| `.github/**`, `.githooks/**`, `.gitignore` | **L1** | Yes | **No** | These are the security controls |
| `.agents/instructions/workspace-config/standards/**` | **L1** | Yes | **No** | Binds every repo in the workspace |
| `.agents/providers/**`, `.agents/AGENT.md`, `.agents/CONTRIBUTING.md` (n5) | **L1** | Yes | **No** | Provider adapters carry endpoint wiring |
| `AGENTS.md` (the rendered file) | **L1** | Only via `.agents/agentsmd/` | **No** | Direct edits fail the `agents-md` CI job |
| **`.agents/policy/**`** | **L2** | **No** | **No** | M12 |
| `home/.chezmoitemplates/*.age`, any `*.age`, `.chezmoisource/**` | **L2** | **No** | **No** | Agent never handles plaintext secrets |
| `.git/**` (n5) | **L2** | **No** | **No** | Direct object/ref manipulation |
| `~/.config/chezmoi/**`, any private key | **L2** | **No** | **No** | Refuse and explain |
| `~/.claude/.credentials.json`, `~/.gemini/state.json`, `~/.codex/*.sqlite`, `~/.copilot/session-store.db` | **L2** | **No** | **No** | Live credentials/state |
| `~/Work/**`; running `bin/dotfiles-clone-repos` | **L2** | **No** | **No** | Employer content |
| Anything under `/usr/` | **L2** | **No** | **No** | pacman-owned |
| `omarchy-plugin-add/-remove`, `pacman -R`, `rm -rf` outside `/tmp` | **L2** | — | **No** | N10: a first plugin install runs unsandboxed upstream code |
| `git push --force`, push to `main`, `git push --no-verify` | **L2** | — | **No** | — |
| `rm ~/.local/state/dtx-sync/manifest.json` | **L2** | — | **No** | Destroys the sync baseline |
| `./sync.sh --system` | **L2** | — | **No** | Deprecated; warns and exits without writing |

### Closing the self-amendment hole — three locks

1. **Classification.** `.agents/policy/**` is **L2**.
2. **The gate reads a merged ref.** `git show origin/main:.agents/policy/write-policy.yaml`
   — an unmerged edit cannot take effect.
3. **No distributed copy.** `sync.sh` skips `policy/` (§0.1); `undo_legacy_dir_symlink`
   excludes it (n10); and the state-dir fallback is now populated **from `origin/main`**,
   not the working tree (n10, bootstrap step 10).

### `write-policy.yaml` — complete coverage (n5)

```yaml
version: 3
# n5: an explicit catch-all first, so the coverage assertion can never fail on a
# path nobody thought of. Last-match-wins, so everything below narrows it.
default: L1
rules:
  - { glob: "**",                       level: L1 }   # catch-all
  # ---- L0: autonomous (edit + apply) ----
  - { glob: ".agents/skills/**",         level: L0 }
  - { glob: ".agents/prompts/**",        level: L0 }
  - { glob: ".agents/workflows/**",      level: L0 }
  - { glob: ".agents/agentsmd/**",       level: L0 }
  - { glob: ".agents/harnesses/**",      level: L0 }
  - { glob: ".agents/rules/**",          level: L0 }
  - { glob: ".agents/validation/**",     level: L0 }
  - { glob: ".agents/automation/**",     level: L0 }
  - { glob: ".agents/instructions/**",   level: L0 }
  - { glob: "docs/**",                   level: L0 }
  - { glob: "tasks/**",                  level: L0 }
  - { glob: "global/**",                 level: L0 }
  - { glob: "README.md",                 level: L0 }
  - { glob: "CHEATSHEET.md",             level: L0 }
  - { glob: "CLAUDE.md",                 level: L0 }
  - { glob: "GEMINI.md",                 level: L0 }
  - { glob: "AGENTS.local.md",           level: L0 }
  # ---- L1: propose only ----
  - { glob: ".agents",                   level: L1 }   # n5: the directory itself
  - { glob: ".agents/AGENT.md",          level: L1 }   # n5
  - { glob: ".agents/CONTRIBUTING.md",   level: L1 }   # n5
  - { glob: ".agents/providers/**",      level: L1 }   # n5
  - { glob: ".agents/instructions/workspace-config/standards/**", level: L1 }
  - { glob: "home/**",                   level: L1 }
  - { glob: "os/**",                     level: L1 }
  - { glob: "bin/**",                    level: L1 }
  - { glob: "scripts/**",                level: L1 }
  - { glob: "setup.sh",                  level: L1 }
  - { glob: "sync.sh",                   level: L1 }
  - { glob: "test-subagents.sh",         level: L1 }
  - { glob: "mise.toml",                 level: L1 }
  - { glob: "AGENTS.md",                 level: L1 }
  - { glob: ".github/**",                level: L1 }
  - { glob: ".githooks/**",              level: L1 }
  - { glob: ".gitignore",                level: L1 }
  - { glob: ".vscode/**",                level: L1 }
  - { glob: ".claude/**",                level: L1 }
  - { glob: ".gemini/**",                level: L1 }
  - { glob: ".codex/**",                 level: L1 }
  - { glob: ".copilot/**",               level: L1 }
  - { glob: ".cursor/**",                level: L1 }
  # ---- L2: human only (most specific; last match wins) ----
  - { glob: ".git/**",                   level: L2 }   # n5
  - { glob: ".agents/policy/**",         level: L2 }
  - { glob: ".chezmoisource/**",         level: L2 }
  - { glob: "**/*.age",                  level: L2 }
  - { glob: "/usr/**",                   level: L2 }
  - { glob: "~/Work/**",                 level: L2 }
  - { glob: "~/.config/chezmoi/**",      level: L2 }
  - { glob: "~/.claude/.credentials.json", level: L2 }
  - { glob: "~/.claude/sessions/**",     level: L2 }
  - { glob: "~/.claude/projects/**",     level: L2 }
  - { glob: "~/.claude/jobs/**",         level: L2 }
  - { glob: "~/.claude/shell-snapshots/**", level: L2 }
  - { glob: "~/.gemini/state.json",      level: L2 }
  - { glob: "~/.codex/*.sqlite*",        level: L2 }
  - { glob: "~/.copilot/session-store.db*", level: L2 }
forbidden_commands:
  - "*git push*--force*"
  - "*git push*--no-verify*"
  - "*omarchy-plugin-remove*"
  - "*omarchy-plugin-add*"
  - "*pacman -R*"
  - "*sync.sh --system*"
  - "*dotfiles-clone-repos*"
# N7: these APPLY the repo to the machine. Denied while the working tree holds
# uncommitted changes to any L1 or L2 path.
apply_commands:
  - "*sync.sh*"
  - "*chezmoi apply*"
  - "*dotfiles-plugins sync*"
  - "*dotfiles-bootstrap*"
  - "*systemctl --user enable*"
# N7: Bash commands whose first file-ish argument should be path-classified.
bash_write_patterns:
  - "sed -i"
  - "tee"
  - "install "
  - "patch "
  - "truncate "
  - "dd of="
```

### `.agents/policy/write-policy-gate.sh` (N6, N7, n6 fixed)

```bash
#!/usr/bin/env bash
# Claude Code PreToolUse gate.
# Contract: hook event JSON on stdin; decision JSON on stdout; exit 0 to allow,
# exit 2 to block. Policy source: `git show origin/main:.agents/policy/write-policy.yaml`,
# falling back to a state-dir copy that bootstrap also seeds from origin/main.
# Fails CLOSED (everything L2) if neither is readable.
set -uo pipefail
REPO="${DOTFILES_REPO:-$HOME/dotfiles}"
POLICY_REF="${WRITE_POLICY_REF:-origin/main}"
POLICY_PATH=".agents/policy/write-policy.yaml"

policy() {
  git -C "$REPO" show "$POLICY_REF:$POLICY_PATH" 2>/dev/null \
    || cat "$HOME/.local/state/dtx-policy/write-policy.yaml" 2>/dev/null \
    || printf 'version: 3\ndefault: L2\nrules: []\n'
}

# N6: the shape Claude Code actually recognises, matching this machine's own
# existing hook envelope. v2 emitted {"decision":"deny"} + exit 0, which fails open.
emit() {  # $1=allow|deny|ask  $2=reason
  jq -nc --arg d "$1" --arg r "$2" \
    '{hookSpecificOutput:{hookEventName:"PreToolUse",permissionDecision:$d,permissionDecisionReason:$r}}'
}
deny(){ emit deny "$1"; exit 2; }          # exit 2 blocks even if JSON is ignored
warn(){ emit allow "$1"; exit 0; }
allow(){ emit allow ""; exit 0; }

# n6: ANCHORED glob->regex. v2's unanchored test() made README.md match
# docs/README.mdx and home/** match x/home/y.
glob_re() {
  local g="$1"
  g="${g/#\~\//$HOME/}"
  g=$(printf '%s' "$g" | sed -e 's/[.[\()+^$|]/\\&/g')   # escape regex metachars
  g="${g//\*\*\//<<GLOBSTARSLASH>>}"
  g="${g//\*\*/<<GLOBSTAR>>}"
  g="${g//\*/[^\/]*}"
  g="${g//<<GLOBSTARSLASH>>/(.*\/)?}"
  g="${g//<<GLOBSTAR>>/.*}"
  printf '^%s$' "$g"
}

classify() {  # $1 = path (abs or repo-relative) -> L0|L1|L2
  local abs rel lvl="" P="$2"
  abs="$1"; [[ $abs == /* ]] || abs="$PWD/$1"
  rel="${abs#"$REPO"/}"
  while IFS=$'\t' read -r glob level; do
    [[ -n $glob ]] || continue
    local re; re=$(glob_re "$glob")
    if [[ $rel =~ $re || $abs =~ $re ]]; then lvl="$level"; fi   # last match wins
  done < <(yq -r '.rules[] | [.glob, .level] | @tsv' <<<"$P")
  printf '%s' "${lvl:-$(yq -r '.default // "L1"' <<<"$P")}"
}

# N7: does the working tree hold uncommitted L1/L2 changes? If so, an apply is
# exactly the thing L1 forbids.
dirty_above_l0() {
  local P="$1" f lvl
  while read -r f; do
    [[ -n $f ]] || continue
    lvl=$(classify "$REPO/$f" "$P")
    [[ $lvl == L0 ]] || { printf '%s (%s)' "$f" "$lvl"; return 0; }
  done < <(git -C "$REPO" status --porcelain --untracked-files=all 2>/dev/null | cut -c4-)
  return 1
}

# N7: best-effort path extraction from a Bash command line.
bash_target_paths() {  # $1=cmd $2=policy -> newline-separated candidate paths
  local cmd="$1" P="$2"
  grep -oE '>>?[[:space:]]*[^[:space:];|&<>]+' <<<"$cmd" | sed -E 's/^>>?[[:space:]]*//'
  while read -r pat; do
    [[ -n $pat ]] || continue
    grep -oE "${pat//\//\\/}[[:space:]]+[^[:space:];|&]+" <<<"$cmd" \
      | sed -E "s|^${pat}[[:space:]]+||"
  done < <(yq -r '.bash_write_patterns[]?' <<<"$P")
  grep -oE '\b(cp|mv)[[:space:]]+[^[:space:];|&]+[[:space:]]+[^[:space:];|&]+' <<<"$cmd" \
    | awk '{print $NF}'
}

ev=$(cat); tool=$(jq -r '.tool_name // ""' <<<"$ev"); P=$(policy)

case "$tool" in
  Bash)
    cmd=$(jq -r '.tool_input.command // ""' <<<"$ev")
    while read -r pat; do
      [[ -n $pat ]] || continue
      # shellcheck disable=SC2053
      [[ $cmd == $pat ]] && deny "Forbidden by write-policy@$POLICY_REF (matches '$pat'). L2 — human only."
    done < <(yq -r '.forbidden_commands[]?' <<<"$P")

    # N7a: applying the repo to the machine while L1/L2 edits are pending.
    while read -r pat; do
      [[ -n $pat ]] || continue
      # shellcheck disable=SC2053
      if [[ $cmd == $pat ]]; then
        if d=$(dirty_above_l0 "$P"); then
          deny "This applies the repo to the live machine, but the working tree has
          uncommitted non-L0 changes: $d. L1 means propose, not apply — commit them
          to a claude/* branch and let a human merge and run this."
        fi
      fi
    done < <(yq -r '.apply_commands[]?' <<<"$P")

    # N7b: Bash-mediated writes (sed -i, tee, cat >, cp/mv, install, patch).
    while read -r f; do
      [[ -n $f ]] || continue
      case "$(classify "$f" "$P")" in
        L2) deny "$f is L2 (human only) per write-policy@$POLICY_REF. Writing it via Bash does not change that." ;;
        L1) warn "$f is L1: you may edit it and open a PR, but must NOT apply the change to the live machine." ;;
      esac
    done < <(bash_target_paths "$cmd" "$P")
    allow ;;

  Write|Edit|MultiEdit|NotebookEdit)
    f=$(jq -r '.tool_input.file_path // .tool_input.notebook_path // ""' <<<"$ev")
    [[ -n $f ]] || allow
    case "$(classify "$f" "$P")" in
      L2) deny "${f#"$REPO"/} is L2 (human only) per write-policy@$POLICY_REF. Explain why the change is needed and let the owner make it." ;;
      L1) warn "${f#"$REPO"/} is L1: you may edit and open a PR, but you must NOT apply this to the live machine (no chezmoi apply / sync.sh / dotfiles-bootstrap for this change)." ;;
      *)  allow ;;
    esac ;;
  *) allow ;;
esac
```

**N7 — stated residual gap.** Path extraction from a shell command line is best-effort. A
heredoc that writes a file, a path built from a variable, a `find -exec`, or a program that
writes as a side effect can still slip past the Bash branch. The guarantee is therefore:
**L2 paths are blocked for every first-party edit tool and for the common Bash write
idioms; the policy is a strong control, not a sandbox.** This is recorded in §12.2 as a
residual risk rather than claimed closed.

### Validator checks

`scripts/validate_dotfiles.sh` gains: every top-level repo path matches at least one glob
(trivially true now via the `**` catch-all, but the check also asserts each path's
*resolved* level is the intended one via a small fixture table); no L0 rule appears after
an L2 rule covering a subset of its paths; every `forbidden_commands`/`apply_commands`
entry is a valid bash glob; the `hyprland.lua` override block is exactly 5 lines (n11b).

---

## 8. Annotated repo tree

```
~/dotfiles/
├── AGENTS.md                    # RENDERED (§1-6 generated, §7-9 from AGENTS.local.md)
├── AGENTS.local.md              # NEW. This repo's own §7-§9.
├── CLAUDE.md  GEMINI.md  README.md  CHEATSHEET.md    # EXISTING
├── setup.sh                     # MODIFIED (§0.1): +--links-only; setup_agent_symlinks()
│                                #   and its 3 call sites deleted; +undo_legacy_dir_symlink();
│                                #   +.cursor pointer file
├── sync.sh                      # MODIFIED (§0.1): one 7-line skip for policy/. Core untouched.
├── mise.toml                    # NEW. Task runner only: bootstrap|sync|drift|adopt|
│                                #   plugins:*|agentsmd|validate
│
├── bin/                         # NEW
│   ├── dotfiles-bootstrap       #   clone -> machine ready, idempotent (§9)
│   ├── dotfiles-adopt           #   machine -> repo; diff first; never commits (§10)
│   ├── dotfiles-drift           #   report only. exit 0 clean / 10 findings / 1 error
│   ├── dotfiles-plugins         #   sync|verify|adopt|status (§2)
│   ├── agentsmd-render          #   render|pointers|--check (§4)
│   ├── dotfiles-discovery-check #   DISCOVERY.md row targets exist
│   └── dotfiles-clone-repos     #   thin wrapper: setup.sh WITHOUT --links-only. L2.
│
├── home/                        # NEW. chezmoi source. destDir=$HOME, workingTree=$REPO
│   ├── .chezmoidata/machines.toml       # valid TOML (N2); includes a `default` profile
│   ├── .chezmoitemplates/secrets.json.age
│   ├── dot_config/
│   │   ├── hypr/{monitors.lua.tmpl,looknfeel.lua,hyprland.lua}
│   │   │                        #   ONLY these 3. NOT tracked (pristine, verified):
│   │   │                        #   .luarc.json autostart.lua bindings.lua
│   │   │                        #   hyprsunset.conf input.lua xdph.conf
│   │   ├── alacritty/alacritty.toml  foot/foot.ini  ghostty/config  kitty/kitty.conf
│   │   ├── git/config
│   │   └── omarchy/{private_shell.json,private_shell.toml}   # both 0600 (n9)
│   │                            #   NOT here: omarchy/{themes,plugins,defaults,hooks}/
│   ├── dot_vscode/settings.json.tmpl
│   └── private_dot_dtx-providers/private_secrets.env.tmpl
│
├── os/                          # NEW
│   ├── omarchy/
│   │   ├── plugins.lock.json    #   keyed on manifest id (§2)
│   │   ├── plugins-src/<id>/    #   owner-authored plugins; must contain no symlink
│   │   ├── tracked-files.txt    #   adopt's allowlist. Population rule in §10. (n7)
│   │   └── .target-version      #   compared against `pacman -Q omarchy` (m1)
│   ├── packages/{pacman.txt,aur.txt}
│   └── systemd/                 #   N8: ALL FOUR units are committed here —
│       ├── dotfiles-sync.service      dotfiles-sync.timer
│       └── dotfiles-drift.service     dotfiles-drift.timer
│
├── .agents/
│   ├── skills/ instructions/ harnesses/ prompts/ workflows/ validation/ automation/ rules/ providers/
│   ├── agentsmd/                #   NEW (§4): §1-6 sources + manifest.yaml + the .py renderer
│   ├── harnesses/DISCOVERY.md   #   NEW. harness -> file it reads -> verified date
│   ├── harnesses/POLICY.md      #   NEW (N11). A pointer only, no rules. Distributable.
│   └── policy/                  #   NEW. L2. NEVER distributed (sync.sh skips it)
│       ├── README.md  write-policy.yaml  write-policy-gate.sh
│
├── .claude/CLAUDE.md  .gemini/GEMINI.md  .codex/AGENTS.md
├── .copilot/copilot-instructions.md   .cursor/rules/workspace.mdc
│                                # all five carry an AGENTSMD:PREFIX BEGIN/END region
├── .github/{copilot-instructions.md,workflows/{vscode-docs-monitor.yml,dotfiles-ci.yml}}
├── .githooks/pre-push
├── global/{ROOT,PROJECTS}.CLAUDE.md, WORK.CLAUDE.template.md, REPO.AGENTS.local.template.md
├── docs/{OS.md,SECRETS.md,STANDARDS.md,AUDIT_REPORT.md,SUBAGENTS_VERIFICATION.md,…}
├── scripts/{validate_dotfiles.sh,validate_workspace_standards.py,…}
└── tasks/                       # EXISTING SEPARATE initiative. Untouched.
```

---

## 9. Bootstrap: `bin/dotfiles-bootstrap`

Contract: **every step is guard + action. On a machine already in the target state it
prints only `ok:` lines, exits 0, mutates nothing, and performs no network I/O.**

```bash
#!/usr/bin/env bash
set -euo pipefail
REPO="${DOTFILES_REPO:-$HOME/dotfiles}"
DRY=0; [[ ${1:-} == --dry-run ]] && DRY=1
run(){ (( DRY )) && { echo "(dry) $*"; return 0; }; "$@"; }
ok(){ echo "ok:   $*"; }
step(){ echo; echo "== $* =="; }
die(){ echo "FATAL: $*" >&2; exit 1; }

# --- 1. Preflight -------------------------------------------------------------
step "preflight"
[[ -f /etc/arch-release ]] || die "not Arch"
command -v omarchy-plugin-validate >/dev/null || die "Omarchy not installed"
OMV=$(pacman -Q omarchy | awk '{print $2}')          # m1
TGT=$(cat "$REPO/os/omarchy/.target-version" 2>/dev/null || echo "$OMV")
echo "omarchy: installed=$OMV  repo-target=$TGT"
[[ $OMV == "$TGT" ]] || echo "WARN: version skew — expect drift findings (docs/OS.md)"
[[ -d $REPO/.git ]] || die "clone the repo to $REPO first"
ok "preflight"

# --- 2. Dependencies ----------------------------------------------------------
step "dependencies"
DEPS=(chezmoi age jq yq rsync git gum mise python-yaml)
missing=(); for p in "${DEPS[@]}"; do pacman -Qq "$p" &>/dev/null || missing+=("$p"); done
if (( ${#missing[@]} )); then run sudo pacman -S --needed --noconfirm "${missing[@]}"
else ok "all deps present"; fi

# --- 3. Secrets gate: HARD STOP ------------------------------------------------
step "secrets"
KEY="$HOME/.config/chezmoi/key.txt"
if [[ ! -f $KEY ]]; then
  cat >&2 <<EOF
FATAL: age private key not found at $KEY

  Deliberately never in the repo. Restore it out-of-band:
    1. password manager -> secure note "dotfiles age key" -> save to $KEY
    2. chmod 600 $KEY
    3. re-run this script
  Full procedure: $REPO/docs/SECRETS.md
EOF
  exit 1
fi
[[ $(stat -c '%a' "$KEY") == 600 ]] || run chmod 600 "$KEY"
ok "age key present"

# --- 4. chezmoi config ---------------------------------------------------------
step "chezmoi config"
CFG="$HOME/.config/chezmoi/chezmoi.toml"
WANT=$(cat <<EOF
sourceDir   = "$REPO/home"
destDir     = "$HOME"
workingTree = "$REPO"
encryption  = "age"

[age]
    identity  = "$KEY"
    recipient = "age1vp83ej2dzlchh6g5fu5nqvkrzy874e8m84x807dtv2vukf5df39sa7c43w"
EOF
)
if [[ -f $CFG ]] && diff -q <(printf '%s\n' "$WANT") "$CFG" >/dev/null; then
  ok "chezmoi.toml already correct"
else
  run mkdir -p "$(dirname "$CFG")"
  (( DRY )) && echo "(dry) would write $CFG" || printf '%s\n' "$WANT" >"$CFG"
fi

# --- 5. Machine known? ---------------------------------------------------------
step "machine data"
HOST=$(hostname)
set +e; DATA=$(chezmoi data 2>&1); rc=$?; set -e
(( rc == 0 )) || { echo "$DATA" >&2; die "chezmoi data failed — bad sourceDir, invalid
  .chezmoidata TOML (N2), a template error, or a bad age identity"; }
if jq -e --arg h "$HOST" '.machines[$h]' <<<"$DATA" >/dev/null 2>&1; then
  ok "machines.toml has an entry for '$HOST'"
else
  jq -e '.machines.default' <<<"$DATA" >/dev/null 2>&1 \
    || die "no [machines.$HOST] AND no [machines.default] — a new machine would render no monitor"
  echo "WARN: no [machines.$HOST] — rendering the 'default' profile (outputs auto-detected)."
  echo "      After first login: hyprctl monitors all, add a table, chezmoi apply."
fi

# --- 5b. Legacy symlink migration + per-tool file symlinks (N1: ONE call) -------
# `--links-only` runs undo_legacy_dir_symlink for agents/vscode/dtx-providers and
# then the five per-tool file symlinks. It clones NO repositories (m2).
step "links and legacy migration"
run "$REPO/setup.sh" --links-only $( ((DRY)) && echo --dry-run )

# --- 6. Apply $HOME config (M3) ------------------------------------------------
step "chezmoi apply"
set +e; DIFF=$(chezmoi diff 2>/tmp/cz.err); rc=$?; set -e
if (( rc != 0 )); then
  cat /tmp/cz.err >&2
  die "chezmoi diff failed (rc=$rc). NOT proceeding: this step renders monitors.lua
       and both secret destinations."
fi
if [[ -z $DIFF ]]; then ok "\$HOME already in sync"
else
  run chezmoi apply
  (( DRY )) || [[ -z "$(chezmoi diff)" ]] || die "chezmoi apply did not converge; run 'chezmoi diff'"
fi

# --- 7. Agent content ----------------------------------------------------------
step "agents"
run "$REPO/sync.sh" $( ((DRY)) && echo --dry-run )
run "$REPO/bin/agentsmd-render" --check "$REPO" \
  || die "AGENTS.md or a pointer file is stale — run: mise run agentsmd"
echo "note: ~/Work and ~/Projects repos are NOT cloned here. Run bin/dotfiles-clone-repos"
echo "      yourself when you want them (L2 — employer content)."

# --- 8. Omarchy plugins --------------------------------------------------------
step "plugins"
set +e; run "$REPO/bin/dotfiles-plugins" $( ((DRY)) && echo verify || echo sync ); rc=$?; set -e
case $rc in
  0)  ok "plugins in sync" ;;
  10) echo "WARN: plugin findings above. A NEEDS-REVIEW line means a first install would"
      echo "      run upstream HEAD unsandboxed before the pin applies — review, then set"
      echo "      DOTFILES_PLUGINS_ALLOW_FIRST_INSTALL=1 (N10)." ;;
  *)  die "dotfiles-plugins failed (rc=$rc)" ;;
esac

# --- 9. Packages: REPORT ONLY --------------------------------------------------
step "packages"
comm -23 <(sort "$REPO/os/packages/pacman.txt") <(pacman -Qqet | sort) >/tmp/pkg-missing || true
if [[ -s /tmp/pkg-missing ]]; then
  echo "Declared but not installed ($(wc -l </tmp/pkg-missing)). Review, then:"
  echo "  sudo pacman -S --needed \$(tr '\n' ' ' </tmp/pkg-missing)"
else ok "package set matches"; fi

# --- 10. Hooks, timers, policy gate (N6, N8, n10) ------------------------------
step "hooks, timers, policy gate"
[[ $(git -C "$REPO" config --get core.hooksPath || true) == .githooks ]] \
  && ok "pre-push hook wired" || run git -C "$REPO" config core.hooksPath .githooks

# N8: all four units ship in the repo now, so a fresh machine has a source.
# A missing source is a WARNING, never a die — timers are not required for
# "machine ready".
for u in dotfiles-sync dotfiles-drift; do
  for ext in service timer; do
    unit="$HOME/.config/systemd/user/$u.$ext"; src="$REPO/os/systemd/$u.$ext"
    if [[ -f $unit ]] && { [[ ! -f $src ]] || cmp -s "$src" "$unit"; }; then ok "$u.$ext current"
    elif [[ -f $src ]]; then run install -Dm644 "$src" "$unit"
    else echo "WARN: no unit source $src and none installed — skipping $u.$ext"; continue; fi
  done
  if [[ -f "$HOME/.config/systemd/user/$u.timer" ]]; then
    systemctl --user is-enabled "$u.timer" &>/dev/null && ok "$u.timer enabled" \
      || { run systemctl --user daemon-reload; run systemctl --user enable --now "$u.timer" \
           || echo "WARN: could not enable $u.timer"; }
  fi
done

# N6: install the gate AND register it. Dropping a script in hooks/ does nothing.
GATE_SRC="$REPO/.agents/policy/write-policy-gate.sh"
GATE="$HOME/.claude/hooks/write-policy-gate.sh"
[[ -f $GATE_SRC ]] || die "missing $GATE_SRC — the write-policy gate is a required deliverable"
if [[ -f $GATE ]] && cmp -s "$GATE_SRC" "$GATE"; then ok "write-policy gate current"
else run install -Dm755 "$GATE_SRC" "$GATE"; fi

SETTINGS="$HOME/.claude/settings.json"
CMD="bash '$GATE'"
if [[ -f $SETTINGS ]] && jq -e --arg c "$CMD" \
     '[.hooks.PreToolUse[]?.hooks[]?.command] | index($c)' "$SETTINGS" >/dev/null 2>&1; then
  ok "write-policy gate registered in settings.json"
else
  (( DRY )) && echo "(dry) would register the gate in $SETTINGS" || {
    [[ -f $SETTINGS ]] || echo '{}' >"$SETTINGS"
    tmp=$(mktemp)
    jq --arg c "$CMD" '
      .hooks //= {} | .hooks.PreToolUse //= [] |
      .hooks.PreToolUse |= (
        if any(.[]; .matcher == "*") then
          map(if .matcher == "*"
              then .hooks += [{type:"command", command:$c, timeout:10}]
              else . end)
        else . + [{matcher:"*", hooks:[{type:"command", command:$c, timeout:10}]}]
        end)' "$SETTINGS" >"$tmp" && mv "$tmp" "$SETTINGS"
    echo "registered write-policy gate in $SETTINGS"
  }
fi

# n10: seed the fallback from origin/main, NOT the working tree, and only if the
# ref exists. (v2's "fresh clone has no origin/main" rationale was simply wrong —
# git clone creates it — and seeding from the working tree defeated lock 2.)
if git -C "$REPO" rev-parse --verify --quiet origin/main >/dev/null; then
  (( DRY )) && echo "(dry) would seed policy fallback from origin/main" || {
    mkdir -p "$HOME/.local/state/dtx-policy"
    git -C "$REPO" show origin/main:.agents/policy/write-policy.yaml \
      >"$HOME/.local/state/dtx-policy/write-policy.yaml"
  }
else
  echo "WARN: origin/main not found; the gate will fail CLOSED (everything L2) until it is."
fi

# --- 11. Verify ----------------------------------------------------------------
step "verify"
run "$REPO/scripts/validate_dotfiles.sh"
set +e; run "$REPO/bin/dotfiles-drift" --quiet; rc=$?; set -e
case $rc in
  0)  ok "no drift" ;;
  10) echo "NOTE: drift findings — expected on a new machine (packages, version skew)."
      echo "      Report: ~/.local/state/dtx-sync/drift-report.md" ;;
  *)  die "dotfiles-drift errored (rc=$rc)" ;;
esac
echo; echo "Machine ready. Re-running this script now is a no-op."
```

**Idempotence, per step:** 1 read-only · 2 precomputed missing set + `--needed` · 3
read-only after one `chmod` · 4 content-compare before write · 5 read-only · 5b
`undo_legacy_dir_symlink` returns immediately unless the path is a symlink, and
`setup_agent_file_symlink` skips already-correct links (`setup.sh:91,136,183`) · 6
`chezmoi diff` guard + post-apply convergence assertion · 7 `sync.sh` writes only when
hashes differ (`sync.sh:279-281`), `agentsmd-render --check` is read-only · 8
`check_installed` short-circuits and skips `git fetch` when the pin already matches (m4) ·
9 report-only · 10 `cmp` / `is-enabled` / `jq … index($c)` guards · 11 read-only.

---

## 10. Reverse sync: `bin/dotfiles-adopt`

**n7 — how `os/omarchy/tracked-files.txt` is populated and maintained.** It is the
human-curated allowlist of `$HOME`-relative paths that `dotfiles-adopt` section B is
permitted to offer for tracking. Rules:

1. **Initial content** = the 10 files in §0.2's tracked set, plus commented-out candidates
   found by the census but deliberately excluded, each with its reason inline:
   ```
   # $HOME-relative paths dotfiles-adopt may offer to track.
   # A line is added by `dotfiles-drift --suggest-tracking` (appended commented-out)
   # or by hand; a human uncomments it to opt in. Removing a line does NOT untrack
   # an already-managed file — use `chezmoi forget` for that.
   .config/hypr/monitors.lua
   .config/hypr/looknfeel.lua
   .config/hypr/hyprland.lua
   .config/alacritty/alacritty.toml
   .config/foot/foot.ini
   .config/ghostty/config
   .config/kitty/kitty.conf
   .config/git/config
   .config/omarchy/shell.json
   .config/omarchy/shell.toml
   # --- candidates, not yet decided ---
   # .config/herdr/config.toml        # tool state + provider wiring; needs secrets review
   # .config/opencode/opencode.json   # same
   # .config/omarchy/extensions/omarchy-menu.jsonc  # deferred one upgrade cycle
   # .config/nvim/                    # plugin-managed tree with its own lockfile
   # .config/mise/                    # machine-local tool installs
   ```
2. **New diverged files are discovered, not guessed:** `bin/dotfiles-drift
   --suggest-tracking` re-runs the §0.2 sweep, and for every file under `~/.config` that
   (a) has an upstream counterpart via `omarchy_default_for`, (b) differs from it, and
   (c) is not already listed or managed, appends a commented-out line with the date.
   Nothing is ever uncommented automatically.
3. **Owner-authored files** (no upstream counterpart) are invisible to the sweep by
   construction — §0.2 states this. They enter the list only by hand.

```bash
#!/usr/bin/env bash
# machine -> repo. Shows a diff for every change and asks. NEVER commits, NEVER pushes.
set -euo pipefail
REPO="${DOTFILES_REPO:-$HOME/dotfiles}"; ADOPTED=0; SKIPPED=0
confirm(){ gum confirm "$1"; }

omarchy_default_for(){ local rel="${1#./}" c d
  [[ $rel == .config/* ]] || return 1
  c="/usr/share/omarchy/config/${rel#.config/}";  [[ -f $c ]] && { echo "$c"; return 0; }
  d="/usr/share/omarchy/default/${rel#.config/}"; [[ -f $d ]] && { echo "$d"; return 0; }
  return 1; }

SKIP_BY_NAME=('.config/hypr/local.lua')          # the unmanaged escape hatch (§5c)

# -- A. chezmoi-managed files that drifted on the machine ----------------------
echo "== A. drift in managed files =="
while IFS= read -r f; do
  [[ -f $f ]] || continue
  rel=${f#"$HOME"/}; printf '%s\n' "${SKIP_BY_NAME[@]}" | grep -qxF "$rel" && continue
  chezmoi diff -- "$f" | head -200
  if confirm "adopt machine version of ~/$rel?"; then chezmoi re-add "$f"; ((ADOPTED++))
  else ((SKIPPED++)); fi
done < <(chezmoi managed --path-style absolute --include files \
         | while read -r p; do [[ -n "$(chezmoi diff -- "$p" 2>/dev/null)" ]] && echo "$p"; done)

# -- B. new candidates, with the corrected pristine guard ----------------------
echo "== B. new candidates =="
while IFS= read -r rel; do
  [[ -n $rel && ${rel:0:1} != '#' ]] || continue
  abs="$HOME/$rel"; [[ -f $abs ]] || continue
  chezmoi managed --path-style absolute | grep -qxF "$abs" && continue
  printf '%s\n' "${SKIP_BY_NAME[@]}" | grep -qxF "$rel" && continue
  if def=$(omarchy_default_for "$rel"); then
    if cmp -s "$abs" "$def"; then
      echo "  SKIP $rel — byte-identical to $def."
      echo "       Omarchy replaces such files by hash on upgrade; tracking it is a"
      echo "       guaranteed future conflict for zero benefit (docs/OS.md)."
      ((SKIPPED++)); continue
    fi
    echo "--- diff vs shipped default ($def) ---"; diff -u "$def" "$abs" | head -200
  else
    echo "  (no upstream default under config/ or default/ — owner-authored)"
  fi
  if confirm "start tracking $rel?"; then
    if grep -qiE '(api[_-]?key|secret|token|password|BEGIN [A-Z ]*PRIVATE KEY)' "$abs"; then
      echo "  !! looks like it contains a secret — adding ENCRYPTED"; chezmoi add --encrypt "$abs"
    else chezmoi add "$abs"; fi
    ((ADOPTED++))
  else ((SKIPPED++)); fi
done < "$REPO/os/omarchy/tracked-files.txt"

# -- C. agent content written at the destination -------------------------------
echo "== C. agent content =="
"$REPO/sync.sh" --pull --dry-run
confirm "run sync.sh --pull for real?" && "$REPO/sync.sh" --pull || ((SKIPPED++))

# -- D. plugins ----------------------------------------------------------------
echo "== D. plugins =="
"$REPO/bin/dotfiles-plugins" status || true
while read -r id; do [[ -n $id ]] || continue
  confirm "adopt plugin '$id' into the lockfile?" \
    && "$REPO/bin/dotfiles-plugins" adopt "$id" || ((SKIPPED++))
done < <("$REPO/bin/dotfiles-plugins" status 2>&1 | awk '/^UNTRACKED plugin installed: /{print $4}')

# -- E. packages ---------------------------------------------------------------
echo "== E. packages =="
diff -u <(sort "$REPO/os/packages/pacman.txt") <(pacman -Qqet | sort) || true
confirm "update os/packages/pacman.txt to match this machine?" \
  && pacman -Qqet | sort >"$REPO/os/packages/pacman.txt" || ((SKIPPED++))

# -- F. regenerate AGENTS.md + the pointer files if their sources moved --------
if ! "$REPO/bin/agentsmd-render" --check "$REPO" >/dev/null 2>&1; then
  echo "== F. AGENTS.md / pointer files are stale =="
  if confirm "re-render them?"; then
    "$REPO/bin/agentsmd-render" render   "$REPO" >"$REPO/AGENTS.md"
    "$REPO/bin/agentsmd-render" pointers "$REPO"
  fi
fi

cat <<EOF

adopted: $ADOPTED   skipped: $SKIPPED

Nothing has been committed. Review and commit yourself:
    cd $REPO && git status && git diff
    git switch -c claude/adopt-\$(date +%Y%m%d)
    git add -p && git commit && gh pr create
EOF
git -C "$REPO" status --short
```

---

## 11. CI and pre-push checks

### `.githooks/pre-push`

```bash
#!/usr/bin/env bash
set -euo pipefail
REPO=$(git rev-parse --show-toplevel); FAIL=0
bad(){ echo "BLOCKED: $*" >&2; FAIL=1; }

# n4: chezmoi source path -> $HOME-relative path (strips attribute prefixes/.tmpl).
chezmoi_source_to_rel() {
  local p="${1#home/}" out="" seg
  p="${p%.tmpl}"
  local IFS=/; for seg in $p; do
    seg="${seg#private_}"; seg="${seg#encrypted_}"; seg="${seg#readonly_}"
    seg="${seg#executable_}"; seg="${seg#symlink_}"; seg="${seg#exact_}"
    [[ $seg == dot_* ]] && seg=".${seg#dot_}"
    out="${out:+$out/}$seg"
  done
  echo "$out"
}

ZERO=0000000000000000000000000000000000000000
while read -r _ lsha _ rsha; do
  [[ $lsha == "$ZERO" ]] && continue
  RANGE=""; REVS=()
  if [[ $rsha == "$ZERO" ]]; then
    base=$(git merge-base "$lsha" origin/HEAD 2>/dev/null \
        || git merge-base "$lsha" origin/main 2>/dev/null || true)
    if [[ -n $base ]]; then RANGE="$base..$lsha"; else REVS=(--all --not --remotes); fi
  else RANGE="$rsha..$lsha"; fi

  if [[ -n $RANGE ]]; then DIFF=(git diff "$RANGE"); NAMES=(git diff --name-only "$RANGE")
  else DIFF=(git log -p "${REVS[@]}"); NAMES=(git log --name-only --pretty=format: "${REVS[@]}"); fi

  # 1. Known-shape secrets in added lines. .age blobs are binary and exempt.
  "${DIFF[@]}" -- . ':(exclude)*.age' | grep -E '^\+' | \
    grep -nEi 'AGE-SECRET-KEY-1|BEGIN [A-Z ]*PRIVATE KEY|sk-[A-Za-z0-9]{20,}|gh[pousr]_[A-Za-z0-9]{30,}|xox[baprs]-|AKIA[0-9A-Z]{16}|(api[_-]?key|secret|token|password)["'"'"' :=]+[A-Za-z0-9_\-]{16,}' \
    && bad "possible secret in ${RANGE:-unpushed commits}"

  # 2. gitleaks if available.
  command -v gitleaks >/dev/null && [[ -n $RANGE ]] && \
    { gitleaks detect --no-banner --redact --log-opts="$RANGE" || bad "gitleaks findings"; }

  # 3. Filenames that must never be tracked.
  "${NAMES[@]}" | sort -u | \
    grep -E '(^|/)(key\.txt|chezmoi\.toml|\.credentials\.json|secrets\.env|settings\.json)$|\.sqlite|session-store\.db' \
    | grep -v '\.age$' && bad "forbidden filename in ${RANGE:-unpushed commits}"
done

# 4. No tracked file is byte-identical to a shipped default — BOTH trees, and
#    n4: with chezmoi attribute prefixes stripped, so all 9 tracked files are checked.
if [[ -d /usr/share/omarchy ]]; then
  while IFS= read -r f; do
    rel=$(chezmoi_source_to_rel "$f")                 # e.g. .config/omarchy/shell.json
    sub="${rel#.config/}"
    for def in "/usr/share/omarchy/config/$sub" "/usr/share/omarchy/default/$sub"; do
      [[ -f $def ]] && cmp -s "$REPO/$f" "$def" \
        && { bad "$f is identical to $def — chezmoi forget it (docs/OS.md)"; break; }
    done
  done < <(git ls-files 'home/dot_config/**')
fi

# 5. No symlink inside any in-repo plugin source.
if [[ -d $REPO/os/omarchy/plugins-src ]]; then
  l=$(find "$REPO/os/omarchy/plugins-src" -type l -print -quit)
  [[ -z $l ]] || bad "symlink in plugin source: $l — omarchy-plugin-validate rejects it"
fi

# 6. AGENTS.md + the five pointer files match the generator, and §1-6 satisfy
#    the invariance rule.
"$REPO/bin/agentsmd-render" --check "$REPO" >/dev/null 2>&1 \
  || bad "AGENTS.md / a pointer file is stale, or §1-6 breaks the invariance rule — run: mise run agentsmd"

# 7. machines.toml parses as TOML (N2).
python3 -c "import tomllib,sys; tomllib.load(open(sys.argv[1],'rb'))" \
  "$REPO/home/.chezmoidata/machines.toml" 2>/dev/null \
  || bad "home/.chezmoidata/machines.toml is not valid TOML"

(( FAIL )) && { echo "Push blocked. Do NOT use --no-verify." >&2; exit 1; }
exit 0
```

### `.github/workflows/dotfiles-ci.yml`

| Job | What it does | Why server-side |
|---|---|---|
| `secrets` | `gitleaks` full-history + the regex sweep on the PR diff | A hook is skippable with `--no-verify` |
| `shell` | `bash -n` + `shellcheck` on every `*.sh`, `bin/*`, `.githooks/*`; `luac -p` on every `home/dot_config/hypr/*.lua` | Catches a broken bootstrap or a Lua error before it reaches a machine |
| `structure` | `scripts/validate_dotfiles.sh`, incl. the 5-line `hyprland.lua` override-block assertion (n11b) | Tree matches README; links resolve |
| `chezmoi` | `python3 -c "import tomllib…"` on `machines.toml` (N2); `chezmoi execute-template` over every `*.tmpl` with a fixture `machines.toml`; asserts `default` exists and renders a monitor line | Catches TOML and template errors without the age key |
| `agents-md` | `bin/agentsmd-render --check` — regenerates §1–§6 from the **repo's** `.agents/skills/` (committed, so deterministic on a runner) and diffs `AGENTS.md` **and** the five pointer regions | N5/N9 |
| `agents-md-invariance` | The fixed `check_invariance` (N3), which now returns non-zero | Enforces M8 mechanically |
| `lockfile` | `jq` schema check; `id` matches the validator's regex and is not `omarchy.*`; each `origin:local` entry's `content_sha256` recomputed from `plugins-src/`; each `id` equals its source `manifest.json` `.id` | Lockfile/source drift caught at PR time |
| `plugin-symlinks` | `find os/omarchy/plugins-src -type l` must be empty | The strictest do-not item, enforced outside the bypassable layer |
| `policy` | Every repo path resolves to its intended level against a fixture table; no L0 rule shadows a later L2 rule; `forbidden_commands`/`apply_commands` are valid globs; the gate's `glob_re` is unit-tested against a fixture of path/glob pairs including the n6 false positives (`docs/README.mdx`, `x/home/y`) | n5, n6 |

### Drift detection

`bin/dotfiles-drift`, run weekly by `dotfiles-drift.timer` and at the end of bootstrap:

1. `chezmoi diff` — any `$HOME` file changed outside the repo.
2. Pristine sweep via `omarchy_default_for` (**both** trees, with `chezmoi_source_to_rel`).
3. `dotfiles-plugins verify` — installed vs locked hash, untracked plugins, NEEDS-REVIEW.
4. `sync.sh --dry-run` — conflicts in agent content.
5. `pacman -Qqet` vs `os/packages/pacman.txt`.
6. `pacman -Q omarchy` vs `os/omarchy/.target-version`.
7. `bin/dotfiles-discovery-check`.
8. **n11b** — `hyprland.lua`'s upstream half vs the shipped file.
9. **n11a** — warn if `~/.local/state/hypr/local.lua` exists (it would shadow the
   documented escape hatch, because `~/.local/state/?.lua` precedes `~/.config/?.lua`).
10. `--suggest-tracking` (opt-in) — append newly-diverged candidates, commented out, to
    `os/omarchy/tracked-files.txt` (n7).

**Exit convention (m10):**

| Code | Meaning | Bootstrap | Timer |
|---|---|---|---|
| `0` | clean | continue | silent |
| `10` | findings — report written, nothing mutated | continue, print a NOTE | notification, unit **succeeds** |
| `1` | the check itself errored | **abort** | unit **fails** |

### `os/systemd/` — all four units committed (N8)

```ini
# dotfiles-sync.service  (verbatim from this machine, now under version control)
[Unit]
Description=Sync dotfiles .agents/ (skills, instructions, harnesses, prompts, workflows, validation, automation) to ~/.agents and ~/.claude/skills

[Service]
Type=oneshot
ExecStart=%h/dotfiles/sync.sh
```
```ini
# dotfiles-sync.timer
[Unit]
Description=Weekly sync of dotfiles .agents/ to this machine
[Timer]
OnCalendar=weekly
Persistent=true
RandomizedDelaySec=1800
[Install]
WantedBy=timers.target
```
```ini
# dotfiles-drift.service
[Unit]
Description=Report dotfiles drift
[Service]
Type=oneshot
ExecStart=%h/dotfiles/bin/dotfiles-drift
SuccessExitStatus=10
```
```ini
# dotfiles-drift.timer
[Unit]
Description=Weekly dotfiles drift report
[Timer]
OnCalendar=weekly
Persistent=true
RandomizedDelaySec=1800
[Install]
WantedBy=timers.target
```

`SuccessExitStatus=10` is what makes the exit convention work: findings notify without
marking the unit failed, while a real error (exit 1) shows up in `systemctl --user --failed`.

---

## 12. Risks

### 12.1 What breaks FIRST on a brand-new machine — ranked

1. **The age private key is not there.** Highest probability, and a *today* risk
   (`CLAUDE.md:36`, "Manual, pending"). Nothing decrypts. **Mitigation:** bootstrap step 3
   is a hard stop with exact recovery text; step 6 no longer swallows the failure.
   **Residual:** with no backup, every secret must be re-issued.
2. **Hostname has no `machines.toml` entry.** Guaranteed on machine #2. **Mitigation:**
   `machines.default` renders `hl.monitor({ output = "," … })` so Hyprland auto-detects
   every output; bootstrap **dies** if neither the host nor `default` exists; CI asserts
   `default` renders a monitor line.
3. **Invalid `machines.toml`.** v2 shipped a file that `tomllib` rejects, which would have
   killed bootstrap step 5 on every machine. **Mitigation:** fixed (N2), plus a
   `toml-parse` gate in both pre-push and CI so it cannot recur.
4. **A Lua error in a tracked hypr file.** v1 shipped one (M11). **Mitigation:** the
   override hook is correct and lives in `hyprland.lua`'s invited tail; `luac -p` runs on
   every tracked hypr Lua file in CI.
5. **A first external-plugin install runs unaudited upstream code (N10).** `omarchy-plugin-add`
   clones and rescans upstream HEAD before the pin applies. **Mitigation:** `cmd_sync`
   refuses a first install unless `DOTFILES_PLUGINS_ALLOW_FIRST_INSTALL=1`; bootstrap
   never sets it and reports `NEEDS-REVIEW`. **Residual: the pin is a reproducibility
   control, not a supply-chain gate.**
6. **Omarchy version skew.** Overrides authored against 4.0.4. Files still apply but may
   reference moved helpers. Drift-report noise, not a hard failure.
7. **The `include | decrypt | fromJson` idiom fails on the installed chezmoi.**
   **Mitigation:** day-1 acceptance test plus the per-destination `encrypted_*.age`
   fallback already running in this repo.

### 12.2 Ongoing risks

| Risk | Likelihood | Mitigation | Residual |
|---|---|---|---|
| Omarchy upgrade replaces a tracked file by hash | High, recurring | Real files mean a content diff, not a broken symlink; weekly drift catches it | You must read the drift report |
| `hyprland.lua`'s upstream half goes stale | Medium | n11b: drift diffs `head -n -5` against the shipped file; CI asserts the block is 5 lines | You must re-apply the block by hand when upstream changes |
| §1–§6 drift per repo, killing the shared prefix | Medium | `agents-md` + `agents-md-invariance` CI jobs, with the N3 fix making the latter actually able to fail | The denylist is hand-maintained; a new kind of repo-specific term slips through until added |
| **An agent writes an L2 path through a Bash idiom the extractor cannot see (N7)** | Medium | The gate covers all first-party edit tools and the common Bash write patterns; `forbidden_commands` covers the destructive verbs; the merged-ref read blocks self-amendment regardless | **Real and accepted: the policy is a strong control, not a sandbox.** A heredoc, a variable-built path, or a program writing as a side effect can bypass path classification. |
| The policy fallback copy goes stale | Low | Seeded from `origin/main` on every bootstrap; the gate prefers the live `git show` and only falls back when git is unavailable | A machine that never re-bootstraps keeps an old fallback |
| `sync.sh` and chezmoi both claim a path | Low | §3 is exclusive by destination; `validate_dotfiles.sh` asserts no chezmoi-managed path lives under `~/.agents`/`~/.claude`; `sync.sh:344-349` refuses dest-inside-src | — |
| Migrating `destDir` breaks the two existing secrets | Medium, one-time | PR 1 does it atomically: apply under the old config, copy both plaintexts to `/dev/shm`, rewrite the source tree, apply under the new config, `diff` both, then land the `setup.sh` edits | `.chezmoisource/` stays one cycle as a rollback |
| An older machine still has the legacy `~/.agents` symlink | Medium | `undo_legacy_dir_symlink` runs in step 5b before `sync.sh`; `sync.sh` independently refuses dest-inside-src | A machine that never re-bootstraps stays broken — documented in `docs/OS.md` |
| `default: L1` makes agents ask constantly | Medium | Deliberate; the L0 globs cover skills, prompts, instructions, docs and tasks | Tune globs, never the default |
| An external plugin's upstream adds a symlink | Low | `omarchy-plugin-validate` after every checkout; a validate failure is fatal for that plugin | It stays uninstalled until upstream fixes it |
| Scope creep into the `tasks/` initiative | Medium | AGENTS.md §7 states `tasks/` is separate; this plan adds nothing under `tasks/` | — |

### 12.3 Sequencing (n12: bootstrap lands last)

1. **Back up the age key to the password manager.** Nothing else ships first.
2. Run the `chezmoi execute-template` acceptance test (§6); record primary-or-fallback in
   `docs/SECRETS.md`.
3. **PR 1** — `home/` source dir, `destDir`/`workingTree` migration, both secrets moved,
   the four `setup.sh` edits from §0.1, `bin/dotfiles-clone-repos`, `docs/SECRETS.md`
   update. (The symlink deletions and the chezmoi migration are two halves of one change
   and must land together.)
4. **PR 2** — the 3 hypr files, `machines.toml` (valid TOML), the 6 other tracked configs,
   `os/omarchy/tracked-files.txt` with its stated population rule, `docs/OS.md` documenting
   both default trees.
5. **PR 3** — `os/omarchy/plugins.lock.json` + `bin/dotfiles-plugins` (zero plugins
   installed today, so it is cheap to land and test).
6. **PR 4** — `.agents/agentsmd/` + `bin/agentsmd-render` + `AGENTS.local.md` + the
   `AGENTSMD:PREFIX` markers in the five pointer files, `.agents/harnesses/DISCOVERY.md`
   and `POLICY.md`.
7. **PR 5** — `.agents/policy/` (README + yaml + gate) and the `sync.sh` policy-skip.
8. **PR 6** — `bin/dotfiles-drift`, `bin/dotfiles-discovery-check`, `mise.toml`,
   `os/systemd/` (all four units).
9. **PR 7** — `bin/dotfiles-bootstrap` (every deliverable its steps reference now exists),
   `.githooks/pre-push`, `dotfiles-ci.yml`, `scripts/validate_dotfiles.sh` additions.
10. Only then: bootstrap machine #2 and treat every surprise as a PR-8 finding.
