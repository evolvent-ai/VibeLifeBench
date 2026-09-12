#!/usr/bin/env python3
import json, os, sys
from pathlib import Path

def main():
    spec=json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
    if not spec.get('expected_checks'):
        print(f"{spec['step']}: non-boundary step (stage {spec['virtual_stage']})")
        return 0
    tests=Path(os.environ.get('HARBOR_TESTS_DIR','/tests'))
    sys.path.insert(0,str(tests))
    import run_verifier
    run_verifier._load_rubric_package()
    run_verifier.validate_stage_evidence(int(spec['virtual_stage']))
    env=run_verifier.HarborEvidence(run_verifier.EVIDENCE_ROOT)
    reports, detail=run_verifier._run_module(f"stage_{spec['virtual_stage']}", env, f"stage{spec['virtual_stage']}")
    return 0 if all(r['passed'] for r in reports) else 1

if __name__ == '__main__': raise SystemExit(main())
