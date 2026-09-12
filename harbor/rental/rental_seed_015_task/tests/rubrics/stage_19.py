from __future__ import annotations
from ._helpers import *


def s19_listing_h_verified_candidate(env) -> bool:
    return (
        stage_ok(env, 19, "s19")
        and listing_h_backend_viable(env)
        and listing_h_route_backend_viable(env)
        and review_has(env, "mer_h", ["elevator", "vehicle noise"])
        and inbox_message_has(env, body_parts=["Clearwave Residence", "18:30", "not required to submit"])
        and notion_has_any(env, ([C.LIST_H, "verification candidate", "route", "elevator", "deposit"], ["Clearwave Residence", "available viewing window", "night noise", "documents"]))
    )


def s19_calendar_conflict_recovery(env) -> bool:
    return (
        stage_ok(env, 19, "s19")
        and parent_meeting_retimed(env)
        and notion_has_any(env, (["parent meeting", "17:40", "18:20", "18:30", "conflict"], ["viewing window", "insufficient buffer", "pending user decision"]))
        and not any("schedule_viewing" in str(call.get("name") or "").lower() for call in _tool_calls(env, 19))
    )


CHECKS = [
    ("s19_listing_h_verified_candidate", s19_listing_h_verified_candidate, 1.75),
    ("s19_calendar_conflict_recovery", s19_calendar_conflict_recovery, 1.75),
]
