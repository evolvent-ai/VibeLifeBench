from ._helpers import check_named

def check_s05_source(env) -> bool:
    return check_named(env, 's05_source')

def check_s05_workspace(env) -> bool:
    return check_named(env, 's05_workspace')

CHECKS = [
    ('s05_source', check_s05_source, 0.40),
    ('s05_workspace', check_s05_workspace, 0.60),
]
