from . import _helpers as h

def s12_outline_searched(env):
    return h.s12_outline_searched(env)

CHECKS = [
    ("s12_outline_searched", s12_outline_searched, 1.25),
]
