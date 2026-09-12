from __future__ import annotations
from ._helpers import *


def s8_scheduled_monitor(env) -> bool:
    refreshed_inputs = (
        used_tool(env, 8, "email")
        and used_tool(env, 8, "calendar")
        and used_tool(env, 8, "review_platform")
        and used_tool(env, 8, "banking")
        and used_tool(env, 8, "maps")
        and used_tool(env, 8, "weather")
        and used_tool(env, 8, "notification_hub")
    )
    scheduled_object_seen = notification_from_trace(env, 8, ["planning consistency review", "candidate calendar", "notification center"])
    durable_refresh = used_tool(env, 8, "notion") and workspace_has(
        env,
        "RISK_REGISTER.json",
        ["email", "calendar", "vendor", "route", "weather", "budget", "notification", "recent review"],
        7,
        stage=8,
    )
    return refreshed_inputs and scheduled_object_seen and durable_refresh


CHECKS = [("s8_scheduled_monitor", s8_scheduled_monitor, 1.75)]
