from __future__ import annotations
from ._helpers import *


def s6_mutation_route_discovered(env) -> bool:
    return (
        maps_backend_alert_active(env, "evt_a_bus_early")
        and tool_stage(env, 6, "maps", "directions", (C.PLACE_A, C.DESTINATION))
        and tool_stage(env, 6, "listing_platform", None, (C.LIST_A,))
        and maps_route_available(env, C.PLACE_A, C.DESTINATION)
        and "reroute" in str(listing_attrs(env, C.LIST_A).get("night_access") or "").casefold()
    )


def s6_status_propagated(env) -> bool:
    return (
        s6_mutation_route_discovered(env)
        and stage_record_persisted(
            env,
            6,
            [
                ("北岸花园", C.LIST_A),
                ("接驳", "末班"),
                ("南门",),
                ("夜间",),
                ("路线", "通勤"),
                ("刷新", "更新"),
            ],
            files=("CANDIDATE_TRACKER.md", "RISK_LOG.md"),
        )
    )


CHECKS = [
    ("s6_mutation_route_discovered", s6_mutation_route_discovered, 1.75),
    ("s6_status_propagated", s6_status_propagated, 1.5),
]
