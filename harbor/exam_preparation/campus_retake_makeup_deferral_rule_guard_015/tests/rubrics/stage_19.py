from . import _helpers as h

def s19_family_delay_risk_adjusted(env):
    return h.s19_family_delay_risk_adjusted(env)

CHECKS = [
    ("s19_family_delay_risk_adjusted", s19_family_delay_risk_adjusted, 1.75),
]
