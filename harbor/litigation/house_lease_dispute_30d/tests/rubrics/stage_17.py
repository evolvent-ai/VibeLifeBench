from ._helpers import check_named

def check_s17_source(env) -> bool:
    return check_named(env, 's17_source')

def check_s17_workspace(env) -> bool:
    return check_named(env, 's17_workspace')

CHECKS = [
    ('s17_source', check_s17_source, 0.40),
    ('s17_workspace', check_s17_workspace, 0.60),
]
