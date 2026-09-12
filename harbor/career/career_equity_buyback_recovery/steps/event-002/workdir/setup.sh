# Generated Harbor step setup
# The script is removed after it runs so later releases stay hidden.
#!/bin/bash
set -euo pipefail
trap 'rm -f -- "$0"' EXIT


wait_for_controller() {
  for i in $(seq 1 30); do
    if curl --noproxy '*' -fsS http://world-controller:8090/health >/dev/null 2>&1; then
      return 0
    fi
    sleep 2
  done
  return 1
}

post_controller() {
  for try in 1 2 3 4 5; do
    if curl --noproxy '*' -fsS "$@" >/dev/null; then
      return 0
    fi
    sleep 2
  done
  return 22
}

wait_for_controller
post_controller -X POST http://world-controller:8090/clock/event-002 -H 'X-Clock-Token: career-equity-clock-7f4b91c2' >/dev/null
