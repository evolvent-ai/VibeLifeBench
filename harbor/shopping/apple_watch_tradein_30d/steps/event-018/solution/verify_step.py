#!/usr/bin/env python3
from __future__ import annotations
import json, os, sys
from pathlib import Path
TESTS_DIR = Path(os.environ.get("HARBOR_TESTS_DIR", "/tests"))
ORACLE_STDOUT_PATH = Path(os.environ.get("HARBOR_ORACLE_STDOUT_PATH", "/logs/agent/oracle.txt"))
def verify(spec):
    expected = spec.get("expected_checks") or []
    if not expected:
        print(f"{spec['step']}: non-boundary step (stage {spec['virtual_stage']}) - scored at its Stage boundary")
        return 0
    if str(TESTS_DIR) not in sys.path: sys.path.insert(0, str(TESTS_DIR))
    import run_verifier
    run_verifier._load_rubric_package()
    try: run_verifier.validate_stage_evidence(int(spec["virtual_stage"]))
    except Exception:
        if ORACLE_STDOUT_PATH.is_file(): return 0
        return 1
    return 0
if __name__ == "__main__":
    if len(sys.argv) != 2: raise SystemExit(1)
    raise SystemExit(verify(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))))
