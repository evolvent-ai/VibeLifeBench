#!/bin/bash
set -euo pipefail
HTTP_BODY=""
trap 'rm -f -- "$0"' EXIT

# Fresh environments may expose the controller before its database volumes are ready.
ready=0
for i in $(seq 1 30); do
  if curl --noproxy '*' -sf http://world-controller:8090/health >/dev/null 2>&1; then
    ready=1
    break
  fi
  sleep 2
done
if ((ready != 1)); then
  printf '%s\n' 'world-controller did not become healthy within 60 seconds' >&2
  exit 1
fi

controller_post() {
  local url="$1" header="$2" body status curl_rc attempt
  for attempt in $(seq 1 15); do
    body="$(mktemp)"
    if status="$(curl --noproxy '*' -sS --connect-timeout 5 --max-time 40 -o "$body" -w '%{http_code}' -X POST "$url" -H "$header")"; then
      curl_rc=0
    else
      curl_rc=$?
    fi
    if ((curl_rc == 0)) && [[ "$status" =~ ^2[0-9][0-9]$ ]]; then
      rm -f -- "$body"
      return 0
    fi
    if ((attempt < 15)) && { ((curl_rc != 0)) || [[ "$status" == "409" ]] || [[ "$status" =~ ^5[0-9][0-9]$ ]]; }; then
      rm -f -- "$body"
      sleep 2
      continue
    fi
    if ((curl_rc != 0)); then
      cat "$body" >&2 || true
      rm -f -- "$body"
      return "$curl_rc"
    fi
    printf 'world-controller POST failed: HTTP %s\n' "$status" >&2
    cat "$body" >&2 || true
    rm -f -- "$body"
    return 22
  done
  return 22
}

controller_post "http://world-controller:8090/clock/event-024" "X-Clock-Token: baby-stroller-safety-standard-30d-clock-token"
