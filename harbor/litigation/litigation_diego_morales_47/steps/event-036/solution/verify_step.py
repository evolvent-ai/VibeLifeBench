#!/usr/bin/env python3
from __future__ import annotations
import json
import os
import sys
from pathlib import Path

TESTS_DIR = Path(os.environ.get("HARBOR_TESTS_DIR", "/tests"))

def main() -> int:
    if len(sys.argv) != 2:
        print("usage: verify_step.py /solution/step_spec.json", file=sys.stderr)
        return 1
    spec = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    expected = spec.get("expected_checks") or []
    if not expected:
        print(f"{spec['step']}: non-boundary step")
        return 0
    if str(TESTS_DIR) not in sys.path:
        sys.path.insert(0, str(TESTS_DIR))
    import run_verifier
    run_verifier._load_rubric_package()
    try:
        run_verifier.validate_stage_evidence(int(spec["virtual_stage"]))
    except Exception:
        if Path(os.environ.get("HARBOR_ORACLE_STDOUT_PATH", "/logs/agent/oracle.txt")).is_file():
            print(f"{spec['step']}: deferred")
            return 0
        return 1
    env = run_verifier.HarborEvidence(run_verifier.EVIDENCE_ROOT)
    reports, detail = run_verifier._run_module(f"stage_{spec['virtual_stage']}", env, f"stage{spec['virtual_stage']}")
    declared = {str(row["check_id"]): float(row["weight"]) for row in expected}
    actual = {str(row["check_id"]): float(row["weight"]) for row in reports}
    failed = [row for row in reports if not row["passed"]]
    ok = not failed and declared == actual
    print(f"{spec['step']}: stage {spec['virtual_stage']} [{('FULL MARKS' if ok else 'SHORTFALL')}]")
    return 0 if ok else 1

if __name__ == "__main__":
    raise SystemExit(main())
