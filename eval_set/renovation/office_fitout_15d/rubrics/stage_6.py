"""
Stage 6 — material_constraints checkers (lead time, stock, VOC, delivery).
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


async def chk_material_cabinet_lead_time_fits_deadline(ctx) -> bool:
    """F7: a long-lead material decision (the glass partition / glass door /
    furniture) is made with lead-time awareness that fits the 60-day fit-up
    window and the 09-01 occupancy date.

    OUTCOME-GROUNDED + EQUIVALENCE-TOLERANT: pass when a decoration/material
    artifact records a long-lead item concept AND lead-time vocabulary AND a
    scheduling anchor (an order/install/delivery date or a day count). No
    specific mat_* token is required — a model that writes "glass partition:
    domestic, 7d lead, order by 07-15" passes.
    """
    import re as _re
    # ANTI-FREEBIE (DETECTION): the long-lead constraint (glass-partition /
    # import customs lead-time) lands as a D9 inbound + lives in the Notion
    # material catalog. A workspace lead-time line alone does not prove the
    # agent DISCOVERED the real item, so require the agent to have queried a
    # material source (catalog / supplier mail) in a plausible window.
    detected = agent_tool_called(
        ctx,
        tool_any=["query_database", "get_page", "read_email", "get_emails", "notion"],
        args_any=[
            "material_catalog", "material catalog", "mat_glass", "mat_workstation",
            "mat_smart_control", "glass_partition", "玻璃隔断", "光晟", "家具",
            "furniture", "工位", "workstation", "lead time", "lead_time", "进口",
            "import", "海关", "customs",
        ],
        min_stage=5,
    )
    if not detected:
        return False
    text = (
        await read_workspace_file(ctx, "decoration_decisions.md")
        + "\n"
        + await read_workspace_file(ctx, "strong_weak_power_plan.md")
        + "\n"
        + await read_workspace_file(ctx, "schedule.md")
    )
    if not text:
        return False
    low = text.lower()
    long_lead_item = has_any(
        low,
        ["glass partition", "玻璃隔断", "隔断", "glass door", "玻璃门",
         "furniture", "家具", "工位", "workstation", "import", "进口", "海关"],
    )
    if not long_lead_item:
        return False
    has_lead_ack = has_any(
        low,
        ["lead_time", "lead time", "工期", "交付周期", "天", "days", "lead",
         "delivery cycle"],
    )
    has_schedule_anchor = (
        has_any(low, ["order_date", "install_date", "下单", "安装日期",
                      "delivery_date", "到货日期", "order by", "before"])
        or bool(_re.search(r"20\d{2}-\d{2}-\d{2}", text))
        or bool(_re.search(r"\d{1,3}\s*(?:d\b|day|天)", low))
    )
    return has_lead_ack and has_schedule_anchor


async def chk_material_tile_backorder_acknowledged(ctx) -> bool:
    """F7: the import-glass customs/lead-time delay is acknowledged with a
    substitute or quantified delay (domestic vs import, 21d vs 7d).

    OUTCOME-GROUNDED + EQUIVALENCE-TOLERANT: pass when a decoration artifact
    surfaces the import/backorder/customs-delay concept AND either proposes
    an alternative (domestic / 国产 / substitute) OR quantifies the delay in
    days. No mat_* token is required.
    """
    import re as _re
    # ANTI-FREEBIE (DETECTION): the import-glass customs/backorder delay is a
    # D9 visible inbound + a Notion material-catalog state; a workspace
    # backorder note alone is response-without-discovery. Require the agent to
    # have queried a material source (catalog / supplier mail) in-window.
    detected = agent_tool_called(
        ctx,
        tool_any=["query_database", "get_page", "read_email", "get_emails", "notion"],
        args_any=[
            "material_catalog", "material catalog", "mat_glass", "glass_partition",
            "玻璃隔断", "光晟", "进口", "import", "海关", "customs", "backorder",
            "缺货", "lead time", "lead_time",
        ],
        min_stage=5,
    )
    if not detected:
        return False
    text = (
        await read_workspace_file(ctx, "decoration_decisions.md")
        + "\n"
        + await read_workspace_file(ctx, "risk_register.md")
    )
    if not text:
        return False
    low = text.lower()
    has_backorder = has_any(
        low,
        ["backorder", "缺货", "调货", "substitute", "替代", "延期", "海关",
         "customs", "import", "进口", "lead time", "lead_time", "21",
         "delay", "缺", "out of stock"],
    )
    if not has_backorder:
        return False
    has_alt = has_any(
        low,
        ["国产", "domestic", "saint-gobain", "替代", "alternative",
         "substitute", "改用", "switch to", "改为"],
    )
    has_delay_days = bool(_re.search(r"\d{1,3}\s*(?:d\b|day|天)", low))
    return has_alt or has_delay_days


async def chk_material_voc_compliance_for_air_quality(ctx) -> bool:
    """F7: main materials carry a low-formaldehyde / VOC compliance note tied
    to the ≤0.05 mg/m³ retest gate.

    OUTCOME-GROUNDED + EQUIVALENCE-TOLERANT: pass when a decoration / fire /
    handover artifact carries a VOC/formaldehyde compliance concept AND
    links it to a material/main-material selection. No insp_std_010 / mat_*
    token is required.
    """
    text = (
        await read_workspace_file(ctx, "decoration_decisions.md")
        + "\n"
        + await read_workspace_file(ctx, "fire_compliance_checklist.md")
        + "\n"
        + await read_workspace_file(ctx, "handover_punch_list.md")
    )
    if not text:
        return False
    low = text.lower()
    voc_terms = has_any(
        low,
        ["low_voc", "low voc", "e0", "e1", "环保", "甲醛", "gb 18582",
         "gb 50325", "tvoc", "voc", "formaldehyde", "0.05", "≤0.05"],
    )
    material_link = has_any(
        low,
        ["主材", "material", "材料", "sku", "partition", "隔断", "paint",
         "涂料", "furniture", "家具", "板材", "证书", "certificate", "declaration",
         "声明"],
    )
    return voc_terms and material_link


async def chk_material_stock_polled_after_mutation(ctx) -> bool:
    """F7 (KEEP — tool-call evidence + state grounding): after the seeded
    material mutation (glass-partition lead-time / customs delay), the agent
    re-queried the material source and surfaced a material outcome.

    Robust source-targeting: matches the material catalog source OR any
    real material id family / supplier inbound. No requirement to echo a
    specific seed token.
    """
    import re as _re
    polled = agent_tool_called(
        ctx,
        tool_any=["query_database", "get_page", "read_email", "get_emails", "notion"],
        args_any=[
            "material_catalog", "material catalog", "mat_glass", "mat_workstation",
            "mat_smart_control", "glass_partition", "玻璃隔断", "光晟",
        ],
        min_stage=9,
    )
    if not polled:
        return False
    # State-grounding: after polling, the agent surfaced a material outcome.
    text = (
        await read_workspace_file(ctx, "decoration_decisions.md")
        + "\n"
        + await read_workspace_file(ctx, "risk_register.md")
    ).lower()
    surfaced = has_any(
        text,
        ["glass partition", "玻璃隔断", "隔断", "国产", "domestic", "进口",
         "import", "lead time", "lead_time", "海关", "customs"],
    ) or bool(_re.search(r"mat_[a-z_]+_\d{3}", text))
    return surfaced


async def chk_material_delivery_calendar_event_exists(ctx) -> bool:
    """F7: selected long-lead materials have a delivery / 进场 slot on the
    calendar or a delivery line in the schedule.

    OUTCOME-GROUNDED + EQUIVALENCE-TOLERANT: pass when a material decision
    exists AND a delivery event/line exists that references either a
    material concept or any real material id. No specific mat_* token is
    required — a delivery calendar event named "glass partition 进场" passes.
    """
    import re as _re
    text = await read_workspace_file(ctx, "decoration_decisions.md")
    if not text:
        return False
    low = text.lower()
    has_material_decision = (
        bool(_re.search(r"mat_[a-z_]+_\d{3}", low))
        or has_any(low, ["glass partition", "玻璃隔断", "隔断", "工位",
                          "workstation", "家具", "smart control", "智能", "lighting"])
    )
    if not has_material_decision:
        return False
    events = await calendar_events_in_window(ctx)
    delivery_terms = ["delivery", "进场", "到货", "送货", "deliver", "install", "安装"]
    material_concepts = ["glass", "玻璃", "隔断", "partition", "工位",
                         "workstation", "家具", "furniture", "smart", "智能",
                         "lighting", "照明"]
    on_cal = any(
        has_any(e.text, delivery_terms)
        and (has_any(e.text, material_concepts) or bool(_re.search(r"mat_[a-z_]+_\d{3}", e.text.lower())))
        for e in events
    )
    schedule_text = (await read_workspace_file(ctx, "schedule.md")).lower()
    in_sched = (
        has_any(schedule_text, delivery_terms)
        and has_any(schedule_text, material_concepts)
    )
    return on_cal or in_sched


CHECKS = [
    ('chk_material_voc_compliance_for_air_quality', chk_material_voc_compliance_for_air_quality, 1.95),
]


# Filing RFI recovery becomes observable only after the Stage-6 approval mutation.
from .stage_5 import chk_filing_rfi_resolved_by_demolition
from .stage_7 import chk_mutation_filing_rfi_response

CHECKS.extend([
    ("chk_filing_rfi_resolved_by_demolition", chk_filing_rfi_resolved_by_demolition, 2.5),
    ("chk_mutation_filing_rfi_response", chk_mutation_filing_rfi_response, 2.5),
])
