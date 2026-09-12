from __future__ import annotations
from ._helpers import *

def s20_sample_issue_followed(env) -> bool:
    try:
        return sample_issue_followed(env)
    except EvidenceError:
        raise
    except Exception:
        return False

CHECKS = [
    ('s20_sample_issue_followed', s20_sample_issue_followed, 1.5),
]
