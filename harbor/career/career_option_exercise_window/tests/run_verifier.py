"""Score career_option_exercise_window from immutable Harbor evidence."""
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

RUBRICS_ROOT = Path(os.environ.get("HARBOR_RUBRICS_ROOT", str(RUNTIME_DIR / "rubrics")))
EVIDENCE_ROOT = Path(os.environ.get("HARBOR_EVIDENCE_ROOT", "/harbor/evidence"))
REWARD_PATH = Path("/logs/verifier/reward.json")
REPORT_PATH = Path("/logs/verifier/checks.json")
STAGE_COUNT = 27
EXPECTED_CHECK_COUNT = 44


class VerifierInfrastructureError(RuntimeError):
    """The harness could not judge the submitted evidence."""


def _load_rubric_package() -> None:
    parent = str(RUBRICS_ROOT.parent)
    if parent not in sys.path:
        sys.path.insert(0, parent)


def _import_module(name: str):
    try:
        return importlib.import_module(f"{RUBRICS_ROOT.name}.{name}")
    except Exception:
        return None


def _parse_check_spec(row: Any, *, tag: str) -> tuple[str, Any, float]:
    if not isinstance(row, (tuple, list)) or len(row) != 3:
        raise ValueError(f"checker spec in {tag} must contain exactly 3 values")
    check_id, checker, weight = row
    if isinstance(weight, bool) or not isinstance(weight, (int, float)):
        raise ValueError(f"checker {check_id!r} in {tag} has non-numeric weight")
    numeric = float(weight)
    if not math.isfinite(numeric) or numeric <= 0.0:
        raise ValueError(f"checker {check_id!r} in {tag} has invalid weight {weight!r}")
    return str(check_id), checker, numeric


def _run_checks(spec: Any, env: HarborEvidence, tag: str) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    reports: list[dict[str, Any]] = []
    atoms: list[dict[str, Any]] = []
    eligible = 0.0
    earned = 0.0
    for raw_spec in spec or []:
        check_id, checker, weight = _parse_check_spec(raw_spec, tag=tag)
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
        score = 1.0 if result else 0.0
        earned_score = score * weight
        atom = {
            "check_id": check_id,
            "applicable": True,
            "eligibility_reason": "unconditional task requirement",
            "check_score": score,
            "weight": weight,
            "earned_score": earned_score,
            "pass_threshold": 1.0,
            "passed": result,
            "evidence": [f"checker:{check_id}"],
        }
        atoms.append(atom)
        reports.append({"name": check_id, **atom, "tags": [tag], "detail": ""})
        eligible += weight
        earned += earned_score
    if eligible < 0.0:
        raise ValueError(f"checker group {tag} has negative eligible weight")
    return reports, {
        "checks": atoms,
        "raw_earned_score": earned,
        "eligible_weight": eligible,
        "excluded_weight": 0.0,
        "normalized_score": earned / eligible if eligible > 0.0 else 0.0,
    }


def _module_weight(module: Any) -> float:
    if module is None or not hasattr(module, "CHECKS"):
        return 0.0
    return sum(_parse_check_spec(row, tag=getattr(module, "__name__", "rubric"))[2] for row in module.CHECKS)


def _module_check_count(module: Any) -> int:
    return len(module.CHECKS) if module is not None and hasattr(module, "CHECKS") else 0


def _task_level_modules() -> list[str]:
    names = []
    for path in sorted(RUBRICS_ROOT.glob("*.py")):
        stem = path.stem
        if stem == "__init__" or stem.startswith("_") or stem.startswith("stage_"):
            continue
        module = _import_module(stem)
        if module is not None and hasattr(module, "CHECKS"):
            names.append(stem)
    return names


def _weight_inventory() -> tuple[dict[str, float], int]:
    _load_rubric_package()
    stages = [_import_module(f"stage_{stage}") for stage in range(STAGE_COUNT)]
    others = {name: _import_module(name) for name in _task_level_modules()}
    inventory = {"stage": sum(_module_weight(module) for module in stages)}
    inventory.update({("cross" if name == "cross_stage" else name): _module_weight(module) for name, module in others.items()})
    count = sum(_module_check_count(module) for module in stages) + sum(_module_check_count(module) for module in others.values())
    return inventory, count


def _run_module(name: str, env: HarborEvidence, tag: str):
    module = _import_module(name)
    if module is None or not hasattr(module, "CHECKS"):
        raise RuntimeError(f"missing or broken rubric module: {name}")
    return _run_checks(module.CHECKS, env, tag)


def _bucket_summary(detail: dict[str, Any], **extra: Any) -> dict[str, Any]:
    return {
        "total_weight": detail["eligible_weight"],
        "earned_weight": detail["raw_earned_score"],
        "ratio": detail["normalized_score"],
        **extra,
    }


def _write_outputs(reward: float, report: dict[str, Any]) -> None:
    REWARD_PATH.parent.mkdir(parents=True, exist_ok=True)
    ok = report.get("status") == "ok"
    REWARD_PATH.write_text(json.dumps({"reward": float(reward), "verifier_ok": 1.0 if ok else 0.0}, allow_nan=False) + "\n", encoding="utf-8")
    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def main() -> int:
    step_name = os.environ.get("HARBOR_STEP_NAME", "")
    virtual_stage = int(os.environ.get("VIRTUAL_STAGE", "0"))
    include_all = os.environ.get("INCLUDE_ALL_BUCKETS") == "1"
    run_stage = os.environ.get("RUN_STAGE_RUBRIC", "1") == "1"
    errors: list[str] = []
    checks: list[dict[str, Any]] = []
    buckets: dict[str, Any] = {}
    inventory, check_count = _weight_inventory()
    if check_count != EXPECTED_CHECK_COUNT:
        errors.append(f"check count is {check_count}, expected {EXPECTED_CHECK_COUNT}")
    env = HarborEvidence(EVIDENCE_ROOT)
    try:
        if include_all:
            stage_details = []
            per_stage = {}
            for stage in range(STAGE_COUNT):
                env.current_stage = stage
                env.validate_stage(stage)
                reports, detail = _run_module(f"stage_{stage}", env, f"stage{stage}")
                checks.extend(reports)
                stage_details.append(detail)
                per_stage[str(stage)] = _bucket_summary(detail)
            task_details = {}
            env.current_stage = max(env.published_stages(), default=STAGE_COUNT - 1)
            for name in _task_level_modules():
                reports, detail = _run_module(name, env, name)
                checks.extend(reports)
                task_details["cross" if name == "cross_stage" else name] = detail
                buckets["cross" if name == "cross_stage" else name] = _bucket_summary(detail)
            stage_earned = sum(d["raw_earned_score"] for d in stage_details)
            stage_total = sum(d["eligible_weight"] for d in stage_details)
            buckets["stage"] = {"earned_weight": stage_earned, "total_weight": stage_total, "ratio": stage_earned / stage_total if stage_total else 0.0, "stages_scored": len(stage_details), "per_stage": per_stage}
            earned = stage_earned + sum(d["raw_earned_score"] for d in task_details.values())
            observed = stage_total + sum(d["eligible_weight"] for d in task_details.values())
            pool_total = sum(inventory.values())
            if not math.isclose(observed, pool_total, abs_tol=1e-9):
                errors.append(f"scored weight {observed} != declared pool {pool_total}")
            reward = earned / pool_total if pool_total > 0 and not errors else 0.0
        elif run_stage:
            env.current_stage = virtual_stage
            env.validate_stage(virtual_stage)
            reports, detail = _run_module(f"stage_{virtual_stage}", env, f"stage{virtual_stage}")
            checks.extend(reports)
            reward = detail["raw_earned_score"] / sum(inventory.values()) if inventory else 0.0
            buckets["stage"] = _bucket_summary(detail, current_stage=virtual_stage, contribution_to_global=reward)
        else:
            reward = 0.0
    except Exception as exc:
        errors.append(f"{type(exc).__name__}: {exc}")
        reward = 0.0
    report = {
        "step": step_name,
        "virtual_stage": virtual_stage,
        "stage_boundary": os.environ.get("STAGE_BOUNDARY") == "1",
        "include_all_buckets": include_all,
        "verifier_mode": "immutable-sidecar-flat-pool",
        "scoring": "global-weighted-flat-pool",
        "pool_total_weight": sum(inventory.values()),
        "weight_inventory": inventory,
        "check_count": check_count,
        "evidence_root": str(EVIDENCE_ROOT),
        "buckets": buckets,
        "reward": reward,
        "status": "ok" if not errors else "infrastructure_error",
        "errors": errors,
        "checks": checks,
    }
    _write_outputs(reward, report)
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
