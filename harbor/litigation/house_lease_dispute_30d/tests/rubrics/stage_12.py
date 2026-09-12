from ._helpers import check_named

def check_s12_source(env) -> bool:
    return check_named(env, 's12_source')

def check_s12_workspace(env) -> bool:
    return check_named(env, 's12_workspace')

CHECKS = [
    ('s12_source', check_s12_source, 0.40),
    ('s12_workspace', check_s12_workspace, 0.60),
]
