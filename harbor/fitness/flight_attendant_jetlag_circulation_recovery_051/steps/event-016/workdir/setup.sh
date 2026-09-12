#!/bin/bash
set -euo pipefail
trap 'rm -f -- "$0" "${HTTP_BODY:-}"' EXIT
ready=0
for i in $(seq 1 30); do
  if curl -sf http://world-controller:8090/health >/dev/null 2>&1; then ready=1; break; fi
  sleep 2
done
[ "$ready" = 1 ] || { echo "world-controller is not ready" >&2; exit 1; }
HTTP_BODY=""
controller_post() {
  local url="$1" header="$2" attempt status curl_rc
  for attempt in 1 2 3 4 5; do
    HTTP_BODY="$(mktemp)"
    if status="$(curl -sS --connect-timeout 5 --max-time 40 -o "$HTTP_BODY" -w "%{http_code}" -X POST "$url" -H "$header")"; then curl_rc=0; else curl_rc=$?; fi
    if ((curl_rc == 0)) && [[ "$status" =~ ^2[0-9][0-9]$ ]]; then rm -f -- "$HTTP_BODY"; HTTP_BODY=""; return 0; fi
    cat "$HTTP_BODY" >&2 || true
    rm -f -- "$HTTP_BODY"; HTTP_BODY=""
    sleep 2
  done
  return 22
}
controller_post http://world-controller:8090/clock/event-016 "X-Clock-Token: flight-attendant-jetlag-clock-9f0243a86b4fc38a"
