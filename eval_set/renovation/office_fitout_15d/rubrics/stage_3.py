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
    """F4: the agent catches the 申品 quote-v1 *exclusions* — the headline
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
        ["设计费", "design fee", "不含设计", "excl. design", "exclude design"],
        ["押金", "fit-up 押金", "deposit", "保证金", "定金"],
        ["工程一切险", "保险", "insurance", "all risk", "不含险"],
        ["不含", "excl", "exclude", "not included", "另计", "addon", "add-on"],
    ]
    concepts = count_groups(text, exclusion_groups)
    has_amount = count_distinct_amounts(text, lo=10000, hi=900000) >= 1
    return concepts >= 2 and has_amount


async def chk_quote_water_electrical_overage_acknowledged(ctx) -> bool:
    """F4: the agent reconciles the strong/weak-power overage — the ~¥30k
    main-line / 电箱 upgrade needed to reach ≥4kW/100㎡ — against budget.

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
        ["强弱电", "强电", "主线", "电箱", "load", "负荷", "strong electric",
         "strong-electric", "kw/100", "main line", "main-line"],
    )
    has_overage = has_any(
        text,
        ["超出", "overage", "exceed", "额外成本", "额外", "upgrade", "升级",
         "additional cost", "extra cost", "增项"],
    )
    has_amount = count_distinct_amounts(text, lo=5000, hi=200000) >= 1
    reserve_noted = has_any(text, ["reserve", "预留", "contingency", "cap", "上限"])
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
        "增值税", "vat", "tax", "专用发票", "发票", "含税", "不含税",
        "税率", "fapiao", "invoice",
    ]
    pending_terms = [
        "pending", "待确认", "待澄清", "澄清中", "未确认", "tbd",
        "clarification", "待回复",
    ]
    durable_pending = has_any(text, tax_terms) and has_any(text, pending_terms)
    if not durable_pending:
        return False

    sent = await sent_email_records(ctx)
    vendor_markers = ["shenpin", "申品", "hi@shenpin-cs.example.com"]
    question_terms = ["confirm", "clarify", "是否", "请确认", "请澄清", "whether", "?", "？"]
    return any(
        has_any(" ".join(record.recipients), vendor_markers)
        and has_any(record.text, tax_terms)
        and has_any(record.text, question_terms)
        for record in sent
    )


async def chk_quote_change_order_handled(ctx) -> bool:
    """F4: the agent processes the mid-project change order (the strong-power
    main-line / 电箱 upgrade, est. ¥30k) — reads the source and logs the
    cost delta against budget.

    OUTCOME-GROUNDED + EQUIVALENCE-TOLERANT: pass when (a) the agent read
    inbound mail in the relevant window, AND (b) a budget artifact records a
    change-order / 变更 / 增项 concept with a concrete delta amount. No
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
        ["change order", "签证", "变更", "co_id", "co #", "增项", "追加",
         "additional", "extra cost", "额外成本", "升级"],
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
        ["玻璃隔断", "玻璃 隔断", "隔断", "划痕", "scratch", "glass partition",
         "glass-partition", "打磨", "抛光", "polish"],
    )
    decision_terms = has_any(
        low,
        ["owner sign-off", "owner accepted", "业主接受", "业主签字",
         "keep on punch list", "保留", "不接受", "rejected", "open",
         "pending", "closed", "已关闭", "整改", "复检"],
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
