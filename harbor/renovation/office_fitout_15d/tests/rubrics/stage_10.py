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
        concept_terms=["fire_inspection", "fire safety", "emergency lighting", "scenario-term"],
        min_stage=10,
        max_stage=10,
    ):
        return False
    sent = await sent_email_records(ctx)
    blob = (await workspace_blob(ctx)) + "\n" + "\n".join(item.text for item in sent)
    has_problem = has_any(blob, ["emergency lighting", "emergency lighting", "scenario-term", "evacuation"])
    has_action = has_any(blob, ["scenario-term", "revise", "correction", "add installation", "resubmit", "revise", "scenario-term"])
    return has_problem and has_action


async def chk_smart_control_decision_is_recorded(ctx) -> bool:
    """A clear D10 smart-control choice and budget impact are recorded."""
    response = stage_response(ctx, stage=10)
    owner_mail = await owner_facing_emails(ctx)
    blob = "\n".join([await workspace_blob(ctx), response, *(m.text for m in owner_mail)])
    has_choice = has_any(blob, ["hdl", "buspro", "lutron", "scenario-term", "mijia"])
    has_decision = has_any(blob, ["scenario-term", "scenario-term", "scenario-term", "approve", "selected", "decision"])
    has_cost_or_tradeoff = has_any(
        blob,
        ["45,000", "45000", "45k", "80,000", "80000", "20,000", "20000", "reliable", "agreement open", "scenario-term"],
    )
    return has_choice and has_decision and has_cost_or_tradeoff


CHECKS = [
    ("chk_fire_rfi_repolled_and_recovery_recorded", chk_fire_rfi_repolled_and_recovery_recorded, 3.0),
    ("chk_smart_control_decision_is_recorded", chk_smart_control_decision_is_recorded, 2.0),
]
