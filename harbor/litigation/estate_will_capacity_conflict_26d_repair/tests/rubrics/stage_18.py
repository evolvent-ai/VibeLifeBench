from ._helpers import check_named

def check_s18_evidence(env) -> bool:
    return check_named(env, 's18_evidence')

def check_s18_workspace(env) -> bool:
    return check_named(env, 's18_workspace')

CHECKS = [
    ('s18_evidence', check_s18_evidence, 0.40),
    ('s18_workspace', check_s18_workspace, 0.60),
]
