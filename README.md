# dotfiles

Github configuration and setup files — centralized and versioned

This repository stores the canonical configuration files that should live in the user's home directory. Files in this repository are mirrored to the home directory using symbolic links so that changes in the repository propagate to the working environment on each machine.


## User context & development environment

### System specifications
- **OS:** Omarchy Linux (Quattro), based on Arch.
- **Editors:** NeoVim (primary) and VS Code (installed via `yay -S visual-studio-code-bin`).
- **Git account:** Single GitHub account used for personal and organization repositories.

---

### Directory layout (Omarchy + IA convention)
The intermediate `~/github` directory was removed; the user uses the home directory (`~`) as the workspace root (`code ~`). This keeps relative paths short and ensures tools and AI agents can read files from the top-level workspace.

- `~/Projects/` — personal repositories (research, experiments).
- `~/Work/` — professional/organization repositories.
- `~/dotfiles/` — the single private repository that contains global environment and editor configuration files.

---

### Dotfiles and symlink structure
Configuration files live in `~/dotfiles/` and are mirrored to the home directory via symbolic links so local tools and agents read the actual configuration from the top-level path:

- `~/dotfiles/directory_tree.md`  -> `~/directory_tree.md`
- `~/dotfiles/.context-global.md` -> `~/.context-global.md`
- `~/dotfiles/claude.md`          -> `~/claude.md`
- `~/dotfiles/.claude`            -> `~/.claude`
- `~/dotfiles/.vscode`            -> `~/.vscode`
- `~/dotfiles/.github`            -> `~/.github`
- `~/dotfiles/.github/copilot-instructions.md` -> `~/.github/copilot-instructions.md`

---

### Useful commands
- Create a symlink:

```bash
ln -sf ~/dotfiles/<file> ~/<file>
```

- Open the home folder in VS Code:

```bash
code ~
```

- NeoVim shortcuts:
	- Enter insert mode: `i`
	- Exit to normal mode: `Esc` or `Ctrl-[`
	- Save and quit: `:wq` or `ZZ`
	- Quit without saving: `:q!` or `ZQ`
	- Undo: `u`

---

### Next steps (for the next session)
1. Implement `~/dotfiles/setup.sh` to recreate the symlink tree on another machine automatically.
2. Draft developer prompts and policies in Markdown to populate `claude.md` and `copilot-instructions.md`.
3. Add an automated or guided repository-cloning workflow for `Projects/` and `Work/`.


