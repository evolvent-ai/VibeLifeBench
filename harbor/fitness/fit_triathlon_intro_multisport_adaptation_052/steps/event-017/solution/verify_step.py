#!/usr/bin/env python3
from __future__ import annotations
import json
import os
import sys
from pathlib import Path

TESTS_DIR = Path(os.environ.get("HARBOR_TESTS_DIR", "/tests"))
ORACLE_STDOUT_PATH = Path(os.environ.get("HARBOR_ORACLE_STDOUT_PATH", "/logs/agent/oracle.txt"))

def verify(spec: dict) -> int:
    expected = spec.get("expected_checks") or []
    if not expected:
        return 0
    if str(TESTS_DIR) not in sys.path:
        sys.path.insert(0, str(TESTS_DIR))
    import run_verifier
    run_verifier._load_rubric_package()
    try:
        run_verifier.validate_stage_evidence(int(spec["virtual_stage"]))
    except Exception:
        return 0 if ORACLE_STDOUT_PATH.is_file() else 1
    env = run_verifier.HarborEvidence(run_verifier.EVIDENCE_ROOT)
    reports, detail = run_verifier._run_module(f"stage_{int(spec['virtual_stage'])}", env, f"stage{spec['virtual_stage']}")
    declared = {str(row["check_id"]): float(row["weight"]) for row in expected}
    actual = {str(row["check_id"]): float(row["weight"]) for row in reports}
    return 0 if actual == declared and all(row["passed"] for row in reports) else 1

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: verify_step.py /solution/step_spec.json")
    raise SystemExit(verify(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))))
