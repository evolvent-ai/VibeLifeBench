from ._helpers import response_check_id, structured_check_id

def s09_weekly_monitor_refresh(env) -> bool:
    return structured_check_id(env, 's09_weekly_monitor_refresh')

def s09_calendar_mock_plan(env) -> bool:
    return structured_check_id(env, 's09_calendar_mock_plan')

CHECKS = [
    ('s09_weekly_monitor_refresh', s09_weekly_monitor_refresh, 1.0),
    ('s09_calendar_mock_plan', s09_calendar_mock_plan, 1.0),
]
