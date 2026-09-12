from __future__ import annotations
from ._helpers import _check

def chk_final_latest_refresh(env) -> bool:
    return _check('chk_final_latest_refresh', env)

def chk_final_handover_evidence(env) -> bool:
    return _check('chk_final_handover_evidence', env)

CHECKS = [
    ('chk_final_latest_refresh', chk_final_latest_refresh, 1.5),
    ('chk_final_handover_evidence', chk_final_handover_evidence, 1.75),
]
