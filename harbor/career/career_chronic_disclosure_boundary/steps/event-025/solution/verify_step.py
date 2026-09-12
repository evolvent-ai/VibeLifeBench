#!/usr/bin/env python3
from __future__ import annotations
import json, os, sys
from pathlib import Path
TESTS_DIR=Path(os.environ.get("HARBOR_TESTS_DIR","/tests"))
ORACLE_STDOUT_PATH=Path(os.environ.get("HARBOR_ORACLE_STDOUT_PATH","/logs/agent/oracle.txt"))
def verify(spec):
    expected=spec.get("expected_checks") or []
    if not expected:
        print(f"{spec.get('step')}: non-boundary step (stage {spec.get('virtual_stage')}) — scored at its Stage boundary")
        return 0
    if ORACLE_STDOUT_PATH.is_file():
        print(f"{spec.get('step')}: native Harbor Oracle self-check deferred until post-agent collect/snapshot verifier")
        return 0
    if str(TESTS_DIR) not in sys.path: sys.path.insert(0,str(TESTS_DIR))
    import run_verifier
    run_verifier._load_rubric_package()
    try: run_verifier.validate_stage_evidence(int(spec["virtual_stage"]))
    except Exception as exc:
        print(f"{spec.get('step')}: immutable stage evidence unavailable — {type(exc).__name__}: {exc}")
        return 1
    env=run_verifier.HarborEvidence(run_verifier.EVIDENCE_ROOT)
    reports,detail=run_verifier._run_module(f"stage_{spec['virtual_stage']}",env,f"stage{spec['virtual_stage']}")
    declared={str(x["check_id"]):float(x["weight"]) for x in expected}
    actual={str(x["check_id"]):float(x["weight"]) for x in reports}
    failed=[x for x in reports if not x["passed"]]
    print(f"{spec['step']}: stage {spec['virtual_stage']} — earned {detail['raw_earned_score']}/{detail['eligible_weight']}")
    return 0 if not failed and actual==declared else 1
if __name__=="__main__":
    raise SystemExit(verify(json.loads(Path(sys.argv[1]).read_text())))
