"""Pin L5 — scoring contract coordinates.

The verifier's flat pool is whatever the bundled rubrics add up to, and
``run_verifier.EXPECTED_CHECK_COUNT`` guards "a check vanished". This pins the
coordinates that gate relies on: every stage module imports cleanly without a
live environment, exports a well-formed CHECKS table (unique ids, callable
checkers, positive weights), the check count matches the verifier's constant,
and the compatibility ``checks`` module stays empty so no check silently
disappears from the pool.

Runnable standalone: ``python3 tests/test_scoring_contract.py``.
"""
import importlib
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

STAGE_MODULES = [f"stage_{i}" for i in range(24)] + ["cross_stage", "final"]


def _expected_check_count():
    with open(os.path.join(HERE, "run_verifier.py"), encoding="utf-8") as fh:
        match = re.search(r"EXPECTED_CHECK_COUNT\s*=\s*(\d+)", fh.read())
    assert match, "run_verifier.py lost its EXPECTED_CHECK_COUNT constant"
    return int(match.group(1))


def test_all_check_tables_wellformed():
    if os.path.join(HERE) not in __import__("sys").path:
        __import__("sys").path.insert(0, os.path.join(HERE))
    seen_ids, total_weight = set(), 0.0
    for module_name in STAGE_MODULES:
        module = importlib.import_module(f"rubrics.{module_name}")
        checks = getattr(module, "CHECKS", None)
        assert isinstance(checks, (list, tuple)) and checks, f"{module_name}.CHECKS missing/empty"
        for entry in checks:
            assert len(entry) == 3, f"{module_name} malformed check entry: {entry!r}"
            check_id, fn, weight = entry
            assert callable(fn), f"{module_name}:{check_id} checker is not callable"
            assert weight > 0, f"{module_name}:{check_id} weight must be positive, got {weight}"
            assert check_id not in seen_ids, f"duplicate check id: {check_id}"
            seen_ids.add(check_id)
            total_weight += weight
    assert total_weight > 0, "rubric pool weight collapsed to zero"
    return seen_ids, total_weight


def test_check_count_matches_verifier_constant():
    if os.path.join(HERE) not in __import__("sys").path:
        __import__("sys").path.insert(0, os.path.join(HERE))
    seen_ids, _total = test_all_check_tables_wellformed()
    expected = _expected_check_count()
    assert len(seen_ids) == expected, (
        f"rubrics expose {len(seen_ids)} checks but run_verifier expects {expected}"
    )


def test_compatibility_module_stays_empty():
    if os.path.join(HERE) not in __import__("sys").path:
        __import__("sys").path.insert(0, os.path.join(HERE))
    checks = importlib.import_module("rubrics.checks")
    assert tuple(checks.CHECKS) == (), "rubrics.checks must remain a compatibility shim"


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"ok  {name}")
