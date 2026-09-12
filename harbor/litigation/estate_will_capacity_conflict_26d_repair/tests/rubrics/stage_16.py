from ._helpers import check_named

def check_s16_evidence(env) -> bool:
    return check_named(env, 's16_evidence')

def check_s16_workspace(env) -> bool:
    return check_named(env, 's16_workspace')

CHECKS = [
    ('s16_evidence', check_s16_evidence, 0.40),
    ('s16_workspace', check_s16_workspace, 0.60),
]
