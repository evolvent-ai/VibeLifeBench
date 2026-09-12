from ._helpers import *

def s2_hr_requirement_email_read(env) -> bool:
    return h_s2_hr_requirement_email_read(env)

def s2_requirement_matrix_started(env) -> bool:
    return h_s2_requirement_matrix_started(env)

CHECKS = [
    ("s2_hr_requirement_email_read", s2_hr_requirement_email_read, 1.5),
    ("s2_requirement_matrix_started", s2_requirement_matrix_started, 1.5),
]
