from __future__ import annotations

from ._helpers import (
    calendar_has,
    notion_has,
    notification_has,
    scheduled_trace,
    stage_record,
    stage_trace_service_count,
)


def chk_s03_week1_calendar_created(env) -> bool:
    calendar = calendar_has(env, (("microbreak activity", "microbreak"), ("eye break", "distance gaze", "eyes-closed rest"), ("walking",)))
    logged = stage_record(env, "calendar_change_log.md", 3, (("personal",), ("microbreak activity",), ("eye break",), ("walking",)), ("Calendar object", "New window", "Formal-course boundary", "Backend verification"))
    return calendar and logged


def chk_s03_notification_monitor_started(env) -> bool:
    source = notification_has(env, (("first plan implementation check",), ("initial_plan_review", "first week"), ("personal_only", "personal")))
    logged = stage_record(env, "notification_monitor_log.md", 3, (("first plan implementation check",), ("calendar",), ("health_tracker",), ("notion",), ("email",), ("notification",)), ("Notification reference", "Triggered at", "Services refreshed", "Action/result", "Read/monitor status"))
    traced = scheduled_trace(env, 3, "ntf_gt_s03_setup") and stage_trace_service_count(
        env, 3, ("calendar", "health_tracker", "notion", "email", "notification_hub")
    ) == 5
    return source and logged and traced


def chk_s03_notion_hub_initialized(env) -> bool:
    return notion_has(env, "neck and shoulder", (("neck",), ("eye", "rest"))) and stage_record(env, "stage_progress.md", 3, (("Notion", "notion"), ("control hub",), ("written and rechecked", "verified")), ("Updated artifacts", "Action/result"))


CHECKS = [
    ("chk_s03_week1_calendar_created", chk_s03_week1_calendar_created, 1.75),
    ("chk_s03_notification_monitor_started", chk_s03_notification_monitor_started, 1.25),
    ("chk_s03_notion_hub_initialized", chk_s03_notion_hub_initialized, 1.5),
]
