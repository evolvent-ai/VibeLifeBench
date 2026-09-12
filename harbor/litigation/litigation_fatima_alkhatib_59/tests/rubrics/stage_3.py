from __future__ import annotations
from ._helpers import *

def s3_initial_delivery_logged(env) -> bool:
    try:
        return initial_delivery_logged(env)
    except EvidenceError:
        raise
    except Exception:
        return False

def s3_delivery_privacy_redacted(env) -> bool:
    try:
        return delivery_privacy_guarded(env)
    except EvidenceError:
        raise
    except Exception:
        return False

CHECKS = [
    ('s3_initial_delivery_logged', s3_initial_delivery_logged, 1.5),
    ('s3_delivery_privacy_redacted', s3_delivery_privacy_redacted, 1.25),
]
