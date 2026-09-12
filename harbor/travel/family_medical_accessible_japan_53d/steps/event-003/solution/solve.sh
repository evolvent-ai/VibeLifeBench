#!/bin/bash
set -euo pipefail
python3 /solution/oracle.py /solution/step_spec.json
if [ "${VERIFY_STEP:-1}" = "1" ]; then
  python3 /solution/verify_step.py /solution/step_spec.json
fi
