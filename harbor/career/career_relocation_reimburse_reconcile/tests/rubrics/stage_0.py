from __future__ import annotations
from ._helpers import derived_text, text_has, used_tool

def s0_dual_track_tracker(env) -> bool:
    corpus = derived_text(env)
    if not corpus.strip():
        return False
    severance = text_has(corpus, [['compensation-alternative-5', 'shortfall alternative 68f126c', 'relocation-reimbursement-shortfall-alternative-6', 'severance']])
    reemploy = text_has(corpus, [['reemployment', 'job-search', 'application', 'interview', 'role', 'offer-alternative-7']])
    return severance and reemploy
CHECKS = [('s0_dual_track_tracker', s0_dual_track_tracker, 3.0)]
