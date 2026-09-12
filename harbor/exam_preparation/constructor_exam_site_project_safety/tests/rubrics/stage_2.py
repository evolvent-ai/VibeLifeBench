from ._helpers import response_check_id, structured_check_id

def s02_project_conflict_refresh(env) -> bool:
    return structured_check_id(env, 's02_project_conflict_refresh')

def s02_site_email_cross_source(env) -> bool:
    return structured_check_id(env, 's02_site_email_cross_source')

CHECKS = [
    ('s02_project_conflict_refresh', s02_project_conflict_refresh, 1.0),
    ('s02_site_email_cross_source', s02_site_email_cross_source, 1.0),
]
