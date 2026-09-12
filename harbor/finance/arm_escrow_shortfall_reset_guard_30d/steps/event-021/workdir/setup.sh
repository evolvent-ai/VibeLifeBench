#!/bin/bash
set -euo pipefail
trap 'rm -f -- "$0"' EXIT

export NO_PROXY='*'
export no_proxy='*'

ready=0
for i in $(seq 1 30); do
  if curl -sf http://world-controller:8090/health >/dev/null 2>&1; then
    ready=1
    break
  fi
  sleep 2
done
if [ "$ready" -ne 1 ]; then
  echo "world-controller did not become ready" >&2
  exit 1
fi

post_controller() {
  local attempt
  for attempt in $(seq 1 5); do
    if curl -fsS "$@" >/dev/null; then
      return 0
    fi
    sleep "$attempt"
  done
  echo "world-controller request failed after 5 attempts" >&2
  return 1
}

post_controller -X POST http://world-controller:8090/clock/event-021 -H 'X-Clock-Token: arm-escrow-shortfall-clock-7f3a9c2d' >/dev/null
