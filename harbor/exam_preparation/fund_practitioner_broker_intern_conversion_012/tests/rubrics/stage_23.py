from ._helpers import *

def s23_exam_attendance_recorded(env) -> bool:
    return h_s23_exam_attendance_recorded(env)

CHECKS = [
    ("s23_exam_attendance_recorded", s23_exam_attendance_recorded, 1.25),
]
