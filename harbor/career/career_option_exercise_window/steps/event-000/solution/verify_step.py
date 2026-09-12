#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path

TESTS_DIR = Path(os.environ.get("HARBOR_TESTS_DIR", "/tests"))
ORACLE_STDOUT_PATH = Path(os.environ.get("HARBOR_ORACLE_STDOUT_PATH", "/logs/agent/oracle.txt"))

def verify(spec):
    expected = spec.get("expected_checks") or []
    if not expected:
        return 0
    if str(TESTS_DIR) not in sys.path:
        sys.path.insert(0, str(TESTS_DIR))
    import run_verifier
    run_verifier._load_rubric_package()
    try:
        run_verifier.HarborEvidence(run_verifier.EVIDENCE_ROOT).validate_stage(int(spec["virtual_stage"]))
    except Exception:
        if ORACLE_STDOUT_PATH.is_file():
            return 0
        return 1
    env = run_verifier.HarborEvidence(run_verifier.EVIDENCE_ROOT)
    reports, detail = run_verifier._run_module(f"stage_{spec['virtual_stage']}", env, f"stage{spec['virtual_stage']}")
    actual = {str(r["check_id"]): float(r["weight"]) for r in reports}
    declared = {str(r["check_id"]): float(r["weight"]) for r in expected}
    return 0 if actual == declared and not any(not r["passed"] for r in reports) else 1

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: verify_step.py /solution/step_spec.json")
    raise SystemExit(verify(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))))
