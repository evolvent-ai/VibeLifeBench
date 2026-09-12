from __future__ import annotations
from ._helpers import *


def s14_fresh_listing_status(env) -> bool:
    return (
        stage_ref_checked(env, 14, "listing_platform", "c")
        and listing_status(env, C.LIST_C) == "active"
        and candidate_c_backend_viable(env)
        and stage_record_persisted(
            env,
            14,
            [("Yunqi Court", C.LIST_C), ("active", "viewable"), ("6650", "665000")],
            files=("CANDIDATE_TRACKER.md",),
        )
    )


def s14_final_candidate_refresh(env) -> bool:
    return (
        s14_fresh_listing_status(env)
        and stage_record_persisted(
            env,
            14,
            [
                ("Yunqi Court", C.LIST_C),
                ("active", "viewable"),
                ("6650", "665000"),
                ("accessible", "doorway width", "ramp", "bathroom"),
                ("written", "proof", "pending verification", "pending on-site verification"),
            ],
            files=("CANDIDATE_TRACKER.md",),
        )
    )


CHECKS = [
    ('s14_fresh_listing_status', s14_fresh_listing_status, 1.25),
    ('s14_final_candidate_refresh', s14_final_candidate_refresh, 1.25),
]
