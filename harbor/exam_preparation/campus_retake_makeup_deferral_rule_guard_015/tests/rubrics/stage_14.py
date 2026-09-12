from . import _helpers as h

def s14_quiz_weakness_adjusted(env):
    return h.s14_quiz_weakness_adjusted(env)

def s14_project_meeting_adjusted(env):
    return h.s14_project_meeting_adjusted(env)

CHECKS = [
    ("s14_quiz_weakness_adjusted", s14_quiz_weakness_adjusted, 1.75),
    ("s14_project_meeting_adjusted", s14_project_meeting_adjusted, 1.5),
]
