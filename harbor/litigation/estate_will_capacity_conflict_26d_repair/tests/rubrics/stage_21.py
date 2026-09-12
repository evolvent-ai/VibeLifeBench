from ._helpers import check_named

def check_s21_evidence(env) -> bool:
    return check_named(env, 's21_evidence')

def check_s21_workspace(env) -> bool:
    return check_named(env, 's21_workspace')

CHECKS = [
    ('s21_evidence', check_s21_evidence, 0.40),
    ('s21_workspace', check_s21_workspace, 0.60),
]
