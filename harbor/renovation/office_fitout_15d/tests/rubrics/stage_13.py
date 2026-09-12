"""Stage 13 — dual-gate recheck verification and owner status grid."""
from __future__ import annotations

from ._helpers import (
    APP_ELECTRICAL,
    APP_FIRE,
    agent_polled_gate,
    budget_within_envelope,
    count_groups,
    has_any,
    stage_response,
    workspace_blob,
)


async def chk_dual_recheck_states_verified(ctx) -> bool:
    """Both gate reads occurred in the dual-recheck decision window."""
    fire_polled = agent_polled_gate(
        ctx,
        app_id=APP_FIRE,
        concept_terms=["fire_inspection", "fire safety", "emergency lighting"],
        min_stage=13,
        max_stage=20,
    )
    electrical_polled = agent_polled_gate(
        ctx,
        app_id=APP_ELECTRICAL,
        concept_terms=["electrical_load", "strong-current and low-voltage systems", "load"],
        min_stage=13,
        max_stage=20,
    )
    return fire_polled and electrical_polled


async def chk_owner_status_grid_covers_gates_and_budget(ctx) -> bool:
    """The requested status grid covers all material gates and budget health."""
    text = stage_response(ctx, stage=13) + "\n" + await workspace_blob(ctx)
    groups = [
        ["fire", "fire"],
        ["strong-current", "electrical", "load"],
        ["formaldehyde", "formaldehyde", "voc"],
        ["emergency lighting", "emergency lighting"],
        ["furniture", "furniture"],
        ["insurance", "insurance"],
        ["one-stop filing", "filing"],
        ["scenario-term", "handover", "handover"],
    ]
    has_coverage = count_groups(text, groups) >= 7
    has_rag = has_any(text, ["scenario-term", "scenario-term", "scenario-term", "green", "amber", "yellow", "red"])
    has_impact = has_any(text, ["09-01", "9/1", "occupancy", "move-in", "scenario-term"])
    return has_coverage and has_rag and has_impact and budget_within_envelope(text)


async def chk_d30_electrical_condition_recorded(ctx) -> bool:
    """The electrical conditional approval is captured as a D+30 obligation."""
    text = (await workspace_blob(ctx)) + "\n" + stage_response(ctx, stage=13)
    has_deadline = has_any(text, ["d+30", "d30", "30 days", "30days", "after occupancy 1 months"])
    has_target = has_any(text, ["4.2", "4.2+", "kw/100", "main-line upgrade"])
    has_cost = has_any(text, ["18,000", "18000", "18k"])
    has_tracking = has_any(text, ["punch", "pending closure", "condition", "conditional", "after-sales"])
    return has_deadline and has_target and has_cost and has_tracking


CHECKS = [
    ("chk_dual_recheck_states_verified", chk_dual_recheck_states_verified, 3.0),
    ("chk_owner_status_grid_covers_gates_and_budget", chk_owner_status_grid_covers_gates_and_budget, 3.0),
    ("chk_d30_electrical_condition_recorded", chk_d30_electrical_condition_recorded, 2.0),
]
