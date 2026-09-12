from __future__ import annotations
from ._helpers import *

def s4_four_shipments_matrix(env) -> bool:
    values = batch_declared_values(env)
    return (
        set(values) == set(BATCH_TRACKING_NUMBERS)
        and all(delivery_status(env, tracking_no) == 'delivered' for tracking_no in BATCH_TRACKING_NUMBERS)
        and tool_used(env, 'delivery_logistics', 'list_shipments', stage=4)
        and batch_matrix_covers_all(env)
    )

def s4_delivery_watch_subscription(env) -> bool:
    return (
        delivery_subscription_exists(env, 'DL-AXG-0720')
        and trace_call_with_terms(env, 4, 'delivery_logistics', ['subscribe_status'], ['DL-AXG-0720'])
    )

CHECKS = [
    ('s4_four_shipments_matrix', s4_four_shipments_matrix, 1.5),
    ('s4_delivery_watch_subscription', s4_delivery_watch_subscription, 1.25),
]
