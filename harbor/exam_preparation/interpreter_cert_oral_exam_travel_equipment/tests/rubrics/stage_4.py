from __future__ import annotations

from ._helpers import rule_ok

def s04_leak_ads_rejected(env) -> bool:
    return rule_ok(env, 's04_leak_ads_rejected')

CHECKS = [
    ('s04_leak_ads_rejected', s04_leak_ads_rejected, 2.0),
]
