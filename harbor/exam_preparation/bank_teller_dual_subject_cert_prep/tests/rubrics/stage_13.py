from __future__ import annotations
from . import _helpers as h


def r25_marketing_calendar_created(env) -> bool:
    return bool(
        h.tool_used(env, 13, "email")
        and h.tool_used(env, 13, "calendar")
        and h.email_message_seen(env, "7 月 26 日外出营销", "manager@binjiang-bank.example")
        and h.calendar_event_match(env, date="2026-07-26", status="confirmed", summary_any=("营销", "社区"))
    )


def r26_conflict_mock_canceled(env) -> bool:
    return bool(
        r25_marketing_calendar_created(env)
        and h.calendar_event(env, "evt_mock_hold_0726", "cancelled")
    )


def r27_mock_rescheduled_to_comp_time(env) -> bool:
    return bool(
        h.tool_used(env, 13, "calendar")
        and h.calendar_has_marketing_reschedule(env)
        and h.durable_evidence_contains(
            env, "calendar change", "calendar_change_log.md",
            "2026-07-26", "2026-07-28", ("16:30", "下午"), ("主管邮件", "调休"), ("取消", "改期"),
        )
    )


CHECKS = [
    ("r25_marketing_calendar_created", r25_marketing_calendar_created, 1.75),
    ("r26_conflict_mock_canceled", r26_conflict_mock_canceled, 1.5),
    ("r27_mock_rescheduled_to_comp_time", r27_mock_rescheduled_to_comp_time, 1.5),
]
