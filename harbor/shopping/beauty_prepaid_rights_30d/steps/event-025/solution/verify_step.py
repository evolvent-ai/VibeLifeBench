#!/usr/bin/env python3
"""Validate one step contract and, when available, its frozen stage evidence."""
from __future__ import annotations

import json
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: verify_step.py STEP_SPEC", file=sys.stderr)
        return 1
    spec_path = Path(sys.argv[1])
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    required = {"step", "virtual_stage", "source_event_id", "response", "response_paraphrase", "actions", "expected_env", "expected_checks", "expected_stage_weight"}
    missing = sorted(required - set(spec))
    if missing:
        print("missing step fields: " + ", ".join(missing), file=sys.stderr)
        return 1

    task_root = Path(__file__).resolve().parents[3]
    map_path = task_root / "environment/world-controller/step-release-map.json"
    step_map = json.loads(map_path.read_text(encoding="utf-8"))
    step_name = str(spec["step"])
    expected_meta = (step_map.get("steps") or {}).get(step_name)
    if not isinstance(expected_meta, dict):
        print(f"{step_name}: missing step-release-map entry", file=sys.stderr)
        return 1
    if (spec["source_event_id"] != expected_meta.get("source_event_id")
            or int(spec["virtual_stage"]) != int(expected_meta.get("virtual_stage", -1))):
        print(f"{step_name}: contract metadata disagrees with step-release-map", file=sys.stderr)
        return 1
    actions = spec["actions"]
    if not isinstance(actions, list) or not actions:
        print(f"{step_name}: actions must be non-empty", file=sys.stderr)
        return 1
    for action in actions:
        if not isinstance(action, dict) or action.get("kind") != "record_event":
            print(f"{step_name}: unsupported action contract", file=sys.stderr)
            return 1
        if (action.get("source_event_id") != spec["source_event_id"]
                or int(action.get("virtual_stage", -1)) != int(spec["virtual_stage"])):
            print(f"{step_name}: action metadata disagrees with step_spec", file=sys.stderr)
            return 1

    before = list(expected_meta.get("before") or [])
    released: list[str] = []
    for release_id in before:
        release_path = task_root / "environment/world-controller/releases" / f"{release_id}.json"
        release = json.loads(release_path.read_text(encoding="utf-8"))
        released.extend(release.get("source_event_ids") or [])
    expected_env = spec["expected_env"]
    if (expected_env.get("preceding_releases") != before
            or expected_env.get("released_mutations") != released):
        print(f"{step_name}: expected_env disagrees with release map", file=sys.stderr)
        return 1

    if str(task_root / "tests") not in sys.path:
        sys.path.insert(0, str(task_root / "tests"))
    try:
        module = __import__(f"rubrics.stage_{int(spec['virtual_stage'])}", fromlist=["CHECKS"])
        actual = [(str(cid), float(weight)) for cid, _fn, weight in module.CHECKS]
        declared = [(str(row["check_id"]), float(row["weight"])) for row in spec["expected_checks"]]
    except Exception as exc:
        print(f"{step_name}: rubric contract import failed: {exc}", file=sys.stderr)
        return 1
    if declared != actual or abs(float(spec["expected_stage_weight"]) - sum(weight for _, weight in actual)) > 1e-9:
        print(f"{step_name}: expected checks/weight disagree with rubric module", file=sys.stderr)
        return 1

    print(f"step={step_name} stage={spec['virtual_stage']} expected_checks={len(declared)} weight={spec['expected_stage_weight']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
