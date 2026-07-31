"""Stage 14 — evidence-gated conditional handover and final-payment hold."""
from __future__ import annotations

from ._helpers import (
    APP_ELECTRICAL,
    APP_FILING,
    APP_FIRE,
    APP_HANDOVER,
    APP_INSURANCE,
    agent_polled_gate,
    app_status,
    budget_within_envelope,
    has_any,
    owner_facing_emails,
    read_workspace_file,
    stage_response,
    workspace_blob,
)


async def chk_handover_gates_verified_before_recommendation(ctx) -> bool:
    """The five live Gate states support only a conditional handover."""
    states = {
        APP_FILING: await app_status(ctx, APP_FILING),
        APP_FIRE: await app_status(ctx, APP_FIRE),
        APP_ELECTRICAL: await app_status(ctx, APP_ELECTRICAL),
        APP_INSURANCE: await app_status(ctx, APP_INSURANCE),
        APP_HANDOVER: await app_status(ctx, APP_HANDOVER),
    }
    expected = {
        APP_FILING: "approved",
        APP_FIRE: "approved",
        APP_ELECTRICAL: "approved_with_conditions",
        APP_INSURANCE: "in_force",
        APP_HANDOVER: "approved_with_conditions",
    }
    if states != expected:
        return False
    decisive = [
        (APP_FIRE, ["fire_inspection", "消防"]),
        (APP_ELECTRICAL, ["electrical_load", "强弱电", "负荷"]),
        (APP_HANDOVER, ["commercial_handover", "handover", "交接", "入驻"]),
    ]
    return all(
        agent_polled_gate(
            ctx,
            app_id=app_id,
            concept_terms=terms,
            min_stage=14,
            max_stage=14,
        )
        for app_id, terms in decisive
    )


async def chk_conditional_go_holds_final_payment(ctx) -> bool:
    """Owner recommendation is conditional and retains final payment."""
    owner_mail = await owner_facing_emails(ctx)
    text = "\n".join([stage_response(ctx, stage=14), await workspace_blob(ctx), *(m.text for m in owner_mail)])
    has_conditional = has_any(text, ["conditional", "附条件", "有条件", "暂缓", "no-go"])
    holds_payment = has_any(
        text,
        ["不释放尾款", "暂缓尾款", "hold final payment", "retain", "保留尾款", "尾款待", "扣留"],
    )
    has_open_item = has_any(
        text,
        ["玻璃划痕", "scratch", "punch", "d+30", "4.2", "竣工图", "空气质量", "复测"],
    )
    return has_conditional and holds_payment and has_open_item


async def chk_budget_and_punch_list_are_durable(ctx) -> bool:
    """Budget envelope and open handover items exist in durable artifacts."""
    budget = await read_workspace_file(ctx, "budget_tracker.md")
    punch = await read_workspace_file(ctx, "handover_punch_list.md")
    if not budget_within_envelope(budget) or not punch.strip():
        return False
    has_issue = has_any(punch, ["玻璃", "scratch", "强电", "electrical", "punch", "待闭环", "open"])
    has_owner_or_due = has_any(punch, ["责任人", "owner", "due", "截止", "d+30", "30 天", "30天"])
    return has_issue and has_owner_or_due


CHECKS = [
    ("chk_handover_gates_verified_before_recommendation", chk_handover_gates_verified_before_recommendation, 3.5),
    ("chk_conditional_go_holds_final_payment", chk_conditional_go_holds_final_payment, 3.0),
    ("chk_budget_and_punch_list_are_durable", chk_budget_and_punch_list_are_durable, 2.0),
]


from .stage_3 import chk_quote_hidden_punchlist_in_EML024_caught

CHECKS.append((
    "chk_quote_hidden_punchlist_in_EML024_caught",
    chk_quote_hidden_punchlist_in_EML024_caught,
    2.5,
))
