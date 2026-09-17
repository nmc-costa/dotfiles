#!/bin/bash
# Shared helpers for dtx-providers adapters. Sourced, not executed directly.

DTX_PROVIDERS_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
DTX_PROVIDERS_REGISTRY="$DTX_PROVIDERS_DIR/registry"
DTX_PROVIDERS_HARNESSES="$DTX_PROVIDERS_DIR/harnesses"
DTX_PROVIDERS_SECRETS="${DTX_PROVIDERS_SECRETS:-$HOME/.dtx-providers/secrets.env}"
DTX_PROVIDERS_RUNTIME="$HOME/.dtx-providers"

dtx_fail() {
  echo "dtx-providers: $*" >&2
  exit 1
}

dtx_provider_json() {
  local id="$1"
  local path="$DTX_PROVIDERS_REGISTRY/$id.json"
  [[ -f $path ]] || dtx_fail "unknown provider: $id (no $path)"
  cat "$path"
}

dtx_harness_json() {
  local id="$1"
  local path="$DTX_PROVIDERS_HARNESSES/$id.json"
  [[ -f $path ]] || dtx_fail "unknown harness: $id (no $path)"
  cat "$path"
}

dtx_list_providers() {
  find "$DTX_PROVIDERS_REGISTRY" -maxdepth 1 -name '*.json' -exec basename {} .json \;
}

dtx_list_harnesses() {
  find "$DTX_PROVIDERS_HARNESSES" -maxdepth 1 -name '*.json' -exec basename {} .json \;
}

# Resolves the *literal* secret value for an env var name from secrets.env.
# Only call this where a literal value truly has to be embedded server-side
# (e.g. rendering the LiteLLM proxy config). Adapters that write a harness's
# own config file must reference the env var by NAME instead, never the
# resolved value -- see opencode.sh / crush.sh / codex.sh.
dtx_resolve_secret() {
  local env_var="$1"
  [[ -f $DTX_PROVIDERS_SECRETS ]] || dtx_fail "secrets file not found: $DTX_PROVIDERS_SECRETS (run 'chezmoi apply' first)"
  local value
  value=$(env -i bash -c "set -a; source '$DTX_PROVIDERS_SECRETS'; printf '%s' \"\${$env_var:-}\"")
  [[ -n $value ]] || dtx_fail "$env_var not set in $DTX_PROVIDERS_SECRETS"
  printf '%s' "$value"
}

dtx_expand_path() {
  printf '%s' "${1/#\~/$HOME}"
}

dtx_backup() {
  local path="$1"
  [[ -f $path ]] || return 0
  cp "$path" "$path.dtx-providers.bak"
}
