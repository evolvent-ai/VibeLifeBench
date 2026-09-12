#!/bin/bash
# Apply this step's Oracle actions, then optionally verify its declared weight.
#
# The world state this step expects (which world-controller
# releases have landed) is recorded in step_spec.json under
# expected_env; Harbor applies it via workdir/setup.sh before the
# agent acts, so by the time this runs the precondition holds.
#
# Self-verification is opt-in because Harbor freezes the stage evidence after
# the solution process returns.
set -euo pipefail
python3 /solution/oracle.py /solution/step_spec.json
if [ "${VERIFY_STEP:-0}" = "1" ]; then
  python3 /solution/verify_step.py /solution/step_spec.json
fi
