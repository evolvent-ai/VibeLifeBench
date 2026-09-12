from ._helpers import *


def s13_delivery_refresh_after_mutation(env):
    return (
        delivery_target_tool_used(env, stage=13)
        and delivery_event_has(env, 'auto_completed', timestamp='2026-07-18T18:51:09+08:00')
    )


def s13_auto_event_distinguished(env):
    return (
        delivery_event_has(env, 'auto_completed', timestamp='2026-07-18T18:51:09+08:00')
        and delivery_event_has(env, 'manual_handoff', timestamp='2026-07-18T19:07:42+08:00')
        and record_event_source_has(env, ROUTE_MATRIX, 'events', 'auto_completed', 'delivery_backend', timestamp='2026-07-18T18:51:09+08:00')
        and record_event_source_has(env, ROUTE_MATRIX, 'events', 'manual_handoff', 'delivery_backend', timestamp='2026-07-18T19:07:42+08:00')
    )


CHECKS = [('s13_delivery_refresh_after_mutation', s13_delivery_refresh_after_mutation, 1.5), ('s13_auto_event_distinguished', s13_auto_event_distinguished, 1.75)]


def evaluate_stage(env):
    return evaluate(CHECKS, env)
