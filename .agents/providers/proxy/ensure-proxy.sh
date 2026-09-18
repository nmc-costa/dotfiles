#!/bin/bash
# Renders the LiteLLM config from the current registry, installs/refreshes the
# systemd --user unit, and (re)starts it. Called by any proxy-mode adapter's
# `apply`, and directly by the TUI's "Apply" flow.

set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
source ../adapters/lib.sh

command -v litellm >/dev/null || dtx_fail "litellm not found on PATH -- install it first (e.g. 'pipx install litellm[proxy]')"

./render-litellm-config.sh

unit_dir="$HOME/.config/systemd/user"
mkdir -p "$unit_dir"
cp dtx-litellm-proxy.service "$unit_dir/dtx-litellm-proxy.service"

systemctl --user daemon-reload
systemctl --user enable --now dtx-litellm-proxy.service
systemctl --user restart dtx-litellm-proxy.service
echo "proxy: dtx-litellm-proxy.service (re)started on 127.0.0.1:4444"
