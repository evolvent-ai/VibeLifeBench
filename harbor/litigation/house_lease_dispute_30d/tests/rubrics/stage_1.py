from ._helpers import check_named

def check_s01_source(env) -> bool:
    return check_named(env, 's01_source')

def check_s01_workspace(env) -> bool:
    return check_named(env, 's01_workspace')

CHECKS = [
    ('s01_source', check_s01_source, 0.40),
    ('s01_workspace', check_s01_workspace, 0.60),
]
