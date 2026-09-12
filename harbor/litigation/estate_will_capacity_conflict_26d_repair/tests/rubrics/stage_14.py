from ._helpers import check_named

def check_s14_evidence(env) -> bool:
    return check_named(env, 's14_evidence')

def check_s14_workspace(env) -> bool:
    return check_named(env, 's14_workspace')

CHECKS = [
    ('s14_evidence', check_s14_evidence, 0.40),
    ('s14_workspace', check_s14_workspace, 0.60),
]
