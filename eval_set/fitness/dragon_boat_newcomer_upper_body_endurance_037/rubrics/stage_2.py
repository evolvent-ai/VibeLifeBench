from __future__ import annotations
from ._helpers import _check

def chk_s02_team_email_deadline(env) -> bool:
    return _check('chk_s02_team_email_deadline', env)

CHECKS = [
    ('chk_s02_team_email_deadline', chk_s02_team_email_deadline, 1.5)
]
