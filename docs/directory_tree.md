# 🗂️ Standard Directory Tree & Environment Context

This file serves as the "source of truth" for the system's directory structure and provides the global context AI Agents (Claude, Copilot, etc.) need to understand the development environment, keep absolute portability, and use clean relative paths.

## 📐 Ecosystem Philosophy
1. **Isolation by Context:** Code is separated by privacy/professional life (`Projects/` vs `Work/`), not by platform (`github/`, `gitlab/`).
2. **Unified Root:** The user's home directory (`~` or `/home/nbugz/`) is assumed to be the working root in the editor (VS Code).
3. **Centralized Dotfiles:** All global configs and AI rules live in the `~/dotfiles` repository and are mirrored at the root via symlinks.

---

## 🗺️ System Structural Map

```text
/home/nbugz/ (~)                # ENVIRONMENT ROOT (Open VS Code here: code ~)
│
├── .dotfiles/                  # PRIVATE CONFIG REPOSITORY (Synced via GitHub)
│   ├── directory_tree.md       # This documentation/structural-context file
│   ├── .context-global.md      # General context instructions for AIs
│   ├── claude.md               # Claude-specific rules and preferences
│   ├── copilot.md              # GitHub Copilot-specific rules and preferences
│   ├── .gitconfig              # Global Git config
│   └── setup.sh                # Automation script for new machines
│
├── Projects/                   # PERSONAL CONTEXT (Own initiatives and studies)
│   ├── .ai-context.md          # Optional context scoped to personal projects only
│   └── [personal-repo]/        # Cloned repositories (Git manages the remote transparently)
│       └── .git/
│
└── Work/                       # PROFESSIONAL CONTEXT (Employment and organizations)
    ├── .work-rules.md          # Company architecture standards and business rules
    └── [company-repo]/         # Organization repositories (e.g. dtx-dashboard)
        └── .git/
```

---

## 🔗 Active Symlinks
To make sure AI extensions find the definitions at the root (`~`), the following files are linked:
* `~/dotfiles/directory_tree.md`  -->  `~/.directory_tree.md` (Optional)
* `~/dotfiles/.context-global.md` -->  `~/.context-global.md`
* `~/dotfiles/claude.md`          -->  `~/claude.md`
* `~/dotfiles/copilot.md`         -->  `~/copilot.md`

---

## 🤖 Instructions for AI Agents (Context Prompt)
> **Directive for the AI:** Whenever referencing file paths, imports, or cross-references, use **paths relative to the user's home directory (`~`)**.
> * **Personal Projects:** Should be referenced as `Projects/project-name/...`
> * **Work Projects:** Should be referenced as `Work/project-name/...`
> * **Configs/Rules:** Should be referenced as `.dotfiles/file-name`
>
> *Never assume an intermediate folder called `github` or `gitlab` at the projects root.*
> * To access global config files, use the symlinks at the root (`~`), e.g. `~/.context-global.md` for the global context.
