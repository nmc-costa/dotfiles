#!/bin/bash
# omarchy-radar: install (copy) the systemd --user unit files and reload the
# user daemon. Does NOT enable or start the timer -- flipping the timer on is
# an explicit, manual step the user runs themselves once the Testing /
# Acceptance-criteria checklist in README.md has passed:
#
#   systemctl --user enable --now omarchy-radar.timer
#
# Safe to re-run any time the unit files change -- it always re-copies and
# re-runs daemon-reload, and never touches the enabled/active state of the
# timer or service.
set -euo pipefail

script_dir="$(cd -P -- "$(dirname -- "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
repo_root="$(cd -P -- "$script_dir/../../../.." >/dev/null 2>&1 && pwd)"
unit_src_dir="$repo_root/systemd/omarchy-radar"
unit_dest_dir="$HOME/.config/systemd/user"

for unit in omarchy-radar.service omarchy-radar.timer; do
  if [[ ! -f "$unit_src_dir/$unit" ]]; then
    echo "install_timer.sh: missing $unit_src_dir/$unit" >&2
    exit 1
  fi
done

mkdir -p "$unit_dest_dir"
cp "$unit_src_dir/omarchy-radar.service" "$unit_dest_dir/omarchy-radar.service"
cp "$unit_src_dir/omarchy-radar.timer" "$unit_dest_dir/omarchy-radar.timer"

systemctl --user daemon-reload

echo "omarchy-radar: installed omarchy-radar.service and omarchy-radar.timer to $unit_dest_dir"
echo "omarchy-radar: ran 'systemctl --user daemon-reload'"
echo
echo "Not enabled or started -- this stays a manual step. When ready:"
echo "  systemctl --user enable --now omarchy-radar.timer"
