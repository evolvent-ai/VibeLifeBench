from ._helpers import *


def s3_delivery_trace_loaded(env):
    return (
        delivery_target_tool_used(env, stage=3)
        and delivery_target_identity_matches(env)
        and delivery_event_has(env, 'manual_handoff', timestamp='2026-07-18T19:07:42+08:00')
    )


def s3_matrix_has_core_events(env):
    return (
        delivery_event_has(env, 'picked_up', timestamp='2026-07-18T18:24:36+08:00')
        and delivery_event_has(env, 'manual_handoff', timestamp='2026-07-18T19:07:42+08:00')
        and record_event_source_has(env, ROUTE_MATRIX, 'events', 'picked_up', 'delivery_backend', timestamp='2026-07-18T18:24:36+08:00')
        and record_event_source_has(env, ROUTE_MATRIX, 'events', 'manual_handoff', 'delivery_backend', timestamp='2026-07-18T19:07:42+08:00')
    )


CHECKS = [('s3_delivery_trace_loaded', s3_delivery_trace_loaded, 1.5), ('s3_matrix_has_core_events', s3_matrix_has_core_events, 1.5)]


def evaluate_stage(env):
    return evaluate(CHECKS, env)
