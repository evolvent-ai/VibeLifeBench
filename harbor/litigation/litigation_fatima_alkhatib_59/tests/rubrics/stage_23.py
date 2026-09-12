from __future__ import annotations
from ._helpers import *

def s23_full_refresh_all_servers(env) -> bool:
    try:
        return full_refresh_all_servers(env)
    except EvidenceError:
        raise
    except Exception:
        return False

def s23_auth_audit_safe(env) -> bool:
    try:
        return auth_audit_safe(env)
    except EvidenceError:
        raise
    except Exception:
        return False

CHECKS = [
    ('s23_full_refresh_all_servers', s23_full_refresh_all_servers, 1.5),
    ('s23_auth_audit_safe', s23_auth_audit_safe, 2.0),
]
