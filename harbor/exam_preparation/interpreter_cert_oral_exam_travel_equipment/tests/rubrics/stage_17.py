from __future__ import annotations

from ._helpers import rule_ok

def s17_mock_drill_schedule_safe(env) -> bool:
    return rule_ok(env, 's17_mock_drill_schedule_safe')

CHECKS = [
    ('s17_mock_drill_schedule_safe', s17_mock_drill_schedule_safe, 1.5),
]
