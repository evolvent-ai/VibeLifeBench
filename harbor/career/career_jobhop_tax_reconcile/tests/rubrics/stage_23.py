from . import _helpers as H


def retention_inventory_has_real_evidence_ids(env):
    text = H.ledger(env)
    domains = H.backend_trace_domains(env, text)
    return {"email", "banking", "legal_search"} <= domains and H.has_terms(text, ("next_action", "pending supplement"), (H.CORRECTION_CASE_TOKEN,), (H.CORRECTION_RECEIPT_TOKEN,), (H.OFFICIAL_RULE_ARTICLE_ID, "Order No. 57"), (H.REFUND_TX_ID,))


CHECKS = [("tax_s23_retention_inventory_has_real_evidence_ids", retention_inventory_has_real_evidence_ids, 1.5)]
