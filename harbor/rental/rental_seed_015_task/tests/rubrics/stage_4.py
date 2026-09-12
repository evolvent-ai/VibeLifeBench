from __future__ import annotations
from ._helpers import *


def s4_morning_chain_segments(env) -> bool:
    return (
        stage_ok(env, 4, "s4")
        and initial_route_matrix_backend_ready(env)
        and notion_has_any(
            env,
            (
                ["Clear Bay Garden", "Mingcheng Court", "Yunanli", "South Creek Garden", "8 minutes", "75"],
                [C.LIST_A, C.LIST_B, C.LIST_D, C.LIST_E, "school drop-off stop", "school-to-office"],
            ),
        )
    )


def s4_supermarket_walk_verified(env) -> bool:
    return (
        stage_ok(env, 4, "s4")
        and tool_stage_parts_any(env, 4, MAPS, None, (["walking"], ["walking"]))
        and tool_stage_results_cover(env, 4, MAPS, "search_places", ["poi_chengwan_fresh", "poi_yunanli_fresh", "poi_nanxiyuan_market"])
        and supermarket_walk_backend_ready(env)
        and notion_has_any(env, (["Clear Bay Fresh Select", "Yunanli Community Market", "South Creek Neighborhood Market", "15"], ["fresh-food", "walking", "entrance", "minutes"]))
    )


CHECKS = [
    ("s4_morning_chain_segments", s4_morning_chain_segments, 1.75),
    ("s4_supermarket_walk_verified", s4_supermarket_walk_verified, 1.5),
]
