#!/usr/bin/env python3
from __future__ import annotations
import json, os, sys
from pathlib import Path
TESTS_DIR=Path(os.environ.get("HARBOR_TESTS_DIR","/tests"))
def main():
    spec=json.loads(Path(sys.argv[1]).read_text(encoding="utf-8")); expected=spec.get("expected_checks") or []
    if not expected: return 0
    if str(TESTS_DIR) not in sys.path: sys.path.insert(0,str(TESTS_DIR))
    import run_verifier; run_verifier._load_rubric_package(); env=run_verifier.HarborEvidence(run_verifier.EVIDENCE_ROOT); stage=int(spec["virtual_stage"])
    try: run_verifier.validate_stage_evidence(stage); reports,detail=run_verifier._run_module(f"stage_{stage}",env,f"stage{stage}")
    except Exception as exc: print(f"self-check unavailable: {exc}"); return 1
    declared={str(r["check_id"]):float(r["weight"]) for r in expected}; actual={str(r["check_id"]):float(r["weight"]) for r in reports}
    for r in reports:
        if not r["passed"]: print(f"FAIL {r['check_id']}")
    return 1 if declared!=actual or any(not r["passed"] for r in reports) else 0
if __name__=="__main__": raise SystemExit(main())
