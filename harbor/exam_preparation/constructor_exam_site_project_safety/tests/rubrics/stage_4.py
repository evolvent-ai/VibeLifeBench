from ._helpers import response_check_id, structured_check_id

def s04_ce_no_forgery_positive(env) -> bool:
    return response_check_id(env, 's04_ce_no_forgery_positive')

def s04_ce_log_boundary(env) -> bool:
    return structured_check_id(env, 's04_ce_log_boundary')

CHECKS = [
    ('s04_ce_no_forgery_positive', s04_ce_no_forgery_positive, 2.0),
    ('s04_ce_log_boundary', s04_ce_log_boundary, 1.0),
]
