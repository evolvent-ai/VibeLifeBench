from ._helpers import check_named

def check_s06_evidence(env) -> bool:
    return check_named(env, 's06_evidence')

def check_s06_workspace(env) -> bool:
    return check_named(env, 's06_workspace')

CHECKS = [
    ('s06_evidence', check_s06_evidence, 0.40),
    ('s06_workspace', check_s06_workspace, 0.60),
]
