#!/bin/bash
set -euo pipefail
HTTP_BODY=""
trap 'rm -f -- "$0"' EXIT

controller_post() {
  local url="$1" header="$2" body status curl_rc
  for attempt in 1 2 3 4 5; do
    body="$(mktemp)"
    if status="$(curl --noproxy "*" -sS --connect-timeout 5 --max-time 40 -o "$body" -w '%{http_code}' -X POST "$url" -H "$header")"; then
      curl_rc=0
    else
      curl_rc=$?
    fi
    if ((curl_rc == 0)) && [[ "$status" =~ ^2[0-9][0-9]$ ]]; then
      rm -f -- "$body"
      return 0
    fi
    if ((curl_rc != 0)); then
      printf 'world-controller POST transport failed (attempt %s/5)\n' "$attempt" >&2
    else
      printf 'world-controller POST failed: HTTP %s (attempt %s/5)\n' "$status" "$attempt" >&2
    fi
    cat "$body" >&2 || true
    rm -f -- "$body"
    [[ "$attempt" == 5 ]] && return 22
    sleep 2
  done
  return 22
}

ready=0
for i in $(seq 1 30); do
  if curl --noproxy "*" -sf --connect-timeout 2 --max-time 5 http://world-controller:8090/health >/dev/null 2>&1; then
    ready=1
    break
  fi
  sleep 2
done
[ "$ready" = 1 ] || { echo "world-controller did not become ready" >&2; exit 1; }

controller_post "http://world-controller:8090/clock/event-006" "X-Clock-Token: dragon-boat-037-clock-20260824"
controller_post "http://world-controller:8090/releases/release-001" "X-Release-Token: dragon-boat-037-release-001-20260824"
