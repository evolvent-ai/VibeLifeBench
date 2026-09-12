from ._helpers import evaluate

def s16_approval_state_sync(env) -> bool:
    return evaluate(env, "s16_approval_state_sync")

def s16_no_final_notice_yet(env) -> bool:
    return evaluate(env, "s16_no_final_notice_yet")

CHECKS = [
    ("s16_approval_state_sync", s16_approval_state_sync, 1.0),
    ("s16_no_final_notice_yet", s16_no_final_notice_yet, 1.0),
]
