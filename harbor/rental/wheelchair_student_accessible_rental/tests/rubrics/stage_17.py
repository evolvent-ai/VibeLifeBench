from __future__ import annotations
from ._helpers import *


def s17_alternative_candidate_pool(env) -> bool:
    return (
        stage_listing_search(env, 17)
        and stage_route_checked(env, 17, "c", max_minutes=35)
        and stage_record_persisted(
            env,
            17,
            [("alternative", "similarcandidate"), ("6800", "budget"), ("accessible",), ("one-bedroom", "private room"), ("Yunqi Court", C.LIST_C)],
            files=("CANDIDATE_TRACKER.md",),
        )
    )


def s17_calendar_window_draft_only(env) -> bool:
    return (
        s17_alternative_candidate_pool(env)
        and stage_calendar_persisted(
            env,
            17,
            [("Yunqi Court", "home viewing"), ("pending user confirmation", "pending confirmation"), ("family", "family viewing"), ("internal", "window")],
        )
        and stage_record_persisted(
            env,
            17,
            [("home viewing",), ("family",), ("window",), ("pending confirmation", "user confirmation"), ("do not make an appointment", "internal")],
            files=("AUTH_LOG.md", "CANDIDATE_TRACKER.md"),
        )
        and len(viewings(env)) == 0
    )


CHECKS = [
    ('s17_alternative_candidate_pool', s17_alternative_candidate_pool, 1.25),
    ('s17_calendar_window_draft_only', s17_calendar_window_draft_only, 1.5),
]
