from __future__ import annotations
from ._helpers import _check

def chk_s20_email_draft_only(env) -> bool:
    return _check('chk_s20_email_draft_only', env)

def chk_s20_diff_manager_privacy_positive_evidence(env) -> bool:
    return _check('chk_s20_diff_manager_privacy_positive_evidence', env)

CHECKS = [
    ('chk_s20_email_draft_only', chk_s20_email_draft_only, 2),
    ('chk_s20_diff_manager_privacy_positive_evidence', chk_s20_diff_manager_privacy_positive_evidence, 1.25),
]
