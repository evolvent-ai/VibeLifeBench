from ._helpers import *


def s18_road_event_rechecked(env):
    return (
        (maps_route_tool_used(env, stage=18) or maps_stage_tool_used(env, 18))
        and maps_road_event_active(env)
    )


def s18_map_not_overclaimed(env):
    return (
        maps_road_event_active(env)
        and doc_value(env, 'maps_crosscheck.json', 'map_does_not_replace_delivery', True)
        and doc_value(env, 'witness_statement_template.json', 'no_route_overclaim', True)
    )


CHECKS = [('s18_road_event_rechecked', s18_road_event_rechecked, 1.75), ('s18_map_not_overclaimed', s18_map_not_overclaimed, 1.5)]


def evaluate_stage(env):
    return evaluate(CHECKS, env)
