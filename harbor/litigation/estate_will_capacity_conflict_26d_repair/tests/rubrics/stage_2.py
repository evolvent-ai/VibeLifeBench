from ._helpers import check_named

def check_s02_evidence(env) -> bool:
    return check_named(env, 's02_evidence')

def check_s02_workspace(env) -> bool:
    return check_named(env, 's02_workspace')

CHECKS = [
    ('s02_evidence', check_s02_evidence, 0.40),
    ('s02_workspace', check_s02_workspace, 0.60),
]
