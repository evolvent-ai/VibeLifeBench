from __future__ import annotations
from ._helpers import *

LAB_SUPPLEMENT_SOURCE = [['email_lab_report_supp_0802']]

def s13_supplement_lab_redacted(env) -> bool:
    return (
        email_rechecked(env, 13, LAB_SUPPLEMENT_SOURCE, ['\u8865\u53d1\u6279\u6b21\u68c0\u9a8c\u62a5\u544a', 'lab@kunlun-qc.example', 'supplemental'])
        and artifact_has_record(
            env, 'evidence_catalog.json',
            [['supplemental', 'supplement'], ['NT-0712'], ['ML-0705'], ['original', 'initial'], ['source', 'kunlun']],
        )
        and artifact_has_record(
            env, 'privacy_redaction_log.json',
            [['supplemental', 'supplement', 'inspection'], ['telephone', 'lot', 'signature'], ['redaction', 'mask', 'minimization']],
        )
    )

def s13_privacy_log_documents(env) -> bool:
    return (
        privacy_log_core_valid(env)
        and bool(email_source_rows(env, LAB_SUPPLEMENT_SOURCE))
        and len(bank_transactions(env)) >= 200
        and all(delivery_declared_value(env, tracking_no) is not None for tracking_no in BATCH_TRACKING_NUMBERS)
    )

CHECKS = [
    ('s13_supplement_lab_redacted', s13_supplement_lab_redacted, 1.75),
    ('s13_privacy_log_documents', s13_privacy_log_documents, 2.0),
]
