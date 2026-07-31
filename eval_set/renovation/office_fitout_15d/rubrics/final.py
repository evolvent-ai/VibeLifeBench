"""
Final readiness checkers (go / no-go grounded in current state of every gate).
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


def _agent_verified_all_compliance_gates(ctx) -> bool:
    verified: set[str] = set()
    good_terms = ("approved", "passed", "closed", "in_force")
    for entry in getattr(ctx, "turn_log", []) or []:
        if entry.get("stage") not in (19, 20):
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
            if not any(term in result_blob for term in good_terms):
                continue
            payload = json.dumps(call_record.get("input") or {}, ensure_ascii=False).lower()
            if "get_visa_application" in name:
                for app_id in COMPLIANCE_APP_IDS:
                    if app_id.lower() in payload:
                        verified.add(app_id)
            elif "list_visa_applications" in name:
                for app_id in COMPLIANCE_APP_IDS:
                    if app_id.lower() in result_blob:
                        verified.add(app_id)
    return verified == set(COMPLIANCE_APP_IDS)


async def chk_final_all_inspections_approved(ctx) -> bool:
    """All five commercial gates are live-good *and* the agent verified and
    recorded that state during closeout.

    Scripted final mutations are world state, not agent performance. A Stage
    19/20 live poll and a durable closeout conclusion are therefore required in
    addition to approved backend state.
    """
    from ._helpers import (
        APP_FIRE, APP_ELECTRICAL, APP_INSURANCE, APP_HANDOVER,
        status_is_approved,
    )
    apps = await compliance_apps(ctx)
    for app_id in COMPLIANCE_APP_IDS:
        status = str((apps.get(app_id) or {}).get("status") or "").lower()
        if not status_is_approved(status):
            return False

    if not _agent_verified_all_compliance_gates(ctx):
        return False

    closeout_text = (
        stage_response(ctx, stage=19)
        + "\n"
        + stage_response(ctx, stage=20)
        + "\n"
        + await read_workspace_file(ctx, "fit_out_plan.md")
        + "\n"
        + await read_workspace_file(ctx, "handover_punch_list.md")
        + "\n"
        + await read_workspace_file(ctx, "communications_log.md")
    )
    gate_groups = [
        ["filing", "备案", "一件事"],
        ["fire", "消防"],
        ["electrical", "强电", "负荷"],
        ["insurance", "保险", "in_force"],
        ["handover", "交付", "交接"],
    ]
    recorded = count_groups(closeout_text, gate_groups) >= 4 and has_any(
        closeout_text,
        ["入驻", "occupancy", "move-in", "尾款", "final payment", "closeout", "关闭"],
    )
    if not recorded:
        return False

    fingerprints = {
        APP_FIRE: ["fire", "消防", "消防验收", "emergency light", "应急照明",
                   "evacuation", "疏散", "sprinkler", "烟感"],
        APP_ELECTRICAL: ["electrical", "强弱电", "强电", "load", "负荷",
                         "kw/100", "电气", "load test"],
        APP_INSURANCE: ["insurance", "工程一切险", "保险", "all risk", "policy",
                        "保单", "third party", "第三方"],
        APP_HANDOVER: ["air quality", "甲醛", "warranty", "保修", "as-built",
                       "竣工图", "occupancy", "占用", "punch", "handover"],
    }
    for app_id, needles in fingerprints.items():
        docs = await visa_application_documents(ctx, app_id)
        refs = " ".join(
            str(d.get("ref") or d.get("name") or d.get("description") or "")
            for d in docs
        )
        if refs and not has_any(refs, needles):
            return False
    return True


def _current_punch_is_open(text: str) -> bool:
    """Classify the current punch state without treating historical OPEN text
    as a permanent blocker. The latest explicit aggregate status wins.
    """
    low = (text or "").lower()
    open_terms = ["current status: open", "status: open", "status: pending",
                  "current: open", "未关闭", "整改中", "待整改"]
    closed_terms = ["current status: all punch items closed", "status: closed",
                    "all closed", "全部关闭", "清零", "punch list cleared"]
    last_open = max((low.rfind(term) for term in open_terms), default=-1)
    last_closed = max((low.rfind(term) for term in closed_terms), default=-1)
    return last_open >= 0 and last_open > last_closed


async def chk_final_no_false_ready_when_blocked(ctx) -> bool:
    """Do not issue an unconditional move-in/payment go while a current gate or
    current punch item is blocked. Historical pending prose is ignored once a
    later explicit closed status exists; an actually clear project passes
    vacuously.
    """
    from ._helpers import status_is_approved
    apps = await compliance_apps(ctx)
    blocked = [
        app_id for app_id in COMPLIANCE_APP_IDS
        if not status_is_approved(str((apps.get(app_id) or {}).get("status") or "").lower())
    ]
    punch_text = await read_workspace_file(ctx, "handover_punch_list.md")
    punch_open = _current_punch_is_open(punch_text)
    if not blocked and not punch_open:
        # Nothing is blocking. Previously this returned True outright, which
        # also rewarded an agent that never worked the task — every gate ends
        # approved in this scenario, so the "vacuous pass" was unconditional.
        # Require the readiness call to actually exist: a punch list plus a
        # stated go/no-go. The veto below is unchanged, so claiming ready while
        # something is blocked still fails.
        decided = (
            stage_response(ctx, stage=19)
            + "\n"
            + stage_response(ctx, stage=20)
            + "\n"
            + await read_workspace_file(ctx, "fit_out_plan.md")
        ).lower()
        return bool(punch_text.strip()) and has_any(
            decided,
            [
                "ready for move-in", "release final payment", "green light",
                "可入住", "释放尾款", "occupancy ready", "准予入驻",
                "conditional", "no-go", "not ready", "暂缓", "hold",
                "do not release", "不释放", "待解决",
            ],
        )

    decision_text = (
        stage_response(ctx, stage=19)
        + "\n"
        + stage_response(ctx, stage=20)
        + "\n"
        + await read_workspace_file(ctx, "fit_out_plan.md")
    ).lower()
    false_ready = (
        has_any(
            decision_text,
            [
                "ready for move-in", "release final payment", "release 尾款",
                "green light", "go ahead", "可入住", "释放尾款", "occupancy ready",
                "准予入驻", "go (unconditional)", "approved for handover",
                "立即释放尾款", "立即入驻",
            ],
        )
        and not has_any(
            decision_text,
            ["conditional", "no-go", "not ready", "暂停", "暂缓",
             "待解决", "hold", "do not release", "不释放", "不准"],
        )
    )
    return not false_ready


async def chk_final_handover_packet_complete(ctx) -> bool:
    """F10: the handover packet covers the commercial occupancy evidence —
    fire acceptance, electrical-load test, formaldehyde retest, insurance,
    warranty, as-built — and the punch list is closed.

    OUTCOME-GROUNDED + EQUIVALENCE-TOLERANT: evidence is matched by broad
    concept groups (CN OR EN) across the handover application's docs OR the
    handover_punch_list.md / fire_compliance_checklist.md artifacts (so a
    capable model that records the packet in the workspace still passes),
    and the punch list must read as closed. No specific seed ID is required.
    """
    from ._helpers import APP_HANDOVER
    docs = await visa_application_documents(ctx, APP_HANDOVER)
    refs = " ".join(
        str(d.get("ref") or d.get("name") or d.get("description") or "") for d in docs
    )
    artifact = (
        await read_workspace_file(ctx, "handover_punch_list.md")
        + "\n"
        + await read_workspace_file(ctx, "fire_compliance_checklist.md")
        + "\n"
        + await read_workspace_file(ctx, "fit_out_plan.md")
    )
    blob = refs + "\n" + artifact
    required = [
        ["warranty", "保修", "质保"],
        ["fire", "消防", "消防验收"],
        ["electrical", "强弱电", "强电", "load", "负荷"],
        ["air quality", "甲醛", "voc", "formaldehyde", "0.05"],
        ["insurance", "工程一切险", "保险", "all risk"],
        ["as-built", "竣工图", "as built"],
        ["occupancy", "占用证", "入驻", "fit-up 押金 退还", "deposit refund"],
    ]
    docs_ok = count_groups(blob, required) >= 5
    text = await read_workspace_file(ctx, "handover_punch_list.md")
    low = text.lower()
    punch_closed = has_any(
        low,
        ["status: closed", "已关闭", "all closed", "punch list cleared",
         "closed", "全部关闭", "清零"],
    ) and not has_any(low, ["open", "pending", "未关闭", "整改中"])
    return docs_ok and punch_closed


CHECKS = [
    ('chk_final_all_inspections_approved', chk_final_all_inspections_approved, 3.5),
    ('chk_final_no_false_ready_when_blocked', chk_final_no_false_ready_when_blocked, 3.5),
    ('chk_final_handover_packet_complete', chk_final_handover_packet_complete, 2.5),
]


async def _fitout_packet_text(ctx) -> str:
    """The durable packet narrative the agent maintains at handover: the punch
    list + fire checklist + fit-out plan artifacts plus the D20 (stage 20)
    closeout response, concatenated and lower-cased. Shared by the split
    packet sub-checks so each reads the same evidence surface the old
    mega-AND did — only now each condition is scored (and grounded) on its
    own instead of gating the entire task behind one 90-point keyword wall.
    """
    return (
        await read_workspace_file(ctx, "handover_punch_list.md")
        + "\n"
        + await read_workspace_file(ctx, "fire_compliance_checklist.md")
        + "\n"
        + await read_workspace_file(ctx, "fit_out_plan.md")
        + "\n"
        + stage_response(ctx, stage=20)
    ).lower()


async def chk_final_packet_fire_cleared(ctx) -> bool:
    """F-packet (fire): the fire-acceptance leg of the handover packet is real.

    BACKEND-GROUNDED: the fire gate (fire_inspection_app_001) must have reached
    a terminal-good live state (approved / passed / closed / in_force) — the
    D13 消防验收 FAIL had to actually be remediated in mock state, not merely
    narrated — AND the packet text must document the fire acceptance / 报备 /
    no-go handling. Both legs can independently be False, so this is not a
    dead check: an un-recovered fire gate fails on the status leg, an
    undocumented packet fails on the text leg.
    """
    from ._helpers import APP_FIRE, status_is_approved
    status = await app_status(ctx, APP_FIRE)
    status_ok = status_is_approved(status)
    text = await _fitout_packet_text(ctx)
    documented = count_groups(
        text, [["消防", "fire"], ["报备", "备案", "验收"], ["活动后补", "after", "整改"], ["no-go", "不能", "阻断"]]
    ) >= 3
    return status_ok and documented


async def chk_final_packet_structure_reviewed(ctx) -> bool:
    """F-packet (structure): the partition / load-bearing review leg is present.

    Text+trace grounded: the packet must document the partition vs. load-bearing wall
    review, AND the agent must have actually consulted the property / structural
    rules rather than asserting it blind.
    """
    text = await _fitout_packet_text(ctx)
    documented = count_groups(
        text, [["隔断", "partition"], ["承重", "load-bearing", "结构"], ["复核", "review", "评估"]]
    ) >= 2
    consulted = agent_tool_called(
        ctx,
        tool_any=["query_database", "get_page", "search", "get_visa_application"],
        args_any=["承重", "load", "partition", "隔断", "structur", "rule_property"],
    )
    return documented and consulted


async def chk_final_packet_voc_cleared(ctx) -> bool:
    """F-packet (VOC / air quality): the formaldehyde/VOC retest leg is real.

    BACKEND-GROUNDED: air-quality clearance is carried by the commercial
    handover application (commercial_handover_001 tracks air_quality_passed /
    punch_list_closed), so require that gate to be in an active-or-approved
    live state (it must at least have been opened/worked, and if closed it
    must be approved-equivalent) AND require the packet text to document a
    third-party VOC/formaldehyde test with evidence. Each leg is independently
    falsifiable.
    """
    from ._helpers import APP_HANDOVER, status_is_approved, status_is_blocking
    status = await app_status(ctx, APP_HANDOVER)
    # A capable run either closes the handover gate (approved-equivalent) or,
    # at minimum, has advanced it off the blocking not_started/draft baseline.
    status_ok = status_is_approved(status) or not status_is_blocking(status)
    text = await _fitout_packet_text(ctx)
    documented = count_groups(
        text,
        [["voc", "甲醛", "formaldehyde"], ["第三方", "third-party", "third party"],
         ["自测截图", "screenshot", "报告", "report"], ["检测", "test", "retest", "复测"]],
    ) >= 3
    return status_ok and documented


async def chk_final_packet_invoice_corrected(ctx) -> bool:
    """F-packet (invoice): the invoice-title correction leg is documented.

    Text+trace grounded (no invoicing backend in scope): the packet must record
    the invoice 抬头 / 个人→公司 correction, AND the agent must have
    communicated it (email / communications log) rather than only asserting it
    in a workspace file.
    """
    text = await _fitout_packet_text(ctx)
    documented = count_groups(
        text,
        [["发票", "invoice"], ["抬头", "title", "台头"], ["个人", "personal", "公司", "company"],
         ["更正", "correct", "修正", "重开"]],
    ) >= 3
    communicated = agent_tool_called(
        ctx,
        tool_any=["send_email", "create_draft", "reply_email"],
        args_any=["发票", "invoice", "抬头", "title"],
    )
    return documented and (communicated or "communications_log" in text)


async def chk_final_packet_payment_authorized(ctx) -> bool:
    """F-packet (auth): the balance-payment / occupancy authorization leg.

    Text+trace grounded, and cross-checked against the no-false-ready rule: the
    packet must document the 尾款 / opening / 入驻 authorization AND the agent
    must have surfaced the owner-facing go/authorization decision (an owner
    email OR a stage-20 closeout narrative), so the balance release is a
    recorded decision, not an unlogged claim.
    """
    text = await _fitout_packet_text(ctx)
    documented = count_groups(
        text,
        [["尾款", "balance", "final payment"], ["开业宣传", "opening", "开业"],
         ["人员入驻", "occupancy", "入驻"], ["授权", "approval", "approve", "authoriz"]],
    ) >= 3
    surfaced = agent_tool_called(
        ctx,
        tool_any=["send_email", "create_draft", "reply_email"],
        args_any=["尾款", "balance", "授权", "occupancy", "入驻"],
    ) or bool(stage_response(ctx, stage=20))
    return documented and surfaced


CHECKS.append(("chk_final_packet_fire_cleared", chk_final_packet_fire_cleared, 3.5))
CHECKS.append(("chk_final_packet_structure_reviewed", chk_final_packet_structure_reviewed, 3.0))
CHECKS.append(("chk_final_packet_voc_cleared", chk_final_packet_voc_cleared, 3.5))
CHECKS.append(("chk_final_packet_invoice_corrected", chk_final_packet_invoice_corrected, 3.0))
CHECKS.append(("chk_final_packet_payment_authorized", chk_final_packet_payment_authorized, 3.0))
