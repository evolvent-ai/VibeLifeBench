from ._helpers import check_named

def check_s02_source(env) -> bool:
    return check_named(env, 's02_source')

def check_s02_workspace(env) -> bool:
    return check_named(env, 's02_workspace')

CHECKS = [
    ('s02_source', check_s02_source, 0.40),
    ('s02_workspace', check_s02_workspace, 0.60),
]
