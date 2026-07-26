from __future__ import annotations
from ._helpers import *


def s1_search_and_save_candidates(env) -> bool:
    return (
        stage_listing_search(env, 1)
        and saved_by_user(env, C.LIST_C)
        and any(stage_saved_listing(env, stage, C.LIST_C) for stage in (0, 1))
        and stage_saved_any_listing_by_user(env, 1)
        and candidate_c_backend_viable(env)
        and stage_record_persisted(
            env,
            1,
            [("云栖苑", C.LIST_C), ("6650", "665000"), ("无障碍", "门宽", "坡道")],
            files=("CANDIDATE_TRACKER.md", "BUDGET_LEDGER.md"),
        )
    )


def s1_subscribe_listing_watch(env) -> bool:
    return (
        s1_search_and_save_candidates(env)
        and any(notification_tool(env, stage, require_write=True) for stage in (0, 1))
        and stage_record_persisted(
            env,
            1,
            [("复核", "监控", "提醒"), ("状态",), ("价格",), ("路线",), ("无障碍",)],
            files=("HEARTBEAT.md", "CANDIDATE_TRACKER.md"),
        )
    )


CHECKS = [
    ('s1_search_and_save_candidates', s1_search_and_save_candidates, 1.5),
    ('s1_subscribe_listing_watch', s1_subscribe_listing_watch, 1.25),
]
