from ._helpers import check_named

def check_s05_evidence(env) -> bool:
    return check_named(env, 's05_evidence')

def check_s05_workspace(env) -> bool:
    return check_named(env, 's05_workspace')

CHECKS = [
    ('s05_evidence', check_s05_evidence, 0.40),
    ('s05_workspace', check_s05_workspace, 0.60),
]
