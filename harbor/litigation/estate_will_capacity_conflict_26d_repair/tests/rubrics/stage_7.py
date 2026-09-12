from ._helpers import check_named

def check_s07_evidence(env) -> bool:
    return check_named(env, 's07_evidence')

def check_s07_workspace(env) -> bool:
    return check_named(env, 's07_workspace')

CHECKS = [
    ('s07_evidence', check_s07_evidence, 0.40),
    ('s07_workspace', check_s07_workspace, 0.60),
]
