"""
Stage 1 — active_source_check checkers (live MCP polling before key decisions).
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
    agent_tool_result_contains,
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


async def chk_active_notion_review_pull_before_shortlist(ctx) -> bool:
    """F2 (KEEP — tool-call evidence): agent queried the Notion vendor /
    contractor reviews source before shortlisting a design-build vendor.

    Robust source-targeting: matches the database name OR any commercial
    design-build provider id family, in either CN/EN. Not an echoed-ID gate
    — it verifies the agent consulted the right source at the right time.
    """
    return agent_tool_called(
        ctx,
        tool_any=["query_database", "get_page", "search_pages", "notion"],
        args_any=[
            "contractor_reviews",
            "contractor-reviews",
            "notion-db-contractor-reviews",
            "contractor_review",
            "commercial_design_build",
            "prov_v3_",
            "design_build",
            "vendor",
        ],
        max_stage=6,
    )


async def chk_active_property_rules_pull_before_calendarizing(ctx) -> bool:
    """F2 (KEEP — tool-call evidence): agent queried the property / building
    rules source before placing noisy / fit-up work on the calendar.

    Robust source-targeting: matches the rules database OR any Lujiazui /
    property rule id family. Verifies the agent consulted the source, not
    that any specific rule token was echoed.
    """
    read_correct_rule = agent_tool_result_contains(
        ctx,
        tool_any=["query_database", "get_page", "notion"],
        args_any=[
            "property_rules", "property-rules", "notion-db-property-rules",
            "property_rule", "rule_property", "rule_lujiazui", "lujiazui",
        ],
        result_groups=[
            ["property rules", "rule_property", "物业", "陆家嘴"],
            ["噪声", "施工时间", "货梯", "holiday", "周末", "工作日"],
        ],
        max_stage=5,
    )
    response = stage_response(ctx, 0) + "\n" + stage_response(ctx, 1)
    applied = count_groups(
        response,
        [
            ["物业", "property", "rule_property"],
            ["噪声", "施工时间", "货梯", "周末", "holiday"],
            ["排期", "日历", "calendar", "避开", "限制", "不得"],
        ],
    ) >= 3
    return read_correct_rule and applied


async def chk_active_inspection_standards_pull_before_handover(ctx) -> bool:
    """F2 (KEEP — tool-call evidence): agent queried the inspection-standards
    source before drafting the final fire / electrical / handover checklist.

    Robust source-targeting: matches the standards database OR any
    inspection-standard id family. Not an echoed-ID gate.
    """
    return agent_tool_called(
        ctx,
        tool_any=["query_database", "get_page", "notion"],
        args_any=[
            "inspection_standards",
            "inspection-standards",
            "notion-db-inspection-standards",
            "inspection_standard",
            "insp_std",
        ],
        min_stage=12,
    )


async def chk_active_compliance_polled_before_demolition(ctx) -> bool:
    """F2 (KEEP — tool-call evidence): agent polled visa_and_advisory for the
    commercial fit-up filing case before driving demolition / fit-up work.

    Robust source-targeting: matches the visa server / endpoints OR the real
    filing application id. Verifies the agent checked live filing status at
    the right time, not that a specific token was echoed.
    """
    observed = agent_tool_result_contains(
        ctx,
        tool_any=["get_visa_application", "list_visa_applications", "visa_and_advisory"],
        args_any=["commercial_fit_up_filing_001", "fit_up_filing", "commercial_fit"],
        result_groups=[
            ["commercial_fit_up_filing_001"],
            ["draft", "pending", "rfi", "approved", "status"],
        ],
        max_stage=9,
    )
    response = stage_response(ctx, 0) + "\n" + stage_response(ctx, 1)
    boundary = count_groups(
        response,
        [
            ["备案", "filing", "commercial_fit_up_filing_001"],
            ["状态", "draft", "pending", "未通过", "待审批"],
            ["拆除前", "开工前", "未批准不", "no-go", "不得开工"],
        ],
    ) >= 3
    return observed and boundary


async def chk_active_quiet_day_recheck_uses_live_tools(ctx) -> bool:
    """F2: on quiet stages 10 and 16, agent called >=4 distinct live tools."""
    categories = [
        {"tool_any": ["get_visa_application", "list_visa_applications"]},
        {"tool_any": ["list_reservations", "get_reservation", "get_room_availability"]},
        {"tool_any": ["get_emails", "read_email"]},
        {"tool_any": ["query_database", "get_page", "search_pages"]},
        {"tool_any": ["get_current_weather", "get_alerts"]},
    ]
    quiet_hits = 0
    for quiet_stage in (10, 11, 16, 17):
        hits = count_tool_categories_called(ctx, categories=categories, stage=quiet_stage)
        quiet_hits = max(quiet_hits, hits)
    return quiet_hits >= 4


async def chk_active_weather_check_before_waterproofing(ctx) -> bool:
    """F2: weather queried for Shanghai before waterproofing / closed-water-test events."""
    return agent_tool_called(
        ctx,
        tool_any=["get_current_weather", "get_alerts"],
        args_any=["shanghai", "shanghai_pudong"],
        min_stage=8,
        max_stage=14,
    )


CHECKS = [
    ('chk_active_notion_review_pull_before_shortlist', chk_active_notion_review_pull_before_shortlist, 6),
    ('chk_active_property_rules_pull_before_calendarizing', chk_active_property_rules_pull_before_calendarizing, 6),
    ('chk_active_compliance_polled_before_demolition', chk_active_compliance_polled_before_demolition, 6),
]
