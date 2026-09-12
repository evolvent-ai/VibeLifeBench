from ._helpers import *

def s21_admit_calendar_place(env) -> bool:
    return h_s21_admit_calendar_place(env)

def s21_admit_calendar_refresh_matrix(env) -> bool:
    return h_s21_admit_calendar_refresh_matrix(env)

CHECKS = [
    ("s21_admit_calendar_place", s21_admit_calendar_place, 1.5),
    ("s21_admit_calendar_refresh_matrix", s21_admit_calendar_refresh_matrix, 1.0),
]
