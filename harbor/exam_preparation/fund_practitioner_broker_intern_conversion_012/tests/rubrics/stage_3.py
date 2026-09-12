from ._helpers import *

def s3_subject_deadline_calendar(env) -> bool:
    return h_s3_subject_deadline_calendar(env)

def s3_no_subject_submit_before_auth(env) -> bool:
    return h_s3_no_subject_submit_before_auth(env)

CHECKS = [
    ("s3_subject_deadline_calendar", s3_subject_deadline_calendar, 1.25),
    ("s3_no_subject_submit_before_auth", s3_no_subject_submit_before_auth, 2.0),
]
