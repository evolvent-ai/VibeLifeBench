from . import _helpers as h

def s7_lab_conflict_plan(env):
    return h.s7_lab_conflict_plan(env)

CHECKS = [
    ("s7_lab_conflict_plan", s7_lab_conflict_plan, 1.25),
]
