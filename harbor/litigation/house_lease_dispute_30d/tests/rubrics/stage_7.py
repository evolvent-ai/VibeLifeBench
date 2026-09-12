from ._helpers import check_named

def check_s07_source(env) -> bool:
    return check_named(env, 's07_source')

def check_s07_workspace(env) -> bool:
    return check_named(env, 's07_workspace')

CHECKS = [
    ('s07_source', check_s07_source, 0.40),
    ('s07_workspace', check_s07_workspace, 0.60),
]
