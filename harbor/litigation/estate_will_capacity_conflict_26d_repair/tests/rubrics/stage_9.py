from ._helpers import check_named

def check_s09_evidence(env) -> bool:
    return check_named(env, 's09_evidence')

def check_s09_workspace(env) -> bool:
    return check_named(env, 's09_workspace')

CHECKS = [
    ('s09_evidence', check_s09_evidence, 0.40),
    ('s09_workspace', check_s09_workspace, 0.60),
]
