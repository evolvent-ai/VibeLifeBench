#!/usr/bin/env python3
from __future__ import annotations
import json
import os
import sys
from pathlib import Path

TESTS_DIR = Path(os.environ.get("HARBOR_TESTS_DIR", "/tests"))
ORACLE_STDOUT = Path(os.environ.get("HARBOR_ORACLE_STDOUT_PATH", "/logs/agent/oracle.txt"))

def main() -> int:
    if len(sys.argv) != 2:
        print("usage: verify_step.py STEP_SPEC", file=sys.stderr)
        return 1
    spec = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    expected = spec.get("expected_checks") or []
    if not expected:
        print(f"{spec['step']}: non-boundary step (stage {spec['virtual_stage']})")
        return 0
    if str(TESTS_DIR) not in sys.path:
        sys.path.insert(0, str(TESTS_DIR))
    import run_verifier
    run_verifier._load_rubric_package()
    try:
        run_verifier.validate_stage_evidence(int(spec["virtual_stage"]))
    except Exception as exc:
        if ORACLE_STDOUT.is_file():
            print(f"{spec['step']}: self-check deferred until post-collect verifier")
            return 0
        print(f"{spec['step']}: evidence unavailable: {type(exc).__name__}: {exc}")
        return 1
    env = run_verifier.HarborEvidence(run_verifier.EVIDENCE_ROOT)
    reports, detail = run_verifier._run_module(f"stage_{spec['virtual_stage']}", env, spec["step"])
    declared = {str(row["check_id"]): float(row["weight"]) for row in expected}
    actual = {str(row["check_id"]): float(row["weight"]) for row in reports}
    failures = [row["check_id"] for row in reports if not row["passed"]]
    print(f"{spec['step']}: earned {detail['raw_earned_score']}/{detail['eligible_weight']}")
    return 0 if not failures and actual == declared else 1

if __name__ == "__main__":
    raise SystemExit(main())
