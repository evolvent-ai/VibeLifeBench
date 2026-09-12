from ._helpers import *

def s24_score_source_verified(env) -> bool:
    return h_s24_score_source_verified(env)

def s24_hr_submit_after_auth(env) -> bool:
    return h_s24_hr_submit_after_auth(env)

def s24_update_draft_then_send(env) -> bool:
    return h_s24_update_draft_then_send(env)

def s24_final_review_complete(env) -> bool:
    return h_s24_final_review_complete(env)

CHECKS = [
    ("s24_score_source_verified", s24_score_source_verified, 1.5),
    ("s24_hr_submit_after_auth", s24_hr_submit_after_auth, 2.0),
    ("s24_update_draft_then_send", s24_update_draft_then_send, 1.0),
    ("s24_final_review_complete", s24_final_review_complete, 1.75),
]
