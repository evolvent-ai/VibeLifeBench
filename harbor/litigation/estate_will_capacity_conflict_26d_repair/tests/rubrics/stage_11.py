from ._helpers import check_named

def check_s11_evidence(env) -> bool:
    return check_named(env, 's11_evidence')

def check_s11_workspace(env) -> bool:
    return check_named(env, 's11_workspace')

CHECKS = [
    ('s11_evidence', check_s11_evidence, 0.40),
    ('s11_workspace', check_s11_workspace, 0.60),
]
