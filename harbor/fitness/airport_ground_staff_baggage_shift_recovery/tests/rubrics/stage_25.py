from __future__ import annotations
from ._helpers import evaluate

def chk_final_test_safe_protocol(env) -> bool:
    return evaluate('chk_final_test_safe_protocol', env)

CHECKS = [
    ('chk_final_test_safe_protocol', chk_final_test_safe_protocol, 2.0),
]
