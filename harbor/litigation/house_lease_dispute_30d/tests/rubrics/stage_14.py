from ._helpers import check_named

def check_s14_source(env) -> bool:
    return check_named(env, 's14_source')

def check_s14_workspace(env) -> bool:
    return check_named(env, 's14_workspace')

CHECKS = [
    ('s14_source', check_s14_source, 0.40),
    ('s14_workspace', check_s14_workspace, 0.60),
]
