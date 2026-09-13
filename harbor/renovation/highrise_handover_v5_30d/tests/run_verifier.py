"""Harbor verifier for the high-rise handover immutable evidence tree.

Every stage is evaluated from `/harbor/evidence/stages/stage-N`, published at
that stage's boundary by the world-controller.  The final step safely
recomputes all rubric modules because their historical inputs are immutable;
no score or evidence is read from the agent-writable workspace.
"""
from __future__ import annotations

import hashlib
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
# The flat-pool denominator is whatever this task's rubrics add up to — NOT a
# spec value. Measured across one task set: 146.0, 118.7, 44.55 and 100.0 all
# occur. Hardcoding 100.0 would silently rescale every reward on any task whose
# rubrics total something else, so the total is computed from the bundled
# rubrics (see _pool_total) and only checked for self-consistency.
EXPECTED_CHECK_COUNT = 68   # guards "a check vanished", not the weight scale
EXPECTED_POOL_TOTAL = 132.5
EXPECTED_BUCKET_WEIGHTS = {"stage": 89.0, "cross": 19.0, "final": 24.5}
EXPECTED_TASK_CHECKS = {
    "cross_stage": [
        ("cs_evidence", 5.0),
        ("cs_auth", 5.0),
        ("cs_updated", 4.5),
        ("cs_funds", 4.5),
    ],
    "final": [
        ("f_budget", 4.5),
        ("f_risk", 4.5),
        ("f_evidence", 4.5),
        ("f_summary", 4.0),
        ("f_tracker", 3.0),
        ("f_no_bad", 4.0),
    ],
}
STAGE_COUNT = 24
REQUIRED_STAGE_FILES = frozenset(
    {"snapshot.json", "trace.json", "response.txt", "trajectory.json"}
)


class VerifierInfrastructureError(RuntimeError):
    """The run could not be scored — as opposed to the agent scoring badly.

    ``reward 0.0`` with a healthy verifier means the agent did the work poorly and
    is the whole basis of the G2 (nop = 0.0) gate. If instead the evidence is
    missing, a rubric fails to import, the weight inventory drifts, or a checker
    raises, nothing was judged at all; reporting 0.0 there blames the agent for a
    broken harness and makes a systematically broken task look merely hard.

    Note that a non-zero exit alone does not reach Harbor: ``tests/test.sh``
    backfills a reward file when the verifier dies, and Harbor's verifier
    discards the exec return code (``await self.environment.exec(...)``; nothing
    under src/harbor/verifier reads ``return_code``). The health bit therefore
    stays numeric in reward.json, while diagnostics are persisted in checks.json.
    """


def _load_rubric_package() -> None:
    parent = str(RUBRICS_ROOT.parent)
    if parent not in sys.path:
        sys.path.insert(0, parent)


def _import_module(name: str):
    try:
        return importlib.import_module(f"{RUBRICS_ROOT.name}.{name}")
    except Exception:  # noqa: BLE001 - packaging failure must fail closed
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


def _run_checks(spec: Any, env: Any, tag: str) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    reports: list[dict[str, Any]] = []
    atoms: list[dict[str, Any]] = []
    eligible = 0.0
    earned = 0.0
    for raw_spec in spec:
        check_id, checker, weight = _parse_check_spec(raw_spec, tag=tag)
        error = ""
        # A checker that raises has not judged the agent — it failed to run.
        # Recording that as passed=False fabricates an agent failure and hides a
        # broken rubric or damaged evidence behind a plausible low score.
        try:
            raw_result = checker(env)
        except Exception as exc:  # noqa: BLE001
            raise VerifierInfrastructureError(
                f"check {check_id!r} ({tag}) raised {type(exc).__name__}: {exc}"
            ) from exc
        if type(raw_result) is not bool:
            raise VerifierInfrastructureError(
                f"check {check_id!r} ({tag}) returned {type(raw_result).__name__}, expected bool"
            )
        passed = raw_result
        check_score = 1.0 if passed else 0.0
        earned_score = check_score * weight
        atom = {
            "check_id": check_id,
            "applicable": True,
            "eligibility_reason": "unconditional task requirement",
            "check_score": check_score,
            "weight": weight,
            "earned_score": earned_score,
            "pass_threshold": 1.0,
            "passed": passed,
            "evidence": [f"checker:{check_id}"],
        }
        atoms.append(atom)
        reports.append(
            {
                "name": check_id,
                "check_id": check_id,
                "passed": passed,
                "check_score": check_score,
                "weight": weight,
                "earned_score": earned_score,
                "pass_threshold": 1.0,
                "applicable": True,
                "evidence": atom["evidence"],
                "tags": [tag],
                "detail": error,
            }
        )
        eligible += weight
        earned += earned_score
    # Empty buckets are valid for unscored transition stages. Only negative
    # eligible weight is an inventory error, and normalization must avoid a
    # division by zero when a legitimate bucket has no checks.
    if eligible < 0.0:
        raise ValueError(f"checker group {tag} has negative eligible weight")
    return reports, {
        "checks": atoms,
        "raw_earned_score": earned,
        "eligible_weight": eligible,
        "excluded_weight": 0.0,
        "normalized_score": (earned / eligible) if eligible > 0.0 else 0.0,
    }


def _module_weight(module: Any) -> float:
    if module is None or not hasattr(module, "CHECKS"):
        return 0.0
    return sum(
        _parse_check_spec(row, tag=getattr(module, "__name__", "rubric"))[2]
        for row in module.CHECKS
    )


def _module_check_count(module: Any) -> int:
    if module is None or not hasattr(module, "CHECKS"):
        return 0
    return len(module.CHECKS)


def _bucket_key(module_name: str) -> str:
    """Report key for a task-level rubric module.

    Only the historical spellings are shortened, so a newly added bucket keeps
    its module name rather than silently merging into an existing key.
    """
    return {"cross_stage": "cross", "tool_call": "tool"}.get(module_name, module_name)


def _task_level_modules() -> list[str]:
    """Non-stage rubric modules carrying weight, discovered rather than listed.

    Hardcoding the bucket names desynchronises numerator from denominator the
    moment a module is added or renamed: the inventory and the grading loop each
    carried their own literal list, so a new bucket had to be registered twice
    and a miss was invisible. Measured — dropping a 5.0-weight ``tool_quality.py``
    into rubrics/ left the inventory reporting the same 95 checks and 100.0 pool
    while the bucket never ran. The ``tool_quality.py`` vs ``tool_call.py`` naming
    split is real across this task set, and is exactly how 8 points went missing.

    Discovery keeps both sides over one set, so a new bucket is scored and
    counted or it fails loudly — never silently dropped.
    """
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
    stage_modules = [_import_module(f"stage_{stage}") for stage in range(STAGE_COUNT)]
    others = {name: _import_module(name) for name in _task_level_modules()}
    inventory = {"stage": sum(_module_weight(module) for module in stage_modules)}
    for name, module in others.items():
        inventory[_bucket_key(name)] = _module_weight(module)
    count = sum(_module_check_count(module) for module in stage_modules) + sum(
        _module_check_count(module) for module in others.values()
    )
    return inventory, count


def _available_step_specs() -> list[Path]:
    # The tests bundle ships a copy of every step spec (tests/step_specs), so the
    # rubric-contract validation below runs on every arm. Falling back to the
    # per-step /solution/step_spec.json alone makes the validation satisfiable
    # only where Harbor mounted a solution — a nop or candidate arm had no spec
    # at all and died as a VerifierInfrastructureError before any rubric ran.
    bundled = sorted((RUNTIME_DIR / "step_specs").glob("event-*/solution/step_spec.json"))
    if bundled:
        return bundled
    local = sorted((RUNTIME_DIR.parent / "steps").glob("event-*/solution/step_spec.json"))
    if local:
        return local
    current = Path(os.environ.get("HARBOR_STEP_SPEC", "/solution/step_spec.json"))
    return [current] if current.is_file() else []


def _expected_stage_checks(spec: dict[str, Any], path: Path) -> list[tuple[str, float]]:
    rows = spec.get("expected_checks")
    if not isinstance(rows, list):
        raise ValueError(f"{path} expected_checks is not a list")
    checks: list[tuple[str, float]] = []
    for row in rows:
        if not isinstance(row, dict) or row.get("expected") is not True:
            raise ValueError(f"{path} has a malformed or non-passing expected check")
        check_id = row.get("check_id")
        weight = row.get("weight")
        if not isinstance(check_id, str) or not check_id:
            raise ValueError(f"{path} has an invalid expected check id")
        if isinstance(weight, bool) or not isinstance(weight, (int, float)):
            raise ValueError(f"{path} check {check_id!r} has an invalid weight")
        checks.append((check_id, float(weight)))
    return checks


def _validate_step_specs() -> None:
    paths = _available_step_specs()
    if not paths:
        raise ValueError("no step_spec.json is available for rubric contract validation")

    boundaries: dict[int, tuple[Path, list[tuple[str, float]], float]] = {}
    for path in paths:
        try:
            spec = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ValueError(f"cannot load step spec {path}: {exc}") from exc
        if not isinstance(spec, dict):
            raise ValueError(f"{path} is not a JSON object")
        try:
            stage = int(spec["virtual_stage"])
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError(f"{path} has no valid virtual_stage") from exc
        checks = _expected_stage_checks(spec, path)
        expected_weight = spec.get("expected_stage_weight")
        if isinstance(expected_weight, bool) or not isinstance(expected_weight, (int, float)):
            raise ValueError(f"{path} has an invalid expected_stage_weight")
        total = sum(weight for _check_id, weight in checks)
        if not math.isclose(total, float(expected_weight), abs_tol=1e-9):
            raise ValueError(f"{path} expected check weights sum to {total}, not {expected_weight}")
        if not spec.get("stage_boundary"):
            if checks or not math.isclose(float(expected_weight), 0.0, abs_tol=1e-9):
                raise ValueError(f"non-boundary {path} declares stage checks or weight")
            continue
        if stage in boundaries:
            raise ValueError(f"stage {stage} has duplicate boundary specs")
        boundaries[stage] = (path, checks, float(expected_weight))

    if len(paths) > 1 and set(boundaries) != set(range(STAGE_COUNT)):
        missing = sorted(set(range(STAGE_COUNT)) - set(boundaries))
        extra = sorted(set(boundaries) - set(range(STAGE_COUNT)))
        raise ValueError(f"stage boundary spec coverage mismatch: missing={missing}, extra={extra}")

    for stage, (path, expected, expected_weight) in boundaries.items():
        module = _import_module(f"stage_{stage}")
        if module is None or not hasattr(module, "CHECKS"):
            raise ValueError(f"{path} has no corresponding stage_{stage} rubric")
        actual = [
            (check_id, weight)
            for check_id, _checker, weight in (
                _parse_check_spec(row, tag=f"stage{stage}") for row in module.CHECKS
            )
        ]
        if actual != expected:
            raise ValueError(f"stage {stage} rubric checks {actual!r} != {path} {expected!r}")
        if not math.isclose(_module_weight(module), expected_weight, abs_tol=1e-9):
            raise ValueError(f"stage {stage} rubric weight does not match {path}")


def _run_module(name: str, env: Any, tag: str) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    module = _import_module(name)
    if module is None or not hasattr(module, "CHECKS"):
        raise RuntimeError(f"missing or broken rubric module: {name}")
    if name.startswith("stage_"):
        try:
            env._rubric_stage = int(name.removeprefix("stage_"))
        except ValueError as exc:
            raise RuntimeError(f"invalid stage rubric module: {name}") from exc
    else:
        env._rubric_stage = STAGE_COUNT - 1
    return _run_checks(module.CHECKS, env, tag)


def _bucket_summary(detail: dict[str, Any], **extra: Any) -> dict[str, Any]:
    return {
        "total_weight": detail["eligible_weight"],
        "earned_weight": detail["raw_earned_score"],
        "ratio": detail["normalized_score"],
        **extra,
    }


def _servers() -> list[str]:
    import tomllib

    for candidate in (Path("/tests/task.toml"), Path("/task.toml"), Path("/harbor/task.toml")):
        if not candidate.is_file():
            continue
        try:
            data = tomllib.loads(candidate.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            continue
        names = [
            server["name"]
            for server in data.get("environment", {}).get("mcp_servers", [])
            if isinstance(server, dict) and server.get("name")
        ]
        if names:
            return names
    try:
        manifest = json.loads((RUNTIME_DIR / "services.json").read_text(encoding="utf-8"))
        return list(manifest["mcp_servers"])
    except Exception:  # noqa: BLE001
        return []


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_stage_evidence(
    stage: int, *, evidence_root: Path | str = EVIDENCE_ROOT
) -> dict[str, Any]:
    """Validate one immutable stage manifest and every declared file hash."""
    root = Path(evidence_root) / "stages" / f"stage-{stage:02d}"
    try:
        manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"stage {stage} has no valid sidecar manifest") from exc
    if not isinstance(manifest, dict):
        raise ValueError(f"stage {stage} manifest is not an object")
    if manifest.get("schema_version") != 1 or manifest.get("kind") != "stage":
        raise ValueError(f"stage {stage} manifest type mismatch")
    if manifest.get("virtual_stage") != stage:
        raise ValueError(f"stage {stage} manifest number mismatch")
    hashes = manifest.get("hashes")
    if not isinstance(hashes, dict) or not hashes:
        raise ValueError(f"stage {stage} manifest has no hashes")
    actual_paths = {
        str(path.relative_to(root)): path
        for path in root.rglob("*")
        if path.is_file() and not path.is_symlink() and path.name != "manifest.json"
    }
    if set(actual_paths) != set(hashes):
        raise ValueError(f"stage {stage} manifest file set mismatch")
    missing_required = REQUIRED_STAGE_FILES - set(actual_paths)
    if missing_required:
        raise ValueError(f"stage {stage} missing required files: {sorted(missing_required)}")
    for relative, path in actual_paths.items():
        recorded = hashes.get(relative)
        if not isinstance(recorded, str) or _sha256(path) != recorded:
            raise ValueError(f"stage {stage} hash mismatch: {relative}")
    try:
        snapshot = json.loads((root / "snapshot.json").read_text(encoding="utf-8"))
        trace = json.loads((root / "trace.json").read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"stage {stage} contains invalid JSON evidence") from exc
    if not isinstance(snapshot, dict) or snapshot.get("stage") != stage:
        raise ValueError(f"stage {stage} snapshot number mismatch")
    if not isinstance(trace, list):
        raise ValueError(f"stage {stage} trace is not a list")
    return manifest


def _validate_inventory() -> tuple[dict[str, float], int]:
    """Require exact stage/spec wiring and the task's declared flat pool."""
    _validate_step_specs()
    task_modules = set(_task_level_modules())
    if task_modules != set(EXPECTED_TASK_CHECKS):
        raise ValueError(
            f"task-level rubric modules {sorted(task_modules)} != "
            f"{sorted(EXPECTED_TASK_CHECKS)}"
        )
    for module_name, expected in EXPECTED_TASK_CHECKS.items():
        module = _import_module(module_name)
        actual = [
            (check_id, weight)
            for check_id, _checker, weight in (
                _parse_check_spec(row, tag=module_name) for row in module.CHECKS
            )
        ]
        if actual != expected:
            raise ValueError(
                f"task-level rubric {module_name} checks {actual!r} != {expected!r}"
            )
    inventory, check_count = _weight_inventory()
    total = sum(inventory.values())
    if set(inventory) != set(EXPECTED_BUCKET_WEIGHTS):
        raise ValueError(f"rubric buckets {sorted(inventory)} != expected buckets")
    for bucket, expected in EXPECTED_BUCKET_WEIGHTS.items():
        if not math.isclose(inventory[bucket], expected, abs_tol=1e-9):
            raise ValueError(
                f"rubric bucket {bucket!r} weight is {inventory[bucket]}, expected {expected}"
            )
    if not math.isclose(total, EXPECTED_POOL_TOTAL, abs_tol=1e-9):
        raise ValueError(f"pool total weight is {total}, expected {EXPECTED_POOL_TOTAL}")
    if check_count != EXPECTED_CHECK_COUNT:
        raise ValueError(f"check count is {check_count}, expected {EXPECTED_CHECK_COUNT}")
    return inventory, check_count


def main() -> int:
    step = os.environ.get("HARBOR_STEP_NAME", "")
    virtual_stage = int(os.environ.get("VIRTUAL_STAGE", "0"))
    stage_boundary = os.environ.get("STAGE_BOUNDARY") == "1"
    run_stage_rubric = os.environ.get("RUN_STAGE_RUBRIC", "1") == "1"
    include_all = os.environ.get("INCLUDE_ALL_BUCKETS") == "1"
    errors: list[str] = []
    buckets: dict[str, dict[str, Any]] = {}
    checks: list[dict[str, Any]] = []
    reward = 0.0

    try:
        inventory, check_count = _validate_inventory()
    except Exception as exc:  # noqa: BLE001
        inventory, check_count = {}, 0
        errors.append(f"inventory: {type(exc).__name__}: {exc}")

    # One context for every stage: the rubrics read only the frozen per-stage
    # files under EVIDENCE_ROOT (snapshot / trace / response / trajectory). There
    # is deliberately no MCP capability and no workspace handle on this object —
    # scoring a historical stage must never be able to observe the final world.
    env = HarborEvidence(EVIDENCE_ROOT)

    if include_all and not errors:
        stage_details: list[dict[str, Any]] = []
        per_stage: dict[str, Any] = {}
        for stage in range(STAGE_COUNT):
            try:
                validate_stage_evidence(stage)
                reports, detail = _run_module(f"stage_{stage}", env, f"stage{stage}")
                stage_details.append(detail)
                checks.extend(reports)
                per_stage[str(stage)] = _bucket_summary(detail)
            except Exception as exc:  # noqa: BLE001
                errors.append(f"stage {stage}: {type(exc).__name__}: {exc}")

        task_details: dict[str, dict[str, Any]] = {}
        if not errors:
            # Same discovery the inventory uses, so numerator and denominator
            # cover one set. A hardcoded list here was half of the dead-bucket
            # failure: a module present in the inventory but absent from this
            # loop contributed weight nobody could earn.
            for module_name in _task_level_modules():
                key, tag = _bucket_key(module_name), module_name
                try:
                    reports, detail = _run_module(module_name, env, tag)
                    task_details[key] = detail
                    checks.extend(reports)
                    buckets[key] = _bucket_summary(detail)
                except Exception as exc:  # noqa: BLE001
                    errors.append(f"{key}: {type(exc).__name__}: {exc}")

        stage_earned = sum(detail["raw_earned_score"] for detail in stage_details)
        stage_total = sum(detail["eligible_weight"] for detail in stage_details)
        buckets["stage"] = {
            "earned_weight": stage_earned,
            "total_weight": stage_total,
            "ratio": stage_earned / stage_total if stage_total else 0.0,
            "stages_scored": len(stage_details),
            "per_stage": per_stage,
        }
        earned_total = stage_earned + sum(
            detail["raw_earned_score"] for detail in task_details.values()
        )
        eligible_total = stage_total + sum(
            detail["eligible_weight"] for detail in task_details.values()
        )
        # The denominator is what the bundled rubrics actually declare; the
        # scored set must match it exactly or numerator and denominator ran over
        # different buckets.
        pool_total = sum(inventory.values())
        if not math.isclose(eligible_total, pool_total, abs_tol=1e-9):
            errors.append(
                f"scored weight {eligible_total} != declared pool {pool_total}: "
                "numerator and denominator cover different bucket sets"
            )
        reward = 0.0 if errors else earned_total / pool_total
        buckets["pool"] = {
            "earned_weight": earned_total,
            "total_weight": pool_total,
            "observed_eligible_weight": eligible_total,
            "ratio": reward,
            "scoring": "global-weighted-flat-pool",
        }
    elif run_stage_rubric and not errors:
        try:
            validate_stage_evidence(virtual_stage)
            reports, detail = _run_module(
                f"stage_{virtual_stage}", env, f"stage{virtual_stage}"
            )
            checks.extend(reports)
            reward = detail["raw_earned_score"] / sum(inventory.values())
            buckets["stage"] = _bucket_summary(
                detail,
                current_stage=virtual_stage,
                contribution_to_global=reward,
            )
        except Exception as exc:  # noqa: BLE001
            errors.append(f"stage {virtual_stage}: {type(exc).__name__}: {exc}")
            reward = 0.0

    report = {
        "step": step,
        "virtual_stage": virtual_stage,
        "stage_boundary": stage_boundary,
        "include_all_buckets": include_all,
        "verifier_mode": "immutable-sidecar-flat-pool",
        "scoring": "global-weighted-flat-pool",
        "pool_total_weight": sum(inventory.values()),
        "weight_inventory": inventory,
        "check_count": check_count,
        "evidence_root": str(EVIDENCE_ROOT),
        "buckets": buckets,
        "reward": reward,
        "status": "ok",
        "errors": errors,
        "checks": checks,
    }
    # Anything still in `errors` here means a stage or bucket did not run, so the
    # pool was scored over a smaller set than it claims. Measured: one bucket
    # failing to import moved pool_total_weight 100.0 -> 88.0 while the reward
    # stayed plausible, hiding 12 points of judgement that never executed.
    if errors:
        raise VerifierInfrastructureError("; ".join(errors[:5]))
    _write_outputs(reward, report)
    return 0


def _write_outputs(reward: float, report: dict[str, Any]) -> None:
    REWARD_PATH.parent.mkdir(parents=True, exist_ok=True)
    status = report.get("status")
    # `verifier_ok` is a health signal, not a score: 1.0 when this step was
    # actually scored, 0.0 when it could not be. It exists so task.toml can gate
    # on it with Harbor's native `min_reward = { verifier_ok = 1.0 }` — the
    # framework treats a missing key or a crashed verifier as -inf and aborts the
    # trial, which is the only mechanism that reliably distinguishes a broken
    # harness from an agent that scored badly. Gating on `reward` itself cannot
    # work here: intermediate steps legitimately score ~0.005 (their slice of the
    # pool), so any useful threshold would abort healthy runs.
    payload = {"reward": reward, "verifier_ok": 0.0 if status and status != "ok" else 1.0}
    REWARD_PATH.write_text(json.dumps(payload, allow_nan=False) + "\n", encoding="utf-8")
    REPORT_PATH.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except VerifierInfrastructureError as exc:
        # Keep diagnostics in checks.json; Harbor 0.20.0 parses every reward.json
        # value as numeric, so a string status there causes a second parser failure.
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
