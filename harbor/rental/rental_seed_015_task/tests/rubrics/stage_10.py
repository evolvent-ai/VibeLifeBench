from __future__ import annotations
from ._helpers import *


def s10_school_route_mutation_rechecked(env) -> bool:
    return (
        tool_stage_parts_any(env, 10, MAPS, None, (["place_b"], ["Mingcheng Court"]))
        and tool_stage(env, 10, NOTICE, None, ["ntf_route_b_traffic"])
        and b_detour_backend_ready(env)
        and notification_has(env, "ntf_route_b_traffic", ["school-area rush-hour change", "one-way restriction"])
        and stage_notion_any(env, 10, ([C.LIST_B, "83", "detour"], ["Mingcheng Court", "Jiangdong South Road detour transfer point", "one-way restriction"]))
        and notion_has_any(env, ([C.LIST_B, "83", "detour"], ["Mingcheng Court", "Jiangdong South Road detour transfer point", "83"]))
    )


CHECKS = [("s10_school_route_mutation_rechecked", s10_school_route_mutation_rechecked, 1.75)]
