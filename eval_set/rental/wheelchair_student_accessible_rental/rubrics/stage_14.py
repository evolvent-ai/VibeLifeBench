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
            [("云栖苑", C.LIST_C), ("active", "可看"), ("6650", "665000")],
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
                ("云栖苑", C.LIST_C),
                ("active", "可看"),
                ("6650", "665000"),
                ("无障碍", "门宽", "坡道", "卫生间"),
                ("书面", "证明", "待核验", "待现场"),
            ],
            files=("CANDIDATE_TRACKER.md",),
        )
    )


CHECKS = [
    ('s14_fresh_listing_status', s14_fresh_listing_status, 1.25),
    ('s14_final_candidate_refresh', s14_final_candidate_refresh, 1.25),
]
