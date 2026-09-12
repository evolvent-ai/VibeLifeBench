"""
Stage 3 — quote_exclusion checkers (exclusions / P.S. additions / change orders).
"""
from __future__ import annotations

from ._helpers import (
    BUDGET_CAP_CNY,
    BUDGET_RESERVE_MIN_CNY,
    COMPLIANCE_APP_IDS,
    NOISY_WORK_TERMS,
    OWNER_EMAIL,
    RENOVATION_WORKSPACE_FILES,
    agent_tool_call_count,
    agent_tool_called,
    budget_has_committed_pending_reserve,
    budget_total_from_workspace,
    calendar_event_in_state,
    calendar_event_window,
    calendar_events_in_window,
    call,
    compliance_apps,
    count_groups,
    count_tool_categories_called,
    email_date_in_window,
    email_record_matches,
    event_in_phase,
    event_is_noisy,
    event_on_statutory_holiday,
    event_starts_or_ends_outside_window,
    has_all,
    has_any,
    hotel_booking_reservation,
    inbox_email_records,
    matching_email_records,
    read_workspace_file,
    reservation_details,
    schedule_dependency_ok,
    sent_email_records,
    stage_response,
    tool_result_ok,
    visa_application_documents,
    visa_application_history,
    app_status,
    visa_application_state,
    workspace_file_exists,
    workspace_file_text,
    workspace_text,
)


async def chk_quote_exclusions_reconciled(ctx) -> bool:
    """F4: the agent catches the Shenpin quote-v1 *exclusions* — the headline
    ¥760k price excludes design fee, fit-up deposit, and insurance — so the
    true committed cost is reconciled rather than taken at face value.

    OUTCOME-GROUNDED + EQUIVALENCE-TOLERANT: pass when the budget / decision
    artifacts surface ≥2 of the real exclusion concepts (design fee /
    fit-up deposit / insurance not-included) AND a concrete amount appears
    (the exclusion deltas are real numbers). No EML token is required — a
    model that writes "quote excludes ¥40k design fee + ¥30k deposit" passes.
    """
    from ._helpers import count_distinct_amounts
    text = (
        await read_workspace_file(ctx, "budget_tracker.md")
        + "\n"
        + await read_workspace_file(ctx, "vendor_comparison.md")
        + "\n"
        + await read_workspace_file(ctx, "decoration_decisions.md")
    )
    if not text:
        return False
    exclusion_groups = [
        ["design", "design not included", "excl. design", "exclude design"],
        ["scenario-term", "fit-up deposit", "deposit", "guarantee deposit", "deposit"],
        ["contractors all-risk insurance", "insurance", "insurance", "all risk", "insurance not included"],
        ["not included", "excl", "exclude", "not included", "extra charge", "addon", "add-on"],
    ]
    concepts = count_groups(text, exclusion_groups)
    has_amount = count_distinct_amounts(text, lo=10000, hi=900000) >= 1
    return concepts >= 2 and has_amount


async def chk_quote_water_electrical_overage_acknowledged(ctx) -> bool:
    """F4: the agent reconciles the strong/weak-power overage — the ~¥30k
    main-line / scenario-term upgrade needed to reach ≥4kW/100㎡ — against budget.

    OUTCOME-GROUNDED + EQUIVALENCE-TOLERANT: pass when the budget / power
    plan / risk artifacts carry the strong-power concept AND an overage /
    upgrade-cost concept AND a concrete amount, with a reserve / cap
    awareness. No EML / specific-number token is required.
    """
    from ._helpers import count_distinct_amounts
    text = (
        await read_workspace_file(ctx, "budget_tracker.md")
        + "\n"
        + await read_workspace_file(ctx, "strong_weak_power_plan.md")
        + "\n"
        + await read_workspace_file(ctx, "risk_register.md")
    )
    if not text:
        return False
    has_power = has_any(
        text,
        ["strong-current and low-voltage systems", "strong-current", "main line", "scenario-term", "load", "load", "strong electric",
         "strong-electric", "kw/100", "main line", "main-line"],
    )
    has_overage = has_any(
        text,
        ["scenario-term", "overage", "exceed", "scenario-term", "scenario-term", "upgrade", "scenario-term",
         "additional cost", "extra cost", "change order"],
    )
    has_amount = count_distinct_amounts(text, lo=5000, hi=200000) >= 1
    reserve_noted = has_any(text, ["reserve", "reserve", "contingency", "cap", "cap"])
    return has_power and has_overage and has_amount and reserve_noted


async def chk_quote_tax_treatment_clarified_or_pending(ctx) -> bool:
    """The Stage-4 quote omits VAT/fapiao treatment, so the correct outcome is
    a vendor clarification request plus a durable pending flag, not an invented
    final tax decision.
    """
    text = (
        await read_workspace_file(ctx, "budget_tracker.md")
        + "\n"
        + await read_workspace_file(ctx, "vendor_comparison.md")
        + "\n"
        + await read_workspace_file(ctx, "decoration_decisions.md")
    )
    tax_terms = [
        "VAT", "vat", "tax", "scenario-terminvoice", "invoice", "tax included", "tax not included",
        "scenario-term", "fapiao", "invoice",
    ]
    pending_terms = [
        "pending", "pending confirmation", "pending clarification", "scenario-term", "scenario-term", "tbd",
        "clarification", "awaiting reply",
    ]
    durable_pending = has_any(text, tax_terms) and has_any(text, pending_terms)
    if not durable_pending:
        return False

    sent = await sent_email_records(ctx)
    vendor_markers = ["shenpin", "Shenpin", "hi@shenpin-cs.example.com"]
    question_terms = ["confirm", "clarify", "scenario-term", "scenario-term", "scenario-term", "whether", "?", "？"]
    return any(
        has_any(" ".join(record.recipients), vendor_markers)
        and has_any(record.text, tax_terms)
        and has_any(record.text, question_terms)
        for record in sent
    )


async def chk_quote_change_order_handled(ctx) -> bool:
    """F4: the agent processes the mid-project change order (the strong-power
    main-line / scenario-term upgrade, est. ¥30k) — reads the source and logs the
    cost delta against budget.

    OUTCOME-GROUNDED + EQUIVALENCE-TOLERANT: pass when (a) the agent read
    inbound mail in the relevant window, AND (b) a budget artifact records a
    change-order / change / change order concept with a concrete delta amount. No
    EML / exact-number token is required.
    """
    from ._helpers import count_distinct_amounts
    read_evidence = agent_tool_called(
        ctx,
        tool_any=["read_email", "get_emails"],
        min_stage=8,
    )
    text = await read_workspace_file(ctx, "budget_tracker.md")
    text += "\n" + await read_workspace_file(ctx, "risk_register.md")
    if not text:
        return False
    low = text.lower()
    change_concept = has_any(
        low,
        ["change order", "scenario-term", "change", "co_id", "co #", "change order", "scenario-term",
         "additional", "extra cost", "scenario-term", "scenario-term"],
    )
    has_delta = count_distinct_amounts(text, lo=3000, hi=200000) >= 1
    return read_evidence and change_concept and has_delta


async def chk_quote_hidden_punchlist_in_EML024_caught(ctx) -> bool:
    """F4: at handover the agent catches the vendor's hidden-defect P.S. —
    the glass-partition scratch the vendor "polished and won't list" — and
    records a decision (keep on punch list / accept / owner sign-off).

    OUTCOME-GROUNDED + EQUIVALENCE-TOLERANT: pass when the punch list (or
    handover/comms artifacts) surfaces the glass-partition scratch concept
    AND a binary decision. No EML token is required — a model that logs
    "glass partition scratch — vendor says polished; keep open pending
    owner sign-off" passes.
    """
    text = (
        await read_workspace_file(ctx, "handover_punch_list.md")
        + "\n"
        + await read_workspace_file(ctx, "communications_log.md")
        + "\n"
        + await read_workspace_file(ctx, "decoration_decisions.md")
    )
    if not text:
        return False
    low = text.lower()
    item_terms = has_any(
        low,
        ["glasspartition", "glass partition", "partition", "scratch", "scratch", "glass partition",
         "glass-partition", "scenario-term", "scenario-term", "polish"],
    )
    decision_terms = has_any(
        low,
        ["owner sign-off", "owner accepted", "owner accepted", "owner sign-off",
         "keep on punch list", "preserve", "not accept", "rejected", "open",
         "pending", "closed", "closed", "scenario-term", "reinspection"],
    )
    return item_terms and decision_terms


CHECKS = [
]


# The filing first becomes RFI-blocked at Stage 3; score the immediate hold here.
from .stage_5 import chk_filing_no_demolition_while_blocked

CHECKS.append((
    "chk_filing_no_demolition_while_blocked",
    chk_filing_no_demolition_while_blocked,
    3,
))
