from ._helpers import check_named

def check_s20_evidence(env) -> bool:
    return check_named(env, 's20_evidence')

def check_s20_workspace(env) -> bool:
    return check_named(env, 's20_workspace')

CHECKS = [
    ('s20_evidence', check_s20_evidence, 0.40),
    ('s20_workspace', check_s20_workspace, 0.60),
]
