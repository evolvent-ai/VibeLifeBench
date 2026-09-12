#!/bin/sh
set -eu
BASE=$(CDPATH= cd -- "$(dirname "$0")" && pwd)
python3 "$BASE/oracle.py" "$BASE/step_spec.json"
if [ "${VERIFY_STEP:-0}" = "1" ]; then
  python3 "$BASE/verify_step.py" "$BASE/step_spec.json"
fi
