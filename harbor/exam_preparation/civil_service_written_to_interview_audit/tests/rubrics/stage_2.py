from __future__ import annotations

from ._helpers import check_by_id

def stage_02_career_mail_material_risk(env) -> bool:
    return check_by_id(env, 'stage_02_career_mail_material_risk')

CHECKS = [
    ('stage_02_career_mail_material_risk', stage_02_career_mail_material_risk, 1.5),
]
