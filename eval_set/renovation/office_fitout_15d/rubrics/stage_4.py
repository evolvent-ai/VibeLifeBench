"""
Stage 4 — calendar_compliance checkers (noise window, holidays, inspection gates).
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


async def chk_cal_no_noisy_work_outside_window(ctx) -> bool:
    """F5 (rigorous): noisy work respects 08:00-18:00 AND noise-window awareness shows somewhere.

    Hard gate: every noisy calendar event stays inside the 08:00-18:00
    window. Soft gate (multi-path acceptance): the agent's awareness of
    the rule shows up in ANY of several places — (A) the rule_property_*
    noise IDs anywhere in the workspace, (B) a citation of the time
    window with surrounding noise/施工 context in renovation_plan /
    schedule / risk_register, (C) a calendar annotation referencing
    work_window / quiet hours, or (D) any outbound communication
    mentioning the noise window. Any path is enough.
    """
    import re as _re
    events = await calendar_events_in_window(ctx)
    for event in events:
        if not event_is_noisy(event):
            continue
        if event_starts_or_ends_outside_window(
            event, earliest_hm="08:00", latest_hm="18:00",
        ):
            return False

    workspace_blob = (
        await read_workspace_file(ctx, "fit_out_plan.md")
        + "\n"
        + await read_workspace_file(ctx, "schedule.md")
        + "\n"
        + await read_workspace_file(ctx, "risk_register.md")
        + "\n"
        + await read_workspace_file(ctx, "communications_log.md")
    )

    # Path A (DEMOTED to one of several accepted signals): cites any
    # property / Lujiazui noise rule id. No longer the sole gate.
    low_blob = workspace_blob.lower()
    path_a = bool(_re.search(r"rule_(?:property|lujiazui)(?:_v\d+)?_\d{3}", low_blob))
    # Path B: explicit noise window discussion (any phrasing, broad set).
    noise_concept_terms = [
        "噪音", "施工时间", "施工 时间", "施工窗口", "扰民",
        "noise", "noisy", "quiet hours", "work hours", "施工噪音",
    ]
    window_terms = [
        "08:00", "8:00", "18:00", "08-18", "8-18",
        "工作日", "weekday", "work window", "work_window",
        "noise window",
    ]
    path_b = (
        has_any(workspace_blob, noise_concept_terms)
        and has_any(workspace_blob, window_terms)
    )
    # Path C: annotation on a calendar event itself.
    path_c = False
    for event in events:
        blob = event.text + " " + str(event.raw)
        if _re.search(
            r"rule_property(?:_v\d+)?_0?06|rule_property_v\d+_\d{3}|work_window",
            blob,
            _re.IGNORECASE,
        ):
            path_c = True
            break
        if has_any(blob, noise_concept_terms) and has_any(blob, window_terms):
            path_c = True
            break
    # Path D: outbound email mentions noise window or quiet-hour rule.
    sent = await sent_email_records(ctx)
    path_d = any(
        (has_any(s.text, noise_concept_terms) and has_any(s.text, window_terms))
        or bool(_re.search(
            r"rule_property(?:_v\d+)?_0?06|rule_property(?:_v\d+)?_0?16",
            s.text,
            _re.IGNORECASE,
        ))
        for s in sent
    )
    return path_a or path_b or path_c or path_d


async def chk_cal_no_noisy_work_on_statutory_holiday(ctx) -> bool:
    """F5: no noisy work scheduled on a statutory holiday / Sunday AND the
    agent shows awareness of the holiday / quiet-day rule.

    OUTCOME-GROUNDED + EQUIVALENCE-TOLERANT (hard gate = calendar state;
    soft gate = awareness as CONCEPT). The awareness can appear as a
    holiday / quiet-day / weekend-noise concept in ANY maintained file
    (CN OR EN), or as a cited property rule id — the id is now just one of
    several accepted signals, not the sole gate.
    """
    events = await calendar_events_in_window(ctx)
    if events:
        for event in events:
            if event_is_noisy(event) and event_on_statutory_holiday(event):
                return False
    workspace_blob = (
        await read_workspace_file(ctx, "fit_out_plan.md")
        + "\n"
        + await read_workspace_file(ctx, "schedule.md")
        + "\n"
        + await read_workspace_file(ctx, "risk_register.md")
        + "\n"
        + await read_workspace_file(ctx, "communications_log.md")
    )
    awareness = has_any(
        workspace_blob,
        [
            "holiday", "法定节假日", "节假日", "statutory holiday",
            "weekend", "周末", "周日", "sunday", "rest day", "休息日",
            "no noisy", "禁止施工", "不施工", "quiet day", "安静日",
            "rule_property_017", "rule_property", "rule_lujiazui",
        ],
    )
    return awareness


async def chk_cal_tile_after_closed_water_pass(ctx) -> bool:
    """F5: decoration / wet-finish work is sequenced AFTER the concealed-works
    (隐蔽工程) acceptance gate, and is not scheduled while that gate is failed.

    OUTCOME-GROUNDED + DECISION-CORRECTNESS (commercial analogue of the
    tile-after-closed-water gate): the agent must not place
    partition/decoration/finish work before concealed-works acceptance
    passes. Hard gate: calendar sequence holds. The awareness is shown as a
    dependency CONCEPT in any maintained file (CN OR EN). No SCH-* / insp
    token is required.
    """
    events = await calendar_events_in_window(ctx)
    finish_terms = [
        "partition", "隔断", "decoration", "装饰", "装修", "tile", "瓷砖",
        "贴砖", "finish", "饰面", "glass", "玻璃", "wall close", "封墙",
    ]
    gate_terms = [
        "concealed", "隐蔽", "隐蔽工程", "隐蔽验收", "concealed acceptance",
        "concealed-works", "rough-in acceptance", "closed_water",
        "closed-water", "闭水", "waterproof", "防水",
    ]
    deps_ok = schedule_dependency_ok(
        events,
        after_terms=finish_terms,
        before_terms=gate_terms,
    )
    if not deps_ok:
        return False

    from ._helpers import proximity_hit
    annotation_blob = (
        await read_workspace_file(ctx, "risk_register.md")
        + "\n"
        + await read_workspace_file(ctx, "schedule.md")
        + "\n"
        + await read_workspace_file(ctx, "fit_out_plan.md")
        + "\n"
        + await read_workspace_file(ctx, "decoration_decisions.md")
        + "\n"
        + await read_workspace_file(ctx, "communications_log.md")
    )
    # Path A: finish + concealed/gate concepts co-occur within 200 chars.
    path_a = proximity_hit(annotation_blob, finish_terms, gate_terms, window=200)
    # Path B: explicit dependency vocabulary near either phase.
    dep_terms = [
        "depends_on", "depends on", "前置", "依赖", "after", "blocked by",
        "blocked_by", "需要先", "完成后", "通过后", "pass first", "gate",
    ]
    path_b = (
        has_any(annotation_blob, dep_terms)
        and (
            has_any(annotation_blob, finish_terms)
            or has_any(annotation_blob, gate_terms)
        )
    )
    # Path C: outbound communication mentions both concepts.
    sent = await sent_email_records(ctx)
    path_c = any(
        has_any(s.text, finish_terms) and has_any(s.text, gate_terms)
        for s in sent
    )
    return path_a or path_b or path_c


async def chk_cal_electrical_acceptance_before_wall_close(ctx) -> bool:
    """F5: strong/weak-power rough-in must be inspected/accepted BEFORE walls
    are closed (partition / decoration / finish), and finish work is not
    sequenced while the electrical-load gate is failed in live state.

    OUTCOME-GROUNDED + DECISION-CORRECTNESS: hard gate = calendar sequence
    holds AND finish work is not placed while electrical_load_app_001 is in
    a blocking state. Awareness shown as a strong-power / acceptance CONCEPT
    in any maintained file. No insp_std_* / renov_* token is required.
    """
    from ._helpers import APP_ELECTRICAL, status_is_blocking
    events = await calendar_events_in_window(ctx)
    finish_terms = [
        "partition", "隔断", "decoration", "装饰", "装修", "tile", "瓷砖",
        "paint", "油漆", "wall close", "封墙", "finish", "饰面", "glass", "玻璃",
    ]
    electrical_terms = [
        "electrical_acceptance", "电气验收", "强弱电验收", "concealed-electrical",
        "强电", "强弱电", "rough-in", "隐蔽电气", "load test", "负荷",
    ]
    if events:
        deps_ok = schedule_dependency_ok(
            events,
            after_terms=finish_terms,
            before_terms=electrical_terms,
        )
        if not deps_ok:
            return False
        status = await app_status(ctx, APP_ELECTRICAL)
        has_wall_close = any(event_in_phase(e, finish_terms) for e in events)
        if has_wall_close and status_is_blocking(status) and status not in ("draft", "not_started"):
            # Only fail if finish work is placed while the gate is actively
            # failed/RFI (draft/not_started is the seed baseline, not a block).
            return False
    workspace_blob = (
        await read_workspace_file(ctx, "schedule.md")
        + "\n"
        + await read_workspace_file(ctx, "strong_weak_power_plan.md")
        + "\n"
        + await read_workspace_file(ctx, "fire_compliance_checklist.md")
        + "\n"
        + await read_workspace_file(ctx, "fit_out_plan.md")
    )
    has_power = has_any(workspace_blob, electrical_terms)
    has_seq_awareness = has_any(
        workspace_blob,
        ["before", "前", "先", "depends", "前置", "通过后", "gate", "acceptance",
         "验收", "rough-in", "封墙前"],
    )
    return has_power and has_seq_awareness


async def chk_cal_air_quality_window_before_handover(ctx) -> bool:
    """F5: a ventilation / formaldehyde-retest window is planned before
    occupancy handover (formaldehyde ≤0.05 mg/m³ retest gate).

    OUTCOME-GROUNDED + EQUIVALENCE-TOLERANT: pass when a ventilation /
    air-quality concept AND an air-quality-test / formaldehyde concept
    appear together — either on the calendar OR in any maintained file
    (CN OR EN). No insp_std_010 token is required.
    """
    events = await calendar_events_in_window(ctx)
    ventilation_terms = ["ventilation", "通风", "晾", "晾房", "晾置", "air out", "散味"]
    air_quality_terms = [
        "air quality", "空气质量", "甲醛", "voc", "tvoc", "formaldehyde",
        "0.05", "gb 50325", "retest", "复检", "复测", "甲醛检测",
    ]
    cal_ok = False
    if events:
        has_vent = any(has_any(e.text, ventilation_terms) for e in events)
        has_air_q = any(has_any(e.text, air_quality_terms) for e in events)
        cal_ok = has_vent and has_air_q
    workspace_blob = (
        await read_workspace_file(ctx, "schedule.md")
        + "\n"
        + await read_workspace_file(ctx, "fire_compliance_checklist.md")
        + "\n"
        + await read_workspace_file(ctx, "handover_punch_list.md")
        + "\n"
        + await read_workspace_file(ctx, "fit_out_plan.md")
    )
    artifact_ok = (
        has_any(workspace_blob, ventilation_terms)
        and has_any(workspace_blob, air_quality_terms)
    )
    return cal_ok or artifact_ok


async def chk_evidence_5f_noise_complaint_addressed(ctx) -> bool:
    """EVIDENCE (D4 5F 律所 噪音 投诉): communications_log OR risk_register
    surfaces the 5F neighbor / law-firm noise complaint AND a follow-up
    action within 3 stages of D4. (Preserved T05-specific check.)
    """
    from ._helpers import proximity_hit

    neighbor_terms = [
        "5f", "5F", "律所", "律师", "律師", "law firm", "law-firm",
        "lawfirm", "邻里", "邻居", "neighbor", "neighbour", "楼层",
        "5 楼", "五楼",
    ]
    noise_terms = [
        "噪音", "扰民", "noise", "noisy", "施工噪音", "切割", "拆除",
        "低噪音", "low-noise", "low noise", "17:00", "18:00", "19:00",
        "业务 高峰", "peak hour",
    ]

    artifact_blob = (
        await read_workspace_file(ctx, "communications_log.md")
        + "\n"
        + await read_workspace_file(ctx, "risk_register.md")
        + "\n"
        + await read_workspace_file(ctx, "fit_out_plan.md")
        + "\n"
        + await read_workspace_file(ctx, "schedule.md")
    )

    path_a = proximity_hit(artifact_blob, neighbor_terms, noise_terms, window=200)

    sent = await sent_email_records(ctx)
    path_b = any(
        has_any(s.text, neighbor_terms) and has_any(s.text, noise_terms)
        for s in sent
    )

    path_c = False
    events = await calendar_events_in_window(ctx)
    for event in events:
        blob = event.text + " " + str(event.raw)
        if has_any(blob, neighbor_terms) and has_any(blob, noise_terms):
            path_c = True
            break

    return path_a or path_b or path_c


CHECKS = [
    ('chk_cal_no_noisy_work_outside_window', chk_cal_no_noisy_work_outside_window, 3.25),
    ('chk_cal_no_noisy_work_on_statutory_holiday', chk_cal_no_noisy_work_on_statutory_holiday, 1.95),
    ('chk_cal_tile_after_closed_water_pass', chk_cal_tile_after_closed_water_pass, 3.25),
    ('chk_cal_electrical_acceptance_before_wall_close', chk_cal_electrical_acceptance_before_wall_close, 2.6),
    ('chk_cal_air_quality_window_before_handover', chk_cal_air_quality_window_before_handover, 2.6),
    ('chk_evidence_5f_noise_complaint_addressed', chk_evidence_5f_noise_complaint_addressed, 2.5),
]


# The vendor quote first becomes visible in Stage 4.
from .stage_3 import (
    chk_quote_exclusions_reconciled,
    chk_quote_tax_treatment_clarified_or_pending,
)

CHECKS.extend([
    ("chk_quote_exclusions_reconciled", chk_quote_exclusions_reconciled, 2),
    ("chk_quote_tax_treatment_clarified_or_pending", chk_quote_tax_treatment_clarified_or_pending, 1.5),
])
