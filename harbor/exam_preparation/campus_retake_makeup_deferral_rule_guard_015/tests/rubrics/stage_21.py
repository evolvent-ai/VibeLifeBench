from . import _helpers as h

def s21_final_seat_b216_calendar(env):
    return h.s21_final_seat_b216_calendar(env)

def s21_preexam_checklist(env):
    return h.s21_preexam_checklist(env)

CHECKS = [
    ("s21_final_seat_b216_calendar", s21_final_seat_b216_calendar, 2.0),
    ("s21_preexam_checklist", s21_preexam_checklist, 1.5),
]
