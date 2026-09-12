from __future__ import annotations
from ._helpers import *


def s23_last_verified_refresh(env) -> bool:
    return (
        stage_ok(env, 23, "s23")
        and listing_h_backend_viable(env)
        and listing_h_route_backend_viable(env)
        and review_has(env, "mer_h", ["elevator", "vehicle noise"])
        and h_viewing_calendar_event(env)
        and h_travel_buffer_event(env)
        and parent_meeting_cancelled(env)
        and notion_has_any(env, ([C.LIST_H, "last verification", "2026-07-31"], ["Clearwave Residence", "before viewing", "route", "elevator", "documents"]))
    )


CHECKS = [("s23_last_verified_refresh", s23_last_verified_refresh, 1.5)]
