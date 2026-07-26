from __future__ import annotations
from ._helpers import *


def s5_night_shift_recheck(env) -> bool:
    return (
        stage_route_checked(env, 5, "c", max_minutes=35)
        and stage_calendar_observed(env, 5, [("家人",), ("陪看", "陪同")])
        and stage_record_persisted(
            env,
            5,
            [("家人",), ("陪看",), ("不能替", "本人确认", "授权"), ("35",), ("路线",)],
            files=("AUTH_LOG.md", "CANDIDATE_TRACKER.md"),
        )
    )


def s5_roommate_and_elevator_risk(env) -> bool:
    return (
        stage_ref_checked(env, 5, "listing_platform", "b")
        and stage_ref_checked(env, 5, "listing_platform", "c")
        and stage_review_checked(env, 5, "b", [("电梯", "坡道", "入口")])
        and stage_review_checked(env, 5, "c", [("电梯", "坡道"), ("晚高峰", "维修")])
        and candidate_b_backend_trap(env)
        and candidate_c_backend_viable(env)
        and stage_record_persisted(
            env,
            5,
            [("电梯",), ("门宽",), ("卫生间",), ("坡道",), ("待现场", "核验")],
            files=("RISK_LOG.md", "CANDIDATE_TRACKER.md", "LEASE_CHECKLIST.md"),
        )
    )


CHECKS = [
    ('s5_night_shift_recheck', s5_night_shift_recheck, 1.5),
    ('s5_roommate_and_elevator_risk', s5_roommate_and_elevator_risk, 1.25),
]
