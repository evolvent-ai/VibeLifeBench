from __future__ import annotations
from ._helpers import *


def s6_mutation_route_discovered(env) -> bool:
    return (
        stage_map_alert_recovered(env, 6, "a", "evt_a_bus_early")
        and stage_ref_checked(env, 6, "listing_platform", "a")
        and candidate_a_route_risk(env)
    )


def s6_status_propagated(env) -> bool:
    return (
        s6_mutation_route_discovered(env)
        and stage_record_persisted(
            env,
            6,
            [("珞桂家园", C.LIST_A), ("南门",), ("绕行",), ("夜间",), ("路线", "刷新")],
            files=("CANDIDATE_TRACKER.md", "RISK_LOG.md"),
        )
    )


CHECKS = [
    ('s6_mutation_route_discovered', s6_mutation_route_discovered, 1.75),
    ('s6_status_propagated', s6_status_propagated, 1.5),
]
