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
  local url="$1" header="$2" attempt status curl_rc
  for attempt in 1 2 3 4 5; do
    rm -f -- "${HTTP_BODY:-}"
    HTTP_BODY="$(mktemp)"
    if status="$(curl -sS --connect-timeout 5 --max-time 40 -o "$HTTP_BODY" -w '%{http_code}' -X POST "$url" -H "$header")"; then
      curl_rc=0
    else
      curl_rc=$?
    fi
    if ((curl_rc != 0)); then
      cat "$HTTP_BODY" >&2 || true
      if ((attempt < 5)); then sleep 2; continue; fi
      return "$curl_rc"
    fi
    if [[ "$status" =~ ^2[0-9][0-9]$ ]]; then
      return 0
    fi
    if [[ "$status" == 409 ]] && grep -Eiq '(database|table).*(locked|busy)|(locked|busy).*(database|table)' "$HTTP_BODY" && ((attempt < 5)); then
      cat "$HTTP_BODY" >&2 || true
      sleep 2
      continue
    fi
    printf 'controller POST failed: HTTP %s\n' "$status" >&2
    cat "$HTTP_BODY" >&2 || true
    return 22
  done
  return 22
}

post_controller http://world-controller:8090/clock/event-004 "X-Clock-Token: interpreter-cert-oral-exam-travel-equipment-clock-7d3f9a"

