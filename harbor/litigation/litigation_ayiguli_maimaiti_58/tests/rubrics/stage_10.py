from __future__ import annotations
from ._helpers import *

LAB_INITIAL_SOURCE = [['msg_lab_initial_0716']]

def s10_lab_initial_indexed(env) -> bool:
    return (
        email_rechecked(env, 10, LAB_INITIAL_SOURCE, ['NT-0712', 'lab@kunlun-qc.example', 'initial'])
        and artifact_has_record(
            env, 'evidence_catalog.json',
            [['kunlun', 'initial'], ['NT-0712'], ['lab_nt_0712_initial', 'nut'], ['scope', 'sample', 'conclusions']],
        )
        and artifact_has_record(env, 'privacy_redaction_log.json', [['inspection', 'inspected'], ['telephone', 'batch', 'signature'], ['redaction', 'mask', 'minimization']])
    )

def s10_nut_batch_loss(env) -> bool:
    expected = delivery_declared_value(env, 'DL-AXG-0712')
    return (
        expected is not None
        and email_rechecked(env, 10, LAB_INITIAL_SOURCE, ['NT-0712', 'lab@kunlun-qc.example', 'initial'])
        and artifact_has_amount_record(
            env, 'batch_quality_matrix.json', expected,
            [['DL-AXG-0712'], ['NT-0712'], ['damage', 'sale'], ['discard', 'replace', 'loss'], ['inspection', 'kunlun']],
        )
    )

CHECKS = [
    ('s10_lab_initial_indexed', s10_lab_initial_indexed, 1.5),
    ('s10_nut_batch_loss', s10_nut_batch_loss, 1.75),
]
