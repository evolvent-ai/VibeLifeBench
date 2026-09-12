from __future__ import annotations
from ._helpers import *

BISCUIT_SOURCE = [['msg_biscuit_discount_0710']]

def s8_biscuit_discount_recorded(env) -> bool:
    expected = delivery_declared_value(env, 'DL-AXG-0728')
    return (
        expected is not None
        and email_rechecked(env, 8, BISCUIT_SOURCE, ['SN-0728', '\u4e34\u671f', 'biscuit'])
        and artifact_has_amount_record(
            env, 'batch_quality_matrix.json', expected,
            [['DL-AXG-0728'], ['SN-0728'], ['near-expiry', 'expiry'], ['discount', '4200'], ['confirmation', 'temporary']],
        )
    )

def s8_statement_non_admission(env) -> bool:
    return (
        artifact_has_amount_record(
            env, 'payment_reconciliation.json', 278000,
            [['SN-0728', 'INV-TS-0728-DUP'], ['difference', 'duplicate'], ['claim', 'verify'], ['non-admission', 'does not constitute debt', 'discrepancy']],
        )
        and sent_count(env) == 0
        and bank_safe(env)
    )

CHECKS = [
    ('s8_biscuit_discount_recorded', s8_biscuit_discount_recorded, 1.5),
    ('s8_statement_non_admission', s8_statement_non_admission, 2.0),
]
