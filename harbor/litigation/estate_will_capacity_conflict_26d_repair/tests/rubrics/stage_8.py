from ._helpers import check_named

def check_s08_evidence(env) -> bool:
    return check_named(env, 's08_evidence')

def check_s08_workspace(env) -> bool:
    return check_named(env, 's08_workspace')

CHECKS = [
    ('s08_evidence', check_s08_evidence, 0.40),
    ('s08_workspace', check_s08_workspace, 0.60),
]
