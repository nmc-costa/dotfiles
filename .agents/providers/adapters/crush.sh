#!/bin/bash
# Crush: native openai-compat provider via the crushrc DSL (`provider add`, `model add`).
# The literal secret is never written -- crushrc references "$VAR" and Crush expands it
# itself at load time (README.md: "Values support the same $VAR and $(command) expansion").
# See: https://github.com/charmbracelet/crush#custom-providers

set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
source lib.sh

action="${1:-}"
provider_id="${2:-}"
[[ -n $action && -n $provider_id ]] || dtx_fail "usage: crush.sh <apply|remove> <provider-id>"
command -v jq >/dev/null || dtx_fail "jq is required"

provider=$(dtx_provider_json "$provider_id")
harness=$(dtx_harness_json crush)
config_path=$(dtx_expand_path "$(jq -r .configPath <<<"$harness")")

begin_mark="# BEGIN dtx-providers: $provider_id"
end_mark="# END dtx-providers: $provider_id"

strip_block() {
  # Removes any existing managed block for this provider id, in place.
  awk -v b="$begin_mark" -v e="$end_mark" '
    $0 == b { skip = 1; next }
    $0 == e { skip = 0; next }
    !skip { print }
  ' "$config_path"
}

case "$action" in
apply)
  mkdir -p "$(dirname "$config_path")"
  touch "$config_path"
  dtx_backup "$config_path"

  env_var=$(jq -r .apiKeyEnvVar <<<"$provider")
  base_url=$(jq -r .baseURL <<<"$provider")

  block=$(
    echo "$begin_mark  (managed by dtx-providers-tui, do not edit by hand)"
    printf 'provider add %s --type openai-compat \\\n  --base-url "%s" \\\n  --api-key "$%s"\n' \
      "$provider_id" "$base_url" "$env_var"
    echo
    jq -r --arg pid "$provider_id" '
      .models[] |
      "model add \($pid)/\(.id) \\\n  --name \"\(.name)\" \\\n  --context-window \(.contextWindow) \\\n  --default-max-tokens \(.maxOutput)" +
      (if .reasoning then " \\\n  --can-reason true" else "" end)
    ' <<<"$provider"
    echo "$end_mark"
  )

  tmp=$(mktemp)
  strip_block >"$tmp"
  # Drop a trailing blank line left by strip_block before appending, then add the block.
  { cat "$tmp"; echo; echo "$block"; } >"$config_path"
  rm -f "$tmp"
  echo "crush: applied $provider_id -> $config_path"
  ;;
remove)
  [[ -f $config_path ]] || { echo "crush: no config at $config_path, nothing to remove"; exit 0; }
  tmp=$(mktemp)
  strip_block >"$tmp"
  mv "$tmp" "$config_path"
  echo "crush: removed $provider_id -> $config_path"
  ;;
*)
  dtx_fail "unknown action: $action"
  ;;
esac
