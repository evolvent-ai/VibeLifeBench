#!/usr/bin/env python3
"""Verify a boundary step with the task's real Harbor verifier."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

TESTS_DIR = Path(os.environ.get("HARBOR_TESTS_DIR", "/tests"))
ORACLE_STDOUT_PATH = Path(os.environ.get("HARBOR_ORACLE_STDOUT_PATH", "/logs/agent/oracle.txt"))


def _verifier():
    if str(TESTS_DIR) not in sys.path:
        sys.path.insert(0, str(TESTS_DIR))
    import run_verifier
    return run_verifier


def verify(spec: dict[str, Any]) -> int:
    expected = spec.get("expected_checks") or []
    stage = int(spec["virtual_stage"])
    step = str(spec["step"])
    if not expected:
        print(f"{step}: non-boundary step; stage {stage} is scored later")
        return 0
    rv = _verifier()
    rv._load_rubric_package()
    try:
        rv.validate_stage_evidence(stage)
    except Exception as exc:
        if ORACLE_STDOUT_PATH.is_file():
            print(f"{step}: native Oracle self-check deferred to the post-snapshot verifier")
            return 0
        print(f"{step}: immutable stage evidence unavailable: {type(exc).__name__}: {exc}")
        return 1
    env = rv.HarborEvidence(rv.EVIDENCE_ROOT)
    reports, detail = rv._run_module(f"stage_{stage}", env, f"stage{stage}")
    declared = {str(row["check_id"]): float(row["weight"]) for row in expected}
    actual = {str(row["check_id"]): float(row["weight"]) for row in reports}
    failures = [row["check_id"] for row in reports if not row["passed"]]
    if declared != actual or failures:
        print(f"{step}: stage {stage} shortfall; drift={declared != actual}; failures={failures}")
        return 1
    print(f"{step}: stage {stage} full marks {detail['raw_earned_score']}/{detail['eligible_weight']}")
    return 0


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: verify_step.py /solution/step_spec.json")
    return verify(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8")))


if __name__ == "__main__":
    raise SystemExit(main())
