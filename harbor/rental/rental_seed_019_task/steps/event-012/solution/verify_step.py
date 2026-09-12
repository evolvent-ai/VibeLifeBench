#!/usr/bin/env python3
"""Verify a boundary step through the task's real verifier."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

TESTS_DIR = Path(os.environ.get("HARBOR_TESTS_DIR", "/tests"))
ORACLE_STDOUT_PATH = Path(os.environ.get("HARBOR_ORACLE_STDOUT_PATH", "/logs/agent/oracle.txt"))


def verify(spec: dict[str, Any]) -> int:
    expected = spec.get("expected_checks") or []
    stage = int(spec["virtual_stage"])
    step = spec["step"]
    if not expected:
        print(f"{step}: no boundary checks declared for stage {stage}")
        return 0
    if str(TESTS_DIR) not in sys.path:
        sys.path.insert(0, str(TESTS_DIR))
    import run_verifier

    run_verifier._load_rubric_package()
    try:
        run_verifier.validate_stage_evidence(stage)
    except Exception as exc:
        if ORACLE_STDOUT_PATH.is_file():
            print(f"{step}: native Oracle self-check deferred to post-snapshot verifier")
            return 0
        print(f"{step}: stage evidence unavailable: {type(exc).__name__}: {exc}")
        return 1
    env = run_verifier.HarborEvidence(run_verifier.EVIDENCE_ROOT)
    reports, detail = run_verifier._run_module(f"stage_{stage}", env, f"stage{stage}")
    declared = {str(row["check_id"]): float(row["weight"]) for row in expected}
    actual = {str(row["check_id"]): float(row["weight"]) for row in reports}
    failures = [row for row in reports if not row["passed"]]
    print(f"{step}: earned {detail['raw_earned_score']}/{detail['eligible_weight']}")
    return 0 if not failures and declared == actual else 1


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: verify_step.py STEP_SPEC")
    return verify(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8")))


if __name__ == "__main__":
    raise SystemExit(main())
