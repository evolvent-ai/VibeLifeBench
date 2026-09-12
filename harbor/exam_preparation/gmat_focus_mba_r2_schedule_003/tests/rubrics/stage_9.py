from __future__ import annotations
from . import _helpers as H

def s9_shanghai_cancel_discovered(env) -> bool:
    return H.s9_shanghai_cancel_discovered(env)

def s9_hk_or_sg_candidate_retained(env) -> bool:
    return H.s9_hk_or_sg_candidate_retained(env)

CHECKS = [
    ("s9_shanghai_cancel_discovered", s9_shanghai_cancel_discovered, 1.75),
    ("s9_hk_or_sg_candidate_retained", s9_hk_or_sg_candidate_retained, 1.5)
]
