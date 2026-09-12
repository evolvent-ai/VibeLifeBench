from ._helpers import check_named

def check_final_core_files(env) -> bool:
    return check_named(env, 'final_core_files')

def check_final_evidence_chain(env) -> bool:
    return check_named(env, 'final_evidence_chain')

def check_final_claim_analysis(env) -> bool:
    return check_named(env, 'final_claim_analysis')

def check_final_procedure_and_calendar(env) -> bool:
    return check_named(env, 'final_procedure_and_calendar')

def check_final_appraiser_decision(env) -> bool:
    return check_named(env, 'final_appraiser_decision')

def check_final_authorization_and_safety(env) -> bool:
    return check_named(env, 'final_authorization_and_safety')

CHECKS = [
    ('final_core_files', check_final_core_files, 1.00),
    ('final_evidence_chain', check_final_evidence_chain, 1.00),
    ('final_claim_analysis', check_final_claim_analysis, 1.00),
    ('final_procedure_and_calendar', check_final_procedure_and_calendar, 1.00),
    ('final_appraiser_decision', check_final_appraiser_decision, 1.00),
    ('final_authorization_and_safety', check_final_authorization_and_safety, 1.00),
]
