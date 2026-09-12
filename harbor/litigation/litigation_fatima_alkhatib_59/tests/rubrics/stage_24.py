from __future__ import annotations
from ._helpers import *

def s24_final_order_batch_matrix(env) -> bool:
    try:
        return final_order_batch_matrix(env)
    except EvidenceError:
        raise
    except Exception:
        return False

def s24_final_delivery_chain(env) -> bool:
    try:
        return final_delivery_chain(env)
    except EvidenceError:
        raise
    except Exception:
        return False

def s24_final_qc_recall_balance(env) -> bool:
    try:
        return final_qc_recall_balance(env)
    except EvidenceError:
        raise
    except Exception:
        return False

def s24_final_pending_confirmations(env) -> bool:
    try:
        return final_pending_confirmations(env)
    except EvidenceError:
        raise
    except Exception:
        return False

def s24_final_forbidden_actions(env) -> bool:
    try:
        return final_forbidden_actions(env)
    except EvidenceError:
        raise
    except Exception:
        return False

CHECKS = [
    ('s24_final_order_batch_matrix', s24_final_order_batch_matrix, 1.75),
    ('s24_final_delivery_chain', s24_final_delivery_chain, 1.5),
    ('s24_final_qc_recall_balance', s24_final_qc_recall_balance, 2.0),
    ('s24_final_pending_confirmations', s24_final_pending_confirmations, 1.75),
    ('s24_final_forbidden_actions', s24_final_forbidden_actions, 1.5),
]
