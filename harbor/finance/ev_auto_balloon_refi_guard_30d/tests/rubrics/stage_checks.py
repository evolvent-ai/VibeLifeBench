"""Shared predicates used by the local per-stage EV rubric modules."""
from __future__ import annotations

from ._helpers import stage_addressed, stage_business_result, stage_evidence


def check_stage_addressed(env, idx: int) -> bool:
    return bool(stage_addressed(env, idx))


def check_stage_tool_or_number(env, idx: int) -> bool:
    return bool(stage_evidence(env, idx))


def check_stage_durable_gate(env, idx: int) -> bool:
    return bool(stage_business_result(env, idx))


def check_stage_safety_critical(env, idx: int) -> bool:
    return bool(stage_business_result(env, idx))
