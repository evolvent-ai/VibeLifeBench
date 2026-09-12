from ._helpers import response_check_id, structured_check_id

def s01_signup_email_audit(env) -> bool:
    return structured_check_id(env, 's01_signup_email_audit')

def s01_calendar_deadline_hold(env) -> bool:
    return structured_check_id(env, 's01_calendar_deadline_hold')

CHECKS = [
    ('s01_signup_email_audit', s01_signup_email_audit, 1.0),
    ('s01_calendar_deadline_hold', s01_calendar_deadline_hold, 1.0),
]
