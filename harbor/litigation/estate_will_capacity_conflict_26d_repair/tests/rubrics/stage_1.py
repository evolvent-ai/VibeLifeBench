from ._helpers import check_named

def check_s01_evidence(env) -> bool:
    return check_named(env, 's01_evidence')

def check_s01_workspace(env) -> bool:
    return check_named(env, 's01_workspace')

CHECKS = [
    ('s01_evidence', check_s01_evidence, 0.40),
    ('s01_workspace', check_s01_workspace, 0.60),
]
