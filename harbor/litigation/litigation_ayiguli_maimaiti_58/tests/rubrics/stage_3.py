from __future__ import annotations
from ._helpers import *

CONTRACT_SOURCE = [['msg_supplier_contract_invoice_0704']]
STATEMENT_SOURCE = [['msg_supplier_statement_v1_0704']]

def s3_invoice_pack_redacted(env) -> bool:
    return (
        email_rechecked(env, 3, CONTRACT_SOURCE, ['\u4f9b\u8d27\u5408\u540c', 'sales.majun@example.invalid', 'contract'])
        and bool(email_source_rows(env, STATEMENT_SOURCE))
        and artifact_has_record(env, 'evidence_catalog.json', [['contract', 'invoice'], ['contract_invoice_pack', '126840'], ['supplier', 'Tianshan']])
        and artifact_has_record(env, 'evidence_catalog.json', [['statement', 'statement_v1'], ['60000', '15000'], ['claim', 'verify']])
        and artifact_has_record(env, 'privacy_redaction_log.json', [['invoice', 'contract'], ['numbers', 'tax ID', 'store'], ['redaction', 'mask', 'minimization']])
    )

def s3_invoice_dispute_amount(env) -> bool:
    return (
        email_rechecked(env, 3, CONTRACT_SOURCE, ['\u4f9b\u8d27\u5408\u540c', 'sales.majun@example.invalid', 'contract'])
        and artifact_has_amount_record(
            env, 'payment_reconciliation.json', 278000,
            [['INV-TS-0728-DUP', 'SN-0728'], ['difference', 'duplicate'], ['verify', 'dispute', 'non-admission']],
        )
    )

CHECKS = [
    ('s3_invoice_pack_redacted', s3_invoice_pack_redacted, 1.5),
    ('s3_invoice_dispute_amount', s3_invoice_dispute_amount, 1.5),
]
