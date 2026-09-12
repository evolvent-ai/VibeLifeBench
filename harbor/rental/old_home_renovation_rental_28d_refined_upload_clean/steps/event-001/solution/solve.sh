#!/bin/bash
# Reference solution for event-001: apply this step's agent actions,
# then verify they earn this step's declared rubric weight.
#
# The world state this step expects (which world-controller
# releases have landed) is recorded in step_spec.json under
# expected_env; Harbor applies it via workdir/setup.sh before the
# agent acts, so by the time this runs the precondition holds.
#
# VERIFY_STEP=0 skips self-verification (useful when replaying a
# step whose Stage is scored at a later boundary step).
set -euo pipefail
python3 /solution/oracle.py /solution/step_spec.json
if [ "${VERIFY_STEP:-1}" = "1" ]; then
  python3 /solution/verify_step.py /solution/step_spec.json
fi
