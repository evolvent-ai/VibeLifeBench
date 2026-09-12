from __future__ import annotations
from ._helpers import *

def s11_delivery_mutation_detected(env) -> bool:
    return (
        delivery_status(env, 'DL-AXG-0720') == 'exception'
        and trace_call_with_terms(env, 11, 'delivery_logistics', ['track_package'], ['DL-AXG-0720'])
        and batch_matrix_has_tracking(
            env, 'DL-AXG-0720',
            groups=[['exception', 'anomaly'], ['22', '24'], ['Nurgul', 'owner', 'mismatch']],
        )
    )

def s11_delivery_issue_created(env) -> bool:
    return (
        delivery_status(env, 'DL-AXG-0720') == 'exception'
        and delivery_issue_exists(env, 'DL-AXG-0720', 'missing_item')
        and trace_call_with_terms(env, 11, 'delivery_logistics', ['report_issue'], ['DL-AXG-0720'])
    )

CHECKS = [
    ('s11_delivery_mutation_detected', s11_delivery_mutation_detected, 2.0),
    ('s11_delivery_issue_created', s11_delivery_issue_created, 1.75),
]
