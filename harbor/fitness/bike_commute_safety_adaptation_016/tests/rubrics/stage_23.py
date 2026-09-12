from __future__ import annotations
from ._helpers import _check

def chk_s23_route_roadwork_adjusted(env) -> bool:
    return _check('chk_s23_route_roadwork_adjusted', env)

CHECKS = [
    ('chk_s23_route_roadwork_adjusted', chk_s23_route_roadwork_adjusted, 1.5),
]
