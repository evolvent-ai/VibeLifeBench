from __future__ import annotations

from ._helpers import service_count, task_writes_paired_authorized

ALLOWED = ("calendar", "health_tracker", "weather", "notion", "email")


def chk_tool_successful_cross_service_refresh(env) -> bool:
    return service_count(getattr(env, "current_stage", 27), env) >= 4


def chk_tool_writes_are_paired_and_authorized(env) -> bool:
    return task_writes_paired_authorized(env)


CHECKS = [
    ("chk_tool_successful_cross_service_refresh", chk_tool_successful_cross_service_refresh, 1.0),
    ("chk_tool_writes_are_paired_and_authorized", chk_tool_writes_are_paired_and_authorized, 1.0),
]
