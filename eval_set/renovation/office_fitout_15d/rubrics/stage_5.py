"""
Stage 5 — property_filing_gate checkers (pending → RFI → approved sequencing).
"""
from __future__ import annotations

import json

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


async def chk_filing_application_exists(ctx) -> bool:
    """All five commercial compliance applications exist at Stage 5 and the
    agent has actually observed them through successful live tool results.

    Existence is independent of lifecycle status: at this point insurance is
    already ``in_force`` while downstream fire/electrical/handover records may
    legitimately still be ``draft`` or ``not_started``.
    """
    required_apps = [
        "commercial_fit_up_filing_001",
        "fire_inspection_app_001",
        "electrical_load_app_001",
        "insurance_certificate_001",
        "commercial_handover_001",
    ]
    apps = await compliance_apps(ctx)
    exists = all(isinstance(apps.get(app_id), dict) and bool(apps.get(app_id)) for app_id in required_apps)

    observed: set[str] = set()
    for entry in getattr(ctx, "turn_log", []) or []:
        entry_stage = entry.get("stage")
        if isinstance(entry_stage, int) and entry_stage > 5:
            continue
        for call_record in entry.get("tool_calls", []) or []:
            if call_record.get("succeeded") is False:
                continue
            name = str(call_record.get("name") or "").lower()
            if "visa_application" not in name:
                continue
            result = call_record.get("result")
            if result in (None, "", [], {}):
                continue
            result_blob = json.dumps(result, ensure_ascii=False, default=str).lower()
            payload = json.dumps(call_record.get("input") or {}, ensure_ascii=False).lower()
            if "get_visa_application" in name:
                for app_id in required_apps:
                    if app_id.lower() in payload:
                        observed.add(app_id)
            elif "list_visa_applications" in name:
                for app_id in required_apps:
                    if app_id.lower() in result_blob:
                        observed.add(app_id)
    return exists and observed == set(required_apps)


async def chk_filing_rfi_resolved_by_demolition(ctx) -> bool:
    """The Stage-3 filing RFI has recovered by Stage 6 and the agent re-polled
    the live filing record after working the missing-document issue.

    The world mutation alone is not scoreable agent behavior; a live recheck in
    the Stage-3..6 recovery window is mandatory.
    """
    from ._helpers import APP_FILING, status_is_blocking
    history = await visa_application_history(ctx, APP_FILING)
    final_status = await app_status(ctx, APP_FILING)
    rfi_seen = any(str(item.get("to") or "").lower() == "rfi" for item in history)
    recovered = rfi_seen and (
        (not status_is_blocking(final_status))
        or str(final_status).lower() in ("approved", "processing", "pending", "submitted")
    )
    rechecked = agent_tool_called(
        ctx,
        tool_any=["get_visa_application", "list_visa_applications"],
        min_stage=3,
        max_stage=6,
    )
    return recovered and rechecked


async def chk_filing_no_demolition_while_blocked(ctx) -> bool:
    """F6: while the Jingan one-stop filing is blocked (RFI / rejected), the
    agent does NOT drive fit-up / demolition work past the gate.

    DECISION-CORRECTNESS (commercial analogue of "no demolition while
    blocked"): hard gate = no fit-up / demolition calendar event in
    ``confirmed`` state while commercial_fit_up_filing_001 is RFI/rejected.
    Soft gate (multi-path, EQUIVALENCE-TOLERANT) = awareness of the block
    shown as a CONCEPT in workspace text, an outbound email pairing the
    filing with a gate term, a deferred calendar event, or an explicit
    hold statement. The filing app_id is one accepted signal, not the gate.
    """
    from ._helpers import APP_FILING, status_is_blocking, proximity_hit
    status = await app_status(ctx, APP_FILING)
    # draft/not_started is the seed baseline for other apps; for the filing
    # the real block is rfi/rejected.
    if status not in ("rfi", "rejected", "denied"):
        return True
    fitup_terms = [
        "demolition", "拆除", "破坏性", "拆改", "demo", "fit-up", "fit up",
        "进场", "施工", "fit-out start", "开工",
    ]
    events = await calendar_events_in_window(ctx)
    for event in events:
        if not event_in_phase(event, fitup_terms):
            continue
        event_status = str(event.raw.get("status") or "").lower()
        if event_status == "confirmed":
            return False

    text = (
        await read_workspace_file(ctx, "risk_register.md")
        + "\n"
        + await read_workspace_file(ctx, "schedule.md")
        + "\n"
        + await read_workspace_file(ctx, "communications_log.md")
        + "\n"
        + await read_workspace_file(ctx, "fit_out_plan.md")
    )
    gate_terms = [
        "blocked", "gated", "未通过", "等待", "被卡", "暂停", "待批",
        "rfi", "paused", "hold off", "hold-off", "推迟", "延后",
        "pending approval", "未批准", "尚未通过", "stop", "stop-work",
        "不可开工", "filing pending", "备案未过",
    ]
    # Path A: proximity (≤200 chars) in workspace.
    path_a = proximity_hit(text, fitup_terms, gate_terms, window=200)
    # Path B: outbound email pairs filing concept with a gate term.
    sent = await sent_email_records(ctx)
    filing_markers = (APP_FILING, "fit_up_filing", "备案", "一件事", "filing")
    path_b = any(
        has_any(s.text, list(filing_markers)) and has_any(s.text, gate_terms)
        for s in sent
    )
    # Path C: calendar shows fit-up work deferred AND a reschedule/cancel call.
    rescheduled = any(
        event_in_phase(e, fitup_terms)
        and str(e.raw.get("status") or "").lower() in ("tentative", "cancelled", "canceled")
        for e in events
    )
    path_c = rescheduled and agent_tool_called(
        ctx,
        tool_any=["update_event", "patch_event", "delete_event"],
    )
    # Path D: explicit pause/hold statement on fit-up work.
    path_d = has_any(
        text,
        [
            "on hold", "paused", "暂停", "deferred", "暂缓", "延后开工",
            "hold fit-up", "暂缓进场", "暂停施工",
        ],
    )
    return path_a or path_b or path_c or path_d


async def chk_filing_response_to_property_warning(ctx) -> bool:
    """F6 (rigorous): outbound reply to property warning shows substantive action.

    For each inbound property warning, an outbound reply to the same
    sender domain must demonstrate substantive engagement via any one of
    these acceptance paths:
      * Path A — cites the application_id explicitly AND has any
        remediation concept (broad set of synonyms).
      * Path B — has any remediation concept AND any time-commitment
        (a date / 本周 / by Friday / 立即 / immediately / specific day).
      * Path C — has any remediation concept AND any concrete
        deliverable (drawing / 图纸 / certificate / 资质 / agreement /
        协议 / signature / commitment letter / 承诺书).
    Any path is sufficient. This rewards the agent who responds
    substantively even if their phrasing doesn't include the app_id.
    """
    inbound = await inbox_email_records(ctx)
    property_warnings = [
        r for r in inbound
        if has_any(
            r.from_addr + " " + r.subject,
            ["property", "物业", "complaints@"],
        )
        and has_any(
            r.text,
            ["warning", "stop", "rfi", "备案", "整改", "投诉", "complaint"],
        )
    ]
    if not property_warnings:
        return False

    sent = await sent_email_records(ctx)
    # Path-A app-id anchors (one of three accepted paths, never the sole gate).
    app_ids = (
        "commercial_fit_up_filing_001",
        "fire_inspection_app_001",
        "electrical_load_app_001",
    )
    remediation_terms = [
        "图纸", "资质", "承诺书", "协议", "签字", "签章",
        "上传", "附件", "提交", "submit", "upload",
        "BIM", "LOD", "drawing", "drawings", "certificate",
        "license", "qualifications", "commitment",
        "整改", "修正", "修订", "rework", "update", "remediation",
        "回复", "回函", "respond", "response", "reply",
    ]
    time_commitment_terms = [
        "本周", "本月", "today", "立即", "immediately", "asap",
        "by friday", "by monday", "this week", "next week",
        "before", "之前", "deadline", "截止",
    ]
    deliverable_terms = [
        "图纸", "drawing", "drawings", "blueprint",
        "资质", "license", "certificate", "qualifications",
        "承诺书", "commitment letter", "协议", "agreement",
        "签字", "signature", "签章", "stamp",
    ]
    import re as _re
    date_re = _re.compile(r"20\d{2}-\d{2}-\d{2}|\d{1,2}/\d{1,2}|\d{1,2}月\d{1,2}日")

    for warning in property_warnings:
        wdom = warning.from_addr.split("@")[-1].lower()
        matched = False
        for s in sent:
            recip_domains = {addr.split("@")[-1].lower() for addr in s.recipients}
            if wdom not in recip_domains:
                continue
            blob_low = s.text.lower()
            cites_app = any(app_id.lower() in blob_low for app_id in app_ids)
            has_remediation = any(t.lower() in blob_low for t in remediation_terms)
            has_time = (
                any(t.lower() in blob_low for t in time_commitment_terms)
                or bool(date_re.search(s.text))
            )
            has_deliverable = any(t.lower() in blob_low for t in deliverable_terms)
            path_a = cites_app and has_remediation
            path_b = has_remediation and has_time
            path_c = has_remediation and has_deliverable
            if path_a or path_b or path_c:
                matched = True
                break
        if not matched:
            return False
    return True


CHECKS = [
    ('chk_filing_application_exists', chk_filing_application_exists, 2),
    ('chk_filing_response_to_property_warning', chk_filing_response_to_property_warning, 2),
]
