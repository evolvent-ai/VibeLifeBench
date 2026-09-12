from ._helpers import check_named

def check_s04_evidence(env) -> bool:
    return check_named(env, 's04_evidence')

def check_s04_workspace(env) -> bool:
    return check_named(env, 's04_workspace')

CHECKS = [
    ('s04_evidence', check_s04_evidence, 0.40),
    ('s04_workspace', check_s04_workspace, 0.60),
]
