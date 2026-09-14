# dotfiles

Central repository for all agent configs, skills, workflows, and environment setup. Synced across machines via git for seamless collaboration with AI agents (Crush, Copilot, Gemini, Cline).

**Quick Links:**
- **`AGENTS.md`** — AI agent setup and skills management
- **`setup.sh`** — Automated one-click machine setup
- **`sync-skills.sh`** — Distribute skills to all agents 



# Contexto do Utilizador & Ambiente de Desenvolvimento

## 💻 Especificações do Sistema
* **SO:** Omarchy Linux (Versão Quattro), baseado em Arch. Sistema opinativo (omakase).
* **Editores Ativos:** NeoVim (nativo/eficiência máxima) e VS Code (rede de segurança visual instalado via `yay -S visual-studio-code-bin`).
* **Conta Git:** Mesma conta do GitHub usada para repositórios pessoais e da organização.

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


---

### Next steps (for the next session)
1. Implement `~/dotfiles/setup.sh` to recreate the symlink tree on another machine automatically.
2. Draft developer prompts and policies in Markdown to populate `claude.md` and `copilot-instructions.md`.
3. Add an automated or guided repository-cloning workflow for `Projects/` and `Work/`.


