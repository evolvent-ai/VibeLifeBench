from __future__ import annotations
from ._helpers import *


def s0_notion_started(env) -> bool:
    notion_write = used_tool(env, 0, "notion", "API-post-page") or used_tool(env, 0, "notion", "API-patch-block-children")
    return (
        notion_write
        and workspace_has(env, "CITY_CULTURE_PLAN.json", ["cross-cultural icebreaking", "onboarding new colleagues", "low-intensity", "organizational belonging"], 3, stage=0)
        and workspace_has(env, "RISK_REGISTER.json", ["46000", "authorization", "privacy", "accessible"], 3, stage=0)
    )


def s0_calendar_candidate(env) -> bool:
    return used_tool_with_value(env, 0, "calendar", "update_event", ["evt_culture_day_hold"]) and calendar_event_has(env, "city culture event", "2026-07-21", stage=0)


CHECKS = [("s0_notion_started", s0_notion_started, 1.5), ("s0_calendar_candidate", s0_calendar_candidate, 1.5)]
