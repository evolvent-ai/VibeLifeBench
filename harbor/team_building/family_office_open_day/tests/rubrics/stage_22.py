from __future__ import annotations
from ._helpers import *

def s22_survey_issue_to_sop(env) -> bool:
    reviewed = used(env, 22, "notion", "API-post-search") or used(env, 22, "notion", "API")
    return reviewed and stage_persisted(env, 22, [["photography"], ["late"], ["delete-group-photo", "delete"], ["SOP"]])

CHECKS = [
    ('s22_survey_issue_to_sop', s22_survey_issue_to_sop, 1.5),
]
