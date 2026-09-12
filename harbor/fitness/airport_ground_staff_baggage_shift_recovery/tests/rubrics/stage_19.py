from __future__ import annotations
from ._helpers import evaluate

def chk_email_digest_read(env) -> bool:
    return evaluate('chk_email_digest_read', env)

def chk_no_roster_email_reply(env) -> bool:
    return evaluate('chk_no_roster_email_reply', env)

CHECKS = [
    ('chk_email_digest_read', chk_email_digest_read, 1.5),
    ('chk_no_roster_email_reply', chk_no_roster_email_reply, 2.0),
]
