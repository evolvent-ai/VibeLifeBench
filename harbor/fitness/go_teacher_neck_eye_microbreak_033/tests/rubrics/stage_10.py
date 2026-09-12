from __future__ import annotations

from ._helpers import calendar_has, notification_has, scheduled_trace, stage_record


def chk_s10_discover_calendar_mutation(env) -> bool:
    backend = calendar_has(env, (("open class", "open-class"), ("17:30",), ("21:30",)))
    notice = notification_has(env, (("schedule review", "schedulereview"), ("schedule_refresh", "next-week schedule")))
    logged = stage_record(env, "schedule_context_log.md", 10, (("open class",), ("evening session", "17:30", "21:30"), ("continuous teaching",)), ("Schedule object", "Date/time/location", "Personal-reminder impact", "Verified at"))
    traced = scheduled_trace(env, 10, "ntf_gt_s10_calendar", (
        ("calendar", "list_events", {"calendar_id": "cal_go_teacher_primary"}),
    ))
    return backend and notice and logged and traced


def chk_s10_open_class_safe_adjustment(env) -> bool:
    logged = stage_record(env, "calendar_change_log.md", 10, (("open class",), ("distance gaze", "eyes-closed rest", "eye break"), ("de-load", "preserve")), ("Previous window", "New window", "Formal-course boundary", "Backend verification"))
    return logged and calendar_has(env, (("distance gaze", "eyes-closed rest", "eye break", "microbreak"),))


CHECKS = [
    ("chk_s10_discover_calendar_mutation", chk_s10_discover_calendar_mutation, 1.75),
    ("chk_s10_open_class_safe_adjustment", chk_s10_open_class_safe_adjustment, 1.75),
]
