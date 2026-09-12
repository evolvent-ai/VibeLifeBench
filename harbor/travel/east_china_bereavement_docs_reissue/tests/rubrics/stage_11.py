from __future__ import annotations
from ._helpers import check_s11_route_refresh

def s11_route_refresh(env) -> bool:
    return check_s11_route_refresh(env)

CHECKS = [
    ("s11_route_refresh", s11_route_refresh, 1),
]
