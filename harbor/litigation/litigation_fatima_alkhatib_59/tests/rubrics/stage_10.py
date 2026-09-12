from __future__ import annotations
from ._helpers import *

def s10_return_shipment_tracked(env) -> bool:
    try:
        return return_shipment_tracked(env)
    except EvidenceError:
        raise
    except Exception:
        return False

def s10_return_issue_or_subscription(env) -> bool:
    try:
        return return_issue_or_subscription(env)
    except EvidenceError:
        raise
    except Exception:
        return False

CHECKS = [
    ('s10_return_shipment_tracked', s10_return_shipment_tracked, 1.5),
    ('s10_return_issue_or_subscription', s10_return_issue_or_subscription, 1.5),
]
