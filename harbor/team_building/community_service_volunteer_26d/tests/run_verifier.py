"""Score immutable Harbor stage evidence against the migrated rubric package."""
from __future__ import annotations

import importlib
import json
import math
import os
import sys
from pathlib import Path
from typing import Any

RUNTIME_DIR = Path(__file__).resolve().parent
if str(RUNTIME_DIR) not in sys.path:
    sys.path.insert(0, str(RUNTIME_DIR))

from harbor_evidence import HarborEvidence  # noqa: E402

RUBRICS_ROOT = Path(
    os.environ.get("HARBOR_RUBRICS_ROOT", str(RUNTIME_DIR / "rubrics"))
)
EVIDENCE_ROOT = Path(os.environ.get("HARBOR_EVIDENCE_ROOT", "/harbor/evidence"))
REWARD_PATH = Path(os.environ.get("HARBOR_REWARD_PATH", "/logs/verifier/reward.json"))
REPORT_PATH = Path(os.environ.get("HARBOR_REPORT_PATH", "/logs/verifier/checks.json"))
STAGE_COUNT = 26
EXPECTED_CHECK_COUNT = 73
EXPECTED_TOTAL_WEIGHT = 98.5


class VerifierInfrastructureError(RuntimeError):
    """The verifier could not judge the agent's work."""


def _load_rubric_package() -> None:
    parent = str(RUBRICS_ROOT.parent)
    if parent not in sys.path:
        sys.path.insert(0, parent)


def _import_module(name: str) -> Any:
    _load_rubric_package()
    try:
        return importlib.import_module(f"{RUBRICS_ROOT.name}.{name}")
    except Exception as exc:
        raise VerifierInfrastructureError(
            f"cannot import rubric module {name}: {type(exc).__name__}: {exc}"
        ) from exc


def _parse_check(row: Any, tag: str) -> tuple[str, Any, float]:
    if not isinstance(row, (tuple, list)) or len(row) != 3:
        raise VerifierInfrastructureError(f"invalid checker specification in {tag}")
    check_id, checker, weight = row
    if not isinstance(check_id, str) or not callable(checker):
        raise VerifierInfrastructureError(f"invalid checker identity in {tag}")
    if isinstance(weight, bool) or not isinstance(weight, (int, float)):
        raise VerifierInfrastructureError(f"checker {check_id} has non-numeric weight")
    numeric = float(weight)
    if not math.isfinite(numeric) or numeric <= 0.0:
        raise VerifierInfrastructureError(f"checker {check_id} has invalid weight")
    return check_id, checker, numeric


def _module_names() -> list[str]:
    names: list[str] = []
    for path in sorted(RUBRICS_ROOT.glob("*.py")):
        if path.stem == "__init__" or path.stem.startswith("_"):
            continue
        module = _import_module(path.stem)
        if hasattr(module, "CHECKS"):
            names.append(path.stem)
    return names


def _inventory() -> tuple[dict[str, float], int]:
    weights: dict[str, float] = {}
    count = 0
    for name in _module_names():
        module = _import_module(name)
        rows = getattr(module, "CHECKS", None)
        if not isinstance(rows, list):
            raise VerifierInfrastructureError(f"rubric module {name} has no CHECKS list")
        total = sum(_parse_check(row, name)[2] for row in rows)
        key = "stage" if name.startswith("stage_") else (
            "cross" if name == "cross_stage" else name
        )
        weights[key] = weights.get(key, 0.0) + total
        count += len(rows)
    total_weight = sum(weights.values())
    if count != EXPECTED_CHECK_COUNT:
        raise VerifierInfrastructureError(
            f"check count drifted from {EXPECTED_CHECK_COUNT} to {count}"
        )
    if not math.isclose(total_weight, EXPECTED_TOTAL_WEIGHT, abs_tol=1e-9):
        raise VerifierInfrastructureError(
            f"total check weight drifted from {EXPECTED_TOTAL_WEIGHT} to {total_weight}"
        )
    if any(weight <= 0.0 for weight in weights.values()):
        raise VerifierInfrastructureError("one or more rubric buckets have no weight")
    return weights, count


def _run_module(
    name: str, env: HarborEvidence, *, tag: str, scoring_stage: int
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    module = _import_module(name)
    rows = getattr(module, "CHECKS", None)
    if not isinstance(rows, list):
        raise VerifierInfrastructureError(f"rubric module {name} has no CHECKS list")
    env.scoring_stage = scoring_stage
    reports: list[dict[str, Any]] = []
    earned = 0.0
    eligible = 0.0
    for raw in rows:
        check_id, checker, weight = _parse_check(raw, tag)
        try:
            result = checker(env)
        except Exception as exc:
            raise VerifierInfrastructureError(
                f"check {check_id} raised {type(exc).__name__}: {exc}"
            ) from exc
        if type(result) is not bool:
            raise VerifierInfrastructureError(
                f"check {check_id} returned {type(result).__name__}, expected bool"
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
                "pass_threshold": 1.0,
                "applicable": True,
                "evidence": [f"checker:{check_id}"],
                "tags": [tag],
                "detail": "",
            }
        )
        eligible += weight
        earned += earned_score
    if eligible < 0.0:
        raise VerifierInfrastructureError(f"checker group {tag} has negative weight")
    detail = {
        "raw_earned_score": earned,
        "eligible_weight": eligible,
        "normalized_score": (earned / eligible) if eligible > 0.0 else 0.0,
    }
    return reports, detail


def _summary(detail: dict[str, Any], **extra: Any) -> dict[str, Any]:
    return {
        "earned_weight": detail["raw_earned_score"],
        "total_weight": detail["eligible_weight"],
        "ratio": detail["normalized_score"],
        **extra,
    }


def _write_outputs(reward: float, report: dict[str, Any]) -> None:
    REWARD_PATH.parent.mkdir(parents=True, exist_ok=True)
    verifier_ok = 1.0 if report.get("status") == "ok" else 0.0
    REWARD_PATH.write_text(
        json.dumps({"reward": reward, "verifier_ok": verifier_ok}, allow_nan=False)
        + "\n",
        encoding="utf-8",
    )
    REPORT_PATH.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    step = os.environ.get("HARBOR_STEP_NAME", "")
    try:
        virtual_stage = int(os.environ.get("VIRTUAL_STAGE", "0"))
    except ValueError as exc:
        raise VerifierInfrastructureError("VIRTUAL_STAGE is not an integer") from exc
    if virtual_stage < 0 or virtual_stage >= STAGE_COUNT:
        raise VerifierInfrastructureError(f"VIRTUAL_STAGE is out of range: {virtual_stage}")
    run_stage = os.environ.get("RUN_STAGE_RUBRIC", "1") == "1"
    include_all = os.environ.get("INCLUDE_ALL_BUCKETS") == "1"

    inventory, check_count = _inventory()
    pool_total = sum(inventory.values())
    env = HarborEvidence(EVIDENCE_ROOT)
    checks: list[dict[str, Any]] = []
    buckets: dict[str, Any] = {}
    reward = 0.0

    if include_all:
        stage_earned = 0.0
        stage_total = 0.0
        per_stage: dict[str, Any] = {}
        for stage in range(STAGE_COUNT):
            env.validate_stage(stage)
            reports, detail = _run_module(
                f"stage_{stage}", env, tag=f"stage{stage}", scoring_stage=stage
            )
            checks.extend(reports)
            stage_earned += detail["raw_earned_score"]
            stage_total += detail["eligible_weight"]
            per_stage[str(stage)] = _summary(detail)
        buckets["stage"] = {
            "earned_weight": stage_earned,
            "total_weight": stage_total,
            "ratio": stage_earned / stage_total if stage_total > 0.0 else 0.0,
            "stages_scored": STAGE_COUNT,
            "per_stage": per_stage,
        }
        earned = stage_earned
        eligible = stage_total
        for name in _module_names():
            if name.startswith("stage_"):
                continue
            tag = "cross" if name == "cross_stage" else name
            reports, detail = _run_module(
                name, env, tag=tag, scoring_stage=STAGE_COUNT - 1
            )
            checks.extend(reports)
            buckets[tag] = _summary(detail)
            earned += detail["raw_earned_score"]
            eligible += detail["eligible_weight"]
        if not math.isclose(eligible, pool_total, abs_tol=1e-9):
            raise VerifierInfrastructureError(
                f"scored weight {eligible} does not equal declared weight {pool_total}"
            )
        reward = earned / pool_total
        buckets["pool"] = {
            "earned_weight": earned,
            "total_weight": pool_total,
            "ratio": reward,
        }
    elif run_stage:
        env.validate_stage(virtual_stage)
        reports, detail = _run_module(
            f"stage_{virtual_stage}",
            env,
            tag=f"stage{virtual_stage}",
            scoring_stage=virtual_stage,
        )
        checks.extend(reports)
        reward = detail["raw_earned_score"] / pool_total
        buckets["stage"] = _summary(
            detail, current_stage=virtual_stage, contribution_to_global=reward
        )

    report = {
        "step": step,
        "virtual_stage": virtual_stage,
        "include_all_buckets": include_all,
        "verifier_mode": "immutable-stage-evidence",
        "scoring": "global-weighted-flat-pool",
        "pool_total_weight": pool_total,
        "weight_inventory": inventory,
        "check_count": check_count,
        "evidence_root": str(EVIDENCE_ROOT),
        "buckets": buckets,
        "reward": reward,
        "status": "ok",
        "errors": [],
        "checks": checks,
    }
    _write_outputs(reward, report)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        message = (
            str(exc)
            if isinstance(exc, VerifierInfrastructureError)
            else f"{type(exc).__name__}: {exc}"
        )
        _write_outputs(
            0.0,
            {
                "step": os.environ.get("HARBOR_STEP_NAME", ""),
                "evidence_root": str(EVIDENCE_ROOT),
                "reward": 0.0,
                "status": "infrastructure_error",
                "errors": [message],
                "checks": [],
            },
        )
        print(f"VERIFIER INFRASTRUCTURE ERROR: {message}", file=sys.stderr)
        raise SystemExit(1) from exc
