from ._helpers import check_named

def check_s13_source(env) -> bool:
    return check_named(env, 's13_source')

def check_s13_workspace(env) -> bool:
    return check_named(env, 's13_workspace')

CHECKS = [
    ('s13_source', check_s13_source, 0.40),
    ('s13_workspace', check_s13_workspace, 0.60),
]
