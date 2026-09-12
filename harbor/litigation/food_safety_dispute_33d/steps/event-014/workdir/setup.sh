#!/bin/bash
set -euo pipefail
trap 'rm -f -- "$0"' EXIT
ready=0
for i in $(seq 1 30); do
  if curl --noproxy '*' -sf http://world-controller:8090/health >/dev/null 2>&1; then
    ready=1
    break
  fi
  sleep 2
done
[ "$ready" = 1 ] || { echo "world-controller is not ready" >&2; exit 1; }
post_controller() {
  local url="$1" token_header="$2"
  for attempt in $(seq 1 5); do
    if curl --noproxy '*' -fsS -X POST "$url" -H "$token_header" >/dev/null; then return 0; fi
    sleep 1
  done
  return 22
}
post_controller http://world-controller:8090/clock/event-014 'X-Clock-Token: food-safety-clock-33d'
