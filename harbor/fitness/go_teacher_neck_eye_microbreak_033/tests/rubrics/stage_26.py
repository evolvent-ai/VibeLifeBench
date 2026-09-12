from __future__ import annotations

from ._helpers import notification_has, scheduled_trace, stage_record, stage_service_count, stage_trace_service_count


SERVICES = ("calendar", "health_tracker", "notion", "email", "notification_hub")
REFRESH_CALLS = (
    ("calendar", "list_events", {"calendar_id": "cal_go_teacher_primary"}),
    ("health_tracker", "get_metrics", {"user_id": "user_liang_weimin", "type": "score", "since": "2026-07-01", "until": "2026-07-28"}),
    ("notion", "API-post-search", {"query": "Go instructor"}),
    ("email", "get_emails", {"folder": "INBOX"}),
)


def chk_s26_final_prep_service_consistency(env) -> bool:
    notice = notification_has(env, (("pre-closeout consistency check", "pre-close consistency check"), ("final_consistency_review", "five services")))
    logged = stage_record(env, "notification_monitor_log.md", 26, (("pre-closeout consistency check",), ("calendar",), ("health_tracker",), ("notion",), ("email",), ("notification_hub", "notification")), ("Notification reference", "Services refreshed", "Observed change", "Action/result"))
    traced = scheduled_trace(env, 26, "ntf_gt_s26_final", REFRESH_CALLS) and stage_trace_service_count(env, 26, SERVICES) == 5
    return notice and logged and traced


def chk_s26_latest_refresh_5_services(env) -> bool:
    progress = stage_record(env, "stage_progress.md", 26, (("refresh", "recheck"), ("five services", "5"), ("review",)), ("Facts read", "Action/result", "Updated artifacts"))
    traced = scheduled_trace(env, 26, "ntf_gt_s26_final", REFRESH_CALLS) and stage_trace_service_count(env, 26, SERVICES) == 5
    return progress and stage_service_count(env, 26, SERVICES) == 5 and traced


CHECKS = [
    ("chk_s26_final_prep_service_consistency", chk_s26_final_prep_service_consistency, 1.75),
    ("chk_s26_latest_refresh_5_services", chk_s26_latest_refresh_5_services, 1.5),
]
