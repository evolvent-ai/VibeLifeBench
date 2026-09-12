#!/bin/bash
set -euo pipefail
trap 'rm -f -- "$0"' EXIT

# Wait for the controller before issuing state-changing requests.
ready=0
for attempt in $(seq 1 120); do
  if curl -fsS http://world-controller:8090/health >/dev/null 2>&1; then
    ready=1
    break
  fi
  sleep 2
done
[ "$ready" = 1 ] || { echo "world-controller is not ready" >&2; exit 1; }

post_controller() {
  local url="$1" token="$2" status
  for try in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15; do
    status="$(curl -sS -o /dev/null -w '%{http_code}' -X POST "$url" -H "X-Clock-Token: $token" -H "X-Release-Token: $token" || true)"
    if [[ "$status" == 2?? ]]; then return 0; fi
    sleep 2
  done
  return 22
}

post_controller "http://world-controller:8090/clock/event-014" "pottery_invoice_compliance_day-clock-token"
