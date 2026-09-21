# Secrets Management (chezmoi + age)

This repo stores two real secrets, both age-encrypted under `home/` (chezmoi's
source directory — see `docs/AGENT_OS_UNIFICATION_PLAN.md` §1 for why this
moved off `.chezmoisource/` in PR1), both decrypted locally by `chezmoi
apply`, both gitignored at their destination:

1. The `apiKey` inside `~/.vscode/settings.json` (used by a VS Code chat
   extension to talk to a custom LLM endpoint at
   `https://glm53-flash.dtx-colab.com/v1/chat/completions`). It used to be
   committed in plaintext; now it's only at
   `home/dot_vscode/encrypted_settings.json.age`.
2. `~/.dtx-providers/secrets.env` — the same GLM-5.3-Flash API key (and any
   further custom model provider keys added later via `dtx-providers-tui`),
   consumed by the `.agents/providers/` adapters/proxy so opencode, Crush,
   Codex CLI, and Claude Code can all use it too. Encrypted at
   `home/private_dot_dtx-providers/encrypted_private_secrets.env.age`.
   See `.agents/harnesses/PROVIDERS.md` for what consumes it.

Both follow the exact same mechanism described below — this doc was written
for secret #1 and generalizes directly to #2 (just a different source/target
path).

## How it fits into this repo

- `~/dotfiles` is **not** chezmoi's default source directory
  (`~/.local/share/chezmoi`). Instead, `~/dotfiles/home/` is used as a
  dedicated chezmoi source directory (PR1: previously `.chezmoisource/`), so
  chezmoi never touches anything else in the repo (`.agents/`, `.claude/`,
  `setup.sh`, etc. are untouched by chezmoi and keep working exactly as
  before via `setup.sh`/`sync.sh`).
- chezmoi's *destination* directory is `$HOME` (PR1: previously
  `~/dotfiles` itself), so `chezmoi apply` writes the decrypted file
  directly to `~/.vscode/settings.json` and `~/.dtx-providers/secrets.env` —
  real directories since `setup.sh`'s `undo_legacy_dir_symlink` replaced the
  old whole-directory symlinks (see `setup.sh`'s `# === AGENTS & SKILLS
  SETUP ===` section).
- The mapping is controlled by a **local, machine-specific** chezmoi config
  file at `~/.config/chezmoi/chezmoi.toml` (this file is NOT in the repo —
  each machine needs its own copy, see setup steps below):

  ```toml
  sourceDir   = "/home/<you>/dotfiles/home"
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
   sourceDir   = "$HOME/dotfiles/home"
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
   `~/.dtx-providers` from legacy whole-directory symlinks into real
   directories (`undo_legacy_dir_symlink`, idempotent, a no-op if they're
   already real directories) so `chezmoi apply` has a real destination to
   write into.

4. Decrypt and write the real files:
   ```bash
   chezmoi apply
   ```
   This regenerates **both** `~/.vscode/settings.json` and
   `~/.dtx-providers/secrets.env` with their real values, in one command,
   without ever putting either key in git.

5. Verify:
   ```bash
   chezmoi diff       # should print nothing (already in sync)
   cat ~/.vscode/settings.json     # should show the real apiKey
   cat ~/.dtx-providers/secrets.env  # should show DTX_GLM53_FLASH_API_KEY=...
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
# 3. commit the updated home/dot_vscode/encrypted_settings.json.age
cd ~/dotfiles && git add home/dot_vscode/encrypted_settings.json.age
git commit -m "chore: rotate encrypted API key"
git push
```

Or use `chezmoi edit ~/.vscode/settings.json` which decrypts, opens your
editor, and re-encrypts on save in one step.
