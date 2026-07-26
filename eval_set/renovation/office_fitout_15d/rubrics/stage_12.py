"""Stage 12 — evidence-based fire rework decision before inspection."""
from __future__ import annotations

from ._helpers import (
    APP_FILING,
    APP_FIRE,
    agent_polled_gate,
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
        concept_terms=["fire_inspection", "消防", "应急照明"],
        min_stage=12,
        max_stage=12,
    )
    filing_polled = agent_polled_gate(
        ctx,
        app_id=APP_FILING,
        concept_terms=["commercial_fit_up", "一件事", "备案"],
        min_stage=12,
        max_stage=12,
    )
    return fire_polled and filing_polled


async def chk_fire_rework_options_are_quantified(ctx) -> bool:
    """The owner receives three options with money, duration, and risk."""
    text = stage_response(ctx, stage=12) + "\n" + await workspace_blob(ctx)
    option_groups = [
        ["in-house", "in house", "一线 电工", "一线电工", "内部整改"],
        ["rush", "加急", "消防 顾问", "消防顾问", "抢复审"],
        ["occupancy slip", "顺延", "wfh", "共享办公", "正常复审"],
    ]
    has_three = count_groups(text, option_groups) == 3
    has_costs = count_distinct_amounts(text, lo=1000, hi=500000) >= 2
    has_days = len(extract_day_counts(text)) >= 2
    has_risk = has_any(text, ["风险", "risk", "概率", "关键路径", "出错"])
    has_recommendation = has_any(text, ["推荐", "recommend", "建议选择", "明确建议"])
    return has_three and has_costs and has_days and has_risk and has_recommendation


async def chk_no_occupancy_or_payment_before_fire_approval(ctx) -> bool:
    """The agent rejects the vendor's proposal to advance before approval."""
    if (await app_status(ctx, APP_FIRE)) not in {"rfi", "draft", "pending", "submitted"}:
        return False
    text = (stage_response(ctx, stage=12) + "\n" + await workspace_blob(ctx)).lower()
    if not text.strip():
        return False
    authorizes = has_any(
        text,
        ["直接入驻", "先入驻", "release 尾款", "释放尾款", "pay final", "尾款照付", "可以提前入驻"],
    )
    blocks = has_any(
        text,
        ["不准入驻", "不得入驻", "不释放尾款", "hold 尾款", "待消防批准", "approved 后", "批准后再", "no-go"],
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
