"""
Cross-stage chain checkers (multi-stage event chains, e.g. waterproof first-fail → root cause → redo → budget → schedule).
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
    agent_application_status_pairs,
    agent_tool_result_records,
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


async def chk_chain_bim_lod400_decision_rationale(ctx) -> bool:
    """CHAIN T05 (rigorous): BIM/LOD400 decision communicated with rationale.

    Outcome: agent recommends an option for the BIM/LOD400 issue and the
    recommendation includes a rationale (cost/time impact). Multi-path:
      * Path A — outbound email to zhou_mu/COO with any BIM concept AND
        any decision verb AND any quantified impact (amount or days).
      * Path B — renovation_plan.md (or risk_register.md) has the BIM
        concept AND decision language AND quantified impact.
      * Path C — risk_register lists ≥3 alternative options structure
        (any list/bullet markers) alongside BIM concept and quantification.
    """
    from ._helpers import has_decision_language, has_impact_quantification
    bim_terms = [
        "bim", "lod400", "lod 400", "lod", "建筑信息模型", "三维模型",
        "图纸升级", "深化设计", "数字孪生", "一件事", "filing", "备案",
    ]

    sent = await sent_email_records(ctx)
    target_emails: list[str] = []
    for s in sent:
        recipients = " ".join(s.recipients).lower()
        if "zhou_mu" in recipients or "startup-coo" in recipients or "coo" in recipients:
            target_emails.append(s.text)
    email_text = "\n".join(target_emails)

    # Path A — reasoned options-with-recommendation reached the owner. This is
    # a genuine outbound decision (and the D8 user_message explicitly asks Zhou
    # Mu for 3 options + a recommendation), so it stays self-standing.
    if (
        target_emails
        and has_any(email_text, bim_terms)
        and has_decision_language(email_text)
        and has_impact_quantification(email_text)
    ):
        return True

    # ANTI-FREEBIE: the LOD400 escalation is a SCRIPTED filing RFI (D3 → D5 →
    # D9 force_decision flips on commercial_fit_up_filing_001 regardless of the
    # agent). A workspace note merely discussing "BIM/LOD400" therefore does
    # not prove the agent DISCOVERED the platform's LOD400 demand. The
    # workspace-only paths (B/C) now additionally require DETECTION — the agent
    # polled the filing gate in the D3-D9 RFI window.
    from ._helpers import APP_FILING, agent_polled_gate
    polled_filing = agent_polled_gate(
        ctx, app_id=APP_FILING,
        concept_terms=["一件事", "备案", "filing", "fit_up_filing", "bim", "lod"],
        min_stage=3, max_stage=10,
    )

    # Path B — the decision (with rationale + quantified impact) lives in the
    # durable workspace (gated by detection).
    plan_text = (
        await read_workspace_file(ctx, "fit_out_plan.md")
        + "\n"
        + await read_workspace_file(ctx, "decoration_decisions.md")
    )
    risk_text = await read_workspace_file(ctx, "risk_register.md")
    if polled_filing:
        for blob in (plan_text, risk_text):
            if (
                has_any(blob, bim_terms)
                and has_decision_language(blob)
                and has_impact_quantification(blob)
            ):
                return True

    # Path C — risk_register lists multiple options (gated by detection).
    import re as _re
    if polled_filing and has_any(risk_text, bim_terms) and has_impact_quantification(risk_text):
        bullet_count = len(_re.findall(r"^\s*(?:[-*+]|\d+[.)])\s+\S", risk_text, _re.MULTILINE))
        option_count = sum(risk_text.lower().count(tok) for tok in ("option", "选项", "方案"))
        if max(bullet_count, option_count) >= 3:
            return True
    return False


async def chk_chain_fire_drawing_2nd_reject_replan(ctx) -> bool:
    """CHAIN T05 (rigorous): fire-drawing 2nd reject acknowledged AND replanned.

    Outcome: the agent observed the fire visa rejection and recorded
    a replan response. Multi-path:
      * Path A — agent polled fire_inspection visa within a reasonable
        window [stages 9-13] AND a workspace artifact mentions fire
        rework / rejection / integration concept (broad set).
      * Path B — outbound email mentions fire-drawing rejection AND a
        replan/follow-up vocabulary.
      * Path C — live fire visa state is rfi/rejected AND a workspace
        file references the fire issue.
    """
    from ._helpers import APP_FIRE, status_is_blocking
    fire_terms = ["消防", "fire", "fire_inspection", "fire-inspection", "消防验收"]
    rework_terms = [
        "rework", "返工", "退回", "reject", "rejected", "denied", "second reject",
        "第 2 次", "第二次", "整改", "rfi", "fail", "失败", "未通过",
        "replan", "重新规划", "重做", "修订", "重新申报",
    ]

    polled = agent_tool_called(
        ctx,
        tool_any=["get_visa_application", "list_visa_applications"],
        args_any=["fire_inspection_app_001", "fire", "消防"],
        min_stage=9,
        max_stage=14,
    )
    ws_text = (
        await read_workspace_file(ctx, "risk_register.md")
        + "\n"
        + await read_workspace_file(ctx, "communications_log.md")
        + "\n"
        + await read_workspace_file(ctx, "schedule.md")
        + "\n"
        + await read_workspace_file(ctx, "fit_out_plan.md")
        + "\n"
        + await read_workspace_file(ctx, "fire_compliance_checklist.md")
    )
    fire_status = await app_status(ctx, APP_FIRE)

    # Path A — agent polled the fire gate AND recorded a fire rework/replan
    # response in the workspace. (App-id citation DEMOTED: a fire-concept
    # rework note suffices, no literal token required.)
    if polled and has_any(ws_text, fire_terms) and has_any(ws_text, rework_terms):
        return True

    # Path B — outbound email surfaces the fire rejection AND a replan / follow
    # up. Grounded by fire CONCEPT, not the app_id token.
    sent = await sent_email_records(ctx)
    follow_up_terms = [
        "follow up", "follow-up", "回复", "回函", "respond", "next step",
        "replan", "重新", "整改", "修订", "rework", "返工", "重新申报",
    ]
    for s in sent:
        if (
            has_any(s.text, fire_terms)
            and (has_any(s.text, rework_terms) or has_any(s.text, follow_up_terms))
        ):
            return True

    # Path C — live fire gate is in a blocking (denied/rfi/failed) state AND a
    # workspace artifact references the fire issue.
    #
    # ANTI-FREEBIE: the fire gate is SCRIPTED (D10 second-reject → rfi, D13
    # auto-recovery → approved) regardless of the agent. A blocking/denied
    # final state alone is therefore NOT agent contribution, so this STATE
    # path additionally requires DETECTION (the agent actually polled the fire
    # gate in-window) — final scripted state may only CORROBORATE.
    if polled and status_is_blocking(fire_status) and fire_status not in ("draft",):
        if has_any(ws_text, fire_terms):
            return True
    # Also accept the seeded D13 denial being acknowledged even from draft —
    # but only when the agent DISCOVERED it (polled), not as a state freebie.
    if polled and fire_status in ("denied", "rejected", "failed", "rfi") and has_any(ws_text, fire_terms):
        return True
    return False


async def chk_chain_electrical_load_test_replan(ctx) -> bool:
    """CHAIN T05 (rigorous): electrical load gap acknowledged with replan signal.

    Outcome: the agent identifies the strong-electric load gap and
    records a remediation plan. Multi-path:
      * Path A — agent polled the electrical_load visa in a reasonable
        window [stages 11-14] AND a workspace artifact contains both
        a strong-power concept AND any gap/shortfall vocabulary.
      * Path B — workspace artifact carries a specific quantitative marker
        (3.5 kW / 10.5 kW / kW/100㎡) AND any gap term.
      * Path C — outbound email mentions strong electric / load AND
        any remediation vocabulary.
    """
    from ._helpers import APP_ELECTRICAL, status_is_blocking
    polled = agent_tool_called(
        ctx,
        tool_any=["get_visa_application", "list_visa_applications"],
        args_any=["electrical_load_app_001", "强弱电", "强电", "load", "电气"],
        min_stage=10,
        max_stage=14,
    )
    strong_terms = [
        "强电", "强弱电", "strong electric", "strong-electric", "load shortfall",
        "load_shortfall", "主线升级", "main line upgrade", "电力升级",
        "电气主线", "load test", "load_test", "电气负载", "电箱", "负荷",
        "4kw", "4 kw", "kw/100",
    ]
    gap_terms = [
        "不达标", "shortfall", "gap", "未达", "未通过", "fail",
        "整改", "升级", "rework", "不足", "缺口", "deficiency", "3 kw",
        "3.0", "below target", "低于",
    ]
    ws_text = (
        await read_workspace_file(ctx, "risk_register.md")
        + "\n"
        + await read_workspace_file(ctx, "communications_log.md")
        + "\n"
        + await read_workspace_file(ctx, "schedule.md")
        + "\n"
        + await read_workspace_file(ctx, "strong_weak_power_plan.md")
        + "\n"
        + await read_workspace_file(ctx, "budget_tracker.md")
        + "\n"
        + await read_workspace_file(ctx, "fit_out_plan.md")
    )
    elec_status = await app_status(ctx, APP_ELECTRICAL)

    # ANTI-FREEBIE: the electrical gate is SCRIPTED (D13 auto-recovery →
    # approved_with_conditions regardless of the agent) and its baseline load
    # deficit (3 vs 4 kW/100㎡) is seeded into answers_json. A workspace note
    # echoing "强电 升级 不足" OR a blocking final state therefore is NOT agent
    # contribution on its own — both the artifact-only and state-only paths
    # now additionally require DETECTION (the agent actually polled the
    # electrical gate in-window). Outbound-email handling stays self-standing.
    #
    # Path A — polled the electrical gate AND workspace shows a strong-power
    # load gap with a remediation/upgrade plan. (App-id citation DEMOTED to a
    # concept match — no literal token required.)
    if polled and has_any(ws_text, strong_terms) and has_any(ws_text, gap_terms):
        return True
    # Path B — outbound email surfaces the load gap + remediation, by concept.
    # An owner/vendor-facing decision is genuine agent contribution by itself.
    sent = await sent_email_records(ctx)
    for s in sent:
        if has_any(s.text, strong_terms) and has_any(s.text, gap_terms):
            return True
    # Path C — STATE corroboration: the electrical gate is in a blocking state
    # AND a strong-power concept is recorded — accepted ONLY when the agent
    # DISCOVERED the gate (polled), so the scripted state can corroborate but
    # never suffice alone.
    if polled and status_is_blocking(elec_status) and elec_status not in ("draft",) and has_any(ws_text, strong_terms):
        return True
    return False


async def chk_chain_d13_dual_gate_simultaneous_plan(ctx) -> bool:
    """CHAIN T05 (rigorous): D13 dual-gate plan recorded with time-sequencing.

    Outcome: schedule and/or plan acknowledges the D13 dual-gate
    inspection (fire + strong electric) with a time-sequencing signal.
    Multi-path:
      * Path A — schedule.md OR renovation_plan.md contains the D13
        marker AND fire AND strong electric AND a time-sequencing term.
      * Path B — both schedule.md AND renovation_plan.md contain the
        dual-gate concept (any of: 同日 / dual gate / 双门 / both /
        simultaneous) AND fire AND strong electric.
      * Path C — outbound communication confirms the D13 sequence with
        a fire + electric pairing AND a date/time/morning/afternoon
        signal.
    """
    schedule_text = await read_workspace_file(ctx, "schedule.md")
    plan_text = (
        await read_workspace_file(ctx, "fit_out_plan.md")
        + "\n"
        + await read_workspace_file(ctx, "fire_compliance_checklist.md")
    )
    comms_text = await read_workspace_file(ctx, "communications_log.md")

    # D-day markers are DEMOTED to an optional anchor; the real signal is a
    # coherent same-day dual-gate plan (fire + strong-electric inspected
    # together, with a time-sequencing / same-day signal).
    d13_terms = ["d13", "07-13", "2026-07-13", "7-13", "7月13", "7 月 13", "同日验收"]
    fire_terms = ["消防", "fire", "消防验收"]
    strong_terms = [
        "强电", "强弱电", "electrical", "electric load", "load test",
        "strong electric", "负荷", "电气验收",
    ]
    time_seq_terms = [
        "上午", "下午", "同日", "同 日", "morning", "afternoon",
        "dual gate", "dual_gate", "同时", "双 gate", "same day", "同一天",
    ]
    dual_gate_concepts = [
        "dual gate", "dual_gate", "同日", "同时", "simultaneous",
        "both inspections", "双重", "并行", "两项验收", "双门", "two gates",
    ]
    import re as _re

    def _has_time_marker(t: str) -> bool:
        return (
            has_any(t, time_seq_terms)
            or bool(_re.search(r"\d{1,2}:\d{2}", t))
        )

    # ANTI-FREEBIE: the D13 dual-recheck (fire + strong-electric same day) is a
    # SCRIPTED world event whose auto-recovery flips both gates regardless of
    # the agent. A workspace schedule line merely pairing fire + electric is
    # therefore not, on its own, proof the agent DISCOVERED the dual-gate. The
    # durable-artifact paths (A/B/D) now additionally require DETECTION — the
    # agent polled the fire OR electrical gate in the D11-D14 dual-recheck
    # window. The outbound-communication path (C) stays self-standing because
    # an outbound dual-gate confirmation is itself agent contribution.
    from ._helpers import APP_FIRE, APP_ELECTRICAL, agent_polled_gate
    polled_dual = agent_polled_gate(
        ctx, app_id=APP_FIRE,
        concept_terms=["fire", "消防", "消防验收"],
        min_stage=11, max_stage=14,
    ) or agent_polled_gate(
        ctx, app_id=APP_ELECTRICAL,
        concept_terms=["强弱电", "强电", "load", "电气", "负荷"],
        min_stage=11, max_stage=14,
    )

    # Path A — schedule / plan pairs fire + strong-electric with a same-day /
    # time-sequencing signal (the D-day token is no longer required).
    if polled_dual:
        for blob in (schedule_text, plan_text):
            if (
                has_any(blob, fire_terms)
                and has_any(blob, strong_terms)
                and (_has_time_marker(blob) or has_any(blob, dual_gate_concepts))
            ):
                return True
    # Path B — explicit dual-gate concept pairing fire + strong-electric.
    if (
        polled_dual
        and has_any(schedule_text + plan_text, dual_gate_concepts)
        and has_any(schedule_text + plan_text, fire_terms)
        and has_any(schedule_text + plan_text, strong_terms)
    ):
        return True
    # Path C — outbound communication confirms the dual-gate sequence.
    sent = await sent_email_records(ctx)
    for s in sent:
        if (
            has_any(s.text, fire_terms)
            and has_any(s.text, strong_terms)
            and (_has_time_marker(s.text) or has_any(s.text, dual_gate_concepts)
                 or has_any(s.text, d13_terms))
        ):
            return True
    # Path D — comms_log captures the plan (durable artifact → requires the
    # same DETECTION gate as Paths A/B).
    if (
        polled_dual
        and has_any(comms_text, fire_terms)
        and has_any(comms_text, strong_terms)
        and (_has_time_marker(comms_text) or has_any(comms_text, dual_gate_concepts))
    ):
        return True
    return False


async def chk_chain_handover_postponement_communicated(ctx) -> bool:
    """CHAIN T05 (rigorous): handover postponement communicated with day count.

    Outcome: the agent informs the owner/COO that handover will be
    delayed and quantifies the delay. Multi-path:
      * Path A — outbound email to zhou_mu/COO sent in a reasonable
        time window mentions handover/入驻 AND delay/推迟 AND any
        day count ≥1.
      * Path B — renovation_plan.md or schedule.md records the
        handover-delay relationship with a day count ≥1.
      * Path C — communications_log records the postponement with
        a delay vocabulary AND a day count.
    """
    from ._helpers import extract_day_counts
    handover_terms = [
        "入驻", "入住", "handover", "occupancy", "9-01", "09-01",
        "2026-09-01", "交付", "occupancy date", "move-in",
    ]
    delay_terms = [
        "推迟", "delay", "delayed", "postpone", "postponement", "顺延",
        "推后", "延后", "脱期", "推迟到", "shift",
    ]

    sent = await sent_email_records(ctx)
    for s in sent:
        recipients = " ".join(s.recipients).lower()
        if not ("zhou_mu" in recipients or "startup-coo" in recipients or "coo" in recipients):
            continue
        # Time window: a broad post-D8 window (was D11+).
        if not email_date_in_window(s, "2026-07-08", None):
            continue
        if (
            has_any(s.text, handover_terms)
            and has_any(s.text, delay_terms)
            and any(n >= 1 for n in extract_day_counts(s.text))
        ):
            return True

    plan_text = await read_workspace_file(ctx, "fit_out_plan.md")
    schedule_text = await read_workspace_file(ctx, "schedule.md")
    comms_text = await read_workspace_file(ctx, "communications_log.md")
    risk_text = await read_workspace_file(ctx, "risk_register.md")
    for blob in (plan_text, schedule_text, comms_text, risk_text):
        if (
            has_any(blob, handover_terms)
            and has_any(blob, delay_terms)
            and any(n >= 1 for n in extract_day_counts(blob))
        ):
            return True
    return False


CHECKS = [
    ('chk_chain_bim_lod400_decision_rationale', chk_chain_bim_lod400_decision_rationale, 4),
    ('chk_chain_fire_drawing_2nd_reject_replan', chk_chain_fire_drawing_2nd_reject_replan, 4.5),
    ('chk_chain_electrical_load_test_replan', chk_chain_electrical_load_test_replan, 4.5),
    ('chk_chain_d13_dual_gate_simultaneous_plan', chk_chain_d13_dual_gate_simultaneous_plan, 4),
    ('chk_chain_handover_postponement_communicated', chk_chain_handover_postponement_communicated, 4),
]


async def chk_cross_compliance_polled_in_early_mid_closeout_windows(ctx) -> bool:
    """Result-backed compliance coverage across early, mid, and closeout windows.

    Each window must return the relevant commercial objects and current status;
    the durable project record or closeout responses must use the final fire,
    electrical, and handover facts. Three arbitrary service calls do not count.
    """
    records = agent_tool_result_records(
        ctx,
        tool_any=["get_visa_application", "list_visa_applications"],
        min_stage=0,
        max_stage=20,
    )

    def verified_apps(start: int, end: int, allowed: tuple[str, ...]) -> set[str]:
        found: set[str] = set()
        for record in records:
            stage = record["stage"]
            if not isinstance(stage, int) or not start <= stage <= end:
                continue
            pairs = {
                (app, status)
                for app, status in agent_application_status_pairs(record)
                if app in allowed and status
            }
            if "get_visa_application" in record["name"]:
                pairs = {
                    (app, status)
                    for app, status in pairs
                    if app in record["input_text"]
                }
            found.update(app for app, _status in pairs)
        return found

    early = verified_apps(0, 6, ("commercial_fit_up_filing_001",))
    middle_required = {"fire_inspection_app_001", "electrical_load_app_001"}
    middle = verified_apps(7, 14, tuple(middle_required | {"commercial_handover_001"}))
    closeout_required = {
        "fire_inspection_app_001",
        "electrical_load_app_001",
        "commercial_handover_001",
    }
    closeout = verified_apps(15, 20, tuple(closeout_required))
    if early != {"commercial_fit_up_filing_001"}:
        return False
    if not middle_required.issubset(middle):
        return False
    if not closeout_required.issubset(closeout):
        return False

    closeout_records = [
        record
        for record in records
        if isinstance(record["stage"], int)
        and 15 <= record["stage"] <= 20
    ]
    approved_closeout = {
        app
        for record in closeout_records
        for app, status in agent_application_status_pairs(record)
        if app in closeout_required and status == "approved"
    }
    if approved_closeout != closeout_required:
        return False

    durable = await workspace_text(ctx)
    durable += "\n" + "\n".join(stage_response(ctx, stage) for stage in range(15, 21))
    return count_groups(
        durable,
        [
            ["fire_inspection_app_001", "消防验收", "消防复审"],
            ["electrical_load_app_001", "强电复测", "负荷"],
            ["commercial_handover_001", "handover", "交付", "入驻"],
            ["approved", "批准", "通过"],
            ["闭环", "放行", "closeout", "最终状态", "入驻"],
        ],
    ) >= 5


async def chk_cross_schedule_material_and_gate_sources_rechecked(ctx) -> bool:
    """After mid-project changes, the agent rechecked the three sources that
    drive a valid replan: compliance gates, calendar, and material/vendor facts.
    """
    categories = [
        {"tool_any": ["get_visa_application", "list_visa_applications"]},
        {"tool_any": ["list_events", "get_event", "search_events"]},
        {
            "tool_any": [
                "API-post-database-query", "API-retrieve-a-page", "API-post-search",
                "read_email", "get_emails", "search_emails",
            ],
            "args_any": ["material", "glass", "玻璃", "furniture", "家具", "supplier"],
        },
    ]
    if count_tool_categories_called(ctx, categories=categories, min_stage=7, max_stage=20) < 3:
        return False
    matching_stages = {
        stage
        for stage in range(7, 21)
        if any(
            agent_tool_called(
                ctx,
                tool_any=category["tool_any"],
                args_any=category.get("args_any"),
                stage=stage,
            )
            for category in categories
        )
    }
    return len(matching_stages) >= 2


CHECKS.extend([
    ("chk_cross_compliance_polled_in_early_mid_closeout_windows",
     chk_cross_compliance_polled_in_early_mid_closeout_windows, 7.5),
    ("chk_cross_schedule_material_and_gate_sources_rechecked",
     chk_cross_schedule_material_and_gate_sources_rechecked, 3.75),
])


from .stage_9 import chk_evidence_live_gate_repolled_after_silent_mutations

CHECKS.append((
    "chk_evidence_live_gate_repolled_after_silent_mutations",
    chk_evidence_live_gate_repolled_after_silent_mutations,
    3.75,
))
