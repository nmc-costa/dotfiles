#!/bin/bash
# Gemini CLI: verified 2026-09-17 against google-gemini/gemini-cli's docs/cli/settings.md
# and docs/cli/model.md -- there is no base-URL / custom-provider setting at all, only
# model.name to pick among Google's own Gemini models. No proxy trick fixes this: the
# CLI's wire format and endpoint are hardcoded to Google's own API, so there's nothing
# for a local LiteLLM proxy to be pointed at.
#
# This adapter deliberately does nothing but fail loudly, instead of silently
# succeeding without wiring anything up -- see dotfiles/.agents/harnesses/TEMPLATE.md's
# rule against inventing a mechanism that isn't real.

set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
source lib.sh

dtx_fail "gemini-cli: not supported today -- Gemini CLI has no custom-provider / custom-base-URL setting (checked docs/cli/settings.md, docs/cli/model.md). Re-check upstream before retrying; this isn't a bug in this adapter."
