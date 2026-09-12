from . import _helpers as h

def s1_official_notice_read(env):
    return h.s1_official_notice_read(env)

def s1_exam_calendar_created(env):
    return h.s1_exam_calendar_created(env)

CHECKS = [
    ("s1_official_notice_read", s1_official_notice_read, 1.5),
    ("s1_exam_calendar_created", s1_exam_calendar_created, 1.75),
]
