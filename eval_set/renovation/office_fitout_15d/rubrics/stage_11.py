"""Stage 11 — customs-delay recovery, VOC evidence, and badge lead time."""
from __future__ import annotations

from ._helpers import has_any, read_workspace_file, sent_email_records, stage_response, workspace_blob


async def chk_imported_glass_delay_reconciled(ctx) -> bool:
    """The durable plan replaces or de-risks the delayed imported glass."""
    blob = (await workspace_blob(ctx)) + "\n" + stage_response(ctx, stage=11)
    has_delay = has_any(blob, ["海关", "customs", "out_of_stock", "35 天", "42 天", "21 天"])
    has_recovery = has_any(
        blob,
        ["国产替代", "国产 玻璃", "domestic substitute", "mat_glass_partition_002", "mat_glass_door_001", "替换进口"],
    )
    has_schedule_effect = has_any(blob, ["09-01", "9/1", "入驻", "handover", "关键路径", "lead"])
    return has_delay and has_recovery and has_schedule_effect


async def chk_furniture_voc_evidence_requested(ctx) -> bool:
    """A targeted supplier message requests CMA evidence / sampling."""
    sent = await sent_email_records(ctx)
    for record in sent:
        target = " ".join(record.recipients) + " " + record.text
        if not has_any(target, ["aishi", "爱仕", "furniture", "家具"]):
            continue
        has_report = has_any(record.text, ["cma", "检测报告", "test report", "抽检", "sampling"])
        has_threshold = has_any(record.text, ["0.05", "甲醛", "formaldehyde", "enf", "f4"])
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
    has_badge = has_any(text, ["badge", "门禁", "工牌", "证件", "security id"])
    has_lead = has_any(text, ["3-5", "3–5", "提前", "lead time", "工作日", "预约"])
    return has_badge and has_lead


CHECKS = [
    ("chk_imported_glass_delay_reconciled", chk_imported_glass_delay_reconciled, 3.0),
    ("chk_furniture_voc_evidence_requested", chk_furniture_voc_evidence_requested, 2.5),
    ("chk_badge_lead_time_is_planned", chk_badge_lead_time_is_planned, 1.5),
]
