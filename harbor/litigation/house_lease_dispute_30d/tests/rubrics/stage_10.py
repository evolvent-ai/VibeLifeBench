from ._helpers import check_named

def check_s10_source(env) -> bool:
    return check_named(env, 's10_source')

def check_s10_workspace(env) -> bool:
    return check_named(env, 's10_workspace')

CHECKS = [
    ('s10_source', check_s10_source, 0.40),
    ('s10_workspace', check_s10_workspace, 0.60),
]
