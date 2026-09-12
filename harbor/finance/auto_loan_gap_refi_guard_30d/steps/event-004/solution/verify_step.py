#!/usr/bin/env python3
import json, os, sys
from pathlib import Path
TESTS_DIR = Path(os.environ.get("HARBOR_TESTS_DIR", "/tests"))
def verify(spec):
    if str(TESTS_DIR) not in sys.path: sys.path.insert(0, str(TESTS_DIR))
    import run_verifier
    run_verifier._load_rubric_package()
    run_verifier.validate_stage_evidence(int(spec["virtual_stage"]))
    env = run_verifier.HarborEvidence(run_verifier.EVIDENCE_ROOT)
    reports, detail = run_verifier._run_module("stage_" + str(spec["virtual_stage"]), env, spec["step"])
    actual = {str(r["check_id"]): float(r["weight"]) for r in reports}
    declared = {str(r["check_id"]): float(r["weight"]) for r in spec.get("expected_checks", [])}
    failed = [r for r in reports if not r["passed"]]
    print(f"{spec['step']}: stage {spec['virtual_stage']} earned {detail['raw_earned_score']}/{detail['eligible_weight']}")
    for row in failed: print(f"FAIL {row['check_id']} weight={row['weight']}")
    return 1 if failed or actual != declared else 0
if __name__ == "__main__": raise SystemExit(verify(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))))

