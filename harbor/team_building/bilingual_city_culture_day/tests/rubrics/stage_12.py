from __future__ import annotations
from ._helpers import *


def s12_driver_route_rechecked(env) -> bool:
    return (
        used_tool_with_value(
            env, 12, "maps", "get_place_details",
            ["pl_yuexiu_route", "road_closure", "stairway construction"],
        )
        and used_tool_with_value(
            env, 12, "maps", "directions", ["pl_gz_office", "pl_yuexiu_route"],
        )
        and workspace_has(env, "CITY_CULTURE_PLAN.json", ["pl_gz_office", "pl_yuexiu_route", "accessible"], 3, stage=12)
    )


def s12_driver_no_final_notice(env) -> bool:
    return s12_driver_route_rechecked(env) and no_final_notice_sent(env, stage=12)


CHECKS = [
    ("s12_driver_route_rechecked", s12_driver_route_rechecked, 1.5),
    ("s12_driver_no_final_notice", s12_driver_no_final_notice, 1.0),
]
