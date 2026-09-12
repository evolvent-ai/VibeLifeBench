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
  local status curl_rc
  for try in 1 2 3 4 5; do
    rm -f -- "${HTTP_BODY:-}"
    HTTP_BODY="$(mktemp)"
    if status="$(curl -sS --connect-timeout 5 --max-time 40 -o "$HTTP_BODY" -w '%{http_code}' "$@")"; then
      curl_rc=0
    else
      curl_rc=$?
    fi
    if ((curl_rc == 0)) && [[ "$status" =~ ^2[0-9][0-9]$ ]]; then return 0; fi
    cat "$HTTP_BODY" >&2 || true
    if ((try < 5)); then sleep 2; continue; fi
    printf 'controller POST failed: HTTP %s\n' "${status:-curl-error}" >&2
    return 22
  done
}

post_controller -X POST http://world-controller:8090/clock/event-013 \
  -H 'X-Clock-Token: career_jobhop_tax_reconcile-clock-token'
