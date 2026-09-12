from ._helpers import check_named

def check_s00_source(env) -> bool:
    return check_named(env, 's00_source')

def check_s00_workspace(env) -> bool:
    return check_named(env, 's00_workspace')

CHECKS = [
    ('s00_source', check_s00_source, 0.40),
    ('s00_workspace', check_s00_workspace, 0.60),
]
