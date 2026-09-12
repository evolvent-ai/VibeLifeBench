#!/bin/bash
set -euo pipefail
HTTP_BODY=""
trap 'rm -f -- "$0"' EXIT

for i in $(seq 1 30); do
  if curl -sf --connect-timeout 2 --max-time 5 http://world-controller:8090/health >/dev/null 2>&1; then
    break
  fi
  if [[ "$i" -eq 30 ]]; then
    echo "world-controller did not become ready" >&2
    exit 1
  fi
  sleep 2
done
sleep 8

controller_post() {
  local url="$1" header="$2" attempt
  for attempt in $(seq 1 5); do
    if curl -fsS --connect-timeout 5 --max-time 40 -X POST "$url" -H "$header" >/dev/null; then
      return 0
    fi
    sleep $((attempt * 2))
  done
  echo "world-controller POST failed after 5 attempts: $url" >&2
  return 22
}

controller_post "http://world-controller:8090/clock/event-016" "X-Clock-Token: central-ac-clock-20260824"
controller_post "http://world-controller:8090/releases/release-010" "X-Release-Token: central-ac-release-010-20260824"

