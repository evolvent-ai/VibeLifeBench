"""
Stage 9 — evidence checkers (concrete artifact + tool-call counts).
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


# Silent mock_mutation stage indices for this scenario (see event.yaml).
_EVIDENCE_SILENT_MUTATION_STAGES: tuple[int, ...] = (3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 19)

# Quiet stages (no authored user_message; agent gets a silent heartbeat tick).
_EVIDENCE_QUIET_STAGES: tuple[int, ...] = (10, 16)

# Stage where D7_rough_in_calendar_silent mutates the rough-in/inspection calendar.
_EVIDENCE_CALENDAR_MOVE_STAGE: int = 7

_EVIDENCE_ID_REGEX = (
    r"prov_\w+_\d{3}|mat_\w+_\d{3}|rule_property_\w*_?\d{3}"
    r"|insp_std_\w*_?\d{3}|EML-\d{3}|SCH-\d{3}|CHK-\w+-\d{3}|hold_\w+"
    r"|renov_\w+_\d{3}|res_\w+_\d{3}|prov_v\d+_\d{3}|mat_v\d+_\d{3}"
    r"|app_v\d+_\d{3}|rule_property_v\d+_\d{3}|fire_inspection_app_\d{3}"
    r"|electrical_load_app_\d{3}"
)


async def chk_evidence_d5_quote_compared_3plus_vendors(ctx) -> bool:
    """EVIDENCE: vendor_comparison.md genuinely compares ≥3 design-build
    vendors with ≥3 distinct concrete quote amounts.

    DE-BRITTLED for the common failure mode (prose without data)
    while no longer false-negativing a model that NAMES vendors instead of
    echoing prov_* IDs: the vendor count is satisfied by ANY of distinct
    prov_v3_* IDs, distinct vendor names, or ≥3 table rows; the data gate is
    ≥3 distinct quote amounts in any format. Concrete data is still required;
    a specific ID token is not.
    """
    import re as _re
    from ._helpers import count_distinct_amounts
    text = (
        await read_workspace_file(ctx, "vendor_comparison.md")
        + "\n"
        + await read_workspace_file(ctx, "decoration_decisions.md")
    )
    if not text:
        return False
    low = text.lower()
    prov_ids = set(_re.findall(r"prov_v\d+_\d{3}", low))
    vendor_names = {
        n for n in ("沪安", "申品", "永信", "modulux", "chenpin", "hushang")
        if n.lower() in low
    }
    table_rows = len(_re.findall(r"^\s*\|.*\|\s*$", text, _re.MULTILINE))
    distinct_vendor_signal = max(
        len(prov_ids), len(vendor_names), max(0, table_rows - 1)
    )
    distinct_amounts = count_distinct_amounts(text, lo=10000, hi=2000000)
    return distinct_vendor_signal >= 3 and distinct_amounts >= 3


async def chk_evidence_d10_budget_split_3columns(ctx) -> bool:
    """EVIDENCE: budget_tracker.md has structured committed / pending / reserve buckets.

    All three column families must be present (case-insensitive). Tests
    that the model didn't just write a flat total — it must show the
    three-way split that lets a reader judge if commitments are safe.
    """
    text = await read_workspace_file(ctx, "budget_tracker.md")
    if not text:
        return False
    committed_group = ["已签", "已承诺", "已锁定", "committed", "confirmed"]
    reserve_group = ["预留", "reserve", "buffer", "保留", "contingency"]
    pending_group = ["pending", "待定", "在询", "考虑中", "待签"]
    has_committed = has_any(text, committed_group)
    has_reserve = has_any(text, reserve_group)
    has_pending = has_any(text, pending_group)
    return has_committed and has_reserve and has_pending


async def chk_evidence_d15_risk_register_5_risks_with_mitigation(ctx) -> bool:
    """EVIDENCE: risk_register.md lists ≥5 risks with ≥3 mitigation entries.

    Counts risk markers (the word "risk"/"red flag" or numbered list
    items) AND mitigation language. Without mitigation a risk register
    is just a list of complaints.
    """
    import re as _re
    text = await read_workspace_file(ctx, "risk_register.md")
    if not text:
        return False
    risk_count = len(_re.findall(r"[Rr]isk|[Rr]ed\s*flag|风险", text))
    bullet_count = len(_re.findall(r"^\s*(?:[-*+]|\d+[.)])\s+\S", text, _re.MULTILINE))
    risks_ok = max(risk_count, bullet_count) >= 5
    mitigation_terms = [
        "方案", "应对", "缓解", "mitigation", "mitigat", "remediation",
        "缓释", "fallback", "应急", "对策",
    ]
    mit_count = sum(
        text.lower().count(term.lower()) for term in mitigation_terms
    )
    return risks_ok and mit_count >= 3


async def chk_evidence_visa_polled_3plus_times_pre_demolition(ctx) -> bool:
    """EVIDENCE: agent polled visa_and_advisory ≥3 times before stage 6.

    The renovation has four compliance applications. A serious agent
    will re-check filing / waterproof / electrical / handover state
    repeatedly through early stages. Fewer than 3 calls before stage 6
    means the agent went into demolition planning without verifying
    permit status.
    """
    count = agent_tool_call_count(
        ctx,
        tool_any=[
            "get_visa_application",
            "list_visa_applications",
            "visa_and_advisory",
        ],
        max_stage=5,
    )
    return count >= 3


async def chk_evidence_live_gate_repolled_after_silent_mutations(ctx) -> bool:
    """At least three distinct stages re-polled the live compliance source
    within two stages after scripted visa/advisory mutations.

    The former Notion-only check queried a service that did not carry these
    mutations and could count one overlapping poll three times. This version
    follows the actual mutation service and requires distinct-stage evidence.
    """
    candidate_poll_stages = {
        poll_stage
        for mut_stage in _EVIDENCE_SILENT_MUTATION_STAGES
        for poll_stage in range(mut_stage, min(mut_stage + 2, 20) + 1)
        if agent_tool_called(
            ctx,
            tool_any=[
                "get_visa_application",
                "list_visa_applications",
                "get_advisory",
                "visa_and_advisory",
            ],
            stage=poll_stage,
        )
    }
    return len(candidate_poll_stages) >= 3


async def chk_evidence_calendar_repolled_after_event_move(ctx) -> bool:
    """EVIDENCE: agent re-queried calendar within 1-2 stages of a silent event move.

    Looks at the real Stage-7 rough-in calendar mutation
    (event.yaml ``D7_rough_in_calendar_silent``) and
    requires a ``list_events`` (or ``get_events``) call in the next 1-2
    stages.
    """
    s = _EVIDENCE_CALENDAR_MOVE_STAGE
    return agent_tool_called(
        ctx,
        tool_any=["list_events", "get_events", "calendar"],
        min_stage=s,
        max_stage=s + 2,
    )


async def chk_evidence_hotel_booking_polled_for_real_holds(ctx) -> bool:
    """The live reservation/hold source was re-polled on at least two distinct
    stages during the Stage-5..12 hold-life window.

    Two duplicate calls in one turn do not prove that expiry was monitored over
    time, so stage diversity is part of the evidence.
    """
    polled_stages = {
        stage
        for stage in range(5, 13)
        if agent_tool_called(
            ctx,
            tool_any=["list_reservations", "get_reservation", "hotel_booking"],
            stage=stage,
        )
    }
    return len(polled_stages) >= 2


async def chk_evidence_owner_decision_quantified_with_data(ctx) -> bool:
    """EVIDENCE: outbound owner-facing emails carry numbers + an ID ref + a risk callout.

    Scans sent_email_records() for messages addressed to OWNER_EMAIL.
    For each owner-facing email, requires:
        * ≥2 specific numbers (¥ amounts or N天/N day patterns)
        * ≥1 reference to a P1 ID (provider/material/rule/insp/app/hold)
        * ≥1 risk/decision-language token (risk/blocker/go/no-go/RFI/...)
    The check passes if at least 2 owner-facing emails meet the bar.
    """
    import re as _re
    sent = await sent_email_records(ctx)
    if not sent:
        return False
    owner = OWNER_EMAIL.lower()
    qualifying = 0
    id_re = _re.compile(_EVIDENCE_ID_REGEX, _re.IGNORECASE)
    risk_tokens = [
        "risk", "blocker", "block", "go/no-go", "go-no-go",
        "rfi", "delay", "脱期", "顺延", "风险", "拦路",
        "decision", "决策", "拍板",
    ]
    for rec in sent:
        recipients = {addr.lower() for addr in rec.recipients}
        if not any(m in " ".join(recipients) for m in (owner, "zhou_mu", "startup-coo")):
            continue
        text = rec.text
        # Numeric density: count ¥ amounts and "<n>天/day" mentions.
        money_hits = len(_re.findall(r"(?:¥|￥|cny|rmb)\s*\d", text, _re.IGNORECASE))
        money_hits += len(_re.findall(r"\d[\d,]{2,}\s*(?:元|cny|rmb)", text, _re.IGNORECASE))
        day_hits = len(_re.findall(r"\d{1,3}\s*(?:天|日|day|d\b)", text, _re.IGNORECASE))
        numbers_ok = (money_hits + day_hits) >= 2
        # Concrete-anchor gate is DE-BRITTLED: any genuine ID, ISO date, or
        # currency amount counts — not a specific seed token. A capable model
        # that quantifies with real numbers + dates passes without echoing a
        # provider/material/rule ID.
        anchor_ok = (
            bool(id_re.search(text))
            or bool(_re.search(r"20\d{2}-\d{2}-\d{2}", text))
            or numbers_ok
        )
        risk_ok = has_any(text, risk_tokens)
        if numbers_ok and anchor_ok and risk_ok:
            qualifying += 1
    return qualifying >= 2


async def chk_evidence_quiet_day_proactive_polling(ctx) -> bool:
    """EVIDENCE: ≥2 quiet stages each saw a proactive tool query.

    Quiet stages get only a silent heartbeat tick. A passive agent will
    do nothing. A proactive agent will use the quiet day to re-check
    visa / hotel / notion / calendar state. We require at least 2 quiet
    stages to show such a poll.
    """
    polled_count = 0
    for q_stage in _EVIDENCE_QUIET_STAGES:
        polled = agent_tool_called(
            ctx,
            tool_any=[
                "get_visa_application",
                "list_visa_applications",
                "list_reservations",
                "get_reservation",
                "query_database",
                "get_page",
                "search_pages",
                "list_events",
                "get_emails",
                "read_email",
            ],
            stage=q_stage,
        )
        if polled:
            polled_count += 1
    return polled_count >= 2


async def chk_evidence_email_targeted_with_specific_id_refs(ctx) -> bool:
    """EVIDENCE: outbound emails are TARGETED and GROUNDED rather than generic
    prose that could be about any project.

    DE-BRITTLED (was: ≥80% must echo a literal P1 ID — that false-negatives a
    capable model that grounds with names/dates/amounts, and false-positives
    a token-matcher who pastes an ID without substance). The grounding gate
    now accepts ANY concrete anchor — a real ID, an ISO date, a currency
    amount, OR a named scenario entity (a gate/app concept, a vendor name, a
    rule reference). We require ≥70% of the first 5 outbound emails to be
    grounded by at least one such anchor.
    """
    import re as _re
    sent = await sent_email_records(ctx)
    if not sent:
        return False
    id_re = _re.compile(_EVIDENCE_ID_REGEX, _re.IGNORECASE)
    entity_terms = [
        "fire", "消防", "消防验收", "electrical", "强弱电", "强电", "load", "负荷",
        "insurance", "工程一切险", "保险", "handover", "交付", "入驻", "filing",
        "备案", "一件事", "fit-up", "玻璃隔断", "应急照明", "甲醛", "申品", "光晟",
        "强弱电 ≥4kw", "kw/100",
    ]
    sample = sent[:5] if len(sent) >= 5 else sent
    if not sample:
        return False
    grounded = 0
    for rec in sample:
        text = rec.text
        anchor = (
            bool(id_re.search(text))
            or bool(_re.search(r"20\d{2}-\d{2}-\d{2}", text))
            or bool(_re.search(r"(?:¥|￥|cny|rmb)\s*\d", text, _re.IGNORECASE))
            or has_any(text, entity_terms)
        )
        if anchor:
            grounded += 1
    return grounded / len(sample) >= 0.7


async def chk_evidence_badge_compliance_planned(ctx) -> bool:
    """EVIDENCE (D9 + D11 lobby security badge): schedule.md OR
    risk_register.md surfaces fit-up worker badge / ID requirement
    AND the 7-day advance notice / lead-time concept.

    Multi-path acceptance — at least one path must hold:

      Path A — schedule.md mentions worker badge / ID / 实体 badge /
      fit-up 工人 准入 AND a 7-day / D-7 / 7 天 / 7天 / 提前 7
      lead-time annotation (proximity within 300 chars).
      Path B — risk_register.md flags a badge / 准入 risk with a
      mitigation referencing the 7-day advance notice.
      Path C — communications_log.md documents an outbound (vendor /
      property) message coordinating badge applications 7 days in
      advance.
    """
    from ._helpers import proximity_hit

    badge_terms = [
        "badge", "id badge", "worker_badge", "工人 badge", "工人badge",
        "工人 准入", "fit-up 工人", "fit-up worker", "实体 id", "实体id",
        "实体 badge", "实体badge", "工号", "门禁卡", "工人 名单",
        "lobby security", "大堂保安", "大堂 保安", "rule_lujiazui_003",
    ]
    leadtime_terms = [
        "7 天", "7天", "7-day", "7 day", "7 days", "d-7", "提前 7",
        "提前7", "lead time 7", "advance notice 7", "advance 7",
        "seven day", "seven-day", "7d advance",
    ]

    schedule_text = await read_workspace_file(ctx, "schedule.md")
    risk_text = await read_workspace_file(ctx, "risk_register.md")
    comms_text = await read_workspace_file(ctx, "communications_log.md")

    # Path A: schedule.md proximity hit.
    path_a = proximity_hit(schedule_text, badge_terms, leadtime_terms, window=300)

    # Path B: risk_register proximity hit.
    path_b = proximity_hit(risk_text, badge_terms, leadtime_terms, window=300)

    # Path C: communications_log proximity hit (vendor / property coord).
    path_c = proximity_hit(comms_text, badge_terms, leadtime_terms, window=300)

    return path_a or path_b or path_c


CHECKS = [
    ('chk_evidence_d5_quote_compared_3plus_vendors', chk_evidence_d5_quote_compared_3plus_vendors, 3),
    ('chk_evidence_d10_budget_split_3columns', chk_evidence_d10_budget_split_3columns, 3),
    ('chk_evidence_d15_risk_register_5_risks_with_mitigation', chk_evidence_d15_risk_register_5_risks_with_mitigation, 3),
    ('chk_evidence_visa_polled_3plus_times_pre_demolition', chk_evidence_visa_polled_3plus_times_pre_demolition, 3.75),
    ('chk_evidence_calendar_repolled_after_event_move', chk_evidence_calendar_repolled_after_event_move, 3),
    ('chk_evidence_owner_decision_quantified_with_data', chk_evidence_owner_decision_quantified_with_data, 3),
    ('chk_evidence_email_targeted_with_specific_id_refs', chk_evidence_email_targeted_with_specific_id_refs, 3),
    ('chk_evidence_badge_compliance_planned', chk_evidence_badge_compliance_planned, 2.5),
]


from .stage_6 import (
    chk_material_cabinet_lead_time_fits_deadline,
    chk_material_delivery_calendar_event_exists,
    chk_material_stock_polled_after_mutation,
    chk_material_tile_backorder_acknowledged,
)

CHECKS.extend([
    ("chk_material_cabinet_lead_time_fits_deadline", chk_material_cabinet_lead_time_fits_deadline, 3.25),
    ("chk_material_tile_backorder_acknowledged", chk_material_tile_backorder_acknowledged, 2.6),
    ("chk_material_delivery_calendar_event_exists", chk_material_delivery_calendar_event_exists, 1.95),
    ("chk_material_stock_polled_after_mutation", chk_material_stock_polled_after_mutation, 3.25),
])
