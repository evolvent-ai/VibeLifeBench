from ._helpers import check_named

def check_s13_evidence(env) -> bool:
    return check_named(env, 's13_evidence')

def check_s13_workspace(env) -> bool:
    return check_named(env, 's13_workspace')

CHECKS = [
    ('s13_evidence', check_s13_evidence, 0.40),
    ('s13_workspace', check_s13_workspace, 0.60),
]
