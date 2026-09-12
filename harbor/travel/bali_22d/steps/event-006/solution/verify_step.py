#!/usr/bin/env python3
import json, os, sys
from pathlib import Path
TESTS_DIR=Path(os.environ.get("HARBOR_TESTS_DIR","/tests"))
def main():
    spec=json.loads(Path(sys.argv[1]).read_text()); expected=spec.get("expected_checks") or []
    if not expected: return 0
    if str(TESTS_DIR) not in sys.path: sys.path.insert(0,str(TESTS_DIR))
    import run_verifier as rv
    rv._load_rubric_package(); rv.validate_stage_evidence(int(spec["virtual_stage"]))
    env=rv.HarborEvidence(rv.EVIDENCE_ROOT); reports,detail=rv._run_module(f"stage_{spec["virtual_stage"]}",env,f"stage{spec["virtual_stage"]}")
    actual={str(r["check_id"]):float(r["weight"]) for r in reports}; declared={str(r["check_id"]):float(r["weight"]) for r in expected}
    return 0 if actual==declared and all(r["passed"] for r in reports) else 1
if __name__=="__main__": raise SystemExit(main())
