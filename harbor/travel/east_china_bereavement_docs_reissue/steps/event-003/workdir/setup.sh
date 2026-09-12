#!/bin/bash
set -euo pipefail
HTTP_BODY=""
trap 'rm -f -- "$0" "${HTTP_BODY:-}"' EXIT

CLOCK_TOKEN="${CLOCK_TOKEN:-east-china-clock-9f0243a86b4fc38a}"

ready=0
for i in $(seq 1 30); do
  if curl -sf --connect-timeout 3 --max-time 5 http://world-controller:8090/health >/dev/null 2>&1; then
    ready=1
    break
  fi
  sleep 2
done
[ "$ready" = 1 ] || { echo "world-controller not ready after 30 attempts" >&2; exit 1; }

controller_post() {
  local url="$1" header="$2" attempt status curl_rc
  for attempt in 1 2 3 4 5; do
    rm -f -- "${HTTP_BODY:-}"
    HTTP_BODY="$(mktemp)"
    if status="$(curl -sS --connect-timeout 5 --max-time 40 -o "$HTTP_BODY" -w "%{http_code}" -X POST "$url" -H "$header")"; then
      curl_rc=0
    else
      curl_rc=$?
    fi
    if ((curl_rc == 0)) && [[ "$status" =~ ^2[0-9][0-9]$ ]]; then
      return 0
    fi
    if (( attempt < 5 )); then sleep 2; continue; fi
    printf "controller POST failed after 5 attempts: HTTP %s (curl %s)\n" "${status:-none}" "$curl_rc" >&2
    cat "$HTTP_BODY" >&2 || true
    return 22
  done
}

controller_post "http://world-controller:8090/clock/event-003" "X-Clock-Token: ${CLOCK_TOKEN}"
RELEASE_TOKEN_001="${RELEASE_TOKEN_001:-east-china-release-001-7f6c2d91b0a449c2}"
controller_post "http://world-controller:8090/releases/release-001" "X-Release-Token: ${RELEASE_TOKEN_001}"
