from ._helpers import *

def s17_mock_adjustment_done(env) -> bool:
    return h_s17_mock_adjustment_done(env)

CHECKS = [
    ("s17_mock_adjustment_done", s17_mock_adjustment_done, 1.5),
]
