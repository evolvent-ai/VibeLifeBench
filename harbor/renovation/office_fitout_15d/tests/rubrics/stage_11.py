"""Stage 11 — customs-delay recovery, VOC evidence, and badge lead time."""
from __future__ import annotations

from ._helpers import has_any, read_workspace_file, sent_email_records, stage_response, workspace_blob


async def chk_imported_glass_delay_reconciled(ctx) -> bool:
    """The durable plan replaces or de-risks the delayed imported glass."""
    blob = (await workspace_blob(ctx)) + "\n" + stage_response(ctx, stage=11)
    has_delay = has_any(blob, ["scenario-term", "customs", "out_of_stock", "35 days", "42 days", "21 days"])
    has_recovery = has_any(
        blob,
        ["domestic substitute", "domestic glass", "domestic substitute", "mat_glass_partition_002", "mat_glass_door_001", "scenario-termimport"],
    )
    has_schedule_effect = has_any(blob, ["09-01", "9/1", "occupancy", "handover", "critical path", "lead"])
    return has_delay and has_recovery and has_schedule_effect


async def chk_furniture_voc_evidence_requested(ctx) -> bool:
    """A targeted supplier message requests CMA evidence / sampling."""
    sent = await sent_email_records(ctx)
    for record in sent:
        target = " ".join(record.recipients) + " " + record.text
        if not has_any(target, ["aishi", "scenario-term", "furniture", "furniture"]):
            continue
        has_report = has_any(record.text, ["cma", "testscenario-term", "test report", "scenario-term", "sampling"])
        has_threshold = has_any(record.text, ["0.05", "formaldehyde", "formaldehyde", "enf", "f4"])
        if has_report and has_threshold:
            return True
    return False


async def chk_badge_lead_time_is_planned(ctx) -> bool:
    """Security-badge lead time is reflected in schedule/comms/risk state."""
    text = "\n".join(
        [
            await read_workspace_file(ctx, "schedule.md"),
            await read_workspace_file(ctx, "risk_register.md"),
            await read_workspace_file(ctx, "communications_log.md"),
            stage_response(ctx, stage=11),
        ]
    )
    has_badge = has_any(text, ["badge", "scenario-term", "badge", "scenario-term", "security id"])
    has_lead = has_any(text, ["3-5", "3–5", "scenario-termbefore", "lead time", "weekday", "scenario-term"])
    return has_badge and has_lead


CHECKS = [
    ("chk_imported_glass_delay_reconciled", chk_imported_glass_delay_reconciled, 3.0),
    ("chk_furniture_voc_evidence_requested", chk_furniture_voc_evidence_requested, 2.5),
    ("chk_badge_lead_time_is_planned", chk_badge_lead_time_is_planned, 1.5),
]
