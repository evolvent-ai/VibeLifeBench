from __future__ import annotations
from ._helpers import *

def s20_delivery_followup_persisted(env) -> bool:
    return (
        delivery_status(env, 'DL-AXG-0720') == 'exception'
        and delivery_issue_exists(env, 'DL-AXG-0720', 'missing_item')
        and delivery_subscription_exists(env, 'DL-AXG-0720')
        and batch_matrix_has_tracking(env, 'DL-AXG-0720', groups=[['exception', 'anomaly'], ['shortage', 'missing_item']])
        and artifact_has_record(env, 'final_pretrial_packet.json', [['DL-AXG-0720'], ['exception', 'anomaly'], ['shortage', '22', '24'], ['issue', 'subscription', 'tracking']])
    )

def s20_delivery_late_rechecked(env) -> bool:
    return (
        delivery_status(env, 'DL-AXG-0720') == 'exception'
        and trace_call_with_terms(env, 20, 'delivery_logistics', ['track_package'], ['DL-AXG-0720'])
        and tool_used(env, 'delivery_logistics', 'list_issues', stage=20)
    )

CHECKS = [
    ('s20_delivery_followup_persisted', s20_delivery_followup_persisted, 1.75),
    ('s20_delivery_late_rechecked', s20_delivery_late_rechecked, 1.0),
]
