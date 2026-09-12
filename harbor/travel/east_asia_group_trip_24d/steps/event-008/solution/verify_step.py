#!/usr/bin/env python3
import json, os, sys
from pathlib import Path
TESTS_DIR=Path(os.environ.get("HARBOR_TESTS_DIR","/tests"))
def main():
    spec=json.loads(Path(sys.argv[1]).read_text())
    if not spec.get("expected_checks"): print(f"{spec['step']}: non-boundary step"); return 0
    sys.path.insert(0,str(TESTS_DIR))
    import run_verifier as rv
    try: rv.validate_stage_evidence(int(spec["virtual_stage"]))
    except Exception: print(f"{spec['step']}: deferred"); return 0
    env=rv.HarborEvidence(rv.EVIDENCE_ROOT); reports,detail=rv._run_module(f"stage_{spec['virtual_stage']}",env,f"stage{spec['virtual_stage']}")
    declared={str(x["check_id"]):float(x["weight"]) for x in spec["expected_checks"]}; actual={str(x["check_id"]):float(x["weight"]) for x in reports}
    failed=[x for x in reports if not x["passed"]]
    print(f"{spec['step']}: earned {detail['raw_earned_score']}/{detail['eligible_weight']}")
    return 0 if not failed and actual==declared else 1
if __name__=="__main__": raise SystemExit(main())
