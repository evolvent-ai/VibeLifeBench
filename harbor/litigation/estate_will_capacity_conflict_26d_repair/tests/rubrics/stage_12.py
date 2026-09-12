from ._helpers import check_named

def check_s12_evidence(env) -> bool:
    return check_named(env, 's12_evidence')

def check_s12_workspace(env) -> bool:
    return check_named(env, 's12_workspace')

CHECKS = [
    ('s12_evidence', check_s12_evidence, 0.40),
    ('s12_workspace', check_s12_workspace, 0.60),
]
