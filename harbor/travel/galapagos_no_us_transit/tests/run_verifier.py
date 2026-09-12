"""Harbor verifier for the immutable Galapagos stage evidence tree."""
from __future__ import annotations

import importlib
import json
import math
import os
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from harbor_evidence import EvidenceError, HarborEvidence  # noqa: E402

EVIDENCE_ROOT = Path(os.environ.get("HARBOR_EVIDENCE_ROOT", "/harbor/evidence"))
REWARD_PATH = Path(os.environ.get("VERIFIER_REWARD_PATH", "/logs/verifier/reward.json"))
REPORT_PATH = Path(os.environ.get("VERIFIER_REPORT_PATH", "/logs/verifier/checks.json"))
STAGE_COUNT = 25


class VerifierInfrastructureError(RuntimeError):
    """The harness could not judge the evidence."""


def _load(name: str):
    try:
        return importlib.import_module(f"rubrics.{name}")
    except Exception as exc:  # pragma: no cover - exercised by harness failures
        raise VerifierInfrastructureError(f"rubric import failed for {name}: {exc}") from exc


def _spec(row: Any, tag: str) -> tuple[str, Any, float]:
    if not isinstance(row, (tuple, list)) or len(row) != 3:
        raise ValueError(f"invalid checker spec in {tag}")
    name, checker, weight = row
    if isinstance(weight, bool) or not isinstance(weight, (int, float)):
        raise ValueError(f"checker {name!r} in {tag} has non-numeric weight")
    numeric = float(weight)
    if not math.isfinite(numeric) or numeric <= 0.0:
        raise ValueError(f"checker {name!r} in {tag} has invalid weight {weight!r}")
    return str(name), checker, numeric


def _run_checks(specification: Any, env: HarborEvidence, tag: str) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    reports: list[dict[str, Any]] = []
    eligible = 0.0
    earned = 0.0
    for row in specification:
        check_id, checker, weight = _spec(row, tag)
        try:
            result = checker(env)
        except Exception as exc:
            raise VerifierInfrastructureError(
                f"check {check_id!r} ({tag}) raised {type(exc).__name__}: {exc}"
            ) from exc
        if type(result) is not bool:
            raise VerifierInfrastructureError(
                f"check {check_id!r} ({tag}) returned {type(result).__name__}, expected bool"
            )
        earned_score = weight if result else 0.0
        reports.append({
            "name": check_id,
            "check_id": check_id,
            "passed": result,
            "check_score": 1.0 if result else 0.0,
            "weight": weight,
            "earned_score": earned_score,
            "applicable": True,
            "evidence": [f"checker:{check_id}"],
            "tags": [tag],
        })
        eligible += weight
        earned += earned_score
    if eligible < 0.0:
        raise ValueError(f"checker group {tag} has negative eligible weight")
    return reports, {
        "raw_earned_score": earned,
        "eligible_weight": eligible,
        "normalized_score": (earned / eligible) if eligible > 0.0 else 0.0,
    }


def _module_names() -> list[str]:
    names: list[str] = []
    for path in sorted((ROOT / "rubrics").glob("*.py")):
        if path.stem == "__init__" or path.stem.startswith("_") or path.stem.startswith("stage_"):
            continue
        module = _load(path.stem)
        if hasattr(module, "CHECKS"):
            names.append(path.stem)
    return names


def _inventory() -> tuple[dict[str, float], int]:
    stage_total = 0.0
    count = 0
    for stage in range(STAGE_COUNT):
        module = _load(f"stage_{stage}")
        rows = getattr(module, "CHECKS", [])
        stage_total += sum(_spec(row, f"stage{stage}")[2] for row in rows)
        count += len(rows)
    inventory = {"stage": stage_total}
    for name in _module_names():
        module = _load(name)
        rows = getattr(module, "CHECKS", [])
        inventory["cross" if name == "cross_stage" else name] = sum(
            _spec(row, name)[2] for row in rows
        )
        count += len(rows)
    if sum(inventory.values()) <= 0.0:
        raise ValueError("rubric pool has no positive weight")
    return inventory, count


def _write(reward: float, report: dict[str, Any], healthy: bool) -> None:
    REWARD_PATH.parent.mkdir(parents=True, exist_ok=True)
    REWARD_PATH.write_text(
        json.dumps({"reward": float(reward), "verifier_ok": 1.0 if healthy else 0.0}, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def main() -> int:
    step = os.environ.get("HARBOR_STEP_NAME", "")
    virtual_stage = int(os.environ.get("VIRTUAL_STAGE", "0"))
    run_stage = os.environ.get("RUN_STAGE_RUBRIC", "1") == "1"
    include_all = os.environ.get("INCLUDE_ALL_BUCKETS", "0") == "1"
    errors: list[str] = []
    checks: list[dict[str, Any]] = []
    buckets: dict[str, Any] = {}
    env = HarborEvidence(EVIDENCE_ROOT)
    try:
        inventory, check_count = _inventory()
    except Exception as exc:
        inventory, check_count = {}, 0
        errors.append(f"inventory: {type(exc).__name__}: {exc}")

    earned = 0.0
    eligible = 0.0
    if not errors:
        try:
            if include_all:
                stage_earned = stage_eligible = 0.0
                per_stage: dict[str, Any] = {}
                for stage in range(STAGE_COUNT):
                    env.validate_stage(stage)
                    rows, detail = _run_checks(getattr(_load(f"stage_{stage}"), "CHECKS", []), env, f"stage{stage}")
                    checks.extend(rows)
                    stage_earned += detail["raw_earned_score"]
                    stage_eligible += detail["eligible_weight"]
                    per_stage[str(stage)] = detail
                buckets["stage"] = {"earned_weight": stage_earned, "total_weight": stage_eligible, "ratio": stage_earned / stage_eligible if stage_eligible else 0.0, "per_stage": per_stage}
                earned, eligible = stage_earned, stage_eligible
                for name in _module_names():
                    rows, detail = _run_checks(getattr(_load(name), "CHECKS", []), env, name)
                    checks.extend(rows)
                    key = "cross" if name == "cross_stage" else name
                    buckets[key] = {"earned_weight": detail["raw_earned_score"], "total_weight": detail["eligible_weight"], "ratio": detail["normalized_score"]}
                    earned += detail["raw_earned_score"]
                    eligible += detail["eligible_weight"]
            elif run_stage:
                env.validate_stage(virtual_stage)
                rows, detail = _run_checks(getattr(_load(f"stage_{virtual_stage}"), "CHECKS", []), env, f"stage{virtual_stage}")
                checks.extend(rows)
                earned, eligible = detail["raw_earned_score"], detail["eligible_weight"]
                buckets["stage"] = {**detail, "current_stage": virtual_stage, "contribution_to_global": earned / sum(inventory.values())}
        except Exception as exc:
            errors.append(f"scoring: {type(exc).__name__}: {exc}")

    pool_total = sum(inventory.values())
    if not errors and abs(eligible - (pool_total if include_all else eligible)) > 1e-9:
        errors.append("scored weight does not match the declared rubric pool")
    reward = earned / pool_total if pool_total > 0.0 and not errors else 0.0
    report = {
        "step": step,
        "virtual_stage": virtual_stage,
        "include_all_buckets": include_all,
        "verifier_mode": "immutable-sidecar-flat-pool",
        "pool_total_weight": pool_total,
        "weight_inventory": inventory,
        "check_count": check_count,
        "evidence_root": str(EVIDENCE_ROOT),
        "buckets": buckets,
        "reward": reward,
        "status": "ok" if not errors else "infrastructure_error",
        "errors": errors,
        "checks": checks,
    }
    _write(reward, report, not errors)
    if errors:
        print("VERIFIER INFRASTRUCTURE ERROR: " + "; ".join(errors[:3]), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
