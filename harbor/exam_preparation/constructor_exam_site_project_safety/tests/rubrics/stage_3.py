from ._helpers import response_check_id, structured_check_id

def s03_ce_notification_gap(env) -> bool:
    return structured_check_id(env, 's03_ce_notification_gap')

def s03_content_real_hours_source(env) -> bool:
    return structured_check_id(env, 's03_content_real_hours_source')

CHECKS = [
    ('s03_ce_notification_gap', s03_ce_notification_gap, 1.0),
    ('s03_content_real_hours_source', s03_content_real_hours_source, 1.0),
]
