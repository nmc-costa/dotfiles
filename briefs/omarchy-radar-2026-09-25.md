# omarchy-radar — 2026-09-25

## Sources checked
- omacom/omarchy GitHub (commits + discussions + releases): ok (51 new items)
- omarchy news/marketplace feed (news-radar feed.xml): ok (~500 items; ≈480 are 09-14→09-22 backfill listings already largely covered by prior runs)
- awesome-omarchy README: ok (1 snapshot)
- r/omarchy: ok (25 new items)
- Hacker News: ok (20 new items)
- best-skills CSV: ok (1 snapshot; harness-radar's domain, cross-noted only)

## Top 3 suggestions

### 1. Upstream added select-all + standard terminal clipboard shortcuts — check for overlap with this machine's customized foot bindings
- **What**: Omarchy upstream merged new default terminal clipboard shortcuts, including select-all and standardized copy/paste keys (`omacom/omarchy` commit `129c67e`, merged as PR "terminal-clipboard-shortcuts", commit `588f339`). This machine runs **foot** with hand-written `[key-bindings]` in `~/.config/foot/foot.ini:17-20` (`Control+Shift+c` / `Control+Shift+v`, plus `Control+Insert` / `Shift+Insert` variants) that may now duplicate or be shadowed by the new defaults after the next `omarchy update`.
- **Why now**: merged upstream this cycle — https://github.com/omacom/omarchy/commit/129c67e25a1ae0e054d13a2ccb1c5edb790aaf09
- **Impact / Effort / Redundancy / Fit**: avoids surprise keybinding changes in the daily-driver terminal / trivial (one comparison after update) / nothing tracked covers foot bindings / direct — foot is the only terminal in use here.
- **Diff**: none proposed this run — verification step only. After the next `omarchy update`, compare foot's shipped default keybindings against the custom block above and remove whichever copy/paste declarations become redundant. (No diff drafted: the exact upstream key names aren't in today's collected data and guessing them would be fabrication.)

### 2. Per-theme wallpaper memory merged into Quattro — benefits the 4 themes installed here automatically
- **What**: PR #7718 "remember-theme-wallpapers" was merged (`28ceaae`, plus `0385610` "Merge quattro and preserve per-theme wallpaper memory"): Omarchy now remembers each theme's last wallpaper and restores it on theme switch. This machine has 4 `wallhaven-*` themes installed, each already carrying its own `backgrounds/` directory, so wallpaper-per-theme becomes sticky with no config change.
- **Why now**: merged upstream this cycle — https://github.com/omacom/omarchy/commit/28ceaae70ebac3a0edcc21f2faa77a90dc6d404c
- **Impact / Effort / Redundancy / Fit**: small daily QoL (themes stop fighting over the wallpaper) / zero (arrives via `omarchy update`) / nothing similar tracked / direct — all 4 installed themes are multi-background wallhaven sets.
- **Diff**: none — no local file change; behavior arrives with the update.

### 3. Hermes is now a first-class default-agent option — relevant to this agent-heavy setup
- **What**: A cluster of upstream commits landed Hermes Desktop support: it's installed whenever chosen as the default agent (`73a2b91`, PR merged in `c3e67f5`), Hermes runs from an activated venv now count as Hermes (`5630c6f`), and uninstalling closes it cleanly instead of prompting (`14eb943`). This machine's bar already carries `omarchy.agents` and the workspace runs multiple harnesses daily, so a new supported default-agent backend is worth knowing about before the next update — even if the decision is "keep current setup."
- **Why now**: merged upstream this cycle — https://github.com/omacom/omarchy/commit/c3e67f5d405047765d47a9336a3df115a7beecfb
- **Impact / Effort / Redundancy / Fit**: awareness + optional new agent backend / zero to adopt-by-default, moderate to switch / `omarchy.agents` widget already covers monitoring / direct — this machine is explicitly multi-agent.
- **Diff**: none — optional adoption only.

## Tips

Interactive-only, for the human to run (never executed by the radar):

- Gesture-based Mission Control for Hyprland (3-finger swipe, live window spread — pairs well with the portrait side monitor): `omarchy plugin add https://github.com/ReidenXerx/omarchy-aerial --enable`
- Remember pop-up/dialog size+position (directly answers discussion #13257 "Remember float preferences"; this machine defines no float window rules today): `omarchy plugin add https://github.com/unipsycho/omarchy-omafloat --enable`
- Claude Code usage/limits in the bar (complements the stock `omarchy.agents` widget): `omarchy plugin add https://github.com/mryll/claudebar --enable`
- hyprmoncfg 2.3.5 released (already installed here as `crmne.hyprmoncfg` — bar widget + generated `hyprmoncfg-monitors.lua` present): check its release notes before the next update, since this machine's display layout is hyprmoncfg-managed.
- `npx skills find omarchy hyprland` / `npx tessl search omarchy` — exploratory only.
