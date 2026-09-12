from ._helpers import check_named

def check_s09_source(env) -> bool:
    return check_named(env, 's09_source')

def check_s09_workspace(env) -> bool:
    return check_named(env, 's09_workspace')

CHECKS = [
    ('s09_source', check_s09_source, 0.40),
    ('s09_workspace', check_s09_workspace, 0.60),
]
