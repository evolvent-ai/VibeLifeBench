from __future__ import annotations
from ._helpers import *

def s5_route_checked(env) -> bool:
    route = used_tool_with_value(env, 5, "maps", "directions", ["pl_sh_office", "pl_jx_factory"])
    return route and used_tool_with_value(env, 5, "calendar", "update_event", ["evt_factory_hold"]) and calendar_event_has(env, "evt_factory_hold", ["上海", "嘉兴"])

CHECKS = [("s5_route_checked", s5_route_checked, 1.5)]
