from __future__ import annotations
from ._helpers import *


def s18_listing_h_released(env) -> bool:
    return listing_h_backend_viable(env) and stage_listing_detail(env, 18, C.LIST_H)


def s18_route_context_released(env) -> bool:
    return (
        listing_h_route_backend_viable(env)
        and tool_stage(env, 18, MAPS, "get_place_details", ["place_h"])
        and tool_stage(env, 18, MAPS, "get_place_details", ["poi_h_market"])
        and tool_stage_parts_any(env, 18, MAPS, None, (["Clearwave Residence", "Mingcheng Road Primary School"], ["place_h", "place_school"]))
        and tool_stage_parts_any(env, 18, MAPS, None, (["Clearwave Residence", "Clearwave Neighborhood Fresh Market"], ["place_h", "poi_h_market"]))
    )


def s18_review_context_released(env) -> bool:
    return review_has(env, "mer_h", ["elevator", "neighborhood fresh market", "vehicle noise"]) and tool_stage(env, 18, REVIEW, "list_reviews", ["mer_h"])


def s18_research_persisted(env) -> bool:
    return (
        stage_notion_any(env, 18, ([C.LIST_H, "school transportation chain", "night noise"], ["Clearwave Residence", "pending on-site verification", "night noise"]))
        and notion_has_any(env, ([C.LIST_H, "pending on-site verification", "school transportation chain", "night noise"], ["Clearwave Residence", "75", "15", "on-site verification"]))
    )


CHECKS = [
    ("s18_listing_h_released", s18_listing_h_released, 0.40),
    ("s18_route_context_released", s18_route_context_released, 0.30),
    ("s18_review_context_released", s18_review_context_released, 0.20),
    ("s18_research_persisted", s18_research_persisted, 0.35),
]
