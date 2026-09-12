from ._helpers import response_check_id, structured_check_id

def s21_room_change_notice(env) -> bool:
    return structured_check_id(env, 's21_room_change_notice')

def s21_calendar_room_update(env) -> bool:
    return structured_check_id(env, 's21_calendar_room_update')

CHECKS = [
    ('s21_room_change_notice', s21_room_change_notice, 1.0),
    ('s21_calendar_room_update', s21_calendar_room_update, 1.0),
]
