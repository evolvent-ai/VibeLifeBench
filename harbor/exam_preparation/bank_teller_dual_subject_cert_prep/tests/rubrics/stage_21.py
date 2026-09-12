from __future__ import annotations
from . import _helpers as h


def r37_official_final_plan(env) -> bool:
    return bool(
        h.tool_used(env, 21, "notification_hub")
        and h.tool_used(env, 21, "calendar")
        and h.calendar_ticket_matches_backend(env)
        and h.durable_evidence_contains(env, "exam control", "exam_control.md", "2026-08-16", "3机房", "18号", "法律法规", "个人理财")
    )


def r38_pre_exam_checklist_complete(env) -> bool:
    return bool(
        h.any_tool(env, 21, ("notion",))
        and h.tool_used(env, 21, "calendar")
        and h.durable_evidence_contains(
            env, "pre exam checklist", "pre_exam_checklist.md",
            ("身份证", "证件"), "3机房", "18号", ("出发", "路线"), ("拥堵", "缓冲"), ("午休", "简餐"),
        )
    )


def r39_exam_day_reminders(env) -> bool:
    return bool(
        h.tool_used(env, 21, "calendar")
        and h.calendar_has_exam_day_plan(env)
    )


CHECKS = [
    ("r37_official_final_plan", r37_official_final_plan, 1.25),
    ("r38_pre_exam_checklist_complete", r38_pre_exam_checklist_complete, 1.25),
    ("r39_exam_day_reminders", r39_exam_day_reminders, 1.25),
]
