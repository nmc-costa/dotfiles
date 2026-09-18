#!/bin/bash
# opencode: native openai-compat provider, merged into ~/.config/opencode/opencode.json.
# apiKey is written as "{env:VAR}" -- opencode resolves this at load time, so the
# literal secret is never present in this file. See docs: https://opencode.ai/docs/providers/

set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
source lib.sh

action="${1:-}"
provider_id="${2:-}"
[[ -n $action && -n $provider_id ]] || dtx_fail "usage: opencode.sh <apply|remove> <provider-id>"
command -v jq >/dev/null || dtx_fail "jq is required"

provider=$(dtx_provider_json "$provider_id")
harness=$(dtx_harness_json opencode)
config_path=$(dtx_expand_path "$(jq -r .configPath <<<"$harness")")

mkdir -p "$(dirname "$config_path")"
if [[ ! -f $config_path ]]; then
  printf '{\n  "$schema": "https://opencode.ai/config.json",\n  "provider": {}\n}\n' >"$config_path"
fi
dtx_backup "$config_path"

case "$action" in
apply)
  env_var=$(jq -r .apiKeyEnvVar <<<"$provider")
  tmp=$(mktemp)
  jq --argjson provider "$provider" --arg id "$provider_id" --arg envVar "$env_var" '
    .provider //= {}
    | .provider[$id] = {
        npm: "@ai-sdk/openai-compatible",
        name: $provider.displayName,
        options: {
          baseURL: $provider.baseURL,
          apiKey: ("{env:" + $envVar + "}")
        },
        models: (
          $provider.models
          | map({
              (.id): (
                {name: .name}
                + (if .reasoning then {reasoning: true} else {} end)
                + {limit: {context: .contextWindow, output: .maxOutput}}
              )
            })
          | add
        )
      }
  ' "$config_path" >"$tmp"
  mv "$tmp" "$config_path"
  echo "opencode: applied $provider_id -> $config_path"
  ;;
remove)
  tmp=$(mktemp)
  jq --arg id "$provider_id" 'del(.provider[$id])' "$config_path" >"$tmp"
  mv "$tmp" "$config_path"
  echo "opencode: removed $provider_id -> $config_path"
  ;;
*)
  dtx_fail "unknown action: $action"
  ;;
esac
