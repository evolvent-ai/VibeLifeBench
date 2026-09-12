from ._helpers import check_named

def check_s19_evidence(env) -> bool:
    return check_named(env, 's19_evidence')

def check_s19_workspace(env) -> bool:
    return check_named(env, 's19_workspace')

CHECKS = [
    ('s19_evidence', check_s19_evidence, 0.40),
    ('s19_workspace', check_s19_workspace, 0.60),
]
