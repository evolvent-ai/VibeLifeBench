from __future__ import annotations
from ._helpers import (
    authorized_action_resolved,
    business_artifacts_complete,
    final_response_consistent,
    late_source_recheck,
    mutation_reconciled,
    no_bad_advice,
    no_duplicate_successful_writes,
    protected_continuity,
    service_breadth,
    stage_response,
    stage_verified_update,
)


def cross_stage_coverage(env):
    return all(stage_response(env, i).strip() and stage_verified_update(env, i) for i in range(24))


def cross_service_breadth(env):
    return service_breadth(env) == 6 and all(stage_verified_update(env, i) for i in (0, 2, 10, 13, 16, 19, 23))


def cross_mutation_chain(env): return mutation_reconciled(env)
def cross_late_source_recheck(env): return late_source_recheck(env)
def cross_action_consistency(env): return authorized_action_resolved(env) and final_response_consistent(env)
def cross_protected_continuity(env): return protected_continuity(env)
def cross_no_duplicate_or_bad_advice(env): return no_duplicate_successful_writes(env) and no_bad_advice(env) and business_artifacts_complete(env)


CHECKS = [
    ("cross_stage_coverage", cross_stage_coverage, 3.0),
    ("cross_service_breadth", cross_service_breadth, 3.0),
    ("cross_mutation_chain", cross_mutation_chain, 5.0),
    ("cross_late_source_recheck", cross_late_source_recheck, 3.0),
    ("cross_action_consistency", cross_action_consistency, 6.0),
    ("cross_protected_continuity", cross_protected_continuity, 6.0),
    ("cross_no_duplicate_or_bad_advice", cross_no_duplicate_or_bad_advice, 4.0),
]
