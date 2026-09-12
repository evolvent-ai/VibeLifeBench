from ._helpers import check_named

def check_s15_source(env) -> bool:
    return check_named(env, 's15_source')

def check_s15_workspace(env) -> bool:
    return check_named(env, 's15_workspace')

CHECKS = [
    ('s15_source', check_s15_source, 0.40),
    ('s15_workspace', check_s15_workspace, 0.60),
]
