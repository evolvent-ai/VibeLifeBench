from __future__ import annotations
from ._helpers import *

def s2_child_restraint_policy_recorded(env) -> bool:
    return _used_car_road_policy(env, 2) and _child_restraint_policy_backend_ready(env) and _workspace_file_has(env, FILE_RISK_LOG, [['child restraint', 'child'], ['approved', 'as/nzs', 'compliant'], ['forward-facing', 'front'], ['child seat', 'restraint']])

def s2_cc_rv_exclusion_found(env) -> bool:
    return _used_card_lookup(env, 2) and _card_rv_exclusion_backend_ready(env) and _check_text(env, 2, [['issuer', 'card'], ['rv', 'motorhome', 'motorhome'], ['not covered', 'excluded', 'substitute']])

def s2_insurance_budgeted(env) -> bool:
    return _used_car_insurance_plans(env, 2) and _used_card_lookup(env, 2) and _insurance_budget_backend_ready(env) and _workspace_file_has(env, FILE_BUDGET_LEDGER, [['premium', 'insurance'], ['allocation', 'budget'], ['aud', 'cny', 'expense'], ['issuer', 'card'], ['rv', 'motorhome', 'motorhome']])
CHECKS = [('s2_child_restraint_policy_recorded', s2_child_restraint_policy_recorded, 2.0), ('s2_cc_rv_exclusion_found', s2_cc_rv_exclusion_found, 2.0), ('s2_insurance_budgeted', s2_insurance_budgeted, 1.5)]
