"""Stage 13 — dual-gate recheck verification and owner status grid."""
from __future__ import annotations

from ._helpers import (
    APP_ELECTRICAL,
    APP_FIRE,
    agent_polled_gate,
    app_status,
    budget_within_envelope,
    count_groups,
    has_any,
    stage_response,
    workspace_blob,
)


async def chk_dual_recheck_states_verified(ctx) -> bool:
    """Live fire/electrical states and the agent's verification both agree."""
    fire = await app_status(ctx, APP_FIRE)
    electrical = await app_status(ctx, APP_ELECTRICAL)
    if fire != "approved" or electrical != "approved_with_conditions":
        return False
    fire_polled = agent_polled_gate(
        ctx,
        app_id=APP_FIRE,
        concept_terms=["fire_inspection", "消防", "应急照明"],
        min_stage=13,
        max_stage=13,
    )
    electrical_polled = agent_polled_gate(
        ctx,
        app_id=APP_ELECTRICAL,
        concept_terms=["electrical_load", "强弱电", "负荷"],
        min_stage=13,
        max_stage=13,
    )
    return fire_polled and electrical_polled


async def chk_owner_status_grid_covers_gates_and_budget(ctx) -> bool:
    """The requested status grid covers all material gates and budget health."""
    text = stage_response(ctx, stage=13) + "\n" + await workspace_blob(ctx)
    groups = [
        ["消防", "fire"],
        ["强弱电", "electrical", "负荷"],
        ["甲醛", "formaldehyde", "voc"],
        ["应急照明", "emergency lighting"],
        ["软装", "furniture"],
        ["保险", "insurance"],
        ["一件事", "filing"],
        ["押金", "handover", "交接"],
    ]
    has_coverage = count_groups(text, groups) >= 7
    has_rag = has_any(text, ["绿", "黄", "红", "green", "amber", "yellow", "red"])
    has_impact = has_any(text, ["09-01", "9/1", "入驻", "move-in", "影响"])
    return has_coverage and has_rag and has_impact and budget_within_envelope(text)


async def chk_d30_electrical_condition_recorded(ctx) -> bool:
    """The electrical conditional approval is captured as a D+30 obligation."""
    text = (await workspace_blob(ctx)) + "\n" + stage_response(ctx, stage=13)
    has_deadline = has_any(text, ["d+30", "d30", "30 天", "30天", "入驻后 1 个月"])
    has_target = has_any(text, ["4.2", "4.2+", "kw/100", "主线升级"])
    has_cost = has_any(text, ["18,000", "18000", "18k"])
    has_tracking = has_any(text, ["punch", "待闭环", "condition", "附条件", "售后"])
    return has_deadline and has_target and has_cost and has_tracking


CHECKS = [
    ("chk_dual_recheck_states_verified", chk_dual_recheck_states_verified, 3.0),
    ("chk_owner_status_grid_covers_gates_and_budget", chk_owner_status_grid_covers_gates_and_budget, 3.0),
    ("chk_d30_electrical_condition_recorded", chk_d30_electrical_condition_recorded, 2.0),
]
