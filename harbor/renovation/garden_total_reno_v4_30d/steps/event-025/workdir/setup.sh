#!/bin/bash
set -euo pipefail
trap 'rm -f -- "$0"' EXIT

ready=0
for i in $(seq 1 30); do
  if curl -sf http://world-controller:8090/health >/dev/null 2>&1; then ready=1; break; fi
  sleep 2
done
[ "$ready" = 1 ] || { echo "world-controller is not ready" >&2; exit 1; }

post_controller() {
  for try in 1 2 3 4 5; do
    if curl -fsS "$@" >/dev/null; then return 0; fi
    sleep 2
  done
  return 22
}

post_controller -X POST http://world-controller:8090/clock/event-025 \
  -H 'X-Clock-Token: garden_total_reno_v4_30d-clock-token'

post_controller -X POST http://world-controller:8090/releases/release-013 \
  -H 'X-Release-Token: garden-total-reno-v4-30d-release-token'
