#!/bin/bash
# Shared helpers for dtx-providers adapters. Sourced, not executed directly.

DTX_PROVIDERS_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
DTX_PROVIDERS_REGISTRY="$DTX_PROVIDERS_DIR/registry"
DTX_PROVIDERS_HARNESSES="$DTX_PROVIDERS_DIR/harnesses"
DTX_PROVIDERS_SECRETS="${DTX_PROVIDERS_SECRETS:-$HOME/.custom_providers/dtx_providers.env}"
DTX_PROVIDERS_RUNTIME="$HOME/.custom_providers"

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
  # env_var is passed as a positional arg, never interpolated into the script
  # text -- a provider id/env-var-name with shell metacharacters can't inject.
  value=$(env -i bash -c '
    set -a
    source "$1"
    set +a
    var_name="$2"
    printf "%s" "${!var_name:-}"
  ' _ "$DTX_PROVIDERS_SECRETS" "$env_var")
  [[ -n $value ]] || dtx_fail "$env_var not set in $DTX_PROVIDERS_SECRETS"
  printf '%s' "$value"
}

dtx_expand_path() {
  printf '%s' "${1/#\~/$HOME}"
}

# Backs up the pristine, pre-dtx-providers state -- only ever writes the
# .bak once, so a second apply/remove never overwrites it with an
# already-modified version.
dtx_backup() {
  local path="$1"
  [[ -f $path ]] || return 0
  [[ -f "$path.dtx-providers.bak" ]] && return 0
  cp "$path" "$path.dtx-providers.bak"
}

# Enforces a safe id for anything used as a filename component (registry,
# harnesses, adapters, generated launcher names, env var name derivation).
dtx_validate_id() {
  local id="$1"
  [[ $id =~ ^[a-z0-9][a-z0-9-]*$ ]] || dtx_fail "invalid id '$id' -- must match ^[a-z0-9][a-z0-9-]*\$ (lowercase letters, digits, hyphens, can't start with a hyphen)"
}
