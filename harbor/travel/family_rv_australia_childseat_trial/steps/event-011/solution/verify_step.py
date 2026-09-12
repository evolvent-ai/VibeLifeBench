#!/usr/bin/env python3
from __future__ import annotations
import json
import os
import sys
from pathlib import Path
from typing import Any

TESTS_DIR = Path(os.environ.get("HARBOR_TESTS_DIR", "/tests"))

def verify(spec: dict[str, Any]) -> int:
    expected = spec.get("expected_checks") or []
    if not expected:
        return 0
    if str(TESTS_DIR) not in sys.path:
        sys.path.insert(0, str(TESTS_DIR))
    import run_verifier
    run_verifier._load_rubric_package()
    stage = int(spec["virtual_stage"])
    try:
        run_verifier.validate_stage_evidence(stage)
        env = run_verifier.HarborEvidence(run_verifier.EVIDENCE_ROOT)
        reports, detail = run_verifier._run_module(f"stage_{stage}", env, f"stage{stage}")
    except Exception as exc:
        print(f"{spec['step']}: stage {stage} self-check unavailable - {type(exc).__name__}: {exc}")
        return 1
    declared = {str(row["check_id"]): float(row["weight"]) for row in expected}
    actual = {str(row["check_id"]): float(row["weight"]) for row in reports}
    failures = [row for row in reports if not row["passed"]]
    if declared != actual or failures:
        print(f"{spec['step']}: stage {stage} earned {detail['raw_earned_score']}/{detail['eligible_weight']}")
        for row in failures:
            print(f"FAIL {row['check_id']} weight={row['weight']}")
        return 1
    return 0

def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: verify_step.py STEP_SPEC")
    return verify(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8")))

if __name__ == "__main__":
    raise SystemExit(main())
