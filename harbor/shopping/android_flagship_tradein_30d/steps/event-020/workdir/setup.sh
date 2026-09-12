#!/bin/bash
set -euo pipefail
HTTP_BODY=""
trap 'rm -f -- "$0" "${HTTP_BODY:-}"' EXIT

ready=0
for i in $(seq 1 30); do
  if curl -sf http://world-controller:8090/health >/dev/null 2>&1; then ready=1; break; fi
  sleep 2
done
[ "$ready" = 1 ] || { echo "world-controller is not ready" >&2; exit 1; }

post_controller() {
  local url="$1" header="$2" try status curl_rc
  for try in 1 2 3 4 5; do
    rm -f -- "${HTTP_BODY:-}"
    HTTP_BODY="$(mktemp)"
    if status="$(curl -sS --connect-timeout 5 --max-time 40 \
      -o "$HTTP_BODY" -w '%{http_code}' -X POST "$url" -H "$header")"; then
      curl_rc=0
    else
      curl_rc=$?
    fi
    if ((curl_rc == 0)) && [[ "$status" =~ ^2[0-9][0-9]$ ]]; then
      return 0
    fi
    printf 'controller POST attempt %s failed: curl=%s HTTP=%s\n' \
      "$try" "$curl_rc" "${status:-none}" >&2
    cat "$HTTP_BODY" >&2 || true
    sleep 2
  done
  return 22
}

post_controller http://world-controller:8090/clock/event-020 \
  "X-Clock-Token: android_flagship_tradein_30d-clock-token"
post_controller http://world-controller:8090/releases/release-008 \
  "X-Release-Token: android_flagship_tradein_30d-release-008"
