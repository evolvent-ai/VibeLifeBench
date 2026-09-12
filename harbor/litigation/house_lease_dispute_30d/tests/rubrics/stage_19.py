from ._helpers import check_named

def check_s19_source(env) -> bool:
    return check_named(env, 's19_source')

def check_s19_workspace(env) -> bool:
    return check_named(env, 's19_workspace')

CHECKS = [
    ('s19_source', check_s19_source, 0.40),
    ('s19_workspace', check_s19_workspace, 0.60),
]
