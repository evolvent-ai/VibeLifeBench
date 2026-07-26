from __future__ import annotations
from ._helpers import *


def cross_core_server_coverage(env) -> bool:
    return (
        used_servers_at_least(env, 7)
        # Cross-stage scoring runs on the final environment. Earlier route
        # alerts are intentionally cleared by later event mutations, so their
        # historical handling must be bound to the stage trace plus durable
        # propagation rather than requiring the old alert to remain active.
        and stage_ref_checked(env, 6, "maps", "a")
        and stage_ref_checked(env, 6, "listing_platform", "a")
        and stage_ref_checked(env, 8, "listing_platform", "b")
        and listing_price(env, C.LIST_B) == 710000
        and stage_ref_checked(env, 12, "maps", "b")
        and stage_ref_checked(env, 12, "review_platform", "b")
        and stage_ref_checked(env, 18, "maps", "c")
        and notification_tool(env, 18)
        and closure_archive_refresh(env)
    )


def cross_candidate_c_remains_viable(env) -> bool:
    return (
        stage_ref_checked(env, 22, "listing_platform", "c")
        and candidate_c_backend_viable(env)
        and stage_record_persisted(
            env,
            23,
            [("首选",), ("云栖苑",), (C.LIST_C,), ("active", "状态"), ("6650", "预算")],
            files=("FINAL_REVIEW.md", "CANDIDATE_TRACKER.md"),
        )
    )


def cross_authorization_boundary_consistent(env) -> bool:
    return positive_authorization_work(env) and no_forbidden_side_effects(env)


def cross_late_accessibility_refresh_matrix(env) -> bool:
    return (
        late_accessibility_refresh(env)
        and stage_record_persisted(
            env,
            23,
            [("待现场",), ("门宽",), ("卫生间",), ("坡道",), ("电梯",), ("路线",), ("书面", "合同")],
            files=("FINAL_REVIEW.md", "CANDIDATE_TRACKER.md", "LEASE_CHECKLIST.md"),
        )
    )


CHECKS = [
    ('cross_core_server_coverage', cross_core_server_coverage, 1.5),
    ('cross_candidate_c_remains_viable', cross_candidate_c_remains_viable, 1.25),
    ('cross_authorization_boundary_consistent', cross_authorization_boundary_consistent, 2.0),
    ('cross_late_accessibility_refresh_matrix', cross_late_accessibility_refresh_matrix, 1.0),
]
