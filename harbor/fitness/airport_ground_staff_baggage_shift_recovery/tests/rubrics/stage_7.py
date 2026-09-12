from __future__ import annotations
from ._helpers import evaluate

def chk_roster_calendar_replan(env) -> bool:
    return evaluate('chk_roster_calendar_replan', env)

CHECKS = [
    ('chk_roster_calendar_replan', chk_roster_calendar_replan, 1.75),
]
