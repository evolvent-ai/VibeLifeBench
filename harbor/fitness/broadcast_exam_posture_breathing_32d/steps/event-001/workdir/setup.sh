#!/bin/bash
set -euo pipefail
trap 'rm -f -- "$0"' EXIT
# Advance the scenario clock and publish this step's hidden releases.
# The script is removed after it runs so later releases stay hidden.

ready=0
for i in $(seq 1 30); do
  if curl --noproxy '*' -fsS http://world-controller:8090/health >/dev/null 2>&1; then
    ready=1
    break
  fi
  sleep 2
done
[ "$ready" = 1 ] || { echo "world-controller is not ready" >&2; exit 1; }

post_controller() {
  for try in 1 2 3 4 5; do
    if curl --noproxy '*' -fsS "$@" >/dev/null; then
      return 0
    fi
    sleep 2
  done
  return 22
}

post_controller -X POST http://world-controller:8090/clock/event-001 -H 'X-Clock-Token: broadcast-exam-clock-32d'
