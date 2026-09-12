from __future__ import annotations

from ._helpers import calendar_has, health_has, notification_has, scheduled_trace, stage_record


def chk_s24_discover_sat_shift(env) -> bool:
    calendar = calendar_has(env, (("Saturday long Go class (early)", "Saturday long Go class"), ("09:00", "9:00"), ("13:00",), ("shortened lunch break",)))
    notice = notification_has(env, (("pre-Saturday check",), ("saturday_precheck", "break window")))
    logged = stage_record(env, "schedule_context_log.md", 24, (("Saturday long class",), ("early",), ("09:00", "9:00"), ("13:00",), ("lunch break",)), ("Date/time/location", "Available break", "Personal-reminder impact", "Verified at"))
    traced = scheduled_trace(env, 24, "ntf_gt_s24_weekend", (
        ("calendar", "list_events", {"calendar_id": "cal_go_teacher_primary"}),
        ("health_tracker", "get_metrics", {"user_id": "user_liang_weimin", "type": "score", "since": "2026-07-01", "until": "2026-07-28"}),
        ("health_tracker", "get_metrics", {"user_id": "user_liang_weimin", "type": "sleep_minutes", "since": "2026-07-01", "until": "2026-07-28"}),
    ))
    return calendar and notice and logged and traced


def chk_s24_weekend_breaks_protected(env) -> bool:
    health = health_has(env, ("score", "sleep_minutes"), ())
    logged = stage_record(env, "calendar_change_log.md", 24, (("eating",), ("light walking",), ("eyes-closed rest", "eye break"), ("preserve",)), ("New window", "Reason/source", "Backend verification"))
    return health and logged and calendar_has(env, (("eating", "lunch"), ("light walking", "walking"), ("eyes-closed rest", "eye break")))


CHECKS = [
    ("chk_s24_discover_sat_shift", chk_s24_discover_sat_shift, 1.75),
    ("chk_s24_weekend_breaks_protected", chk_s24_weekend_breaks_protected, 1.75),
]
