#!/usr/bin/env python3
"""Verify this boundary step through the task's real rubric implementation."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

TESTS_DIR = Path(os.environ.get("HARBOR_TESTS_DIR", "/tests"))


def _verifier():
    if str(TESTS_DIR) not in sys.path:
        sys.path.insert(0, str(TESTS_DIR))
    import run_verifier  # noqa: PLC0415

    return run_verifier


def verify(spec: dict[str, Any]) -> int:
    expected = spec.get("expected_checks") or []
    stage = int(spec["virtual_stage"])
    step = str(spec["step"])
    if not expected:
        print(f"{step}: no boundary checks declared for stage {stage}")
        return 0

    rv = _verifier()
    env = rv.HarborEvidence(rv.EVIDENCE_ROOT)
    try:
        env.current_stage = stage
        env.validate_stage(stage)
        module = rv._load(f"stage_{stage}")
        reports, detail = rv._run(module.CHECKS, env, f"stage{stage}")
    except Exception as exc:  # noqa: BLE001
        print(f"{step}: stage {stage} verification failed: {type(exc).__name__}: {exc}")
        return 1

    declared = {str(row["check_id"]): float(row["weight"]) for row in expected}
    actual = {str(row["check_id"]): float(row["weight"]) for row in reports}
    failures = [row for row in reports if not row["passed"]]
    drift = declared != actual
    status = "FULL MARKS" if not failures and not drift else "SHORTFALL"
    print(
        f"{step}: stage {stage} - earned {detail['raw_earned_score']}/"
        f"{detail['eligible_weight']} [{status}]"
    )
    if drift:
        print(f"   DRIFT rubric={actual} spec={declared}")
    for row in failures:
        print(f"   FAIL {row['check_id']} (weight {row['weight']})")
    return 0 if not failures and not drift else 1


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: verify_step.py /solution/step_spec.json")
    spec = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    return verify(spec)


if __name__ == "__main__":
    raise SystemExit(main())
