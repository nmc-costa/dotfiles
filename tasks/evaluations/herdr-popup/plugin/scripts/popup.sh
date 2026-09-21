#!/usr/bin/env bash
# popup.sh — trivial pane body for the herdr-popup-spike plugin.
# Prints a banner so the pane's content is visibly attributable to this
# spike, then idles so the pane stays open long enough to inspect with
# `herdr pane list` / `herdr plugin list --json`.
set -uo pipefail

echo "herdr-popup-spike: pane opened successfully"
echo "pid: $$"
date -u +"%Y-%m-%dT%H:%M:%SZ"

exec sleep 300
