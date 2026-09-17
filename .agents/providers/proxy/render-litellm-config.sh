#!/bin/bash
# Regenerates ~/.dtx-providers/litellm-config.yaml from the provider registry.
# Never edit that YAML by hand -- it is always overwritten by this script, and it DOES
# contain literal upstream API keys (LiteLLM is the piece that actually talks to each
# provider's real backend). That's expected, same as .vscode/settings.json in this repo
# (see docs/SECRETS.md): ~/.dtx-providers/ lives inside ~/dotfiles/.dtx-providers/ but is
# gitignored, never committed. Clients (Claude Code, Codex CLI) only ever see the proxy's
# own local master key, never the upstream provider keys.

set -euo pipefail
# Set before any file is created in this script -- this whole directory holds
# secrets (proxy.env, litellm-config.yaml has literal upstream API keys), so
# nothing here should ever depend on the caller's ambient umask.
umask 077

cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../adapters"
source lib.sh

command -v jq >/dev/null || dtx_fail "jq is required"
command -v python3 >/dev/null || dtx_fail "python3 is required (used to emit YAML safely)"

mkdir -p "$DTX_PROVIDERS_RUNTIME"
chmod 700 "$DTX_PROVIDERS_RUNTIME"
proxy_env="$DTX_PROVIDERS_RUNTIME/proxy.env"

if [[ ! -f $proxy_env ]]; then
  master_key="sk-dtx-$(head -c 24 /dev/urandom | base64 | tr -dc 'a-zA-Z0-9' | head -c 32)"
  printf 'DTX_PROXY_MASTER_KEY=%s\nDTX_PROXY_PORT=4444\n' "$master_key" >"$proxy_env"
  echo "proxy: generated a new local master key at $proxy_env"
fi
# shellcheck disable=SC1090
source "$proxy_env"

model_entries_json="[]"
for id in $(dtx_list_providers); do
  provider=$(dtx_provider_json "$id")
  env_var=$(jq -r .apiKeyEnvVar <<<"$provider")
  api_key=$(dtx_resolve_secret "$env_var")
  base_url=$(jq -r .baseURL <<<"$provider")

  entries=$(jq -c --arg pid "$id" --arg baseUrl "$base_url" --arg apiKey "$api_key" '
    .models[] | {
      model_name: ($pid + "/" + .id),
      litellm_params: {
        model: ("openai/" + .id),
        api_base: $baseUrl,
        api_key: $apiKey,
        use_chat_completions_api: true
      }
    }
  ' <<<"$provider")

  model_entries_json=$(jq -c --argjson new "$(jq -s . <<<"$entries")" '. + $new' <<<"$model_entries_json")
done

config_json=$(jq -n --argjson models "$model_entries_json" --arg masterKey "$DTX_PROXY_MASTER_KEY" '
  {model_list: $models, general_settings: {master_key: $masterKey}}
')

python3 -c '
import json, sys, yaml
config = json.load(sys.stdin)
print(yaml.safe_dump(config, sort_keys=False, default_flow_style=False))
' <<<"$config_json" >"$DTX_PROVIDERS_RUNTIME/litellm-config.yaml.tmp" \
  || dtx_fail "python3 + pyyaml are required to render litellm-config.yaml (pip install pyyaml)"

mv "$DTX_PROVIDERS_RUNTIME/litellm-config.yaml.tmp" "$DTX_PROVIDERS_RUNTIME/litellm-config.yaml"
echo "proxy: rendered $DTX_PROVIDERS_RUNTIME/litellm-config.yaml from $(dtx_list_providers | wc -l) provider(s)"
