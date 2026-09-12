from __future__ import annotations

from ._helpers import calendar_has, health_has, notification_has, scheduled_trace, stage_record, workout_has


def chk_s14_discover_eye_fatigue_mutation(env) -> bool:
    source = health_has(env, ("score",), (("eye_fatigue=8/10",), ("screen_review_minutes=125",), ("offscreen_break_needed=true",)))
    workout = workout_has(env, (("screen_review_session",), ("125",)))
    notice = notification_has(env, (("eye-break check",), ("eye_rest_review", "screen-based game review")))
    recorded = stage_record(env, "risk_log.md", 14, (("eye fatigue", "8/10"), ("screen", "125"), ("screen-free",)), ("Evidence/source", "Severity", "Status"))
    traced = scheduled_trace(env, 14, "ntf_gt_s14_eye", (
        ("health_tracker", "get_metrics", {"user_id": "user_liang_weimin", "type": "score", "since": "2026-07-01", "until": "2026-07-28"}),
        ("health_tracker", "list_workouts", {"user_id": "user_liang_weimin", "since": "2026-07-01", "until": "2026-07-28"}),
        ("calendar", "list_events", {"calendar_id": "cal_go_teacher_primary"}),
    ))
    return source and workout and notice and recorded and traced


def chk_s14_screen_review_downgrade(env) -> bool:
    return stage_record(env, "risk_log.md", 14, (("screen-based game review",), ("de-load", "shorten"), ("paper record", "screen-free"), ("distance gaze", "eyes-closed rest")), ("Decision", "Activity change", "Review threshold"))


def chk_s14_eye_break_calendar_updated(env) -> bool:
    logged = stage_record(env, "calendar_change_log.md", 14, (("eye break",), ("screen-free", "paper record", "distance gaze", "eyes-closed rest"), ("screen-based game review",)), ("Previous window", "New window", "Backend verification"))
    return logged and calendar_has(env, (("screen-free", "paper record", "distance gaze", "eyes-closed rest", "eye break"),))


CHECKS = [
    ("chk_s14_discover_eye_fatigue_mutation", chk_s14_discover_eye_fatigue_mutation, 2.0),
    ("chk_s14_screen_review_downgrade", chk_s14_screen_review_downgrade, 2.0),
    ("chk_s14_eye_break_calendar_updated", chk_s14_eye_break_calendar_updated, 1.5),
]
