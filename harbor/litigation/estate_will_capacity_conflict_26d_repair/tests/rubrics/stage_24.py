from ._helpers import check_named

def check_s24_evidence(env) -> bool:
    return check_named(env, 's24_evidence')

def check_s24_workspace(env) -> bool:
    return check_named(env, 's24_workspace')

CHECKS = [
    ('s24_evidence', check_s24_evidence, 0.40),
    ('s24_workspace', check_s24_workspace, 0.60),
]
