from __future__ import annotations
from ._helpers import *


def s17_alternative_candidate_pool(env) -> bool:
    return (
        tool_stage(env, 17, "listing_platform", "search", ("600000",))
        and tool_stage(env, 17, "listing_platform", None, (C.LIST_E,))
        and tool_stage(env, 17, "maps", None, (C.DESTINATION,))
        and listing_within_budget(env, C.LIST_E)
        and stage_any_structured_evidence(env, 17, [("备选", "预算"), ("候补", "预算")])
    )


def s17_calendar_window_draft_only(env) -> bool:
    return (
        tool_stage(env, 17, "calendar", None, ("看房",))
        and positive_authorization_boundary(env, 17, ("看房", "确认"))
    )


CHECKS = [
    ("s17_alternative_candidate_pool", s17_alternative_candidate_pool, 1.25),
    ("s17_calendar_window_draft_only", s17_calendar_window_draft_only, 1.5),
]
