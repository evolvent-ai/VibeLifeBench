from ._helpers import response_check_id, structured_check_id

def s11_project_delay_calendar(env) -> bool:
    return structured_check_id(env, 's11_project_delay_calendar')

def s11_delay_conflict_notion(env) -> bool:
    return structured_check_id(env, 's11_delay_conflict_notion')

CHECKS = [
    ('s11_project_delay_calendar', s11_project_delay_calendar, 1.0),
    ('s11_delay_conflict_notion', s11_delay_conflict_notion, 1.0),
]
