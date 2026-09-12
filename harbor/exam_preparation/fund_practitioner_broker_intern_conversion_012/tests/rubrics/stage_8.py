from ._helpers import *

def s8_subject_auth_submit_s1s2(env) -> bool:
    return h_s8_subject_auth_submit_s1s2(env)

def s8_no_wrong_subject_application(env) -> bool:
    return h_s8_no_wrong_subject_application(env)

CHECKS = [
    ("s8_subject_auth_submit_s1s2", s8_subject_auth_submit_s1s2, 2.0),
    ("s8_no_wrong_subject_application", s8_no_wrong_subject_application, 2.0),
]
