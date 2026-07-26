"""
Stage 8 — communication_targeting checkers (right party, concrete asks).
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


async def chk_comm_contractor_specific_quote_clarification(ctx) -> bool:
    """F9: the agent sends targeted, substantive clarifications to vendors
    about the real quote complications (exclusions / tax / strong-power
    overage / glass-partition lead time).

    OUTCOME-GROUNDED + EQUIVALENCE-TOLERANT: pass when ≥1 outbound email to a
    real vendor domain (申品 / 光晟玻璃 / a design-build vendor) discusses a
    concrete quote/clause concept (CN OR EN). No EML token or renovation
    vendor domain is required — the message is judged on whether it targets
    the right party with a concrete ask.
    """
    sent = await sent_email_records(ctx)
    if not sent:
        return False
    vendor_domain_markers = [
        "shenpin-cs", "shenpin", "申品", "guangshen-partition", "光晟",
        "design-build", "公装", "commercial_design_build", "prov_v3_",
    ]
    clause_concepts = [
        "exclusion", "不含", "另计", "excl", "设计费", "design fee",
        "押金", "deposit", "保证金", "vat", "增值税", "发票", "tax",
        "强弱电", "强电", "load", "负荷", "升级", "upgrade", "overage", "超出",
        "lead time", "lead_time", "工期", "进口", "国产", "玻璃隔断",
        "clarify", "确认", "澄清",
    ]
    qualifying = 0
    for s in sent:
        recip_blob = " ".join(s.recipients).lower() + " " + s.text.lower()
        targets_vendor = has_any(recip_blob, vendor_domain_markers)
        discusses_clause = has_any(s.text, clause_concepts)
        # Targeted: a small, specific recipient set (not a broadcast).
        targeted = len({a.lower() for a in s.recipients}) <= 3
        if targets_vendor and discusses_clause and targeted:
            qualifying += 1
    return qualifying >= 1


async def chk_comm_property_filing_email_to_property_only(ctx) -> bool:
    """F9: filing / fit-up / property-coordination emails go to the property
    (and/or the Jingan platform / fire authority) and do NOT leak to design
    vendors.

    OUTCOME-GROUNDED + DECISION-CORRECTNESS + EQUIVALENCE-TOLERANT: pass when
    ≥1 filing/fit-up email exists, targets a property/authority domain, and
    does NOT also include a known design-build vendor recipient. The message
    is grounded by topic (filing / fit-up window / RFI) — no app_id / rule_id
    literal token is required.
    """
    sent = await sent_email_records(ctx)
    if not sent:
        return False
    filing_emails = [
        s for s in sent
        if has_any(
            s.subject + " " + s.text,
            ["filing", "备案", "一件事", "rfi", "fit-up", "fit up", "进场窗口",
             "fit-up 押金", "property", "物业", "占用", "occupancy 申请"],
        )
    ]
    if not filing_emails:
        return False
    property_authority_markers = [
        "lujiazui-fc", "property", "物业", "management@", "jingan", "静安",
        "jingan-fire", "gov.cn", "fire dept", "消防", "platform", "一件事",
    ]
    vendor_leak_markers = [
        "shenpin-cs", "guangshen-partition", "design-build", "公装",
        "prov_v3_", "commercial_design_build",
    ]
    for s in filing_emails:
        recipients = " ".join(s.recipients).lower()
        if not recipients:
            return False
        targets_property = has_any(recipients, property_authority_markers)
        leaked = has_any(recipients, vendor_leak_markers)
        if targets_property and not leaked:
            return True
    return False


async def chk_comm_owner_decision_request_logged(ctx) -> bool:
    """F9: the communications log records owner-facing decision requests with
    concrete data — who decides, the options, money, and a deadline.

    OUTCOME-GROUNDED + EQUIVALENCE-TOLERANT: pass when the comms log shows the
    owner/COO, a decision/options concept, a concrete amount, and a deadline
    (CN OR EN). Anchoring in a specific ID is a BONUS, not the gate — a model
    that logs "Zhou Mu decision: domestic vs import glass, ¥3k delta, by
    07-15" passes without any seed token.
    """
    text = await read_workspace_file(ctx, "communications_log.md")
    if not text:
        return False
    low = text.lower()
    has_owner = has_any(low, ["owner", "zhou mu", "zhou_mu", "周牧", "coo", "业主"])
    has_decision = has_any(
        low, ["decision", "决定", "决策", "options", "选项", "建议", "go/no-go"]
    )
    from ._helpers import count_distinct_amounts
    has_money = (
        count_distinct_amounts(low, lo=1000, hi=2000000) >= 1
        or has_any(low, ["¥", "cny", "rmb", "元", "万"])
    )
    import re as _re
    has_deadline = (
        has_any(low, ["deadline", "截止", "by ", "before", "之前", "due"])
        or bool(_re.search(r"20\d{2}-\d{2}-\d{2}", text))
    )
    return has_owner and has_decision and has_money and has_deadline


async def chk_comm_inspector_dates_confirmed(ctx) -> bool:
    """F9: the agent confirms inspection dates with the right authority
    (fire / electrical / handover) with a concrete date.

    OUTCOME-GROUNDED + EQUIVALENCE-TOLERANT: pass when ≥1 outbound email to an
    inspection/authority party (fire dept / property / inspector / Jingan
    platform) discusses an inspection concept AND carries a real date. No
    insp_std_* / renov_* token is required.
    """
    import re as _re
    sent = await sent_email_records(ctx)
    if not sent:
        return False
    authority_markers = [
        "inspect", "jingan-fire", "消防", "fire dept", "fire-dept", "gov.cn",
        "lujiazui-fc", "property", "物业", "lingdu", "yanjing", "验收", "platform",
    ]
    inspection_concepts = [
        "fire", "消防", "消防验收", "electrical", "强弱电", "强电", "load",
        "负荷", "handover", "交付", "验收", "acceptance", "inspection", "复检",
        "甲醛",
    ]
    for s in sent:
        recip_blob = " ".join(s.recipients).lower() + " " + s.text.lower()
        is_authority = has_any(recip_blob, authority_markers)
        if not is_authority:
            continue
        discusses_inspection = has_any(s.text, inspection_concepts)
        has_date = bool(_re.search(r"20\d{2}-\d{2}-\d{2}", s.text)) or "2026-" in s.text
        if discusses_inspection and has_date:
            return True
    return False


CHECKS = [
    ('chk_comm_contractor_specific_quote_clarification', chk_comm_contractor_specific_quote_clarification, 1.5),
    ('chk_comm_property_filing_email_to_property_only', chk_comm_property_filing_email_to_property_only, 1.5),
    ('chk_comm_owner_decision_request_logged', chk_comm_owner_decision_request_logged, 1.5),
    ('chk_comm_inspector_dates_confirmed', chk_comm_inspector_dates_confirmed, 1.5),
]


# Checks whose triggering facts first become visible by Stage 8.
from .stage_1 import chk_active_weather_check_before_waterproofing
from .stage_3 import (
    chk_quote_change_order_handled,
    chk_quote_water_electrical_overage_acknowledged,
)

CHECKS.extend([
    ("chk_active_weather_check_before_waterproofing", chk_active_weather_check_before_waterproofing, 3),
    ("chk_quote_water_electrical_overage_acknowledged", chk_quote_water_electrical_overage_acknowledged, 2),
    ("chk_quote_change_order_handled", chk_quote_change_order_handled, 2),
])
