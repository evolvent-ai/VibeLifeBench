#!/bin/bash
set -euo pipefail
HTTP_BODY=""
trap 'rm -f -- "$0" "${HTTP_BODY:-}"' EXIT

ready=0
for i in $(seq 1 30); do
  if curl -sf --connect-timeout 5 --max-time 10 http://world-controller:8090/health >/dev/null 2>&1; then
    ready=1
    break
  fi
  sleep 2
done
[ "$ready" = 1 ] || { echo "world-controller not ready after 60 seconds" >&2; exit 1; }

post_controller() {
  local url="$1" header="$2" attempt status curl_rc
  for attempt in 1 2 3; do
    rm -f -- "${HTTP_BODY:-}"
    HTTP_BODY="$(mktemp)"
    if status="$(curl -sS --connect-timeout 5 --max-time 40 \
      -o "$HTTP_BODY" -w '%{http_code}' -X POST "$url" -H "$header")"; then
      curl_rc=0
    else
      curl_rc=$?
    fi
    if ((curl_rc != 0)); then
      cat "$HTTP_BODY" >&2
      return "$curl_rc"
    fi
    if [[ "$status" =~ ^2[0-9][0-9]$ ]]; then
      return 0
    fi
    if [[ "$status" == 409 ]] &&
      grep -Eiq '(database|table).*(locked|busy)|(locked|busy).*(database|table)' "$HTTP_BODY" &&
      ((attempt < 3)); then
      sleep "$attempt"
      continue
    fi
    printf 'controller POST failed: HTTP %s\n' "$status" >&2
    cat "$HTTP_BODY" >&2
    return 22
  done
}

post_controller "http://world-controller:8090/clock/event-004" "X-Clock-Token: civil-service-clock-token"
