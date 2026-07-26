"""Stage 10 — fire-drawing RFI recovery and smart-control selection."""
from __future__ import annotations

from ._helpers import (
    APP_FIRE,
    agent_polled_gate,
    app_status,
    has_any,
    owner_facing_emails,
    sent_email_records,
    stage_response,
    workspace_blob,
)


async def chk_fire_rfi_repolled_and_recovery_recorded(ctx) -> bool:
    """The agent verifies the live fire RFI and records a concrete correction.

    The scripted RFI alone is never sufficient: the agent must query the gate
    in Stage 10 and leave a durable or outbound recovery action covering the
    rejected emergency-lighting / evacuation drawing.
    """
    if (await app_status(ctx, APP_FIRE)) != "rfi":
        return False
    if not agent_polled_gate(
        ctx,
        app_id=APP_FIRE,
        concept_terms=["fire_inspection", "消防", "应急照明", "疏散"],
        min_stage=10,
        max_stage=10,
    ):
        return False
    sent = await sent_email_records(ctx)
    blob = (await workspace_blob(ctx)) + "\n" + "\n".join(item.text for item in sent)
    has_problem = has_any(blob, ["应急照明", "emergency lighting", "疏散", "evacuation"])
    has_action = has_any(blob, ["重绘", "修订", "补正", "加装", "resubmit", "revise", "整改"])
    return has_problem and has_action


async def chk_smart_control_decision_is_recorded(ctx) -> bool:
    """A clear D10 smart-control choice and budget impact are recorded."""
    response = stage_response(ctx, stage=10)
    owner_mail = await owner_facing_emails(ctx)
    blob = "\n".join([await workspace_blob(ctx), response, *(m.text for m in owner_mail)])
    has_choice = has_any(blob, ["hdl", "buspro", "lutron", "米家", "mijia"])
    has_decision = has_any(blob, ["选择", "选定", "推荐", "approve", "selected", "决定"])
    has_cost_or_tradeoff = has_any(
        blob,
        ["45,000", "45000", "45k", "80,000", "80000", "20,000", "20000", "可靠", "协议开放", "维护"],
    )
    return has_choice and has_decision and has_cost_or_tradeoff


CHECKS = [
    ("chk_fire_rfi_repolled_and_recovery_recorded", chk_fire_rfi_repolled_and_recovery_recorded, 3.0),
    ("chk_smart_control_decision_is_recorded", chk_smart_control_decision_is_recorded, 2.0),
]
