from ._helpers import check_named

def check_s10_evidence(env) -> bool:
    return check_named(env, 's10_evidence')

def check_s10_workspace(env) -> bool:
    return check_named(env, 's10_workspace')

CHECKS = [
    ('s10_evidence', check_s10_evidence, 0.40),
    ('s10_workspace', check_s10_workspace, 0.60),
]
