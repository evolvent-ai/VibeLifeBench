"""
Stage 2 — provider_shortlist checkers (reviews / holds / availability evidence).
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


async def chk_shortlist_excludes_high_risk_kuaijie(ctx) -> bool:
    """F3: the agent surfaces the high-risk design-build vendor's red flags
    (申品 prov_v3_002: only takes ≥300㎡, non-refundable deposit, later a
    kickback offer) and either declines it or attaches an explicit risk
    note / owner-accepted-risk caveat if selected.

    OUTCOME-GROUNDED + EQUIVALENCE-TOLERANT: the risky vendor is identified
    by ANY of its real markers (name 申品 / prov_v3_002 / its complaint
    keywords) and the awareness is shown as a risk CONCEPT (CN OR EN). A
    capable model that names "申品" instead of echoing the ID still passes.
    No single literal ID is required.
    """
    text = (
        await read_workspace_file(ctx, "vendor_comparison.md")
        + "\n"
        + await read_workspace_file(ctx, "fit_out_plan.md")
        + "\n"
        + await read_workspace_file(ctx, "decoration_decisions.md")
        + "\n"
        + await read_workspace_file(ctx, "risk_register.md")
    )
    if not text:
        return False
    from ._helpers import proximity_hit
    vendor_markers = ["申品", "shenpin", "prov_v3_002"]
    if not has_any(text, vendor_markers):
        # Awareness can also be shown generically: any vendor flagged with a
        # commercial design-build risk concept counts.
        generic_risk = proximity_hit(
            text,
            ["vendor", "供应商", "design-build", "公装", "承包商"],
            ["risk", "风险", "red flag", "不退", "deposit", "押金", "排除",
             "exclude", "不推荐", "caution"],
            window=200,
        )
        return generic_risk
    # Vendor named: require a risk concept attached near it OR an exclusion.
    risk_terms = [
        "risk", "风险", "red flag", "不退", "non-refundable", "押金 不退",
        "deposit", "押金", "最低 300", "≥300", "仅承接", "min project",
        "不推荐", "exclude", "排除", "ethics", "贿赂", "kickback", "感谢费",
        "owner accepted", "业主接受", "caveat", "caution", "已知风险",
    ]
    return proximity_hit(text, vendor_markers, risk_terms, window=300) or has_any(
        text, ["排除 申品", "不选 申品", "decline shenpin", "exclude shenpin"],
    )


async def chk_shortlist_evidence_cites_review_ids(ctx) -> bool:
    """F3: the vendor comparison is grounded in real review evidence —
    multiple vendors are compared with concrete rating / review signals.

    OUTCOME-GROUNDED + EQUIVALENCE-TOLERANT (review-anchor demoted): we
    require ≥2 distinct vendors AND a review/rating SIGNAL (a numeric rating
    like 4.8/5, a review-count, or rating/口碑/评价 vocabulary). Echoing a
    specific rev_* / prov_* ID is a BONUS, never the gate — a model that
    writes "申品 4.8★ (94 reviews)" passes without any seed token.
    """
    import re as _re
    text = await read_workspace_file(ctx, "vendor_comparison.md")
    if not text:
        return False
    low = text.lower()
    prov_ids = set(_re.findall(r"prov_v\d+_\d{3}", low))
    vendor_names = {
        n for n in ("沪安", "申品", "永信", "modulux", "chenpin", "hushang")
        if n.lower() in low
    }
    distinct_vendors = max(len(prov_ids), len(vendor_names))
    # Review/rating signal (any form).
    rating_signal = (
        bool(_re.search(r"\b[1-5](?:\.\d)?\s*(?:/\s*5|★|星|stars?)", low))
        or has_any(low, ["rating", "评分", "评级", "口碑", "review", "评价", "好评"])
    )
    return distinct_vendors >= 2 and rating_signal


async def chk_shortlist_holds_tracked_with_expiry(ctx) -> bool:
    """F3: vendor holds / deposits with expiry are tracked with a decision.

    OUTCOME-GROUNDED + STATE-AWARE: pass if BOTH (a) the agent polled
    hotel_booking reservation state during the hold-life window, AND (b) the
    workspace records a hold/deposit with an expiry date AND an action verb
    (confirm / release / extend / 锁定 / 放弃 / 续约). The expiry-tracking
    concept and a real ISO date are required, but no specific hold_id /
    prov_* token is — a model that writes the real hold expiry it read from
    state (e.g. "deposit hold expires 2026-06-10, decision: release") passes.
    """
    import re as _re
    polled = agent_tool_called(
        ctx,
        tool_any=[
            "list_reservations", "get_reservation", "get_room_availability",
            "hotel_booking",
        ],
        max_stage=12,
    )
    text = (
        await read_workspace_file(ctx, "vendor_comparison.md")
        + "\n"
        + await read_workspace_file(ctx, "risk_register.md")
        + "\n"
        + await read_workspace_file(ctx, "decoration_decisions.md")
        + "\n"
        + await read_workspace_file(ctx, "communications_log.md")
    )
    if not text:
        return False
    low = text.lower()
    has_hold_concept = has_any(
        low,
        ["hold", "deposit", "押金", "定金", "expiry", "expires", "到期",
         "有效期", "refund", "退款", "cancellation"],
    )
    has_expiry_date = bool(_re.search(r"20\d{2}-\d{2}-\d{2}", text))
    has_decision = has_any(
        low,
        ["confirm", "release", "extend", "锁", "放弃", "续约", "确认",
         "释放", "退还", "保留", "decision"],
    )
    return polled and has_hold_concept and has_expiry_date and has_decision


async def chk_shortlist_call_hotel_booking_for_availability(ctx) -> bool:
    """F3 (KEEP — tool-call evidence + state grounding): agent polled
    hotel_booking (the vendor-hold backend) for availability / holds, and at
    least one reservation exists in live state.

    Robust source-targeting: matches any hotel_booking endpoint with no
    requirement to echo a specific hold_id / prov_* token.
    """
    called = agent_tool_called(
        ctx,
        tool_any=[
            "search_hotels",
            "get_room_availability",
            "list_reservations",
            "get_reservation",
            "hotel_booking",
        ],
        max_stage=12,
    )
    if not called:
        return False
    # State grounding: verify at least 1 reservation exists in live state.
    reservations = await reservation_details(ctx)
    return len(reservations) >= 1


CHECKS = [
    ('chk_shortlist_excludes_high_risk_kuaijie', chk_shortlist_excludes_high_risk_kuaijie, 2),
    ('chk_shortlist_evidence_cites_review_ids', chk_shortlist_evidence_cites_review_ids, 1.5),
    ('chk_shortlist_holds_tracked_with_expiry', chk_shortlist_holds_tracked_with_expiry, 2),
    ('chk_shortlist_call_hotel_booking_for_availability', chk_shortlist_call_hotel_booking_for_availability, 1.5),
]
