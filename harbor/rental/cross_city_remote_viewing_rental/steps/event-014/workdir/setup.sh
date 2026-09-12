# Generated Harbor step setup
# The script is removed after it runs so later releases stay hidden.
#!/bin/bash
set -euo pipefail
trap 'rm -f -- "$0"' EXIT

export NO_PROXY="world-controller,${NO_PROXY:-}"
export no_proxy="world-controller,${no_proxy:-}"

ready=0
for i in $(seq 1 30); do
  if curl -sf http://world-controller:8090/health >/dev/null 2>&1; then
    ready=1
    break
  fi
  sleep 2
done
[ "$ready" = 1 ] || { echo "world-controller did not become ready" >&2; exit 1; }

post_controller() {
  local url="$1"
  local header="$2"
  for try in 1 2 3 4 5; do
    if curl -fsS -X POST "$url" -H "$header" >/dev/null; then
      return 0
    fi
    sleep 2
  done
  echo "controller POST failed after 5 attempts: $url" >&2
  return 22
}
post_controller 'http://world-controller:8090/clock/event-014' 'X-Clock-Token: cross-city-remote-viewing-clock-20260824'
