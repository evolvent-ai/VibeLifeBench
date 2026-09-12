from __future__ import annotations
from ._helpers import *


def s5_route_checked(env) -> bool:
    return (
        used_tool_with_value(env, 5, "maps", "directions", ["pl_gz_office", "pl_yuexiu_route"])
        and used_tool_with_value(env, 5, "calendar", "update_event", ["evt_culture_day_hold"])
        and calendar_event_has(env, "city culture event", "2026-07-21", stage=5)
        and workspace_has(env, "CITY_CULTURE_PLAN.json", ["pl_gz_office", "pl_yuexiu_route", "low-intensity", "accessible"], 3, stage=5)
    )


CHECKS = [("s5_route_checked", s5_route_checked, 1.5)]
