from __future__ import annotations
from ._helpers import *

def s5_product_instruction_logged(env) -> bool:
    try:
        return product_instruction_logged(env)
    except EvidenceError:
        raise
    except Exception:
        return False

def s5_after_sales_thread_indexed(env) -> bool:
    try:
        return after_sales_thread_indexed(env)
    except EvidenceError:
        raise
    except Exception:
        return False

def s5_misuse_candidate_cross_checked(env) -> bool:
    try:
        return misuse_candidate_cross_checked(env)
    except EvidenceError:
        raise
    except Exception:
        return False

CHECKS = [
    ('s5_product_instruction_logged', s5_product_instruction_logged, 1.75),
    ('s5_after_sales_thread_indexed', s5_after_sales_thread_indexed, 1.5),
    ('s5_misuse_candidate_cross_checked', s5_misuse_candidate_cross_checked, 1.5),
]
