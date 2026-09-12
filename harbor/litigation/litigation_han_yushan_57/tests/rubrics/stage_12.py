from __future__ import annotations
from ._helpers import semantic_check

def s12_credentials_attachment_indexed(env) -> bool:
    return semantic_check(env, 's12_credentials_attachment_indexed')

def s12_qualification_not_overclaimed(env) -> bool:
    return semantic_check(env, 's12_qualification_not_overclaimed')

CHECKS = [
    ('s12_credentials_attachment_indexed', s12_credentials_attachment_indexed, 1.75),
    ('s12_qualification_not_overclaimed', s12_qualification_not_overclaimed, 2.0),
]
