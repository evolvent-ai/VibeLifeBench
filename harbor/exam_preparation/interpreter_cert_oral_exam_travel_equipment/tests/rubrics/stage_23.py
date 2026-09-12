from __future__ import annotations

from ._helpers import rule_ok

def s23_final_handoff_complete(env) -> bool:
    return rule_ok(env, 's23_final_handoff_complete')

def s23_final_reply_consistent(env) -> bool:
    return rule_ok(env, 's23_final_reply_consistent')

CHECKS = [
    ('s23_final_handoff_complete', s23_final_handoff_complete, 2.0),
    ('s23_final_reply_consistent', s23_final_reply_consistent, 1.25),
]
