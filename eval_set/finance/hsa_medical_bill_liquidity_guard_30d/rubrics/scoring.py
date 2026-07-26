"""Flat-pool scoring for long-horizon finance tasks.

Scoring is passed-atomic-weight / total-atomic-weight. The hierarchical
stage/final/cross ratios and gate flags are still computed and exposed on
ScoreBreakdown for diagnostics, but no longer gate the score.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


BUCKET_WEIGHTS = {"stage": 0.35, "final": 0.40, "cross": 0.25}


@dataclass(frozen=True)
class ScoreBreakdown:
    score: float
    stage_ratio: float
    final_ratio: float
    cross_ratio: float
    raw_final_ratio: float
    raw_cross_ratio: float
    stage_completed: int
    stage_count: int
    final_gate_passed: bool
    cross_gate_passed: bool
    incomplete_stages: tuple[int, ...]
    failed_final_checks: tuple[str, ...]
    failed_cross_checks: tuple[str, ...]


def _weighted_ratio(check_ids: list[str], outcomes: Mapping[str, bool], weights: Mapping[str, float]) -> float:
    total = sum(float(weights[check_id]) for check_id in check_ids)
    if total <= 0:
        return 0.0
    passed = sum(float(weights[check_id]) for check_id in check_ids if bool(outcomes.get(check_id, False)))
    return passed / total


def aggregate_score(
    outcomes: Mapping[str, bool],
    weights: Mapping[str, float],
    *,
    stage_count: int = 24,
) -> ScoreBreakdown:
    """Score atomic outcomes using complete-Stage and integrated Task gates.

    Atomic outcomes remain independently visible. Credit is hierarchical:
    a Stage contributes only when every atomic check in that Stage passes,
    and Final/Cross buckets contribute only when their complete contracts pass.
    """
    incomplete_stages: list[int] = []
    completed = 0
    for stage in range(stage_count):
        prefix = f"s{stage}_"
        check_ids = sorted(check_id for check_id in weights if check_id.startswith(prefix))
        if not check_ids:
            incomplete_stages.append(stage)
            continue
        if all(bool(outcomes.get(check_id, False)) for check_id in check_ids):
            completed += 1
        else:
            incomplete_stages.append(stage)
    stage_ratio = completed / stage_count if stage_count else 0.0

    final_ids = sorted(check_id for check_id in weights if check_id.startswith("final_"))
    cross_ids = sorted(check_id for check_id in weights if check_id.startswith("cs_"))
    raw_final_ratio = _weighted_ratio(final_ids, outcomes, weights)
    raw_cross_ratio = _weighted_ratio(cross_ids, outcomes, weights)
    failed_final = tuple(check_id for check_id in final_ids if not bool(outcomes.get(check_id, False)))
    failed_cross = tuple(check_id for check_id in cross_ids if not bool(outcomes.get(check_id, False)))
    final_gate = bool(final_ids) and not failed_final
    cross_gate = bool(cross_ids) and not failed_cross
    final_ratio = raw_final_ratio if final_gate else 0.0
    cross_ratio = raw_cross_ratio if cross_gate else 0.0

    # flat_pool: score is passed atomic weight over total atomic weight.
    # Stage/final/cross ratios and gate flags are still computed above, but
    # only as diagnostics — they no longer zero out a bucket's contribution.
    total_weight = sum(float(w) for w in weights.values())
    passed_weight = sum(
        float(w) for check_id, w in weights.items() if bool(outcomes.get(check_id, False))
    )
    score = (passed_weight / total_weight) if total_weight > 0 else 0.0
    return ScoreBreakdown(
        score=score,
        stage_ratio=stage_ratio,
        final_ratio=final_ratio,
        cross_ratio=cross_ratio,
        raw_final_ratio=raw_final_ratio,
        raw_cross_ratio=raw_cross_ratio,
        stage_completed=completed,
        stage_count=stage_count,
        final_gate_passed=final_gate,
        cross_gate_passed=cross_gate,
        incomplete_stages=tuple(incomplete_stages),
        failed_final_checks=failed_final,
        failed_cross_checks=failed_cross,
    )
