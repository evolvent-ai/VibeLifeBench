#!/bin/bash
set -uo pipefail
mkdir -p /logs/verifier
# The verifier imports from /tests, which is the delivered tree itself. Without
# this, every run leaves __pycache__/*.pyc next to the sources - build artifacts
# the delivery must not carry, and which reappear after each cleanup because the
# run regenerates them.
export PYTHONDONTWRITEBYTECODE=1
if python /tests/run_verifier.py; then exit 0; fi
# The verifier failed. It normally writes its own numeric reward.json - do NOT
# overwrite that. Harbor reads the reward file and discards our exit code. Keep
# the health bit numeric because
# Harbor parses every reward.json value as a numeric reward; diagnostics belong in
# checks.json. Synthesize both files only if Python died before writing them.
test -f /logs/verifier/reward.json ||
  printf '{"reward":0.0,"verifier_ok":0.0}\n' > /logs/verifier/reward.json
test -f /logs/verifier/checks.json ||
  printf '{"status":"infrastructure_error","errors":["verifier exited before writing diagnostics"]}\n' > /logs/verifier/checks.json
exit 1
