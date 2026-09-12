from ._helpers import check_named

def check_s11_source(env) -> bool:
    return check_named(env, 's11_source')

def check_s11_workspace(env) -> bool:
    return check_named(env, 's11_workspace')

CHECKS = [
    ('s11_source', check_s11_source, 0.40),
    ('s11_workspace', check_s11_workspace, 0.60),
]
