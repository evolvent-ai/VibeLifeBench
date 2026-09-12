from __future__ import annotations
from ._helpers import *

def s22_survey_issue_to_sop(env) -> bool:
    # The feedback anomaly concerns Technical Support missing part of the review.
    return used(env, 22, 'notion') and any_write(env, 22) and state_has(env, 22, [['satisfaction'], ['support', 'duty', 'participation', 'miss'], ['SOP', 'follow-up'], ['next', 'SOP', 'follow-up']])

CHECKS = [
    ('s22_survey_issue_to_sop', s22_survey_issue_to_sop, 1.5),
]
