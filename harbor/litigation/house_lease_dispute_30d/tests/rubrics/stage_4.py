from ._helpers import check_named

def check_s04_source(env) -> bool:
    return check_named(env, 's04_source')

def check_s04_workspace(env) -> bool:
    return check_named(env, 's04_workspace')

CHECKS = [
    ('s04_source', check_s04_source, 0.40),
    ('s04_workspace', check_s04_workspace, 0.60),
]
