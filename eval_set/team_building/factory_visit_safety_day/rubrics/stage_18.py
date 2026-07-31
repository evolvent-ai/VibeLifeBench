from __future__ import annotations
from ._helpers import *

def s18_preflight_subscription(env) -> bool:
    return active_subscription_created_at_stage(env, 18, "policy_update")

def s18_calendar_updated(env) -> bool:
    return used_tool_with_value(env, 18, "calendar", "update_event", ["evt_factory_hold"]) and calendar_event_has(env, "evt_factory_hold", ["2026-07-21", "上海", "嘉兴"]) and durable_has(env, [["48小时", "执行前"], ["人员"], ["ppe", "防护"], ["路线"], ["保险"]])

CHECKS = [("s18_preflight_subscription", s18_preflight_subscription, 1.5), ("s18_calendar_updated", s18_calendar_updated, 1.5)]
