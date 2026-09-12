from __future__ import annotations
from ._helpers import *

def s1_all_required_servers_touched(env) -> bool:
    try:
        return all_required_servers_touched(env, stage=1)
    except EvidenceError:
        raise
    except Exception:
        return False

def s1_object_index_created(env) -> bool:
    try:
        return object_index_created(env)
    except EvidenceError:
        raise
    except Exception:
        return False

CHECKS = [
    ('s1_all_required_servers_touched', s1_all_required_servers_touched, 1.5),
    ('s1_object_index_created', s1_object_index_created, 1.25),
]
