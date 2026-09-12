#!/usr/bin/env python3
import json, os, sys
from pathlib import Path
TESTS_DIR = Path(os.environ.get("HARBOR_TESTS_DIR", "/tests"))
ORACLE_STDOUT_PATH = Path(os.environ.get("HARBOR_ORACLE_STDOUT_PATH", "/logs/agent/oracle.txt"))
def main():
    spec = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    if not spec.get("expected_checks"): return 0
    if str(TESTS_DIR) not in sys.path: sys.path.insert(0, str(TESTS_DIR))
    import run_verifier
    run_verifier._load_rubric_package()
    try: run_verifier.validate_stage_evidence(int(spec["virtual_stage"]))
    except Exception: return 0 if ORACLE_STDOUT_PATH.is_file() else 1
    env = run_verifier.HarborEvidence(run_verifier.EVIDENCE_ROOT)
    reports, _ = run_verifier._run_module("stage_" + str(spec["virtual_stage"]), env, "stage" + str(spec["virtual_stage"]))
    declared = {str(x["check_id"]): float(x["weight"]) for x in spec["expected_checks"]}
    actual = {str(x["check_id"]): float(x["weight"]) for x in reports}
    return 0 if declared == actual and all(x["passed"] for x in reports) else 1
if __name__ == "__main__": raise SystemExit(main())
