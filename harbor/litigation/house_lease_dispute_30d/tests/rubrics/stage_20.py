from ._helpers import check_named

def check_s20_source(env) -> bool:
    return check_named(env, 's20_source')

def check_s20_workspace(env) -> bool:
    return check_named(env, 's20_workspace')

CHECKS = [
    ('s20_source', check_s20_source, 0.40),
    ('s20_workspace', check_s20_workspace, 0.60),
]
