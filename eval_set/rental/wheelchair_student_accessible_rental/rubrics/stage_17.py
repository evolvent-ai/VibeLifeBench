from __future__ import annotations
from ._helpers import *


def s17_alternative_candidate_pool(env) -> bool:
    return (
        stage_listing_search(env, 17)
        and stage_route_checked(env, 17, "c", max_minutes=35)
        and stage_record_persisted(
            env,
            17,
            [("备选", "相似候选"), ("6800", "预算"), ("无障碍",), ("一居", "主卧"), ("云栖苑", C.LIST_C)],
            files=("CANDIDATE_TRACKER.md",),
        )
    )


def s17_calendar_window_draft_only(env) -> bool:
    return (
        s17_alternative_candidate_pool(env)
        and stage_calendar_persisted(
            env,
            17,
            [("云栖苑", "看房"), ("待本人确认", "待确认"), ("家人", "陪看"), ("内部", "窗口")],
        )
        and stage_record_persisted(
            env,
            17,
            [("看房",), ("家人",), ("窗口",), ("待确认", "本人确认"), ("不预约", "内部")],
            files=("AUTH_LOG.md", "CANDIDATE_TRACKER.md"),
        )
        and len(viewings(env)) == 0
    )


CHECKS = [
    ('s17_alternative_candidate_pool', s17_alternative_candidate_pool, 1.25),
    ('s17_calendar_window_draft_only', s17_calendar_window_draft_only, 1.5),
]
