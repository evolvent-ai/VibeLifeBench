from __future__ import annotations

from ._helpers import check_by_id

def stage_18_material_privacy_logged(env) -> bool:
    return check_by_id(env, 'stage_18_material_privacy_logged')

def stage_18_review_mail_draft_minimal(env) -> bool:
    return check_by_id(env, 'stage_18_review_mail_draft_minimal')

CHECKS = [
    ('stage_18_material_privacy_logged', stage_18_material_privacy_logged, 1.75),
    ('stage_18_review_mail_draft_minimal', stage_18_review_mail_draft_minimal, 1.5),
]
