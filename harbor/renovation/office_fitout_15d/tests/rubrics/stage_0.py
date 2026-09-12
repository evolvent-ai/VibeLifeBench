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
        ["filing", "filing", "one-stop filing", "jingan", "Jingan"],
        ["design", "design", "schematic", "bim", "detailing"],
        ["fire", "fire", "fire acceptance", "fire acceptance"],
        ["electrical", "strong-current", "strong-current", "load", "load"],
        ["partition", "partition", "glass", "glass", "decoration", "decoration"],
        ["lighting", "lighting", "emergency light", "emergency lighting"],
        ["hvac", "HVAC", "smart", "low-voltage"],
        ["furniture", "furniture", "workstation", "workstation", "meeting room"],
        ["insurance", "insurance", "contractors all-risk insurance", "all risk"],
        ["handover", "delivery", "occupancy", "occupancy", "completion"],
        ["inspection", "acceptance", "acceptance"],
        ["compliance", "compliance", "rule", "standard"],
        ["budget", "budget", "cost"],
        ["reserve", "reserve", "contingency", "buffer"],
        ["schedule", "schedule", "schedule", "timeline"],
        ["punch", "scenario-term", "punch list", "residual"],
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
      * explicit dependency vocabulary appears (prerequisite / depends_on / after /
        gate / blocked by / passedafter ...)
      * inspection-gate awareness appears as a CONCEPT (fire / electrical /
        handover acceptance), not a specific insp_std_* token
    No SCH-* / insp_std_* literal token is required.
    """
    text = await read_workspace_file(ctx, "schedule.md")
    if not text:
        return False
    phase_groups = [
        ["filing", "filing", "one-stop filing", "jingan", "Jingan"],
        ["design", "design", "schematic", "detailing", "bim"],
        ["fire", "fire acceptance"],
        ["strong", "strong-current", "strong-current", "power plan", "load"],
        ["fit-up", "delivery"],
        ["emergency light", "emergency lighting", "emergency lighting"],
        ["rough", "rough-in", "rough in", "concealed", "concealed"],
        ["concealed acceptance", "concealed acceptance", "concealed-works"],
        ["partition", "partition", "glass", "glass", "decoration", "decoration"],
        ["lighting", "lighting", "smart", "smart", "hvac", "HVAC"],
        ["furniture", "furniture", "workstation", "workstation", "meeting room"],
        ["fire acceptance", "fire acceptance", "fire inspection"],
        ["electrical test", "load test", "load test", "electrical acceptance"],
        ["air quality", "formaldehyde", "voc", "formaldehyde"],
        ["handover", "delivery", "occupancy", "occupancy", "punch"],
    ]
    phases_covered = count_groups(text, phase_groups)
    has_dependencies = has_any(
        text,
        [
            "depends_on", "depends on", "prerequisite", "depends on", "blocked by",
            "blocked_by", "after", "gate", "scenario-term", "passedafter", "after completion",
            "pass first", "scenario-termfirst", "prerequisite",
        ],
    )
    has_gate_awareness = has_any(
        text,
        [
            "fire", "fire safety", "electrical", "strong-current and low-voltage systems", "strong-current", "load",
            "load", "handover", "delivery", "acceptance", "acceptance", "inspection",
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
            "Hushang", "Shenpin", "Yongxin", "modulux", "chenpin", "hushang",
            "commercial fit-out", "design-build", "design build", "designconstruction",
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
                ["rating", "rating", "rating", "reputation", "review"],
                ["quote", "scenario-term", "price", "scenario-term", "price"],
                ["risk", "risk", "complaint", "scenario-term", "red flag"],
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
        ["bim", "filing rfi", "filing", "one-stop filing", "rfi", "detailing", "lod"],
        ["fire", "fire", "one-shot", "one-shot", "fire acceptance", "rejected"],
        ["electrical", "strong-current", "strong-current", "load", "load", "not passed", "deficit"],
        ["fit-up window", "fit-up", "entry window", "fit-up", "window"],
        ["insurance", "contractors all-risk insurance", "insurance", "all risk", "in force"],
        ["emergency light", "emergency lighting", "24", "points"],
        ["lead time", "lead_time", "schedule", "delivery lead time", "backorder", "import"],
        ["voc", "formaldehyde", "tvoc", "formaldehyde", "0.05", "environmental"],
        ["kickback", "bribery", "scenario-term", "kickback", "ethics", "kickback"],
        ["budget", "budget", "reserve", "reserve", "overrun", "overrun"],
    ]
    traps_ok = count_groups(text, trap_groups) >= 5
    has_mitigation = has_any(
        text,
        [
            "mitigation", "scenario-term", "response", "fallback", "fallback", "countermeasure",
            "scenario-term", "emergency", "remediation", "scenario-term", "plan b", "scenario-term",
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
