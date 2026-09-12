from ._helpers import check_named

def check_s21_source(env) -> bool:
    return check_named(env, 's21_source')

def check_s21_workspace(env) -> bool:
    return check_named(env, 's21_workspace')

CHECKS = [
    ('s21_source', check_s21_source, 0.40),
    ('s21_workspace', check_s21_workspace, 0.60),
]
