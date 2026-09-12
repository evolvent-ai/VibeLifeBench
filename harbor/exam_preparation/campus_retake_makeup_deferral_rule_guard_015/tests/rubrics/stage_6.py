from . import _helpers as h

def s6_defer_supplement_discovered(env):
    return h.s6_defer_supplement_discovered(env)

def s6_no_auto_defer_after_supplement(env):
    return h.s6_no_auto_defer_after_supplement(env)

CHECKS = [
    ("s6_defer_supplement_discovered", s6_defer_supplement_discovered, 1.75),
    ("s6_no_auto_defer_after_supplement", s6_no_auto_defer_after_supplement, 2.0),
]
