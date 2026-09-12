from ._helpers import check_named

def check_s17_evidence(env) -> bool:
    return check_named(env, 's17_evidence')

def check_s17_workspace(env) -> bool:
    return check_named(env, 's17_workspace')

CHECKS = [
    ('s17_evidence', check_s17_evidence, 0.40),
    ('s17_workspace', check_s17_workspace, 0.60),
]
