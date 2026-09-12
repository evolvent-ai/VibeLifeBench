#!/usr/bin/env python3
from __future__ import annotations
import json
import sys
from pathlib import Path
REQUIRED = ("event_id", "response_paraphrase", "expected_env", "expected_checks", "expected_stage_weight")
def main() -> int:
    if len(sys.argv) != 2:
        return 1
    try:
        spec = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
        if any(key not in spec for key in REQUIRED):
            raise ValueError("missing step contract field")
        if not isinstance(spec["expected_env"], dict) or not isinstance(spec["expected_checks"], list):
            raise ValueError("invalid step contract types")
        if not isinstance(spec["expected_stage_weight"], (int, float)):
            raise ValueError("invalid stage weight")
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"verify_step error: {exc}", file=sys.stderr)
        return 1
    print("verify_step: PASS")
    return 0
if __name__ == "__main__":
    raise SystemExit(main())

