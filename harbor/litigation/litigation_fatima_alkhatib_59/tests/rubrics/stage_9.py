from __future__ import annotations
from ._helpers import *

def s9_same_batch_orders_counted(env) -> bool:
    try:
        return same_batch_orders_counted(env)
    except EvidenceError:
        raise
    except Exception:
        return False

CHECKS = [
    ('s9_same_batch_orders_counted', s9_same_batch_orders_counted, 1.75),
]
