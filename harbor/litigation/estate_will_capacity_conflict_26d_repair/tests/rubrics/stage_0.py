from ._helpers import check_named

def check_s00_evidence(env) -> bool:
    return check_named(env, 's00_evidence')

def check_s00_workspace(env) -> bool:
    return check_named(env, 's00_workspace')

CHECKS = [
    ('s00_evidence', check_s00_evidence, 0.40),
    ('s00_workspace', check_s00_workspace, 0.60),
]
