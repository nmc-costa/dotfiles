#!/bin/bash
# Installs/refreshes the tsk-sweep systemd --user units and (re)enables the
# timer, following the ensure-*.sh convention
# (.agents/providers/proxy/ensure-proxy.sh). Idempotent — safe to re-run
# after dotfiles updates.

set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"

command -v python3 >/dev/null || { echo "python3 not found on PATH" >&2; exit 1; }
test -x ../../tasks/sweep.py || test -f ../../tasks/sweep.py || { echo "tasks/sweep.py not found next to this script -- run it from a dotfiles checkout" >&2; exit 1; }

unit_dir="$HOME/.config/systemd/user"
mkdir -p "$unit_dir"
cp tsk-sweep.service tsk-sweep.timer "$unit_dir/"

systemctl --user daemon-reload
systemctl --user enable --now tsk-sweep.timer
systemctl --user restart tsk-sweep.timer
echo "tsk-sweep: timer enabled, sweep every 10min (logs: journalctl --user -u tsk-sweep.service)"
