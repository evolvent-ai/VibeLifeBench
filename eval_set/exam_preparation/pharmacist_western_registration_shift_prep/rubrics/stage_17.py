from __future__ import annotations

from ._helpers import email_result_seen, stage_calendar_event_written


def r31_temp_night_shift_created(env) -> bool:
    return bool(
        email_result_seen(env, 17, "msg_temp_shift")
        and stage_calendar_event_written(env, 17, "夜班", date="2026-09-08")
    )


def r32_daytime_study_shifted_after_night(env) -> bool:
    return bool(
        r31_temp_night_shift_created(env)
        and stage_calendar_event_written(env, 17, "复习", date="2026-09-09")
    )


CHECKS = [
    ("r31_temp_night_shift_created", r31_temp_night_shift_created, 1.5),
    ("r32_daytime_study_shifted_after_night", r32_daytime_study_shifted_after_night, 2.0),
]
