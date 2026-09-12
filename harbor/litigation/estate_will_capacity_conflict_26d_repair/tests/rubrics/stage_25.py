from ._helpers import check_named

def check_s25_evidence(env) -> bool:
    return check_named(env, 's25_evidence')

def check_s25_workspace(env) -> bool:
    return check_named(env, 's25_workspace')

CHECKS = [
    ('s25_evidence', check_s25_evidence, 0.40),
    ('s25_workspace', check_s25_workspace, 0.60),
]
