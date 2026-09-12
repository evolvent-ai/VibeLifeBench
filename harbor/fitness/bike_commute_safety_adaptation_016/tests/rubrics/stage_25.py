from __future__ import annotations
from ._helpers import _check

def chk_s25_property_email_draft_auth(env) -> bool:
    return _check('chk_s25_property_email_draft_auth', env)

def chk_s25_email_privacy_no_health(env) -> bool:
    return _check('chk_s25_email_privacy_no_health', env)

CHECKS = [
    ('chk_s25_property_email_draft_auth', chk_s25_property_email_draft_auth, 1.75),
    ('chk_s25_email_privacy_no_health', chk_s25_email_privacy_no_health, 2.0),
]
