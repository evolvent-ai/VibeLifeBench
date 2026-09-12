#!/usr/bin/env python3
from __future__ import annotations
import json
import sys
from pathlib import Path

spec = json.loads(Path(sys.argv[1] if len(sys.argv) > 1 else "step_spec.json").read_text(encoding="utf-8"))
expected = {row.get("check_id") for row in spec.get("expected_checks", []) if isinstance(row, dict)}
if not expected:
    print(f"step={spec.get('step', '?')} no expected checks")
    raise SystemExit(0)
try:
    sys.path.insert(0, "/tests")
    from harbor_env import HarborEnv
    from run_verifier import _load_rubric_package, _run_module
    with open("/tests/services.json", encoding="utf-8") as fh:
        env = HarborEnv(json.load(fh)["mcp_servers"])
    env.set_stage(int(spec.get("stage", 0)))
    _load_rubric_package()
    reports, _ = _run_module(f"stage_{int(spec.get('stage', 0))}", env, f"stage_{int(spec.get('stage', 0))}")
    passed = {row["check_id"] for row in reports if row.get("passed")}
    missing = sorted(expected - passed)
    if missing:
        print(f"step={spec.get('step', '?')} missing_checks={missing}")
        raise SystemExit(1)
    print(f"step={spec.get('step', '?')} passed_all={len(expected)} OK")
except Exception as exc:
    print(f"step={spec.get('step', '?')} verify_step_error: {exc}")
    raise SystemExit(1)

