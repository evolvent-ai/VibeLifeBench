from __future__ import annotations

from ._helpers import rule_ok

def s08_health_voice_replan(env) -> bool:
    return rule_ok(env, 's08_health_voice_replan')

CHECKS = [
    ('s08_health_voice_replan', s08_health_voice_replan, 2.0),
]
