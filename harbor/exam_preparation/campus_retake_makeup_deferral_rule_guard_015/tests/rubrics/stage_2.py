from . import _helpers as h

def s2_defer_rule_portal_searched(env):
    return h.s2_defer_rule_portal_searched(env)

def s2_requirement_matrix_recorded(env):
    return h.s2_requirement_matrix_recorded(env)

CHECKS = [
    ("s2_defer_rule_portal_searched", s2_defer_rule_portal_searched, 1.5),
    ("s2_requirement_matrix_recorded", s2_requirement_matrix_recorded, 1.5),
]
