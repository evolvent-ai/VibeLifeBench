from __future__ import annotations
from ._helpers import *

def s18_preflight_subscription(env) -> bool:
    return active_subscription_created_at_stage(env, 18, "policy_update")

def s18_calendar_updated(env) -> bool:
    return used_tool_with_value(env, 18, "calendar", "update_event", ["evt_factory_hold"]) and calendar_event_has(env, "evt_factory_hold", ["2026-07-21", "Shanghai", "Jiaxing"]) and durable_has(env, [["hours", "before"], ["participants"], ["PPE", "protection"], ["route"], ["insurance"]])

CHECKS = [("s18_preflight_subscription", s18_preflight_subscription, 1.5), ("s18_calendar_updated", s18_calendar_updated, 1.5)]
