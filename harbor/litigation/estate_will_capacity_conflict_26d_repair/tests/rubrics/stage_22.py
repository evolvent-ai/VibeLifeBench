from ._helpers import check_named

def check_s22_evidence(env) -> bool:
    return check_named(env, 's22_evidence')

def check_s22_workspace(env) -> bool:
    return check_named(env, 's22_workspace')

CHECKS = [
    ('s22_evidence', check_s22_evidence, 0.40),
    ('s22_workspace', check_s22_workspace, 0.60),
]
