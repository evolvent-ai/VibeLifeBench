from __future__ import annotations
from . import _helpers as H

def s15_mock_score_logged(env) -> bool:
    return H.s15_mock_score_logged(env)

def s15_mock_plan_adjusted(env) -> bool:
    return H.s15_mock_plan_adjusted(env)

CHECKS = [
    ("s15_mock_score_logged", s15_mock_score_logged, 1.25),
    ("s15_mock_plan_adjusted", s15_mock_plan_adjusted, 1.25)
]
