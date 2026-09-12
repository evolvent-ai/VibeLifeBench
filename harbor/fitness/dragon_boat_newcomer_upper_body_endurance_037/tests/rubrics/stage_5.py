from __future__ import annotations
from ._helpers import _check

def chk_s05_team_email_draft_only(env) -> bool:
    return _check('chk_s05_team_email_draft_only', env)

CHECKS = [
    ('chk_s05_team_email_draft_only', chk_s05_team_email_draft_only, 2.0)
]
