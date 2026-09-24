# herdr-commander: Quick UI for tasks/ commands

**Status:** Ready to use with overlay placement patch (upstream PR pending).

herdr-commander is a command palette (picker) inside herdr that autodiscovers tasks from `.vscode/tasks.json` and runs them in a new pane, split, or tab. It reduces CLI friction for repetitive `tasks/` commands.

## Why this matters

Today:
```bash
python3 tasks/brief.py          # type this every time
python3 tasks/sweep.py
python3 tasks/dispatch.py --task-id X --provider claude
```

With herdr-commander:
```bash
herdr                           # (already running)
<hotkey>                        # open picker overlay
brief                           # fuzzy search
<Enter>                         # runs in a split, no typing
```

All five `tasks/` commands in one place, inside your existing herdr multiplexer (same place you already have notifications).

## Setup

1. **Upstream PR** (one-time):
   - Fork [`lurepos/herdr-commander`](https://github.com/lurepos/herdr-commander)
   - Change `placement = "popup"` → `placement = "overlay"` in `herdr-plugin.toml` (in both `[[panes]]` and `[[actions]]`)
   - Open PR to upstream

2. **Once merged:**
   ```bash
   herdr plugin install herdr.commander
   ```

3. **Already configured:**
   - `.vscode/tasks.json` in this repo has 5 real entries:
     - `task-brief: What needs me?`
     - `task-sweep: Detect SLA/blocked facts`
     - `task-notify: Deliver pending facts`
     - `task-rebuild-kanban: Regenerate board`
     - `task-dispatch: Launch task on provider` (with `pickString` for provider, `promptString` for task id)

## Usage

Open herdr and press the hotkey for your command palette (varies by herdr config — typically `Ctrl+K` or similar). Type to fuzzy-filter, press Enter to run.

The task runs in a new split. Kill it with `Ctrl+C` (no orphan processes — verified in the spike).

## Updating tasks

Edit `.vscode/tasks.json` directly. herdr-commander autodiscovers changes on next picker open.

```bash
cd ~/dotfiles
# edit .vscode/tasks.json
git add .vscode/tasks.json
git commit -m "tasks: add new herdr-commander entry"
```

## What is herdr-commander **not**

- ❌ Required for anything — CLI always works: `python3 tasks/brief.py`
- ❌ A dependency — remove it anytime without breaking `tasks/`
- ❌ A replacement for terminal muscle memory — it's just faster fuzzy-select

**Rule:** The CLI is the contract. herdr-commander is UI decoration.

## See also

- `tasks/evaluations/herdr-commander/README.md` — full spike verdict (placement blocker, testing results, process lifecycle)
- `tasks/CHEATSHEET.md` § "Which interface for which question" — how herdr-commander fits into task workflow choices
- `.vscode/tasks.json` — the source of truth for what picker discovers
