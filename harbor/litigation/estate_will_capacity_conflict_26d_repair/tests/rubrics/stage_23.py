from ._helpers import check_named

def check_s23_evidence(env) -> bool:
    return check_named(env, 's23_evidence')

def check_s23_workspace(env) -> bool:
    return check_named(env, 's23_workspace')

CHECKS = [
    ('s23_evidence', check_s23_evidence, 0.40),
    ('s23_workspace', check_s23_workspace, 0.60),
]
