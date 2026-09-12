#!/bin/bash
set -euo pipefail
trap 'rm -f -- "$0"' EXIT
ready=0
for i in $(seq 1 30); do
  if curl -sf http://world-controller:8090/health >/dev/null 2>&1; then ready=1; break; fi
  sleep 2
done
[ "$ready" = 1 ] || { echo "world-controller did not become ready" >&2; exit 1; }
post_controller() {
  local url="$1" header="$2" token="$3" status
  for try in 1 2 3 4 5; do
    status="$(curl -sS -o /tmp/controller-response -w "%{http_code}" -X POST "$url" -H "$header: $token" || true)"
    [[ "$status" == 2?? ]] && return 0
    sleep 2
  done
  return 22
}
post_controller http://world-controller:8090/clock/event-031 X-Clock-Token galapagos-no-us-transit-clock-20260825
