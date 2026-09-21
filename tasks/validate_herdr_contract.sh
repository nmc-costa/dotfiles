#!/usr/bin/env bash
# Deterministic CI gate for tasks/notify.py's herdr integration —
# tasks/plans/human-in-the-loop-notifications.md §3. Detects a real
# change in herdr's contract (rate-limit behavior, JSON shape) instead of
# depending on ambient state. Confirmed empirically on this machine
# (herdr 0.8.2): back-to-back `herdr notification show` calls in the same
# shell return "shown" then "rate_limited" — the window is under 1s.
set -euo pipefail

if ! command -v herdr >/dev/null 2>&1; then
  echo "SKIP: herdr not installed"
  exit 0
fi

a=$(herdr notification show "tsk-probe-1" --body "CI contract probe" | jq -r .result.reason)
b=$(herdr notification show "tsk-probe-2" --body "CI contract probe" | jq -r .result.reason)

if [ "$a" = "shown" ] && [ "$b" = "rate_limited" ]; then
  echo "OK: herdr contract unchanged (shown, rate_limited)"
  exit 0
fi

echo "FAIL: herdr contract changed (got: $a, $b — expected: shown, rate_limited)"
exit 1
