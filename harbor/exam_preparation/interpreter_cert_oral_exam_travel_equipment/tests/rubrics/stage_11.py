from __future__ import annotations

from ._helpers import rule_ok

def s11_route_disruption_recovery(env) -> bool:
    return rule_ok(env, 's11_route_disruption_recovery')

CHECKS = [
    ('s11_route_disruption_recovery', s11_route_disruption_recovery, 1.75),
]
