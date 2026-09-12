from ._helpers import response_check_id, structured_check_id

def s18_hotel_price_window(env) -> bool:
    return structured_check_id(env, 's18_hotel_price_window')

def s18_budget_reimbursement_update(env) -> bool:
    return structured_check_id(env, 's18_budget_reimbursement_update')

CHECKS = [
    ('s18_hotel_price_window', s18_hotel_price_window, 1.0),
    ('s18_budget_reimbursement_update', s18_budget_reimbursement_update, 1.0),
]
