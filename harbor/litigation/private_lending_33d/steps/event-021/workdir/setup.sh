#!/bin/bash
set -euo pipefail
HTTP_BODY=""
trap 'rm -f -- "$0" "${HTTP_BODY:-}"' EXIT

controller_post() {
  local url="$1" header="$2" attempt status curl_rc
  for attempt in 1 2 3 4 5; do
    rm -f -- "${HTTP_BODY:-}"
    HTTP_BODY="$(mktemp)"
    if status="$(curl -sS --connect-timeout 5 --max-time 40 -o "$HTTP_BODY" -w '%{http_code}' -X POST "$url" -H "$header")"; then curl_rc=0; else curl_rc=$?; fi
    if ((curl_rc == 0)) && [[ "$status" =~ ^2[0-9][0-9]$ ]]; then return 0; fi
    if ((attempt < 5)); then sleep 2; continue; fi
    if ((curl_rc != 0)); then cat "$HTTP_BODY" >&2; return "$curl_rc"; fi
    printf 'world-controller POST failed after 5 attempts: HTTP %s\n' "$status" >&2
    cat "$HTTP_BODY" >&2
    return 22
  done
}

ready=0
for i in $(seq 1 30); do
  if curl -sf http://world-controller:8090/health >/dev/null 2>&1; then
    ready=1
    break
  fi
  sleep 2
done
[ "$ready" = 1 ] || { echo 'world-controller did not become ready' >&2; exit 1; }

controller_post http://world-controller:8090/clock/event-021 'X-Clock-Token: private-lending-33d-clock-token'
