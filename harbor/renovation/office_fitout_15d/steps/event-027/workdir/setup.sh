#!/bin/bash
set -euo pipefail
trap 'rm -f -- "$0"' EXIT

ready=0
for i in $(seq 1 30); do
  if curl --noproxy "*" -sf http://world-controller:8090/health >/dev/null 2>&1; then
    ready=1
    break
  fi
  sleep 2
done
[ "$ready" = 1 ] || { echo "world-controller not ready" >&2; exit 1; }

post_controller() {
  local url="$1"; shift
  local try status
  for try in 1 2 3 4 5; do
    status="$(curl --noproxy "*" -sS -o /dev/null -w '%{http_code}' "$@" "$url" 2>/dev/null || true)"
    if [[ "$status" == 2?? ]]; then return 0; fi
    sleep 2
  done
  echo "controller POST failed: $url" >&2
  return 22
}

post_controller http://world-controller:8090/clock/event-027 -X POST -H 'X-Clock-Token: office-fitout-15d-clock-20260824'
