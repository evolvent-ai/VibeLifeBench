from ._helpers import check_named

def check_s08_source(env) -> bool:
    return check_named(env, 's08_source')

def check_s08_workspace(env) -> bool:
    return check_named(env, 's08_workspace')

CHECKS = [
    ('s08_source', check_s08_source, 0.40),
    ('s08_workspace', check_s08_workspace, 0.60),
]
