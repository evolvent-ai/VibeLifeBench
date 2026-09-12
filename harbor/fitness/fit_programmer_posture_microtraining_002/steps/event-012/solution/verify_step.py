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
print(f"step={spec.get('step', '?')} expected_checks={len(expected)} recorded")
