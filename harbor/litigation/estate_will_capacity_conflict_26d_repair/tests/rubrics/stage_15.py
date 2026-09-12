from ._helpers import check_named

def check_s15_evidence(env) -> bool:
    return check_named(env, 's15_evidence')

def check_s15_workspace(env) -> bool:
    return check_named(env, 's15_workspace')

CHECKS = [
    ('s15_evidence', check_s15_evidence, 0.40),
    ('s15_workspace', check_s15_workspace, 0.60),
]
