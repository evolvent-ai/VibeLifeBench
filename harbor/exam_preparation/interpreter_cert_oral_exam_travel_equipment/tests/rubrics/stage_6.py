from __future__ import annotations

from ._helpers import rule_ok

def s06_delivery_delay_recovery(env) -> bool:
    return rule_ok(env, 's06_delivery_delay_recovery')

CHECKS = [
    ('s06_delivery_delay_recovery', s06_delivery_delay_recovery, 1.75),
]
