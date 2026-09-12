"""Shared predicates used by the local per-stage divorce rubric modules."""
from __future__ import annotations

from ._helpers import stage_business_result, stage_evidence


def check_stage_evidence(env, idx: int) -> bool:
    return bool(stage_evidence(env, idx))


def check_stage_business_result(env, idx: int) -> bool:
    return bool(stage_business_result(env, idx))
