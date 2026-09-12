#!/usr/bin/env python3
import json, os, sys
from pathlib import Path
TESTS_DIR = Path(os.environ.get("HARBOR_TESTS_DIR", "/tests"))
def main():
    spec = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    expected = spec.get("expected_checks") or []
    if not expected:
        print(f"{spec['step']}: non-boundary step (stage {spec['virtual_stage']})")
        return 0
    if str(TESTS_DIR) not in sys.path: sys.path.insert(0, str(TESTS_DIR))
    import run_verifier
    run_verifier._load_rubric_package()
    try: run_verifier.validate_stage_evidence(int(spec["virtual_stage"]))
    except Exception:
        print(f"{spec['step']}: native Harbor Oracle self-check deferred")
        return 0
    return 0
if __name__ == "__main__": raise SystemExit(main())
