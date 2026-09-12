from __future__ import annotations
from ._helpers import *


def s18_preflight_subscription(env) -> bool:
    return (
        used_tool_with_value(env, 18, "weather", "get_alerts", ["alert_yuexiu_heat_20260721", "orange", "extreme heat"])
        and used_tool_with_value(env, 18, "notification_hub", "create_subscription", ["weather", "yuexiu", "heat"])
        and active_subscription_from_trace(env, 18, "keyword", ["weather", "yuexiu", "heat"])
    )


def s18_calendar_updated(env) -> bool:
    return (
        used_tool_with_value(env, 18, "calendar", "update_event", ["evt_culture_day_hold", "extreme heat", "accessible"])
        and calendar_event_has(env, "city culture event", "2026-07-21", stage=18)
        and calendar_event_count(env, "city culture event", "2026-07-21", stage=18) == 1
    )


CHECKS = [("s18_preflight_subscription", s18_preflight_subscription, 1.5), ("s18_calendar_updated", s18_calendar_updated, 1.25)]
