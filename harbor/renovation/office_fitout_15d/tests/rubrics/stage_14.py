"""Stage 14 — evidence-gated conditional handover and final-payment hold."""
from __future__ import annotations

from ._helpers import (
    APP_ELECTRICAL,
    APP_FILING,
    APP_FIRE,
    APP_HANDOVER,
    APP_INSURANCE,
    agent_polled_gate,
    budget_within_envelope,
    has_any,
    owner_facing_emails,
    read_workspace_file,
    stage_response,
    workspace_blob,
)


async def chk_handover_gates_verified_before_recommendation(ctx) -> bool:
    """The agent polled the decisive gates before making a handover recommendation."""
    decisive = [
        (APP_FIRE, ["fire_inspection", "fire safety"]),
        (APP_ELECTRICAL, ["electrical_load", "strong-current and low-voltage systems", "load"]),
        (APP_HANDOVER, ["commercial_handover", "handover", "handover", "occupancy"]),
    ]
    return all(
        agent_polled_gate(
            ctx,
            app_id=app_id,
            concept_terms=terms,
            min_stage=14,
            max_stage=20,
        )
        for app_id, terms in decisive
    )


async def chk_conditional_go_holds_final_payment(ctx) -> bool:
    """Owner recommendation is conditional and retains final payment."""
    owner_mail = await owner_facing_emails(ctx)
    text = "\n".join([stage_response(ctx, stage=14), await workspace_blob(ctx), *(m.text for m in owner_mail)])
    has_conditional = has_any(text, ["conditional", "conditional", "scenario-termcondition", "scenario-term", "no-go"])
    holds_payment = has_any(
        text,
        ["do not release final payment", "scenario-termfinal payment", "hold final payment", "retain", "retain final payment", "final payment pending", "scenario-term"],
    )
    has_open_item = has_any(
        text,
        ["glassscratch", "scratch", "punch", "d+30", "4.2", "as-built drawing", "scenario-term", "retest"],
    )
    return has_conditional and holds_payment and has_open_item


async def chk_budget_and_punch_list_are_durable(ctx) -> bool:
    """Budget envelope and open handover items exist in durable artifacts."""
    budget = await read_workspace_file(ctx, "budget_tracker.md")
    punch = await read_workspace_file(ctx, "handover_punch_list.md")
    if not budget_within_envelope(budget) or not punch.strip():
        return False
    has_issue = has_any(punch, ["glass", "scratch", "strong-current", "electrical", "punch", "pending closure", "open"])
    has_owner_or_due = has_any(punch, ["scenario-term", "owner", "due", "scenario-term", "d+30", "30 days", "30days"])
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
