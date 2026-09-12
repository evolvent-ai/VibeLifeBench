"""Score immutable Harbor stage evidence against the migrated rubric package."""
from __future__ import annotations

import importlib
import json
import math
import os
import sys
from pathlib import Path
from typing import Any


TESTS_DIR = Path(__file__).resolve().parent
if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))

from harbor_evidence import EvidenceError, HarborEvidence  # noqa: E402


RUBRICS_ROOT = Path(os.environ.get("HARBOR_RUBRICS_ROOT", TESTS_DIR / "rubrics"))
EVIDENCE_ROOT = Path(os.environ.get("HARBOR_EVIDENCE_ROOT", "/harbor/evidence"))
REWARD_PATH = Path(os.environ.get("HARBOR_REWARD_PATH", "/logs/verifier/reward.json"))
REPORT_PATH = Path(os.environ.get("HARBOR_REPORT_PATH", "/logs/verifier/checks.json"))
STAGE_COUNT = 22
EXPECTED_CHECK_COUNT = 54


class VerifierInfrastructureError(RuntimeError):
    """Evidence or verifier code failed before the agent could be judged."""


def _load_package() -> None:
    parent = str(RUBRICS_ROOT.parent)
    if parent not in sys.path:
        sys.path.insert(0, parent)


def _import_module(name: str):
    _load_package()
    try:
        return importlib.import_module(f"{RUBRICS_ROOT.name}.{name}")
    except Exception as exc:  # noqa: BLE001
        raise VerifierInfrastructureError(
            f"unable to import rubric module {name}: {type(exc).__name__}: {exc}"
        ) from exc


def _task_modules() -> list[str]:
    names: list[str] = []
    for path in sorted(RUBRICS_ROOT.glob("*.py")):
        stem = path.stem
        if stem == "__init__" or stem.startswith("_") or stem.startswith("stage_"):
            continue
        module = _import_module(stem)
        if hasattr(module, "CHECKS"):
            names.append(stem)
    return names


def _parse_spec(row: Any, tag: str) -> tuple[str, Any, float]:
    if not isinstance(row, (tuple, list)) or len(row) != 3:
        raise VerifierInfrastructureError(f"invalid check specification in {tag}")
    check_id, checker, weight = row
    if not callable(checker):
        raise VerifierInfrastructureError(f"check {check_id!r} in {tag} is not callable")
    if isinstance(weight, bool) or not isinstance(weight, (int, float)):
        raise VerifierInfrastructureError(f"check {check_id!r} has a non-numeric weight")
    numeric = float(weight)
    if not math.isfinite(numeric) or numeric < 0.0:
        raise VerifierInfrastructureError(f"check {check_id!r} has invalid weight {weight!r}")
    return str(check_id), checker, numeric


def _inventory() -> tuple[dict[str, float], int]:
    modules = [f"stage_{stage}" for stage in range(STAGE_COUNT)] + _task_modules()
    weights: dict[str, float] = {}
    count = 0
    for name in modules:
        module = _import_module(name)
        if not hasattr(module, "CHECKS"):
            raise VerifierInfrastructureError(f"rubric module {name} has no CHECKS")
        weights[name] = sum(_parse_spec(row, name)[2] for row in module.CHECKS)
        count += len(module.CHECKS)
    if count != EXPECTED_CHECK_COUNT:
        raise VerifierInfrastructureError(
            f"rubric inventory has {count} checks, expected {EXPECTED_CHECK_COUNT}"
        )
    if sum(weights.values()) <= 0.0:
        raise VerifierInfrastructureError("rubric inventory has no positive weight")
    return weights, count


def _run_module(name: str, env: HarborEvidence, stage: int) -> tuple[list[dict[str, Any]], float, float]:
    env._rubric_stage = stage
    module = _import_module(name)
    reports: list[dict[str, Any]] = []
    eligible = 0.0
    earned = 0.0
    for row in module.CHECKS:
        check_id, checker, weight = _parse_spec(row, name)
        try:
            result = checker(env)
        except Exception as exc:  # noqa: BLE001
            raise VerifierInfrastructureError(
                f"check {check_id!r} raised {type(exc).__name__}: {exc}"
            ) from exc
        if type(result) is not bool:
            raise VerifierInfrastructureError(
                f"check {check_id!r} returned {type(result).__name__}, expected bool"
            )
        score = 1.0 if result else 0.0
        earned_score = score * weight
        reports.append(
            {
                "name": check_id,
                "check_id": check_id,
                "passed": result,
                "check_score": score,
                "weight": weight,
                "earned_score": earned_score,
                "applicable": True,
                "tags": [name],
                "evidence": [f"checker:{check_id}"],
            }
        )
        eligible += weight
        earned += earned_score
    if eligible < 0.0:
        raise VerifierInfrastructureError(f"checker group {name} has negative eligible weight")
    return reports, earned, eligible


def _write_outputs(reward: float, report: dict[str, Any], verifier_ok: float) -> None:
    REWARD_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REWARD_PATH.write_text(
        json.dumps({"reward": float(reward), "verifier_ok": float(verifier_ok)}, allow_nan=False)
        + "\n",
        encoding="utf-8",
    )
    REPORT_PATH.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    step = os.environ.get("HARBOR_STEP_NAME", "")
    stage = int(os.environ.get("VIRTUAL_STAGE", "0"))
    run_stage = os.environ.get("RUN_STAGE_RUBRIC", "1") == "1"
    include_all = os.environ.get("INCLUDE_ALL_BUCKETS", "0") == "1"
    inventory, check_count = _inventory()
    pool_total = sum(inventory.values())
    env = HarborEvidence(EVIDENCE_ROOT)
    checks: list[dict[str, Any]] = []
    buckets: dict[str, Any] = {}
    earned_total = 0.0
    eligible_total = 0.0

    if include_all:
        for rubric_stage in range(STAGE_COUNT):
            env.validate_stage(rubric_stage)
            reports, earned, eligible = _run_module(
                f"stage_{rubric_stage}", env, rubric_stage
            )
            checks.extend(reports)
            earned_total += earned
            eligible_total += eligible
            buckets[f"stage_{rubric_stage}"] = {
                "earned_weight": earned,
                "eligible_weight": eligible,
                "normalized_score": (earned / eligible) if eligible > 0.0 else 0.0,
            }
        for name in _task_modules():
            reports, earned, eligible = _run_module(name, env, STAGE_COUNT - 1)
            checks.extend(reports)
            earned_total += earned
            eligible_total += eligible
            buckets[name] = {
                "earned_weight": earned,
                "eligible_weight": eligible,
                "normalized_score": (earned / eligible) if eligible > 0.0 else 0.0,
            }
        if not math.isclose(eligible_total, pool_total, abs_tol=1e-9):
            raise VerifierInfrastructureError(
                f"scored weight {eligible_total} differs from declared pool {pool_total}"
            )
    elif run_stage:
        env.validate_stage(stage)
        reports, earned_total, eligible_total = _run_module(f"stage_{stage}", env, stage)
        checks.extend(reports)
        buckets[f"stage_{stage}"] = {
            "earned_weight": earned_total,
            "eligible_weight": eligible_total,
            "normalized_score": (
                earned_total / eligible_total if eligible_total > 0.0 else 0.0
            ),
        }

    reward = earned_total / pool_total
    report = {
        "status": "ok",
        "step": step,
        "virtual_stage": stage,
        "include_all_buckets": include_all,
        "verifier_mode": "immutable-stage-evidence",
        "pool_total_weight": pool_total,
        "eligible_weight": eligible_total,
        "earned_weight": earned_total,
        "check_count": check_count,
        "buckets": buckets,
        "reward": reward,
        "errors": [],
        "checks": checks,
    }
    _write_outputs(reward, report, 1.0)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (VerifierInfrastructureError, EvidenceError, ValueError) as exc:
        _write_outputs(
            0.0,
            {
                "status": "infrastructure_error",
                "step": os.environ.get("HARBOR_STEP_NAME", ""),
                "reward": 0.0,
                "errors": [f"{type(exc).__name__}: {exc}"],
                "checks": [],
            },
            0.0,
        )
        print(f"VERIFIER INFRASTRUCTURE ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
