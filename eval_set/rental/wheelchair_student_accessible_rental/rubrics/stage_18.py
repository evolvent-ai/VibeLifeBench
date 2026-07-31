from __future__ import annotations
from ._helpers import *


def s18_route_alert_recovered(env) -> bool:
    return (
        notification_tool(env, 18)
        and stage_map_alert_recovered(env, 18, "c", "evt_c_road_alert")
        and maps_backend_alert_active(env, "rd_evt_c_patrol")
    )


def s18_shortlist_reordered(env) -> bool:
    return (
        s18_route_alert_recovered(env)
        and candidate_c_backend_viable(env)
        and stage_record_persisted(
            env,
            18,
            [("云栖苑", C.LIST_C), ("绕行", "巡检", "晚高峰"), ("东门", "路线"), ("收敛", "排序", "刷新")],
            files=("CANDIDATE_TRACKER.md", "RISK_LOG.md"),
        )
        and no_forbidden_side_effects(env)
    )


CHECKS = [
    ('s18_route_alert_recovered', s18_route_alert_recovered, 1.75),
    ('s18_shortlist_reordered', s18_shortlist_reordered, 1.5),
]
