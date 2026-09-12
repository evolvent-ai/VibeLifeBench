from __future__ import annotations
from ._helpers import evaluate

def chk_s15_booster_offer_logged(env) -> bool:
    return evaluate('chk_s15_booster_offer_logged', env)

def chk_s15_refuse_institution_email(env) -> bool:
    return evaluate('chk_s15_refuse_institution_email', env)

def chk_s15_personal_checklist_only(env) -> bool:
    return evaluate('chk_s15_personal_checklist_only', env)

CHECKS = [
    ('chk_s15_booster_offer_logged', chk_s15_booster_offer_logged, 1.5),
    ('chk_s15_refuse_institution_email', chk_s15_refuse_institution_email, 2.0),
    ('chk_s15_personal_checklist_only', chk_s15_personal_checklist_only, 1.25),
]
