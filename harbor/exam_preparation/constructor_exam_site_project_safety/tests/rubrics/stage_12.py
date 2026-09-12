from ._helpers import response_check_id, structured_check_id

def s12_ce_recheck_email(env) -> bool:
    return structured_check_id(env, 's12_ce_recheck_email')

def s12_ce_deadline_calendar(env) -> bool:
    return structured_check_id(env, 's12_ce_deadline_calendar')

CHECKS = [
    ('s12_ce_recheck_email', s12_ce_recheck_email, 1.0),
    ('s12_ce_deadline_calendar', s12_ce_deadline_calendar, 1.0),
]
