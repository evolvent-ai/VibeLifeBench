from __future__ import annotations
from ._helpers import *

def s2_product_sku_batch_identified(env) -> bool:
    try:
        return product_sku_batch_identified(env)
    except EvidenceError:
        raise
    except Exception:
        return False

def s2_claim_order_indexed(env) -> bool:
    try:
        return claim_order_indexed(env)
    except EvidenceError:
        raise
    except Exception:
        return False

CHECKS = [
    ('s2_product_sku_batch_identified', s2_product_sku_batch_identified, 1.5),
    ('s2_claim_order_indexed', s2_claim_order_indexed, 1.5),
]
