"""
Stage 0 — workspace_artifact checkers (durable .md files exist and have substance).
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


async def chk_artifact_core_files_exist(ctx) -> bool:
    """F1: the master fit-out plan covers the breadth of the commercial
    project AND ≥2 of the 3 core artifacts have real structure + a concrete
    anchor (ID / ISO date / currency) showing they are not empty skeletons.

    OUTCOME-GROUNDED + EQUIVALENCE-TOLERANT: domain coverage is measured by
    concept *groups* (Chinese OR English synonyms), the plan can live in
    ``fit_out_plan.md`` and the schedule in ``schedule.md``, and the
    "real content" gate is ``has_real_anchor`` (any genuine ID / date /
    amount) — NOT a specific seed-ID token. No single literal ID is
    required to pass.
    """
    from ._helpers import has_real_anchor, has_structure
    plan_text = (
        await read_workspace_file(ctx, "fit_out_plan.md")
        + "\n"
        + await read_workspace_file(ctx, "requirements_brief.md")
    )
    schedule_text = await read_workspace_file(ctx, "schedule.md")
    blob = (plan_text + "\n" + schedule_text)
    # Commercial fit-out domain groups (CN OR EN). ≥10 of 16 must appear.
    domain_groups = [
        ["filing", "备案", "一件事", "jingan", "静安"],
        ["design", "设计", "schematic", "bim", "深化"],
        ["fire", "消防", "fire acceptance", "消防验收"],
        ["electrical", "强弱电", "强电", "load", "负荷"],
        ["partition", "隔断", "glass", "玻璃", "decoration", "装饰"],
        ["lighting", "照明", "emergency light", "应急照明"],
        ["hvac", "空调", "smart control", "智能", "弱电"],
        ["furniture", "家具", "工位", "workstation", "会议室"],
        ["insurance", "保险", "工程一切险", "all risk"],
        ["handover", "交付", "入驻", "occupancy", "竣工"],
        ["inspection", "验收", "acceptance"],
        ["compliance", "合规", "rule", "规范"],
        ["budget", "预算", "cost"],
        ["reserve", "预留", "contingency", "buffer"],
        ["schedule", "排期", "工期", "timeline"],
        ["punch", "整改", "punch list", "残留"],
    ]
    domain_hits = count_groups(blob, domain_groups)
    if domain_hits < 10:
        return False
    core_files = ("fit_out_plan.md", "budget_tracker.md", "schedule.md")
    qualifying = 0
    for name in core_files:
        text = await read_workspace_file(ctx, name)
        if not text or len(text) < 300:
            continue
        if not has_structure(text):
            continue
        # Concrete content (any real ID / ISO date / currency amount), not a
        # specific seed token — this is the de-brittled anchor gate.
        if not has_real_anchor(text):
            continue
        qualifying += 1
    return qualifying >= 2


async def chk_artifact_budget_has_committed_pending_reserve(ctx) -> bool:
    """F1: budget_tracker.md is internally consistent within the authorized
    envelope (hard cap ¥800k + ¥40k reserve).

    OUTCOME-GROUNDED (internal-consistency, not number-string matching):
      * committed / pending / reserve buckets are present and parseable
      * reserve maintained at/above the ¥40,000 minimum
      * committed within the ¥800k hard cap
      * committed + pending + reserve within the ¥840k envelope
    BONUS (non-gating): citing a concrete vendor/provider id strengthens
    the artifact but its absence never fails a model that did the math.
    """
    from ._helpers import budget_within_envelope
    text = await read_workspace_file(ctx, "budget_tracker.md")
    if not text:
        return False
    return budget_within_envelope(
        text, cap=BUDGET_CAP_CNY, reserve_min=BUDGET_RESERVE_MIN_CNY,
    )


async def chk_artifact_schedule_sequenced(ctx) -> bool:
    """F1: schedule.md sequences the commercial fit-out phases with explicit
    dependency / gate ordering and an inspection-gate awareness.

    OUTCOME-GROUNDED + EQUIVALENCE-TOLERANT:
      * ≥10 of the 15 commercial phases are present (concept groups, CN/EN)
      * explicit dependency vocabulary appears (前置 / depends_on / after /
        gate / blocked by / 通过后 ...)
      * inspection-gate awareness appears as a CONCEPT (fire / electrical /
        handover acceptance), not a specific insp_std_* token
    No SCH-* / insp_std_* literal token is required.
    """
    text = await read_workspace_file(ctx, "schedule.md")
    if not text:
        return False
    phase_groups = [
        ["filing", "备案", "一件事", "jingan", "静安"],
        ["design", "设计", "schematic", "深化", "bim"],
        ["fire drawing", "消防图", "消防", "fire"],
        ["strong", "强电", "强弱电", "power plan", "load"],
        ["fit-up window", "fit-up", "进场", "fit up window"],
        ["emergency light", "应急照明", "emergency lighting"],
        ["rough", "rough-in", "rough in", "隐蔽", "concealed"],
        ["concealed acceptance", "隐蔽验收", "concealed-works"],
        ["partition", "隔断", "玻璃", "glass", "decoration", "装饰"],
        ["lighting", "照明", "smart", "智能", "hvac", "空调"],
        ["furniture", "家具", "工位", "workstation", "会议室"],
        ["fire acceptance", "消防验收", "fire inspection"],
        ["electrical test", "负荷测试", "load test", "电气验收"],
        ["air quality", "甲醛", "voc", "formaldehyde"],
        ["handover", "交付", "入驻", "occupancy", "punch"],
    ]
    phases_covered = count_groups(text, phase_groups)
    has_dependencies = has_any(
        text,
        [
            "depends_on", "depends on", "前置", "依赖", "blocked by",
            "blocked_by", "after", "gate", "门", "通过后", "完成后",
            "pass first", "需要先", "prerequisite",
        ],
    )
    has_gate_awareness = has_any(
        text,
        [
            "fire", "消防", "electrical", "强弱电", "强电", "load",
            "负荷", "handover", "交付", "验收", "acceptance", "inspection",
        ],
    )
    return phases_covered >= 10 and has_dependencies and has_gate_awareness


async def chk_artifact_contractor_comparison_rows(ctx) -> bool:
    """F1: vendor_comparison.md genuinely compares ≥3 design-build vendors
    on rating / quote / risk dimensions with concrete figures.

    OUTCOME-GROUNDED + EQUIVALENCE-TOLERANT:
      * ≥3 distinct vendor rows — counted by ANY of: distinct prov_v3_*
        IDs, distinct vendor names, or ≥3 row markers in a table — so a
        capable model that names vendors instead of echoing IDs still
        passes
      * the comparison shows rating + quote + risk dimensions (CN OR EN)
      * carries ≥3 distinct concrete quote amounts (real numbers, any
        format) so the comparison is data-grounded, not prose
    No specific prov_* / rev_* literal token is required.
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
    # Vendor-row count via three equivalent signals.
    prov_ids = set(_re.findall(r"prov_v\d+_\d{3}", low))
    vendor_names = [
        n for n in (
            "沪安", "申品", "永信", "modulux", "chenpin", "hushang",
            "公装", "design-build", "design build", "设计施工",
        )
        if n.lower() in low
    ]
    table_rows = len(_re.findall(r"^\s*\|.*\|\s*$", text, _re.MULTILINE))
    distinct_vendor_signal = max(
        len(prov_ids), len(set(vendor_names)), max(0, table_rows - 1)
    )
    rows_ok = distinct_vendor_signal >= 3
    has_dimensions = (
        count_groups(
            low,
            [
                ["rating", "评分", "评级", "口碑", "review"],
                ["quote", "报价", "价格", "总价", "price"],
                ["risk", "风险", "complaint", "投诉", "red flag"],
            ],
        )
        >= 3
    )
    has_data = count_distinct_amounts(text, lo=10000, hi=2000000) >= 3
    return rows_ok and has_dimensions and has_data


async def chk_artifact_risk_register_has_known_traps(ctx) -> bool:
    """F1: risk_register.md surfaces ≥5 of the real commercial fit-out traps
    and carries mitigation language.

    OUTCOME-GROUNDED + EQUIVALENCE-TOLERANT: each trap is a broad concept
    group (CN OR EN synonyms) drawn from the scenario's actual hazards
    (BIM/filing RFI, fire one-shot fail, electrical load deficit, fit-up
    window discipline, insurance-before-fit-up, emergency-light count,
    glass-partition lead time, VOC/formaldehyde, kickback ethics). A
    capable model that describes the hazard without echoing a seed ID still
    passes; mitigation must be present so the register is actionable, not a
    list of complaints. No specific rule_*/prov_*/hold_* token is required.
    """
    text = await read_workspace_file(ctx, "risk_register.md")
    if not text:
        return False
    trap_groups = [
        ["bim", "filing rfi", "备案", "一件事", "rfi", "深化", "lod"],
        ["fire", "消防", "one-shot", "一次性", "消防验收", "驳回"],
        ["electrical", "强弱电", "强电", "load", "负荷", "不达标", "deficit"],
        ["fit-up window", "fit-up", "进场窗口", "fit up window", "窗口"],
        ["insurance", "工程一切险", "保险", "all risk", "在保"],
        ["emergency light", "应急照明", "24", "点位"],
        ["lead time", "lead_time", "工期", "交付周期", "backorder", "进口"],
        ["voc", "甲醛", "tvoc", "formaldehyde", "0.05", "环保"],
        ["kickback", "贿赂", "感谢费", "回扣", "ethics", "利益输送"],
        ["budget", "预算", "reserve", "预留", "超支", "overrun"],
    ]
    traps_ok = count_groups(text, trap_groups) >= 5
    has_mitigation = has_any(
        text,
        [
            "mitigation", "缓解", "应对", "fallback", "备用", "对策",
            "缓释", "应急", "remediation", "措施", "plan b", "预案",
        ],
    )
    return traps_ok and has_mitigation


CHECKS = [
    ('chk_artifact_core_files_exist', chk_artifact_core_files_exist, 1),
    ('chk_artifact_budget_has_committed_pending_reserve', chk_artifact_budget_has_committed_pending_reserve, 1.5),
    ('chk_artifact_schedule_sequenced', chk_artifact_schedule_sequenced, 1.5),
    ('chk_artifact_contractor_comparison_rows', chk_artifact_contractor_comparison_rows, 1),
    ('chk_artifact_risk_register_has_known_traps', chk_artifact_risk_register_has_known_traps, 1),
]
