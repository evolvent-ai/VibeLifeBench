#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

TESTS_DIR = Path(os.environ.get("HARBOR_TESTS_DIR", "/tests"))


def verify(spec: dict[str, Any]) -> int:
    if str(TESTS_DIR) not in sys.path:
        sys.path.insert(0, str(TESTS_DIR))
    import run_verifier
    stage = int(spec["virtual_stage"])
    run_verifier._load_rubric_package()
    run_verifier.validate_stage_evidence(stage)
    env = run_verifier.HarborEvidence(run_verifier.EVIDENCE_ROOT)
    env.current_stage = stage
    reports, detail = run_verifier._run_module(f"stage_{stage}", env, f"stage{stage}")
    declared = {str(row["check_id"]): float(row["weight"]) for row in spec.get("expected_checks", [])}
    actual = {str(row["check_id"]): float(row["weight"]) for row in reports}
    failures = [row for row in reports if not row["passed"]]
    ok = actual == declared and not failures
    print(f"{spec['step']}: stage {stage} earned {detail['raw_earned_score']}/{detail['eligible_weight']} [{'FULL MARKS' if ok else 'SHORTFALL'}]")
    return 0 if ok else 1


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: verify_step.py /solution/step_spec.json")
    raise SystemExit(verify(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))))
