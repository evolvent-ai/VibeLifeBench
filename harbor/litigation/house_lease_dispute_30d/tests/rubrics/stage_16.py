from ._helpers import check_named

def check_s16_source(env) -> bool:
    return check_named(env, 's16_source')

def check_s16_workspace(env) -> bool:
    return check_named(env, 's16_workspace')

CHECKS = [
    ('s16_source', check_s16_source, 0.40),
    ('s16_workspace', check_s16_workspace, 0.60),
]
