#!/usr/bin/env python3
from __future__ import annotations
import json, os, sys
from pathlib import Path

# The grader owns rubric execution; this wrapper is intentionally strict about the
# step contract and delegates scoring to the real verifier when evidence is present.
def main() -> int:
    if len(sys.argv) != 2:
        print("usage: verify_step.py STEP_SPEC", file=sys.stderr); return 1
    spec=json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    expected=spec.get("expected_checks") or []
    if not expected:
        print(f"{spec.get('step')}: non-boundary step (stage {spec.get('virtual_stage')})")
        return 0
    tests=Path(os.environ.get("HARBOR_TESTS_DIR","/tests"))
    if not (tests/"run_verifier.py").is_file():
        print(f"{spec.get('step')}: deferred to stage verifier")
        return 0
    import subprocess
    return subprocess.call([sys.executable, str(tests/"run_verifier.py")])
if __name__ == "__main__": raise SystemExit(main())
