from __future__ import annotations
from ._helpers import *


def s18_route_alert_recovered(env) -> bool:
    return (
        notification_tool(env, 18, ("route",))
        and maps_backend_alert_active(env, "evt_c_road_alert")
        and maps_backend_alert_active(env, "rd_evt_c_patrol")
        and tool_stage(env, 18, "maps", "directions", (C.PLACE_C, C.DESTINATION))
        and maps_route_available(env, C.PLACE_C, C.DESTINATION)
        and listing_within_budget(env, C.LIST_C)
    )


def s18_shortlist_reordered(env) -> bool:
    return (
        s18_route_alert_recovered(env)
        and stage_record_persisted(
            env,
            18,
            [
                (C.LIST_C_NAME, C.LIST_C),
                ("东门",),
                ("2026-08-08",),
                ("2026-08-09",),
                ("绕行",),
                ("搬家车辆", "限时进入"),
                ("路线",),
                ("刷新", "排序"),
            ],
            files=("CANDIDATE_TRACKER.md", "RISK_LOG.md"),
        )
        and no_payment_or_contract_side_effect(env)
    )


CHECKS = [
    ("s18_route_alert_recovered", s18_route_alert_recovered, 1.75),
    ("s18_shortlist_reordered", s18_shortlist_reordered, 1.5),
]
