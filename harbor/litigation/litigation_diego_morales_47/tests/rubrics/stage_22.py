from ._helpers import *


def s22_backend_review_reconciled(env):
    return (
        delivery_target_tool_used(env, stage=22)
        and delivery_event_has(env, 'backend_review', timestamp='2026-08-27T10:00:00+08:00')
        and record_event_source_has(env, ROUTE_MATRIX, 'events', 'backend_review', 'delivery_backend')
    )


CHECKS = [('s22_backend_review_reconciled', s22_backend_review_reconciled, 1.75)]


def evaluate_stage(env):
    return evaluate(CHECKS, env)
