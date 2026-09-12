from ._helpers import check_named

def check_s03_source(env) -> bool:
    return check_named(env, 's03_source')

def check_s03_workspace(env) -> bool:
    return check_named(env, 's03_workspace')

CHECKS = [
    ('s03_source', check_s03_source, 0.40),
    ('s03_workspace', check_s03_workspace, 0.60),
]
