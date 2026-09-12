#!/usr/bin/env python3
from __future__ import annotations
import json
import os
import subprocess
import sys
from pathlib import Path

def verify(spec: dict) -> int:
    boundary = spec.get("stage_boundary") is True
    expected = spec.get("expected_checks")
    if boundary and (not isinstance(expected, list) or not expected):
        raise ValueError("stage-boundary step must declare expected_checks")
    if not boundary and expected:
        raise ValueError("non-boundary step must not declare expected_checks")
    for row in expected or []:
        if not isinstance(row, dict) or not isinstance(row.get("check_id"), str):
            raise ValueError("expected_checks entries require check_id")
        weight = row.get("weight")
        if isinstance(weight, bool) or not isinstance(weight, (int, float)) or weight <= 0:
            raise ValueError("invalid expected check weight")
    verifier = Path(os.environ.get("HARBOR_RUN_VERIFIER", "/tests/run_verifier.py"))
    if not verifier.is_file():
        raise FileNotFoundError(f"required Harbor verifier is missing: {verifier}")
    env = dict(os.environ, HARBOR_STEP_NAME=str(spec.get("step", "")), VIRTUAL_STAGE=str(spec.get("virtual_stage", 0)), STAGE_BOUNDARY="1" if boundary else "0", RUN_STAGE_RUBRIC="1" if boundary else "0")
    result = subprocess.run([sys.executable, str(verifier)], env=env, check=False)
    if result.returncode:
        raise RuntimeError(f"Harbor verifier exited with status {result.returncode}")
    return 0

def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("step_spec.json")
    try:
        return verify(json.loads(path.read_text(encoding="utf-8")))
    except Exception as exc:
        print(f"verify_step error: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
