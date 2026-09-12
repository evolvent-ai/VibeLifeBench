from __future__ import annotations
from ._helpers import *


def s0_notion_started(env) -> bool:
    wrote = (
        used_tool(env, 0, "notion", "API-post-page")
        or used_tool(env, 0, "notion", "API-patch-block-children")
        or used_tool(env, 0, "notion", "API-update-a-block")
    )
    return wrote and notion_page_has(
        env,
        page_id=CONTROL_PAGE_ID,
        content_groups=[
            ["factory visit", "team day", "team", "day"],
            ["budget", "cap", "company"],
            ["risk", "day"],
            ["authorization", "confirm"],
            ["pending confirmation", "pending"],
        ],
        forbidden_content=["assistant maintains each stage"],
    )


def s0_calendar_candidate(env) -> bool:
    return used_tool_with_value(env, 0, "calendar", "update_event", ["evt_factory_hold"]) and calendar_event_has(env, "evt_factory_hold", ["2026-07-21", "factory visit"])


CHECKS = [("s0_notion_started", s0_notion_started, 1.5), ("s0_calendar_candidate", s0_calendar_candidate, 1.5)]
