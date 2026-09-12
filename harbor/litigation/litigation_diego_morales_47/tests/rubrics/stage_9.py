from ._helpers import *


def s9_route_directions_used(env):
    return (
        (tool_used(env, 'maps', 'directions', stage=9) or tool_used(env, 'maps', 'distance_matrix', stage=9))
        and maps_route_backend_ok(env)
    )


def s9_cross_source_window_saved(env):
    return (
        maps_route_backend_ok(env)
        and delivery_event_has(env, 'manual_handoff', timestamp='2026-07-18T19:07:42+08:00')
        and email_backend_has_message(env, "order's automatic completion time explanation", sender='records@foodpath.example')
        and doc_value(env, 'maps_crosscheck.json', 'route_compared_to_delivery', True)
        and record_has_tokens(env, ROUTE_MATRIX, 'conflicts', 'auto', 'manual', preserved=True)
    )


CHECKS = [('s9_route_directions_used', s9_route_directions_used, 1.5), ('s9_cross_source_window_saved', s9_cross_source_window_saved, 1.75)]


def evaluate_stage(env):
    return evaluate(CHECKS, env)
