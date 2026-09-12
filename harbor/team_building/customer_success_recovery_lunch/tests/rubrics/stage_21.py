from __future__ import annotations
from ._helpers import *

def s21_return_route_safe(env) -> bool:
    # This indoor event has no return shuttle. The safety closure is staffing
    # coverage, onsite contacts, split movement, and an updated notice.
    return used(env, 21, 'maps') and any_write(env, 21) and state_has(env, 21, [['coverage', 'staffing'], ['onsite', 'contact', 'flow', 'split'], ['opt out', 'low-pressure', 'quiet'], ['notice', 'reminder']])

def s21_return_route_refresh(env) -> bool:
    return stage_server_hits(env, 21, [('maps', None), ('notification_hub', None), ('calendar', None), ('notion', None)]) >= 2

CHECKS = [
    ('s21_return_route_safe', s21_return_route_safe, 1.75),
    ('s21_return_route_refresh', s21_return_route_refresh, 1.0),
]
