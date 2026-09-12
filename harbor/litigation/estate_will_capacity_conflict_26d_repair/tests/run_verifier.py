"""Score the estate task exclusively from immutable Harbor stage evidence."""
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

from harbor_evidence import EvidenceError, HarborEvidence  # noqa: E402

RUBRICS_ROOT = Path(os.environ.get("HARBOR_RUBRICS_ROOT", RUNTIME_DIR / "rubrics"))
EVIDENCE_ROOT = Path(os.environ.get("HARBOR_EVIDENCE_ROOT", "/harbor/evidence"))
REWARD_PATH = Path(os.environ.get("HARBOR_REWARD_PATH", "/logs/verifier/reward.json"))
REPORT_PATH = Path(os.environ.get("HARBOR_REPORT_PATH", "/logs/verifier/checks.json"))
STAGE_COUNT = 26
EXPECTED_CHECK_COUNT = 64


class VerifierInfrastructureError(RuntimeError):
    """Scoring did not run completely, rather than the agent scoring poorly."""


def _load_rubric_package() -> None:
    parent = str(RUBRICS_ROOT.parent)
    if parent not in sys.path:
        sys.path.insert(0, parent)


def _import_module(name: str):
    try:
        return importlib.import_module(f"{RUBRICS_ROOT.name}.{name}")
    except Exception as exc:
        raise VerifierInfrastructureError(
            f"cannot import rubric module {name}: {type(exc).__name__}: {exc}"
        ) from exc


def _parse_check_spec(row: Any, *, tag: str) -> tuple[str, Any, float]:
    if not isinstance(row, (tuple, list)) or len(row) != 3:
        raise VerifierInfrastructureError(
            f"checker spec in {tag} must contain exactly three values"
        )
    check_id, checker, weight = row
    if not callable(checker):
        raise VerifierInfrastructureError(f"checker {check_id!r} in {tag} is not callable")
    if isinstance(weight, bool) or not isinstance(weight, (int, float)):
        raise VerifierInfrastructureError(
            f"checker {check_id!r} in {tag} has a non-numeric weight"
        )
    numeric = float(weight)
    if not math.isfinite(numeric) or numeric <= 0.0:
        raise VerifierInfrastructureError(
            f"checker {check_id!r} in {tag} has invalid weight {weight!r}"
        )
    return str(check_id), checker, numeric


def _run_checks(
    spec: Any, env: HarborEvidence, tag: str
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    if not isinstance(spec, (tuple, list)):
        raise VerifierInfrastructureError(f"checker group {tag} is not a list")
    reports: list[dict[str, Any]] = []
    atoms: list[dict[str, Any]] = []
    eligible = 0.0
    earned = 0.0
    for raw_spec in spec:
        check_id, checker, weight = _parse_check_spec(raw_spec, tag=tag)
        try:
            raw_result = checker(env)
        except Exception as exc:
            raise VerifierInfrastructureError(
                f"check {check_id!r} ({tag}) raised {type(exc).__name__}: {exc}"
            ) from exc
        if type(raw_result) is not bool:
            raise VerifierInfrastructureError(
                f"check {check_id!r} ({tag}) returned "
                f"{type(raw_result).__name__}, expected bool"
            )
        check_score = 1.0 if raw_result else 0.0
        earned_score = check_score * weight
        atom = {
            "check_id": check_id,
            "applicable": True,
            "eligibility_reason": "unconditional task requirement",
            "check_score": check_score,
            "weight": weight,
            "earned_score": earned_score,
            "pass_threshold": 1.0,
            "passed": raw_result,
            "evidence": [f"checker:{check_id}"],
        }
        atoms.append(atom)
        reports.append(
            {
                "name": check_id,
                "check_id": check_id,
                "passed": raw_result,
                "check_score": check_score,
                "weight": weight,
                "earned_score": earned_score,
                "pass_threshold": 1.0,
                "applicable": True,
                "evidence": atom["evidence"],
                "tags": [tag],
                "detail": "",
            }
        )
        eligible += weight
        earned += earned_score
    if eligible < 0.0:
        raise VerifierInfrastructureError(
            f"checker group {tag} has negative eligible weight"
        )
    return reports, {
        "checks": atoms,
        "raw_earned_score": earned,
        "eligible_weight": eligible,
        "excluded_weight": 0.0,
        "normalized_score": (earned / eligible) if eligible > 0.0 else 0.0,
    }


def _module_checks(name: str) -> Any:
    module = _import_module(name)
    if not hasattr(module, "CHECKS"):
        raise VerifierInfrastructureError(f"rubric module {name} has no CHECKS")
    return module.CHECKS


def _task_level_modules() -> list[str]:
    names: list[str] = []
    for path in sorted(RUBRICS_ROOT.glob("*.py")):
        stem = path.stem
        if stem == "__init__" or stem.startswith("_") or stem.startswith("stage_"):
            continue
        module = _import_module(stem)
        if hasattr(module, "CHECKS"):
            names.append(stem)
    return names


def _bucket_key(module_name: str) -> str:
    return "cross" if module_name == "cross_stage" else module_name


def _inventory() -> tuple[dict[str, float], int]:
    _load_rubric_package()
    inventory = {"stage": 0.0}
    check_count = 0
    seen: set[str] = set()
    for stage in range(STAGE_COUNT):
        rows = _module_checks(f"stage_{stage}")
        check_count += len(rows)
        for row in rows:
            check_id, _checker, weight = _parse_check_spec(row, tag=f"stage{stage}")
            if check_id in seen:
                raise VerifierInfrastructureError(f"duplicate check id: {check_id}")
            seen.add(check_id)
            inventory["stage"] += weight
    for module_name in _task_level_modules():
        key = _bucket_key(module_name)
        rows = _module_checks(module_name)
        inventory[key] = 0.0
        check_count += len(rows)
        for row in rows:
            check_id, _checker, weight = _parse_check_spec(row, tag=module_name)
            if check_id in seen:
                raise VerifierInfrastructureError(f"duplicate check id: {check_id}")
            seen.add(check_id)
            inventory[key] += weight
    if check_count != EXPECTED_CHECK_COUNT:
        raise VerifierInfrastructureError(
            f"check count is {check_count}, expected {EXPECTED_CHECK_COUNT}"
        )
    if sum(inventory.values()) <= 0.0:
        raise VerifierInfrastructureError("rubric pool has no positive weight")
    return inventory, check_count


def _run_module(
    name: str, env: HarborEvidence, tag: str
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    return _run_checks(_module_checks(name), env, tag)


def _bucket_summary(detail: dict[str, Any], **extra: Any) -> dict[str, Any]:
    return {
        "total_weight": detail["eligible_weight"],
        "earned_weight": detail["raw_earned_score"],
        "ratio": detail["normalized_score"],
        **extra,
    }


def validate_stage_evidence(
    stage: int, *, evidence_root: Path | str = EVIDENCE_ROOT
) -> None:
    evidence = HarborEvidence(evidence_root)
    evidence.validate_stage(stage)
    evidence.snapshot(stage)
    evidence.trace(stage)
    evidence.response(stage)
    evidence.trajectory(stage)


def _write_outputs(reward: float, report: dict[str, Any]) -> None:
    REWARD_PATH.parent.mkdir(parents=True, exist_ok=True)
    status = report.get("status")
    payload = {
        "reward": float(reward),
        "verifier_ok": 0.0 if status and status != "ok" else 1.0,
    }
    REWARD_PATH.write_text(
        json.dumps(payload, allow_nan=False) + "\n", encoding="utf-8"
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
    stage_boundary = os.environ.get("STAGE_BOUNDARY") == "1"
    run_stage_rubric = os.environ.get("RUN_STAGE_RUBRIC", "1") == "1"
    include_all = os.environ.get("INCLUDE_ALL_BUCKETS") == "1"

    inventory, check_count = _inventory()
    pool_total = sum(inventory.values())
    buckets: dict[str, dict[str, Any]] = {}
    checks: list[dict[str, Any]] = []
    reward = 0.0

    if include_all:
        stage_details: list[dict[str, Any]] = []
        per_stage: dict[str, Any] = {}
        for stage in range(STAGE_COUNT):
            validate_stage_evidence(stage)
            stage_env = HarborEvidence(EVIDENCE_ROOT, stage_limit=stage)
            reports, detail = _run_module(
                f"stage_{stage}", stage_env, f"stage{stage}"
            )
            checks.extend(reports)
            stage_details.append(detail)
            per_stage[str(stage)] = _bucket_summary(detail)

        task_details: dict[str, dict[str, Any]] = {}
        final_env = HarborEvidence(EVIDENCE_ROOT, stage_limit=STAGE_COUNT - 1)
        for module_name in _task_level_modules():
            key = _bucket_key(module_name)
            reports, detail = _run_module(module_name, final_env, module_name)
            checks.extend(reports)
            task_details[key] = detail
            buckets[key] = _bucket_summary(detail)

        stage_earned = sum(row["raw_earned_score"] for row in stage_details)
        stage_eligible = sum(row["eligible_weight"] for row in stage_details)
        buckets["stage"] = {
            "earned_weight": stage_earned,
            "total_weight": stage_eligible,
            "ratio": stage_earned / stage_eligible if stage_eligible else 0.0,
            "stages_scored": len(stage_details),
            "per_stage": per_stage,
        }
        earned_total = stage_earned + sum(
            row["raw_earned_score"] for row in task_details.values()
        )
        eligible_total = stage_eligible + sum(
            row["eligible_weight"] for row in task_details.values()
        )
        if not math.isclose(eligible_total, pool_total, abs_tol=1e-9):
            raise VerifierInfrastructureError(
                f"scored weight {eligible_total} differs from declared pool {pool_total}"
            )
        reward = earned_total / pool_total
        buckets["pool"] = {
            "earned_weight": earned_total,
            "total_weight": pool_total,
            "observed_eligible_weight": eligible_total,
            "ratio": reward,
            "scoring": "global-weighted-flat-pool",
        }
    elif run_stage_rubric:
        validate_stage_evidence(virtual_stage)
        env = HarborEvidence(EVIDENCE_ROOT, stage_limit=virtual_stage)
        reports, detail = _run_module(
            f"stage_{virtual_stage}", env, f"stage{virtual_stage}"
        )
        checks.extend(reports)
        reward = detail["raw_earned_score"] / pool_total
        buckets["stage"] = _bucket_summary(
            detail,
            current_stage=virtual_stage,
            contribution_to_global=reward,
        )

    report = {
        "step": step,
        "virtual_stage": virtual_stage,
        "stage_boundary": stage_boundary,
        "include_all_buckets": include_all,
        "verifier_mode": "immutable-sidecar-flat-pool",
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
    except (VerifierInfrastructureError, EvidenceError) as exc:
        _write_outputs(
            0.0,
            {
                "step": os.environ.get("HARBOR_STEP_NAME", ""),
                "evidence_root": str(EVIDENCE_ROOT),
                "reward": 0.0,
                "status": "infrastructure_error",
                "errors": [str(exc)],
                "checks": [],
            },
        )
        print(f"VERIFIER INFRASTRUCTURE ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
