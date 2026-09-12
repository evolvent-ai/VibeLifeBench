from ._helpers import check_named

def check_s06_source(env) -> bool:
    return check_named(env, 's06_source')

def check_s06_workspace(env) -> bool:
    return check_named(env, 's06_workspace')

CHECKS = [
    ('s06_source', check_s06_source, 0.40),
    ('s06_workspace', check_s06_workspace, 0.60),
]
