from __future__ import annotations

from ._helpers import check_by_id

def stage_11_ticket_print_calendar(env) -> bool:
    return check_by_id(env, 'stage_11_ticket_print_calendar')

def stage_11_exam_day_calendar(env) -> bool:
    return check_by_id(env, 'stage_11_exam_day_calendar')

CHECKS = [
    ('stage_11_ticket_print_calendar', stage_11_ticket_print_calendar, 1.5),
    ('stage_11_exam_day_calendar', stage_11_exam_day_calendar, 1.5),
]
