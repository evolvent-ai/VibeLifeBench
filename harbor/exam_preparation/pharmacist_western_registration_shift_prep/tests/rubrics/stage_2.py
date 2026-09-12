from __future__ import annotations

from ._helpers import email_result_seen, stage_calendar_event_written


def r06_shift_email_to_calendar(env) -> bool:
    email_seen = email_result_seen(env, 2, "msg_shift_aug")
    calendar_synced = bool(
        stage_calendar_event_written(env, 2, date="2026-08-05")
        and stage_calendar_event_written(env, 2, date="2026-08-06")
    )
    return bool(email_seen and calendar_synced)


CHECKS = [
    ("r06_shift_email_to_calendar", r06_shift_email_to_calendar, 1.5),
]
