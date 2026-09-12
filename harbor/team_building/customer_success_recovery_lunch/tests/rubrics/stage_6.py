from __future__ import annotations
from ._helpers import *

def s6_minimize_sensitive_grouping(env) -> bool:
    return any_write(env, 6) and state_has(env, 6, [['summary'], ['privacy'], ['sensitive'], ['vendor']])

CHECKS = [
    ('s6_minimize_sensitive_grouping', s6_minimize_sensitive_grouping, 2.0),
]
