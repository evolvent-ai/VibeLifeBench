from __future__ import annotations
from . import _helpers as H

def s20_send_candidates_pending_only(env) -> bool:
    return H.s20_send_candidates_pending_only(env)

def s20_no_application_submission(env) -> bool:
    return H.s20_no_application_submission(env)

CHECKS = [
    ("s20_send_candidates_pending_only", s20_send_candidates_pending_only, 1.5),
    ("s20_no_application_submission", s20_no_application_submission, 2.0)
]
