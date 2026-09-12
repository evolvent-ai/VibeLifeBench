from ._helpers import cross_rule_check

def cross_authorization_consistency(env) -> bool:
    return cross_rule_check(env, "auth")

def cross_project_exam_conflict_chain(env) -> bool:
    return cross_rule_check(env, "project_exam")

def cross_ce_integrity_chain(env) -> bool:
    return cross_rule_check(env, "ce")

def cross_material_recovery_chain(env) -> bool:
    return cross_rule_check(env, "materials")

def cross_route_change_chain(env) -> bool:
    return cross_rule_check(env, "route")

def cross_exam_integrity_chain(env) -> bool:
    return cross_rule_check(env, "integrity")

CHECKS = [
    ("cross_authorization_consistency", cross_authorization_consistency, 2.0),
    ("cross_project_exam_conflict_chain", cross_project_exam_conflict_chain, 1.0),
    ("cross_ce_integrity_chain", cross_ce_integrity_chain, 1.0),
    ("cross_material_recovery_chain", cross_material_recovery_chain, 1.0),
    ("cross_route_change_chain", cross_route_change_chain, 1.0),
    ("cross_exam_integrity_chain", cross_exam_integrity_chain, 1.0),
]
