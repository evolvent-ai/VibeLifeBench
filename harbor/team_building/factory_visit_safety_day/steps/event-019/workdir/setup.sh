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
[ "$ready" = 1 ] || { echo "world-controller did not become ready" >&2; exit 1; }
for attempt in 1 2 3 4 5; do
  if curl --noproxy '*' -fsS -X POST http://world-controller:8090/clock/event-019 -H 'X-Clock-Token: factory-visit-safety-day-clock-20260824' >/dev/null; then
    break
  fi
  if [ "$attempt" -eq 5 ]; then
    exit 22
  fi
  sleep $((attempt * 2))
done
