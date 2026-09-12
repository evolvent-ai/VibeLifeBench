from __future__ import annotations
from ._helpers import *

def s17_return_sample_damage_logged(env) -> bool:
    try:
        return return_sample_damage_logged(env)
    except EvidenceError:
        raise
    except Exception:
        return False

CHECKS = [
    ('s17_return_sample_damage_logged', s17_return_sample_damage_logged, 1.5),
]
