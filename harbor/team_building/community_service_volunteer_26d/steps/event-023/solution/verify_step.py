#!/usr/bin/env python3
"""Self-check a step's reference solution: did its actions earn full marks?

A step's ``solution/`` is a closed loop:

1. ``expected_env``    — the world state the step must observe (which
   world-controller releases have landed before it acts);
2. ``actions``         — the agent behaviour the reference solution performs;
3. ``expected_checks`` — the rubric checks that behaviour must satisfy.

``oracle.py`` does (2). This module closes the loop by running (3) and reporting
whether the step actually earned its declared weight.

**It scores through the real verifier, not a copy of it.** The Stage rubric is
evaluated by importing ``run_verifier``'s own ``_run_module`` / ``_run_checks``
and calling them on the same rubric module the graded run uses. An earlier
version re-implemented that loop here, which silently diverged: the real path
rejects non-Boolean checker results and malformed weights as *errors*, whereas a
hand-rolled ``checker(env) is True`` quietly treats them as a plain failure. A
self-check that is more lenient than the grader is worse than none — it certifies
solutions the grader will reject.

Only boundary steps are scored. In an offline replay, the sidecar has already
published immutable evidence and this module verifies full marks immediately.
Harbor's native Oracle runs ``solve.sh`` *before* its collect/snapshot phase;
when ``/logs/agent/oracle.txt`` identifies that lifecycle and the boundary
evidence is not published yet, the self-check is explicitly deferred to the
same verifier that Harbor invokes immediately after snapshot. Missing evidence
in every non-Oracle context remains a hard failure. A non-boundary step declares
no expected checks and exits 0 after confirming exactly that.

Exit status: 0 = the step earned everything it declared, 1 = it did not.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

TESTS_DIR = Path(os.environ.get("HARBOR_TESTS_DIR", "/tests"))
ORACLE_STDOUT_PATH = Path(
    os.environ.get("HARBOR_ORACLE_STDOUT_PATH", "/logs/agent/oracle.txt")
)


def _verifier():
    """Import the graded run's verifier module so scoring stays single-sourced."""
    if str(TESTS_DIR) not in sys.path:
        sys.path.insert(0, str(TESTS_DIR))
    import run_verifier  # noqa: PLC0415

    return run_verifier


def verify(spec: dict[str, Any]) -> int:
    expected = spec.get("expected_checks") or []
    stage = int(spec["virtual_stage"])
    step = spec["step"]

    if not expected:
        print(f"{step}: non-boundary step (stage {stage}) — scored at its Stage boundary")
        return 0

    rv = _verifier()
    rv._load_rubric_package()
    try:
        env = rv.HarborEvidence(rv.EVIDENCE_ROOT)
        env.validate_stage(stage)
    except Exception as exc:  # noqa: BLE001
        if ORACLE_STDOUT_PATH.is_file():
            print(
                f"{step}: native Harbor Oracle self-check deferred until "
                f"post-agent collect/snapshot verifier (stage {stage})"
            )
            return 0
        print(
            f"{step}: immutable stage {stage} evidence is unavailable — "
            f"{type(exc).__name__}: {exc}"
        )
        return 1

    declared = {str(row["check_id"]): float(row["weight"]) for row in expected}
    declared_weight = sum(declared.values())

    try:
        # Same entry point the graded run uses for a Stage.
        reports, detail = rv._run_module(
            f"stage_{stage}", env, tag=f"stage{stage}", scoring_stage=stage
        )
    except Exception as exc:  # noqa: BLE001
        print(f"{step}: stage {stage} rubric failed to run — {type(exc).__name__}: {exc}")
        return 1

    earned = detail["raw_earned_score"]
    eligible = detail["eligible_weight"]
    failures = [
        f"{r['check_id']}: {r['detail'] or 'returned False'} (weight {r['weight']})"
        for r in reports
        if not r["passed"]
    ]

    # The spec's declared expectation must match the rubric it claims to satisfy;
    # a mismatch means the spec drifted from the rubric and the "full marks"
    # claim is measured against the wrong target.
    drift: list[str] = []
    actual = {str(r["check_id"]): float(r["weight"]) for r in reports}
    if actual != declared:
        for cid in sorted(set(actual) | set(declared)):
            if actual.get(cid) != declared.get(cid):
                drift.append(f"{cid}: rubric={actual.get(cid)} spec={declared.get(cid)}")

    status = "FULL MARKS" if not failures and not drift else "SHORTFALL"
    print(
        f"{step}: stage {stage} — earned {earned}/{eligible} "
        f"(declared {declared_weight}) [{status}]"
    )
    for line in drift:
        print(f"   DRIFT {line}")
    for line in failures:
        print(f"   FAIL  {line}")
    return 0 if not failures and not drift else 1


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: verify_step.py /solution/step_spec.json")
    spec = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    return verify(spec)


if __name__ == "__main__":
    raise SystemExit(main())
