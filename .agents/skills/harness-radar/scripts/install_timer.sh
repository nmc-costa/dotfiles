#!/bin/bash
# harness-radar/scripts/install_timer.sh — copies this radar's systemd
# --user unit files into place and reloads the systemd user manager.
# Deliberately does NOT enable or start anything: enabling a recurring,
# unattended automation is a persistent change the plan calls out as an
# explicit, separate, human-confirmed step (see the family plan's
# "Testing" section, step 7, and harness-radar/README.md's acceptance
# criteria) -- never folded silently into installation.
#
# After running this, the manual next step (only after you've decided
# you're ready) is:
#   systemctl --user enable --now harness-radar.timer

set -euo pipefail

SCRIPT_DIR="$(cd -P -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd -P -- "$SCRIPT_DIR/.." && pwd)"
REPO_DIR="$(cd -P -- "$SKILL_DIR/../../.." && pwd)"
UNIT_SRC_DIR="$REPO_DIR/systemd/harness-radar"
UNIT_DEST_DIR="$HOME/.config/systemd/user"

for unit in harness-radar.service harness-radar.timer; do
  [[ -f "$UNIT_SRC_DIR/$unit" ]] || { echo "install_timer.sh: missing $UNIT_SRC_DIR/$unit" >&2; exit 1; }
done

mkdir -p "$UNIT_DEST_DIR"
cp -f "$UNIT_SRC_DIR/harness-radar.service" "$UNIT_DEST_DIR/harness-radar.service"
cp -f "$UNIT_SRC_DIR/harness-radar.timer" "$UNIT_DEST_DIR/harness-radar.timer"

systemctl --user daemon-reload

echo "harness-radar: units copied to $UNIT_DEST_DIR and daemon-reload run."
echo "Not enabled or started -- when you're ready, run:"
echo "  systemctl --user enable --now harness-radar.timer"
