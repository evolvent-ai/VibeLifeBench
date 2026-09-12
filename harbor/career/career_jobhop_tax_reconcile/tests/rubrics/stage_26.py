from . import _helpers as H


def final_records_are_backend_traceable(env):
    text = H.corpus(env)
    return {"email", "banking", "job_board", "legal_search"} <= H.backend_trace_domains(env, text) and H.has_terms(text, (H.REFUND_TX_ID,), (H.CORRECTION_RECEIPT_TOKEN,), ("evidence", "source_id", "evidence"))


CHECKS = [("tax_s26_final_records_are_backend_traceable", final_records_are_backend_traceable, 2.0)]
