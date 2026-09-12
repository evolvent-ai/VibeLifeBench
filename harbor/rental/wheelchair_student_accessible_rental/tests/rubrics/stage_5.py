from __future__ import annotations
from ._helpers import *


def s5_night_shift_recheck(env) -> bool:
    return (
        stage_route_checked(env, 5, "c", max_minutes=35)
        and stage_calendar_observed(env, 5, [("family",), ("family viewing", "accompany")])
        and stage_record_persisted(
            env,
            5,
            [("family",), ("family viewing",), ("cannot replace", "user confirmation", "authorization"), ("35",), ("route",)],
            files=("AUTH_LOG.md", "CANDIDATE_TRACKER.md"),
        )
    )


def s5_roommate_and_elevator_risk(env) -> bool:
    return (
        stage_ref_checked(env, 5, "listing_platform", "b")
        and stage_ref_checked(env, 5, "listing_platform", "c")
        and stage_review_checked(env, 5, "b", [("elevator", "ramp", "entrance")])
        and stage_review_checked(env, 5, "c", [("elevator", "ramp"), ("evening peak", "repair")])
        and candidate_b_backend_trap(env)
        and candidate_c_backend_viable(env)
        and stage_record_persisted(
            env,
            5,
            [("elevator",), ("doorway width",), ("bathroom",), ("ramp",), ("pending on-site verification", "verification")],
            files=("RISK_LOG.md", "CANDIDATE_TRACKER.md", "LEASE_CHECKLIST.md"),
        )
    )


CHECKS = [
    ('s5_night_shift_recheck', s5_night_shift_recheck, 1.5),
    ('s5_roommate_and_elevator_risk', s5_roommate_and_elevator_risk, 1.25),
]
