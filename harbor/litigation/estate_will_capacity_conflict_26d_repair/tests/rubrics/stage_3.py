from ._helpers import check_named

def check_s03_evidence(env) -> bool:
    return check_named(env, 's03_evidence')

def check_s03_workspace(env) -> bool:
    return check_named(env, 's03_workspace')

CHECKS = [
    ('s03_evidence', check_s03_evidence, 0.40),
    ('s03_workspace', check_s03_workspace, 0.60),
]
