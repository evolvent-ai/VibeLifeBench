#!/bin/bash
set -euo pipefail
python3 /solution/oracle.py /solution/step_spec.json
if [[ "${VERIFY_STEP:-0}" == "1" ]]; then
  python3 /solution/verify_step.py
fi
