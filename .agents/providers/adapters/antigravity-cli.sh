#!/bin/bash
# Antigravity CLI (real binary: `agy`, not `antigravity`) -- investigated
# 2026-09-17: no `models add`/`provider add`, no base-url/endpoint/proxy/
# custom-provider flag or env var anywhere in `agy --help`. `agy models`
# only lists a closed set served by Google's own Antigravity backend.
# `strings` on the binary shows an internal CustomModelsConfig/
# MODEL_PROVIDER_OPENAI/provider_api_key concept, but also
# TEAMS_FEATURES_OPENAI_DISABLED -- this looks gated behind a Google
# Workspace/Antigravity Teams admin policy, not something reachable from a
# local CLI or config file. See harnesses/antigravity-cli.json for the full
# note. Fails loudly instead of pretending to apply -- see
# adapters/gemini-cli.sh's history for why that matters.

set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
source lib.sh

dtx_fail "antigravity-cli: not supported today -- no custom-provider mechanism reachable from the local CLI/config (see harnesses/antigravity-cli.json for what was checked). Re-verify against agy's current --help / docs before retrying, and check for Google Workspace/Antigravity Teams admin access if you have it."
