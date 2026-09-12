#!/bin/bash
set -uo pipefail
mkdir -p /logs/verifier
export PYTHONDONTWRITEBYTECODE=1
if python /tests/run_verifier.py; then exit 0; fi

# Harbor reads reward.json even when the verifier process exits nonzero. Keep
# every reward value numeric and put infrastructure diagnostics in checks.json.
test -f /logs/verifier/reward.json ||
  printf '{"reward":0.0,"verifier_ok":0.0}\n' > /logs/verifier/reward.json
test -f /logs/verifier/checks.json ||
  printf '{"status":"infrastructure_error","errors":["verifier exited before writing diagnostics"]}\n' > /logs/verifier/checks.json
exit 1
