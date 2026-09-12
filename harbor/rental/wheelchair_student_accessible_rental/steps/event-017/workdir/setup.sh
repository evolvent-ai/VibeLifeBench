#!/bin/bash
export NO_PROXY="world-controller,calendar,email,legal-search,listing-platform,maps,notification-hub,notion,review-platform,localhost,127.0.0.1"
export no_proxy="$NO_PROXY"
for i in $(seq 1 30); do curl -sf http://world-controller:8090/health >/dev/null 2>&1 && break; sleep 2; done
set -euo pipefail

post_controller() {
  local path="$1" header="$2"
  for attempt in $(seq 1 5); do
    if curl -fsS -X POST "http://world-controller:8090${path}" -H "$header" >/dev/null; then
      return 0
    fi
    sleep $((attempt * 2))
  done
  return 1
}
trap 'rm -f -- "$0"' EXIT

post_controller '/clock/event-017' 'X-Clock-Token: wheelchair-clock-2b8a9e1f4c6d7e8a'
post_controller '/releases/release-011' 'X-Release-Token: wheelchair-release-011-2b8a9e1f4c6d7e8a9b7c6d5e4f3a2b1c'
