from ._helpers import *


def s4_places_geocoded(env):
    return (
        (tool_used(env, 'maps', 'geocode', stage=4) or tool_used(env, 'maps', 'search_places', stage=4))
        and maps_place_checked(env, MERCHANT_PLACE)
        and maps_place_checked(env, GATE_PLACE)
    )


def s4_map_baseline_recorded(env):
    return (
        maps_place_checked(env, MERCHANT_PLACE)
        and maps_place_checked(env, GATE_PLACE)
        and doc_value(env, 'maps_crosscheck.json', 'merchant_place_id', MERCHANT_PLACE)
        and doc_value(env, 'maps_crosscheck.json', 'delivery_gate_place_id', GATE_PLACE)
    )


CHECKS = [('s4_places_geocoded', s4_places_geocoded, 1.5), ('s4_map_baseline_recorded', s4_map_baseline_recorded, 1.5)]


def evaluate_stage(env):
    return evaluate(CHECKS, env)
