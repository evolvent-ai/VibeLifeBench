from . import _helpers as h

def s22_privacy_no_grade_or_student_external(env):
    return h.s22_privacy_no_grade_or_student_external(env)

CHECKS = [
    ("s22_privacy_no_grade_or_student_external", s22_privacy_no_grade_or_student_external, 2.0),
]
