#!/bin/bash
set -euo pipefail
trap 'rm -f -- "$0"' EXIT

ready=0
for i in $(seq 1 30); do
  curl -sf http://world-controller:8090/health >/dev/null 2>&1 && { ready=1; break; }
  sleep 2
done
[ "$ready" = 1 ] || { echo "world-controller did not become ready" >&2; exit 1; }

post_controller() {
  local url="$1" header="$2" body status attempt
  for attempt in 1 2 3 4 5; do
    body="$(mktemp)"
    status="$(curl -sS --connect-timeout 5 --max-time 40 -o "$body" -w '%{http_code}' -X POST "$url" -H "$header")" || status="000"
    if [[ "$status" == 2?? ]]; then
      rm -f -- "$body"
      return 0
    fi
    printf 'world-controller POST failed: HTTP %s (attempt %s/5)\n' "$status" "$attempt" >&2
    cat "$body" >&2
    rm -f -- "$body"
    [[ "$attempt" -lt 5 ]] && sleep 2
  done
  return 22
}

post_controller "http://world-controller:8090/clock/event-018" "X-Clock-Token: career_espp_refund_recovery_clock_token"
