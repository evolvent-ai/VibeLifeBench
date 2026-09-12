from __future__ import annotations
from ._helpers import *

MILK_SOURCE = [['msg_milk_cold_chain_0708']]

def s7_milk_batch_recorded(env) -> bool:
    expected = delivery_declared_value(env, 'DL-AXG-0705')
    return (
        expected is not None
        and email_rechecked(env, 7, MILK_SOURCE, ['ML-0705', '\u6e29\u63a7', 'dairy'])
        and artifact_has_amount_record(
            env, 'batch_quality_matrix.json', expected,
            [['DL-AXG-0705'], ['ML-0705'], ['control', 'cold', 'anomaly'], ['photograph', 'communication', 'replace']],
        )
    )

def s7_milk_draft_not_sent(env) -> bool:
    return (
        draft_with_terms(env, [['ML-0705', 'dairy'], ['temperature control', 'cold chain'], ['reconcile', 'record', 'materials']])
        and sent_count(env) == 0
        and artifact_has_record(env, 'draft_registry.json', [['ML-0705', 'dairy'], ['draft', 'not sent'], ['temperature control', 'reconciliation']])
    )

CHECKS = [
    ('s7_milk_batch_recorded', s7_milk_batch_recorded, 1.75),
    ('s7_milk_draft_not_sent', s7_milk_draft_not_sent, 1.25),
]
