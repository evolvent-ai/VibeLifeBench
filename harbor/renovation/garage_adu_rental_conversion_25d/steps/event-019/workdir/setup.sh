#!/bin/bash
set -euo pipefail
ready=0
for i in $(seq 1 30); do
  if curl -sf http://world-controller:8090/health >/dev/null 2>&1; then
    ready=1
    break
  fi
  sleep 2
done
if [[ "$ready" != 1 ]]; then
  echo "world-controller did not become ready after 30 attempts" >&2
  exit 1
fi
HTTP_BODY=""
trap "rm -f -- \"\$0\" \"\${HTTP_BODY:-}\"" EXIT

post_controller() {
  local url="$1" header="$2" status curl_rc
  for try in 1 2 3 4 5; do
    HTTP_BODY="$(mktemp)"
    if status="$(curl -sS --connect-timeout 5 --max-time 40 -o "$HTTP_BODY" -w "%{http_code}" -X POST "$url" -H "$header")"; then
      curl_rc=0
    else
      curl_rc=$?
    fi
    if ((curl_rc == 0)) && [[ "$status" =~ ^2[0-9][0-9]$ ]]; then
      return 0
    fi
    printf "world-controller POST failed (attempt %s/5): HTTP %s\n" "$try" "${status:-connection error}" >&2
    cat "$HTTP_BODY" >&2 || true
    rm -f -- "$HTTP_BODY"
    HTTP_BODY=""
    sleep 2
  done
  return 22
}

# The controller calls below are intentionally step-specific.
post_controller http://world-controller:8090/clock/event-019 'X-Clock-Token: garage-adu-rental-conversion-25d-clock-20260824'
post_controller http://world-controller:8090/releases/release-011 'X-Release-Token: garage-adu-rental-conversion-25d-release-011-20260824-token'
