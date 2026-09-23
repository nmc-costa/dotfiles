# Secrets Management (chezmoi + age)

This repo stores two real secrets, both age-encrypted under `.chezmoi-source/`
(chezmoi's source directory — renamed from `home/` on 2026-09-23, see "Porque
`.chezmoi-source/` e não `home/`" below), both decrypted locally by `chezmoi
apply`, both gitignored at their destination:

1. The `apiKey` inside `~/.vscode/settings.json` (used by a VS Code chat
   extension to talk to a custom LLM endpoint at
   `https://glm53-flash.dtx-colab.com/v1/chat/completions`). It used to be
   committed in plaintext; now it's only at
   `.chezmoi-source/dot_vscode/encrypted_settings.json.age`.
2. `~/.custom_providers/dtx_providers.env` — the same GLM-5.3-Flash API key
   (and any further custom model provider keys added later via
   `dtx-providers-tui`), consumed by the `.agents/providers/` adapters/proxy
   so opencode, Crush, Codex CLI, and Claude Code can all use it too.
   Encrypted at `.chezmoi-source/private_dot_custom_providers/
   encrypted_dtx_providers.env.age`. See `.agents/harnesses/PROVIDERS.md` for
   what consumes it.

Both follow the exact same mechanism described below — this doc was written
for secret #1 and generalizes directly to #2 (just a different source/target
path).

## Porque `.chezmoi-source/` e não `home/`

PR1 (`docs/AGENT_OS_UNIFICATION_PLAN.md`, commit `81de91f`, PR #34) renamed
this directory from `.chezmoisource/` to `home/` without writing down why —
no rationale for that specific name exists anywhere in the plan, the commit
message, or this doc's earlier version. In practice the name caused real
confusion: it reads as "this directory *is* your home directory" rather than
"this is chezmoi's source tree, and its *contents* map onto `$HOME` once
decrypted" — colliding semantically with `$HOME`/`/home/` in a repo that
already has to reason carefully about both. It also produced at least one
real bug elsewhere in the plan (references to a literal `x/home/y` path
getting confused with this directory).

Renamed to `.chezmoi-source/` on 2026-09-23: self-descriptive (names the
tool, not the destination), and the leading dot keeps it out of the way at
the top of a repo listing. The *contents* still use chezmoi's own `dot_`/
`private_`/`encrypted_` prefix convention to say what each file becomes at
the destination — the source directory's own name has no bearing on that
mapping (verified directly: `sourceDir` can be located/named anything;
chezmoi only cares about `dot_`/`private_`/`encrypted_` prefixes on each
path segment *inside* it, and completely ignores any segment that starts
with a literal `.`, which is reserved for chezmoi's own special files like
`.chezmoiignore`).

Same 2026-09-23 pass also renamed the provider-secret subdirectory from
`private_dot_dtx-providers/` to `private_dot_custom_providers/` (decrypting
to `~/.custom_providers/dtx_providers.env` instead of
`~/.dtx-providers/secrets.env`) — `custom_providers` was chosen over the
shorter `private_providers` because `private_` is itself a chezmoi prefix
keyword that always strips out of the final name (tested: a source directory
literally named `private_providers` decrypts to `.providers`, never
`.private_providers`) — so `private_providers` alone can never survive as
literal text in the destination path, and `custom_providers` avoids that
trap entirely while also not colliding with `~/dotfiles/.agents/providers/`
(the *system*, unaffected by this rename, still lives there).

## How it fits into this repo

- `~/dotfiles` is **not** chezmoi's default source directory
  (`~/.local/share/chezmoi`). Instead, `~/dotfiles/.chezmoi-source/` is used
  as a dedicated chezmoi source directory, so chezmoi never touches anything
  else in the repo (`.agents/`, `.claude/`, `setup.sh`, etc. are untouched by
  chezmoi and keep working exactly as before via `setup.sh`/`sync.sh`).
- chezmoi's *destination* directory is `$HOME`, so `chezmoi apply` writes the
  decrypted file directly to `~/.vscode/settings.json` and
  `~/.custom_providers/dtx_providers.env` — real directories since
  `setup.sh`'s `undo_legacy_dir_symlink` replaced the old whole-directory
  symlinks (see `setup.sh`'s `# === AGENTS & SKILLS SETUP ===` section).
- The mapping is controlled by a **local, machine-specific** chezmoi config
  file at `~/.config/chezmoi/chezmoi.toml` (this file is NOT in the repo —
  each machine needs its own copy, see setup steps below):

  ```toml
  sourceDir   = "/home/<you>/dotfiles/.chezmoi-source"
  destDir     = "/home/<you>"
  workingTree = "/home/<you>/dotfiles"
  encryption  = "age"

  [age]
      identity  = "/home/<you>/.config/chezmoi/key.txt"
      recipient = "age1vp83ej2dzlchh6g5fu5nqvkrzy874e8m84x807dtv2vukf5df39sa7c43w"
  ```

  The `recipient` (public key) above is safe to keep in this doc — it is not
  secret. The `identity` (private key) is never committed anywhere (see
  below).

## The age private key — where it lives and how to handle it

- The private key file is **`~/.config/chezmoi/key.txt`** on the machine
  where it was generated. It is *not* in this git repo and never will be —
  anyone with that file (plus the encrypted blob in this repo) can recover
  the real API key.
- **You must back this file up yourself, out-of-band** (password manager
  entry, e.g. 1Password/Bitwarden "secure note" with the file contents, or an
  encrypted USB/physical copy). This assistant cannot know your backup
  situation, so nothing was done here beyond generating the key and leaving
  it at that path with `chmod 600`.
- **Done 2026-09-21**: backed up as a Bitwarden secure note named
  `dotfiles age key` (free tier — pasted as plain text, no file attachment
  needed for a key this size). This is the owner's actual current backup;
  the bullet above stays as general guidance for anyone else using this repo.
- If you lose this file with no backup, you lose access to decrypt
  `encrypted_settings.json.age` — you would need to generate a **new** age
  key, then re-encrypt the real API key value again with the new recipient
  (the value itself would have to come from wherever else you keep it, e.g.
  the LLM provider's dashboard).
- Never paste the private key contents into a chat, commit, issue, or any
  place that might get logged or synced to a public location.

## New-machine setup

On a fresh machine, after `chezmoi` and `age` are installed
(`sudo pacman -S chezmoi age` on Arch/Omarchy) and after cloning this repo to
`~/dotfiles`:

1. **Transport the age private key to the new machine out-of-band** — copy
   it from your password manager / physical backup to
   `~/.config/chezmoi/key.txt` on the new machine, then:
   ```bash
   chmod 600 ~/.config/chezmoi/key.txt
   ```
   This step cannot be scripted or automated here — the private key is
   deliberately never in this repo.

2. Create the local chezmoi config (this file is also not in the repo —
   create it once per machine):
   ```bash
   mkdir -p ~/.config/chezmoi
   cat > ~/.config/chezmoi/chezmoi.toml <<'EOF'
   sourceDir   = "$HOME/dotfiles/.chezmoi-source"
   destDir     = "$HOME"
   workingTree = "$HOME/dotfiles"
   encryption  = "age"

   [age]
       identity  = "$HOME/.config/chezmoi/key.txt"
       recipient = "age1vp83ej2dzlchh6g5fu5nqvkrzy874e8m84x807dtv2vukf5df39sa7c43w"
   EOF
   ```
   (Expand `$HOME` to your actual home directory if your chezmoi version
   doesn't expand it — check with `chezmoi doctor` afterwards.)

3. Run `./setup.sh --links-only` first — this converts `~/.vscode` and
   `~/.custom_providers` from legacy whole-directory symlinks into real
   directories (`undo_legacy_dir_symlink`, idempotent, a no-op if they're
   already real directories) so `chezmoi apply` has a real destination to
   write into.

4. Decrypt and write the real files:
   ```bash
   chezmoi apply
   ```
   This regenerates **both** `~/.vscode/settings.json` and
   `~/.custom_providers/dtx_providers.env` with their real values, in one
   command, without ever putting either key in git.

5. Verify:
   ```bash
   chezmoi diff       # should print nothing (already in sync)
   cat ~/.vscode/settings.json          # should show the real apiKey
   cat ~/.custom_providers/dtx_providers.env  # should show DTX_GLM53_FLASH_API_KEY=...
   ```

This preserves the original "copy one key, get the same LLM endpoint config
everywhere" convenience — the one thing you now copy out-of-band is the small
age private key file instead of grepping/copy-pasting the API key itself out
of a committed `settings.json`.

## Updating the secret later

If the API key ever needs to change (rotation, new endpoint, etc.), on any
machine that has the private key configured:

```bash
# 1. edit ~/.vscode/settings.json with the new value locally
# 2. re-encrypt it back into the source state:
chezmoi add --encrypt ~/.vscode/settings.json
# 3. commit the updated .chezmoi-source/dot_vscode/encrypted_settings.json.age
cd ~/dotfiles && git add .chezmoi-source/dot_vscode/encrypted_settings.json.age
git commit -m "chore: rotate encrypted API key"
git push
```

Or use `chezmoi edit ~/.vscode/settings.json` which decrypts, opens your
editor, and re-encrypts on save in one step.
