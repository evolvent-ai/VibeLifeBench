"""Stage 12 — evidence-based fire rework decision before inspection."""
from __future__ import annotations

import re

from ._helpers import (
    APP_FILING,
    APP_FIRE,
    agent_application_status_pairs,
    agent_polled_gate,
    agent_tool_result_records,
    app_status,
    count_distinct_amounts,
    count_groups,
    extract_day_counts,
    has_any,
    stage_response,
    workspace_blob,
)


async def chk_fire_and_filing_gates_repolled(ctx) -> bool:
    """Both requested live applications are queried during Stage 12."""
    fire_status = await app_status(ctx, APP_FIRE)
    filing_status = await app_status(ctx, APP_FILING)
    if not fire_status or not filing_status:
        return False
    fire_polled = agent_polled_gate(
        ctx,
        app_id=APP_FIRE,
        concept_terms=["fire_inspection", "fire safety", "emergency lighting"],
        min_stage=12,
        max_stage=12,
    )
    filing_polled = agent_polled_gate(
        ctx,
        app_id=APP_FILING,
        concept_terms=["commercial_fit_up", "one-stop filing", "filing"],
        min_stage=12,
        max_stage=12,
    )
    return fire_polled and filing_polled


async def chk_fire_rework_options_are_quantified(ctx) -> bool:
    """The owner receives three options with money, duration, and risk."""
    text = stage_response(ctx, stage=12) + "\n" + await workspace_blob(ctx)
    option_groups = [
        ["in-house", "in house", "internal remediation"],
        ["rush", "rush", "fire consultant", "fire consultant", "rush reinspection"],
        ["occupancy slip", "defer", "wfh", "coworking", "routine reinspection"],
    ]
    has_three = count_groups(text, option_groups) == 3
    has_costs = count_distinct_amounts(text, lo=1000, hi=500000) >= 2
    has_days = len(extract_day_counts(text)) >= 2
    has_risk = has_any(text, ["risk", "risk", "scenario-term", "critical path", "error"])
    has_recommendation = has_any(text, ["scenario-term", "recommend", "recommend select", "scenario-termrecommend"])
    return has_three and has_costs and has_days and has_risk and has_recommendation


async def chk_no_occupancy_or_payment_before_fire_approval(ctx) -> bool:
    """The agent rejects the vendor's proposal to advance before approval."""
    # Bind the pre-approval assertion to a successful agent poll in the
    # decision window.  The frozen stage snapshot may already contain the
    # later approval from the same event, so it cannot answer this question.
    records = agent_tool_result_records(
        ctx,
        tool_any=["get_visa_application"],
        args_any=[APP_FIRE],
        min_stage=12,
        max_stage=20,
    )
    preapproval_states = {"rfi", "draft", "pending", "submitted"}
    fire_preapproval_seen = any(
        (app, status) in {
            (APP_FIRE.lower(), candidate)
            for candidate in preapproval_states
        }
        for record in records
        if (
            "get_visa_application" not in record.get("name", "")
            or APP_FIRE.lower() in record.get("input_text", "")
        )
        for app, status in agent_application_status_pairs(record)
    )
    # A final-step replay can expose only stage 20.  In that shape there is no
    # historical decision-window trace to contradict the preserved text leg;
    # the decision-window poll remains authoritative whenever it is present.
    stages = {
        entry.get("stage")
        for entry in getattr(ctx, "turn_log", []) or []
        if isinstance(entry, dict)
    }
    has_historical_window = any(
        isinstance(stage, int) and 12 <= stage < 20 for stage in stages
    ) or any(
        isinstance(record.get("stage"), int) and 12 <= record["stage"] < 20
        for record in records
    )
    if has_historical_window and not fire_preapproval_seen:
        return False
    text = (stage_response(ctx, stage=12) + "\n" + await workspace_blob(ctx)).lower()
    if not text.strip():
        return False
    authorization_terms = [
        "scenario-termoccupancy", "occupy first", "release final payment",
        "scenario-termfinal payment", "pay final", "pay final payment",
        "early occupancy allowed",
    ]
    # A prohibition such as "do not release final payment" contains the
    # positive phrase as a substring.  Treat only an unnegated occurrence as
    # authorization while keeping the original vocabulary unchanged.
    authorizes = any(
        not re.search(
            r"(?:\bno\b|\bnot\b|\bdo\s+not\b|\bmust\s+not\b|\bcannot\b|\bwithout\b)\W*$",
            text[max(0, match.start() - 32):match.start()],
        )
        for term in authorization_terms
        for match in re.finditer(re.escape(term), text)
    )
    blocks = has_any(
        text,
        ["no occupancy", "must not occupy", "do not release final payment", "hold final payment", "pending fire approval", "approved after", "scenario-termafteragain", "no-go"],
    )
    return blocks and not authorizes


CHECKS = [
    ("chk_fire_and_filing_gates_repolled", chk_fire_and_filing_gates_repolled, 2.5),
    ("chk_fire_rework_options_are_quantified", chk_fire_rework_options_are_quantified, 3.0),
    ("chk_no_occupancy_or_payment_before_fire_approval", chk_no_occupancy_or_payment_before_fire_approval, 3.0),
]


from .stage_1 import chk_active_inspection_standards_pull_before_handover

CHECKS.append((
    "chk_active_inspection_standards_pull_before_handover",
    chk_active_inspection_standards_pull_before_handover,
    6,
))


from .stage_9 import chk_evidence_hotel_booking_polled_for_real_holds

CHECKS.append((
    "chk_evidence_hotel_booking_polled_for_real_holds",
    chk_evidence_hotel_booking_polled_for_real_holds,
    3,
))
